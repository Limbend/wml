<script setup lang="ts">
import type { IProduct } from '~/types/Products/Products.types';
import { initialProduct } from '../data';
import * as Yup from 'yup';
import type { TStatus } from '~/types/index.types';

import { Form } from 'vee-validate';

type Props = {
  loading?: TStatus;
  productToEdit?: IProduct;
  visible: Boolean;
};

const props = defineProps<Props>();

const emits = defineEmits(['submit', 'delete']);

const schema = Yup.object().shape({
  name: Yup.string()
    .max(50, 'Максимальное количество символов 50')
    .required('Поле обязательное для заполнения'),
  model: Yup.string().max(255, 'Максимальное количество символов 255').nullable(),
  price: Yup.number().nullable().nullable(),
  is_purchased: Yup.boolean().nullable(),
  buy_date: Yup.date().nullable(),
  guarantee: Yup.number().nullable(),
  shop: Yup.string().nullable().max(255, 'Максимальное количество символов 255'),
  priority: Yup.number().nullable(),
});

const { handleSubmit, defineField, submitCount, errors, resetForm } = useForm<IProduct>({
  validationSchema: schema,
  initialValues: props.productToEdit?.id
    ? { ...props.productToEdit }
    : { ...initialProduct },
});

const [name] = defineField('name');
const [model] = defineField('model');
const [price] = defineField('price');
const [purchased] = defineField('is_purchased');
const [buy_date] = defineField('buy_date') as any;
const [guarantee] = defineField('guarantee');
const [shop] = defineField('shop');
const [priority] = defineField('priority');

// deprecated, but that was so cool, why did they deprecate it, wtf!?
/* const [name, model, purchased, price] = useFieldModel(['name', 'model', 'purchased', 'price']); */

const onSubmit: any = handleSubmit((values: IProduct) => {
  const preparedData = { ...values };
  preparedData.buy_date =
    preparedData.buy_date && new Date(preparedData.buy_date).toLocaleDateString('en-CA');
  emits('submit', preparedData);
  !props.visible && resetForm();
});
</script>

<template>
  <Form class="w-full flex flex-col" novalidate @submit="onSubmit">
    <div class="flex flex-col gap-y-5 mb-5">
      <div class="w-full flex justify-between pt-1">
        <div class="flex items-center gap-2 mb-2">
          <Checkbox v-model="purchased" inputId="purchased" :binary="true" />
          <label for="purchased" class="ml-1 cursor-pointer">Приобретено</label>
        </div>
        <Button
          v-if="productToEdit?.id"
          icon="pi pi-trash"
          aria-label="Delete"
          label="Удалить"
          severity="danger"
          size="small"
          text
          @click="$emit('delete', productToEdit?.id)" />
      </div>
      <div class="flex flex-col gap-y-1">
        <FloatLabel variant="on">
          <InputText
            class="w-full"
            :class="submitCount && errors.name && 'p-invalid'"
            type="text"
            id="product-name"
            v-model="name" />
          <label
            for="product-name"
            :class="submitCount && errors.name && '!text-errorColor'"
            ><sup class="text-errorColor">*</sup>Наименование</label
          >
        </FloatLabel>
        <small v-if="submitCount" class="ml-2 text-errorColor">{{ errors.name }}</small>
      </div>

      <div class="flex flex-col gap-y-1">
        <FloatLabel variant="on">
          <InputText
            class="w-full"
            type="text"
            id="product-model"
            :class="submitCount && errors.model && 'p-invalid'"
            v-model="model" />
          <label
            for="product-model"
            :class="submitCount && errors.model && '!text-errorColor'"
            >Модель</label
          >
        </FloatLabel>
        <small v-if="submitCount" class="ml-2 text-errorColor">{{ errors.model }}</small>
      </div>

      <div class="flex flex-col gap-y-1">
        <FloatLabel variant="on">
          <InputNumber
            class="w-full"
            :class="submitCount && errors.price && 'p-invalid'"
            type="text"
            id="product-price"
            :minFractionDigits="2"
            :max="99999999"
            currency="RUB"
            mode="currency"
            v-model="price" />
          <label
            for="product-price"
            :class="submitCount && errors.price && '!text-errorColor'"
            >Цена</label
          >
        </FloatLabel>
        <small v-if="submitCount" class="ml-2 text-errorColor">{{ errors.price }}</small>
      </div>

      <div class="flex flex-col gap-y-1">
        <FloatLabel variant="on">
          <DatePicker
            dateFormat="dd.mm.yy"
            class="w-full"
            v-model="buy_date"
            id="product-buy-date"
            :invalid="Boolean(submitCount) && Boolean(errors.buy_date)"
            showIcon
            iconDisplay="input" />
          <label
            for="product-buy-date"
            :class="submitCount && errors.buy_date && '!text-errorColor'"
            >Дата покупки</label
          >
        </FloatLabel>
        <small v-if="submitCount" class="ml-2 text-errorColor">{{
          errors.buy_date
        }}</small>
      </div>

      <div class="flex flex-col gap-y-1">
        <FloatLabel variant="on">
          <InputNumber
            class="w-full"
            :class="submitCount && errors.guarantee && 'p-invalid'"
            type="text"
            id="product-guarantee"
            :max="99999999"
            v-model="guarantee" />
          <label
            for="product-guarantee"
            :class="submitCount && errors.guarantee && '!text-errorColor'"
            >Гарантийный срок, месяцы</label
          >
        </FloatLabel>
        <small v-if="submitCount" class="ml-2 text-errorColor">{{
          errors.guarantee
        }}</small>
      </div>

      <div class="flex flex-col gap-y-1">
        <FloatLabel variant="on">
          <InputText
            class="w-full"
            :class="submitCount && errors.shop && 'p-invalid'"
            type="text"
            id="product-shop"
            v-model="shop" />
          <label
            for="product-shop"
            :class="submitCount && errors.shop && '!text-errorColor'"
            >Место приобретения</label
          >
        </FloatLabel>
        <small v-if="submitCount" class="ml-2 text-errorColor">{{ errors.shop }}</small>
      </div>

      <div class="flex flex-col gap-y-1">
        <FloatLabel variant="on">
          <InputNumber
            v-model="priority"
            id="product-priority"
            showButtons
            buttonLayout="horizontal"
            :step="1"
            :min="1"
            :max="10"
            fluid>
            <template #incrementicon>
              <span class="pi pi-plus" />
            </template>
            <template #decrementicon>
              <span class="pi pi-minus" />
            </template>
          </InputNumber>
          <label for="product-priority">Приоритет</label>
        </FloatLabel>
        <small v-if="submitCount" class="ml-2 text-errorColor">{{
          errors.priority
        }}</small>
      </div>
    </div>

    <Button
      :label="productToEdit?.id ? 'Сохранить' : 'Создать'"
      type="submit"
      :loading="loading === 'loading'" />
  </Form>
</template>
