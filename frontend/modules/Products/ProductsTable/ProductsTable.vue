<script setup lang="ts">
import type {
    DataTableRowDoubleClickEvent,
    DataTableSortEvent,
} from 'primevue/datatable';
import { initialTableColumns } from '../data';
import type { IProduct } from '~/types/Products/Products.types.ts';
import type { TStatus } from '~/types/index.types';

interface Props {
    products: IProduct[];
    loadingCheckbox: Record<string, TStatus>;
    loading: boolean;
}

const props = defineProps<Props>();

const emit = defineEmits([
    'edit',
    'changePurchasedState',
    'sort',
    'addProduct',
    'search',
]);

const searchValue = ref('');

const setColumnField = (value: string | { name: string }, field: keyof IProduct) => {
    if (!value) return '-';
    else if (
        typeof value === 'string' &&
        (field === 'buy_date' || field === 'guarantee_end_date')
    ) {
        return new Date(value).toLocaleDateString('ru-RU');
    } else if (field === 'shop' && typeof value === 'object') {
        return value.name;
    } else {
        return value;
    }
};

const onEdit = (value: DataTableRowDoubleClickEvent) => {
    if (props.loadingCheckbox[value.data.id] === 'loading') return;

    emit('edit', toRaw(value.data));
};

const onSort = (value: DataTableSortEvent) => {
    emit('sort', {
        field: value.sortField || undefined,
        desc: value.sortOrder === 1 ? false : true,
    });
};

const searchInputHandle = debounce(() => {
    emit('search', searchValue.value);
}, 1000);

const searchEmptyInputHandle = () => {
    searchValue.value = '';
    emit('search', searchValue.value);
};
</script>

<template>
    <div class="flex flex-wrap gap-x-4 gap-y-2 justify-between items-center mb-4">
        <IconField class="flex-grow">
            <InputText
                v-model="searchValue"
                class="w-full"
                placeholder="Поиск..."
                type="text"
                id="product-search"
                @input="searchInputHandle" />
            <InputIcon
                v-if="!loading && searchValue.length"
                class="pi pi-times cursor-pointer"
                @click="searchEmptyInputHandle" />
            <InputIcon v-if="loading" class="pi pi-spin pi-spinner" />
        </IconField>

        <Button icon="pi pi-plus" label="Создать" outlined @click="emit('addProduct')" />
    </div>

    <DataTable
        :value="products"
        selection-mode="single"
        :loading="loading"
        removableSort
        @sort="onSort"
        @row-dblclick="onEdit"
        lazy>
        <Column field="is_purchased">
            <template #body="{ data }">
                <Checkbox
                    v-model="data.is_purchased"
                    binary
                    :disabled="loadingCheckbox[data.id] === 'loading'"
                    @click="$emit('changePurchasedState', toRaw(data))" />
            </template>
        </Column>

        <Column
            v-for="column in initialTableColumns"
            :header="column.header"
            :field="column.field"
            :sortable="column.sortable ? true : false">
            <template #body="{ data }">{{
                setColumnField(data[column.field], column.field)
            }}</template>
        </Column>

        <template #empty>
            <div class="w-full flex gap-3 justify-center">
                <div
                    class="border-solid justify-center border rounded flex gap-3 items-center p-4 w-full">
                    <i class="pi pi-folder-open"></i>
                    <p>Список товаров пуст</p>
                </div>
            </div>
        </template>
    </DataTable>
</template>
