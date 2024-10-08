<script setup lang="ts">
import type { IProduct } from '~/types/Products/Products.types';

import ProductService from '~/services/ProductsServices/ProductsService';
import type { TStatus } from '~/types/index.types';

const emit = defineEmits(['onCreate']);

const loading = ref<TStatus | undefined>(undefined);

const onSubmit = async (formData: IProduct) => {
  loading.value = 'loading';
  const { data, status } = await ProductService.createProduct(formData);
  loading.value = status.value;
  if (data.value.product_id) {
    const newProduct = {
      ...formData,
      ...data.value?.auto_generated_fields,
      id: data.value.product_id
    };
    emit('onCreate', newProduct);
  }
};
</script>

<template>
  <ProductPopover :loading="loading" @submit="onSubmit" />
</template>
