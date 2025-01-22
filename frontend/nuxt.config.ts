import Lara from '@primevue/themes/lara';
import { ariaLocaleRu, localeRu } from './assets/styles/primeVue/localization';

// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
    compatibilityDate: '2024-04-03',
    app: {
        head: {
            charset: 'utf-8',
            viewport: 'width=device-width, initial-scale=1',
            title: 'wml for Maksowny',
        },
    },
    devtools: { enabled: true },
    typescript: {
        typeCheck: true,
    },
    modules: [
        '@primevue/nuxt-module',
        '@nuxtjs/tailwindcss',
        '@pinia/nuxt',
        [
            '@vee-validate/nuxt',
            {
                autoImports: true,
            },
        ],
    ],
    plugins: ['~/plugins/VeeValidateConfig.ts'],
    primevue: {
        usePrimeVue: true,
        options: {
            theme: {
                preset: Lara,
            },
            locale: {
                ...localeRu,
                aria: {
                    ...ariaLocaleRu,
                },
            },
        },
        autoImport: false,
        components: {
            include: [
                'Button',
                'DataTable',
                'Toast',
                'Drawer',
                'ConfirmDialog',
                'FloatLabel',
                'FileUpload',
                'InputText',
                'InputNumber',
                'DatePicker',
                'Checkbox',
                'Column',
                'IconField',
                'InputIcon',
                'Popover',
            ],
        },
    },
    tailwindcss: {
        exposeConfig: true,
        viewer: true,
    },
    css: ['~/assets/styles/tailwind/base.css', '~/assets/styles/main.scss'],
    components: [{ path: '~/modules', pathPrefix: false }, '~/components'],
    runtimeConfig: {
        public: {
            apiBase: '',
        },
        s3: {
            accessKeyId: process.env.S3_ACCESS_KEY_ID,
            secretAccessKey: process.env.S3_SECRET_ACCESS_KEY,
            bucketName: process.env.S3_BUCKET_NAME,
            path: process.env.S3_ENDPOINT_URL,
        },
    },
    vite: {
        define: {
            'process.env.NUXT_SSR_API_BASE': JSON.stringify(
                process.env.NUXT_SSR_API_BASE,
            ),
        },
        css: {
            preprocessorOptions: {
                scss: { api: 'modern-compiler' },
            },
        },
        build: {
            sourcemap: true,
        },
    },
    sourcemap: { server: true, client: false },
});
