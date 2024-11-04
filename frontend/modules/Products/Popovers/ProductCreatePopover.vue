<script setup lang="ts">
import type { IProduct } from '~/types/Products/Products.types';

import ProductService from '~/services/ProductsServices/ProductsService';
import type { TStatus } from '~/types/index.types';

type Props = {
  visible: Boolean;
};

defineProps<Props>();

const emit = defineEmits(['onCreate']);

const loading = ref<TStatus | undefined>(undefined);

const onSubmit = async (formData: IProduct) => {
  loading.value = 'loading';
  const { data, status } = await ProductService.createProduct(formData);
  loading.value = status.value;
  if ('product_id' in data.value.content) {
    const newProduct = {
      ...formData,
      ...data.value?.content.auto_generated_fields,
      id: data.value.content.product_id,
    };
    emit('onCreate', newProduct);
  }
};
</script>

<template>
  <ProductPopover :visible="visible" :loading="loading" @submit="onSubmit" />
</template>
