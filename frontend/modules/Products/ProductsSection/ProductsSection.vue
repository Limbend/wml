<script setup lang="ts">
import ProductService from '~/services/ProductsServices/ProductsService';
import type { IProduct } from '~/types/Products/Products.types';

const { data } = await ProductService.getAll({});

// POPOVER
const addPopover = ref(false);
const editPopover = ref(false);
const productToEdit = ref<IProduct>();

const createProductHandler = (newProduct: IProduct) => {
  data.value.products?.unshift(newProduct);
  addPopover.value = false;
};

const editProductHandler = (editedProduct: IProduct) => {
  const productToEdit = data.value.products?.findIndex((i) => i.id === editedProduct.id);
  if (productToEdit && data.value.products) {
    data.value.products[productToEdit] = { ...editedProduct };
  }

  editPopover.value = false;
};

const openEditPopover = (product: IProduct) => {
  productToEdit.value = product;
  editPopover.value = true;
};

watchEffect(() => {
  if (editPopover.value || addPopover.value) {
    document.body.style.overflow = 'hidden';
  } else {
    document.body.style.overflow = '';
  }
});
</script>

<template>
  <section>
    <div class="flex flex-wrap gap-2 justify-between items-center mb-4">
      <h1 class="whitespace-nowrap">Список покупок</h1>
      <Button icon="pi pi-plus" label="Создать" outlined @click="addPopover = true" />
    </div>

    <ProductsTable :products="data.products || []" @edit="openEditPopover" />

    <Drawer
      v-model:visible="addPopover"
      header="Создать покупку"
      position="right"
      class="!w-full md:!w-[70%] lg:!w-[40%]">
      <ProductCreatePopover @on-create="createProductHandler" />
    </Drawer>

    <Drawer
      v-model:visible="editPopover"
      header="Редактировать покупку"
      position="right"
      class="!w-full md:!w-[70%] lg:!w-[40%]">
      <ProductEditPopover :productToEdit="productToEdit" @on-edit="editProductHandler" />
    </Drawer>
  </section>
</template>
