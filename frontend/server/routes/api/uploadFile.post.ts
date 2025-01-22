import { Writable } from 'stream';
import formidable from 'formidable';
import { PutObjectCommand, S3Client } from '@aws-sdk/client-s3';
import VolatileFile from 'formidable/VolatileFile';

const allowedMimeTypes = ['application/pdf', 'image/png', 'image/jpeg', 'image/jpg'];

export default defineEventHandler(async event => {
    let originalFilename = '';
    const form = formidable({
        multiples: false,
        fileWriteStreamHandler: (file: VolatileFile | undefined) => {
            if (!file) {
                return new Writable({
                    write(chunk, encoding, callback) {
                        callback(new Error('Чек не найден'));
                    },
                });
            }

            const config = useRuntimeConfig(); // Ваши переменные окружения
            const s3Client = new S3Client({
                credentials: {
                    accessKeyId: config.s3.accessKeyId,
                    secretAccessKey: config.s3.secretAccessKey,
                },
                endpoint: config.s3.path,
                forcePathStyle: true,
                region: 'us-east-1',
            });

            originalFilename = (file as any).originalFilename;
            const mimeType = (file as any).mimetype || 'application/octet-stream';
            if (!allowedMimeTypes.includes(mimeType)) {
                return new Writable({
                    write(chunk, encoding, callback) {
                        callback(new Error('Недопустимый формат чека'));
                    },
                });
            }
            const fileName = getQuery(event).productId + '.' + mimeType.split('/')[1];

            // Создаем массив для накопления чанков
            const chunks: Buffer[] = [];

            return new Writable({
                write(chunk, encoding, callback) {
                    // Добавляем чанк в массив
                    chunks.push(Buffer.from(chunk));
                    callback();
                },
                final(callback) {
                    // После завершения потока собираем все чанки в один буфер
                    const fullBuffer = Buffer.concat(chunks);

                    // Отправляем Чек на S3
                    const uploadCommand = new PutObjectCommand({
                        Bucket: config.s3.bucketName, // Имя бакета S3
                        Key: `${new Date().getFullYear()}/${fileName}`, // Имя чека в бакете
                        Body: fullBuffer, // Полный Чек
                        ContentType: mimeType, // Тип содержимого
                    });

                    s3Client
                        .send(uploadCommand)
                        .then(() => {
                            console.log(
                                `Чек успешно загружен на S3: ${originalFilename}`,
                            );
                            callback();
                        })
                        .catch(err => {
                            console.error(`Ошибка загрузки чека в S3: ${err.message}`);
                            callback(err);
                        });
                },
            });
        },
    });

    try {
        // Парсим входящий запрос
        await new Promise((resolve, reject) => {
            form.parse(event.req, err => {
                if (err) reject(err);
                else resolve(null);
            });
        });

        return {
            statusCode: 200,
            message: `Чек успешно загружен на S3: ${originalFilename}`,
        };
    } catch (error) {
        console.error('Ошибка при загрузке чека:', error);
        if (error instanceof Error) {
            throw createError({
                statusCode: 400,
                statusMessage: error.message,
            });
        } else {
            throw createError({
                statusCode: 500,
                statusMessage: 'Неизвестная ошибка при обработке чека',
            });
        }
    }
});
