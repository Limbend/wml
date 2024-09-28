<script setup>
import { initialTableColumns } from '../data';

const products = ref([]);
</script>

<template>
  <section>
    <p>Таблица с продуктами</p>
    <DataTable :value="products">
      <Column v-for="column in initialTableColumns" :header="column.header" :field="column.field" />

      <template #empty>
        <div class="w-full flex gap-3 justify-center">
          <div class="border-solid border rounded flex gap-3 items-center p-4">
            <i class="pi pi-folder-open"></i>
            <p>Список товаров пуст</p>
          </div>
        </div>
      </template>
    </DataTable>
  </section>
</template>
