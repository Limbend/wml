<script setup lang="ts">
import LaunchService from '~/services/ProductsServices/ProductsService';

const products = await LaunchService.getAll({});

// POPOVER
const addPopover = ref(false);
</script>

<template>
  <section>
    <div class="flex justify-between items-center mb-4">
      <h1>Список покупок</h1>

      <Button icon="pi pi-plus" label="Создать" outlined @click="addPopover = true" />
    </div>

    <ProductsTable :products="products.data.value.products || []" />

    <Drawer
      v-model:visible="addPopover"
      header="Создать покупку"
      position="right"
      class="!w-full md:!w-[70%] lg:!w-[40%]">
      <ProductPopover />
    </Drawer>
  </section>
</template>
