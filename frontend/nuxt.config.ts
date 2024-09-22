import Aura from '@primevue/themes/aura';

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
  modules: ['@primevue/nuxt-module'],
  primevue: {
    options: {
      theme: {
        preset: Aura
      }
    }
  },
  postcss: {
    plugins: {
      tailwindcss: {},
      autoprefixer: {}
    }
  },
  css: ['~/assets/styles/tailwind/base.css', '~/assets/styles/main.scss'],
  components: [{ path: '~/modules', pathPrefix: false }, '~/components']
});
