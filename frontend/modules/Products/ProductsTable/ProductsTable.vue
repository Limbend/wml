<script setup lang="ts">
import { initialTableColumns } from '../data';
import type { IProduct } from '~/types/Products/Products.types.ts';

interface Props {
  products: IProduct[];
}

defineProps<Props>();
</script>

<template>
  <DataTable :value="products">
    <Column
      v-for="column in initialTableColumns"
      :header="column.header"
      :field="column.field as string" />

    <template #empty>
      <div class="w-full flex gap-3 justify-center">
        <div class="border-solid justify-center border rounded flex gap-3 items-center p-4 w-full">
          <i class="pi pi-folder-open"></i>
          <p>Список товаров пуст</p>
        </div>
      </div>
    </template>
  </DataTable>
</template>
