<script setup lang="ts">
import type { DataTableRowDoubleClickEvent } from 'primevue/datatable';
import { initialTableColumns } from '../data';
import type { IProduct } from '~/types/Products/Products.types.ts';
import type { TStatus } from '~/types/index.types';

interface Props {
  products: IProduct[];
  loadingCheckbox: Record<string, TStatus>;
}

const props = defineProps<Props>();

const emit = defineEmits(['edit', 'changePurchasedState']);

const setColumnField = (value: string, field: keyof IProduct) => {
  if (!value) return '-';
  else if (field === 'buy_date' || field === 'guarantee_end_date') {
    return new Date(value).toLocaleDateString('ru-RU');
  } else {
    return value;
  }
};

const onEdit = (value: DataTableRowDoubleClickEvent) => {
  if (props.loadingCheckbox[value.data.id] === 'loading') return;

  emit('edit', toRaw(value.data));
};
</script>

<template>
  <DataTable :value="products" selection-mode="single" @row-dblclick="onEdit">
    <Column field="is_purchased">
      <template #body="{ data }">
        <Checkbox
          v-model="data.is_purchased"
          binary
          :disabled="loadingCheckbox[data.id] === 'loading'"
          @click="$emit('changePurchasedState', toRaw(data))" />
      </template>
    </Column>

    <Column v-for="column in initialTableColumns" :header="column.header" :field="column.field">
      <template #body="{ data }">{{ setColumnField(data[column.field], column.field) }}</template>
    </Column>

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
