import { defineNuxtPlugin } from '#app';
import { configure } from 'vee-validate';

export default defineNuxtPlugin(() => {
  configure({
    validateOnInput: false,
    validateOnBlur: false,
    validateOnChange: false,
    validateOnModelUpdate: true,
  });
});
