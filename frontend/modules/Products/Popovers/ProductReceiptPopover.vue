<script setup lang="ts">
import type { FileUploadSelectEvent } from 'primevue';
import { messageHandler } from '~/api/messageHandler/messageHandler';
const fileUpload = ref();
const file = ref();

type Props = {
    productId: Number;
};
const props = defineProps<Props>();

const upload = async () => {
    const formData = new FormData();
    formData.append('file', file.value);
    formData.append('nameById', `${props.productId}`);

    const response = await fetch(`/api/uploadFile?productId=${props.productId}`, {
        method: 'POST',
        body: formData,
    });
    const result = await response.json();
    if (result.message) {
        messageHandler({
            message: result.message,
            type: result.statusCode !== 200 ? 'error' : 'success',
        });
    }
};

const onSelectedFiles = (event: FileUploadSelectEvent) => {
    if (event.files.length) {
        file.value = event.files[0];
    }
};
</script>

<template>
    <form class="flex justify-between gap-2" v-if="productId === 1">
        <FileUpload
            ref="fileUpload"
            mode="basic"
            name="file"
            accept=".jpeg, .jpg, .png, .pdf"
            :maxFileSize="1000000"
            @select="onSelectedFiles" />
        <Button
            label="Загрузить"
            @click="upload"
            severity="secondary"
            :disabled="!file" />
    </form>
    <div v-else class="flex flex-col gap-2">
        <div class="flex justify-between gap-x-2">
            <a href="http://localhost:9400/wml/2025/1.pdf" target="_blank">
                <Button
                    icon="pi pi-download"
                    aria-label="download"
                    size="small"
                    text
                    severity="info" />
            </a>

            <Button
                icon="pi pi-trash"
                aria-label="Delete"
                label="Удалить"
                severity="danger"
                size="small"
                text />
        </div>
        <object
            data="http://localhost:9400/wml/2025/1.pdf"
            type="application/pdf"
            class="max-w-[40vw] h-[40vh] max-md:max-w-[70vw] max-sm:max-w-[320px] object-contain"></object>
    </div>
</template>
