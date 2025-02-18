<script setup lang="ts">
import type { IProduct } from '~/types/Products/Products.types';
import type { TStatus } from '~/types/index.types';
import ProductService from '~/services/ProductsServices/ProductsService';
import { useConfirm } from 'primevue/useconfirm';

import ConfirmDialog from 'primevue/confirmdialog';

const confirm = useConfirm();

// infinite scroll
const infiniteScrollTrigger = ref<HTMLElement | null>(null);
const rowsByPage = 25;
const currentPage = ref(0);
const sortParams = ref<{ field?: keyof IProduct; desc?: boolean }>({});
const searchParam = ref('');

const productParams = computed(() => {
    return {
        by: rowsByPage,
        chunk: currentPage.value,
        ...sortParams.value,
        search_query: searchParam.value || undefined,
    };
});

const { data } = await ProductService.getAll(productParams.value);

// Products
const products = ref<IProduct[]>([...data.value.content]);
const infinityScrollLoading = ref<TStatus>('success');
const productsLoading = ref<TStatus>('success');
let totalCount = data.value.total_count;

const fetchProducts = async (infinityScroll?: boolean) => {
    const { data } = await ProductService.getAll(
        productParams.value,
        infinityScroll ? infinityScrollLoading : productsLoading,
    );

    if (infinityScroll && data.value.content.length) {
        totalCount = data.value.total_count;
        products.value.push(...data.value.content);
    } else {
        totalCount = data.value.total_count;
        products.value = data.value.content;
    }
};

// POPOVER
const addPopover = ref(false);
const editPopover = ref(false);
const productToEdit = ref<IProduct>();

// DELETE
const loadingDelete = ref<TStatus | undefined>();

// PURCHASED CHECKBOX
const purchasedCheckboxLoading = ref<Record<string, TStatus>>({});

// RECEIPT
const receiptPopover = ref();
const selectedProductReceipt = ref<IProduct>();

const openProductReceiptPopover = (product: IProduct, event: Event) => {
    receiptPopover.value.hide();
    selectedProductReceipt.value = product;
    nextTick(() => {
        receiptPopover.value.show(event);
    });
};

// SORT
const changeSortParams = async (params: { field?: keyof IProduct; desc?: boolean }) => {
    sortParams.value = params;
    currentPage.value = 0;
    await fetchProducts();
};

const changeSearchParam = async (value: string) => {
    searchParam.value = value;
    currentPage.value = 0;
    await fetchProducts();
};

const createProductHandler = (newProduct: IProduct) => {
    products.value.unshift(newProduct);
    addPopover.value = false;
};

const editProductHandler = (editedProduct: IProduct) => {
    const productToEdit = products.value.findIndex(i => i.id === editedProduct.id);
    products.value[productToEdit] = { ...editedProduct };

    editPopover.value = false;
};

const openEditPopover = (product: IProduct) => {
    productToEdit.value = product;
    editPopover.value = true;
};

const deleteProductConfirm = (productId: number) => {
    confirm.require({
        group: 'productDelete',
        message: 'Это действие будет невозможно отменить',
        header: 'Удалить покупку?',
        icon: 'pi pi-info-circle',
        rejectProps: {
            label: 'Отмена',
            severity: 'secondary',
            outlined: true,
        },
        acceptProps: {
            label: 'Удалить',
            severity: 'danger',
            loading: loadingDelete.value === 'loading',
        },
        accept: async () => {
            await deleteProductHandler(productId);
        },
        reject: () => undefined,
    });
};

const deleteProductHandler = async (productId: number) => {
    loadingDelete.value = 'loading';
    const deletedProduct = products.value.find(i => i.id === productId);
    const { data, status } = await ProductService.deleteProduct(
        { product_id: productId, ...productParams.value },
        deletedProduct?.name || '',
    );
    loadingDelete.value = status.value;

    if (status.value === 'success') {
        products.value = products.value?.filter(i => i.id !== productId);
        if (
            data.value.content.length &&
            !products.value.some(i => i.id === data.value.content[0].id)
        ) {
            products.value.push(data.value.content[0]);
        }
        totalCount -= 1;
        editPopover.value = false;
    }
};

const changePurchasedStateHandler = async (product: IProduct) => {
    if (product.id) purchasedCheckboxLoading.value[product.id] = 'loading';

    const newProduct = await ProductService.editProduct({
        id: product.id,
        is_purchased: !product.is_purchased,
        name: product.name,
    });

    if ('id' in newProduct.data.value?.content) {
        const productToEdit = products.value?.findIndex(i => i.id === product.id);
        products.value[productToEdit].is_purchased = !product.is_purchased;
    }
    if (newProduct.status.value !== 'pending' && product.id)
        delete purchasedCheckboxLoading.value[product.id];
};

watchEffect(() => {
    if (!document) return;
    if (editPopover.value || addPopover.value) {
        document.body.style.overflow = 'hidden';
    } else {
        document.body.style.overflow = '';
    }
});

// Инициализация Intersection Observer
watchEffect(() => {
    if (!infiniteScrollTrigger.value) return;

    const observer = new IntersectionObserver(
        async ([entry]) => {
            if (entry.isIntersecting) {
                currentPage.value += 1;
                await fetchProducts(true);
            }
        },
        { rootMargin: '0px 0px 100px 0px' }, // Триггер срабатывает за 100px до видимости элемента
    );

    observer.observe(infiniteScrollTrigger.value);

    return () => {
        observer.disconnect();
    };
});
</script>

<template>
    <section class="p-4">
        <div class="flex flex-wrap gap-2 justify-between items-center mb-4">
            <h1 class="whitespace-nowrap">Список покупок</h1>
        </div>
        <ProductsTable
            :products="products"
            :loadingCheckbox="purchasedCheckboxLoading"
            :loading="productsLoading === 'loading'"
            @add-product="addPopover = true"
            @edit="openEditPopover"
            @change-purchased-state="changePurchasedStateHandler"
            @sort="changeSortParams"
            @search="changeSearchParam"
            @receipt="openProductReceiptPopover" />

        <UILoader v-if="infinityScrollLoading === 'loading'" />
        <div
            ref="infiniteScrollTrigger"
            class="h-1"
            v-show="
                infinityScrollLoading === 'success' && products.length < totalCount
            "></div>

        <Drawer
            v-model:visible="addPopover"
            header="Создать покупку"
            position="right"
            class="!w-full md:!w-[70%] lg:!w-[40%]">
            <ProductCreatePopover
                :visible="addPopover"
                @on-create="createProductHandler" />
        </Drawer>

        <Drawer
            v-model:visible="editPopover"
            header="Редактировать покупку"
            position="right"
            class="!w-full md:!w-[70%] lg:!w-[40%]">
            <ProductEditPopover
                :visible="editPopover"
                :productToEdit="productToEdit"
                @on-edit="editProductHandler"
                @on-delete="deleteProductConfirm" />
        </Drawer>

        <Popover ref="receiptPopover">
            <div v-if="selectedProductReceipt" class="rounded flex flex-col">
                <ProductReceiptPopover :productId="selectedProductReceipt.id || 0" />
            </div>
        </Popover>
    </section>

    <ConfirmDialog group="productDelete" />
</template>
