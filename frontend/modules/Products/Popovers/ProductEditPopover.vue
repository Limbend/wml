<script setup lang="ts">
import type { IProduct } from '~/types/Products/Products.types';

import ProductService from '~/services/ProductsServices/ProductsService';
import type { TStatus } from '~/types/index.types';

type Props = {
  productToEdit?: IProduct;
  visible: Boolean;
};

defineProps<Props>();

const emits = defineEmits(['onEdit', 'onDelete']);

const loading = ref<TStatus | undefined>(undefined);

const onSubmit = async (formData: IProduct) => {
  loading.value = 'loading';
  const { data, status } = await ProductService.editProduct(formData);
  loading.value = status.value;
  if ('id' in data.value?.content) {
    const newProduct = {
      ...formData,
      ...data.value?.content,
    };

    emits('onEdit', newProduct);
  }
};
</script>

<template>
  <ProductPopover
    :loading="loading"
    :productToEdit="productToEdit"
    :visible="visible"
    @submit="onSubmit"
    @delete="(id: number) => $emit('onDelete', id)" />
</template>
