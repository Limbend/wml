import Lara from '@primevue/themes/lara';
import { ariaLocaleRu, localeRu } from './assets/styles/primeVue/localization';

// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  runtimeConfig: {
    public: {
      apiBase: '',
    },
  },
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
    [
      '@vee-validate/nuxt',
      {
        autoImports: true,
      },
    ],
  ],
  plugins: ['~/plugins/VeeValidateConfig.ts'],
  primevue: {
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
  },
  tailwindcss: {
    exposeConfig: true,
    viewer: true,
  },
  css: ['~/assets/styles/tailwind/base.css', '~/assets/styles/main.scss'],
  components: [{ path: '~/modules', pathPrefix: false }, '~/components'],
  vite: {
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
