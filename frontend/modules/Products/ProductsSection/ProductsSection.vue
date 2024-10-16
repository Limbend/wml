<script setup lang="ts">
import ProductService from '~/services/ProductsServices/ProductsService';
import type { IProduct } from '~/types/Products/Products.types';
import { useConfirm } from 'primevue/useconfirm';

import ConfirmDialog from 'primevue/confirmdialog';
import type { TStatus } from '~/types/index.types';

const confirm = useConfirm();

const { data } = await ProductService.getAll({});

// POPOVER
const addPopover = ref(false);
const editPopover = ref(false);
const productToEdit = ref<IProduct>();

// DELETE
const loadingDelete = ref<TStatus | undefined>();

// PURCHASED CHECKBOX
const purchasedCheckboxLoading = ref<Record<string, TStatus>>({});

const createProductHandler = (newProduct: IProduct) => {
  data.value.content?.unshift(newProduct);
  addPopover.value = false;
};

const editProductHandler = (editedProduct: IProduct) => {
  const productToEdit = data.value.content?.findIndex((i) => i.id === editedProduct.id);
  data.value.content[productToEdit] = { ...editedProduct };

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
      outlined: true
    },
    acceptProps: {
      label: 'Удалить',
      severity: 'danger',
      loading: loadingDelete.value === 'loading'
    },
    accept: async () => {
      await deleteProductHandler(productId);
    },
    reject: () => undefined
  });
};

const deleteProductHandler = async (productId: number) => {
  loadingDelete.value = 'loading';
  const result = await ProductService.deleteProduct({ product_id: productId });
  loadingDelete.value = 'success';

  if (result) {
    data.value.content = data.value.content?.filter((i) => i.id !== productId);
    editPopover.value = false;
  }
};

const changePurchasedStateHandler = async (product: IProduct) => {
  if (product.id) purchasedCheckboxLoading.value[product.id] = 'loading';

  const newProduct = await ProductService.editProduct({
    id: product.id,
    is_purchased: !product.is_purchased,
    name: product.name
  });

  if ('id' in newProduct.data.value?.content) {
    const productToEdit = data.value.content?.findIndex((i) => i.id === product.id);
    data.value.content[productToEdit].is_purchased = !product.is_purchased;
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
</script>

<template>
  <section>
    <div class="flex flex-wrap gap-2 justify-between items-center mb-4">
      <h1 class="whitespace-nowrap">Список покупок</h1>
      <Button icon="pi pi-plus" label="Создать" outlined @click="addPopover = true" />
    </div>

    <ProductsTable
      :products="data?.content || []"
      :loadingCheckbox="purchasedCheckboxLoading"
      @edit="openEditPopover"
      @change-purchased-state="changePurchasedStateHandler" />

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
      <ProductEditPopover
        :productToEdit="productToEdit"
        @on-edit="editProductHandler"
        @on-delete="deleteProductConfirm" />
    </Drawer>
  </section>

  <ConfirmDialog group="productDelete" />
</template>
