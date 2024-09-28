import Lara from '@primevue/themes/lara';

// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2024-04-03',
  app: {
    head: {
      charset: 'utf-8',
      viewport: 'width=device-width, initial-scale=1',
      title: 'wml for Maksowny'
    }
  },
  devtools: { enabled: true },
  typescript: {
    typeCheck: true
  },
  modules: ['@primevue/nuxt-module', '@nuxtjs/tailwindcss'],
  primevue: {
    options: {
      theme: {
        preset: Lara
      }
    },
    autoImport: false
  },
  tailwindcss: {
    exposeConfig: true,
    viewer: true
  },
  css: ['~/assets/styles/tailwind/base.css', '~/assets/styles/main.scss'],
  components: [{ path: '~/modules', pathPrefix: false }, '~/components'],
  vite: {
    css: {
      preprocessorOptions: {
        scss: { api: 'modern-compiler' }
      }
    },
    build: {
      sourcemap: true
    }
  },
  sourcemap: { server: true, client: false }
});
