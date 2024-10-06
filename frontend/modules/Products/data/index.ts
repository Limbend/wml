import type { IProduct } from '~/types/Products/Products.types.ts';

export const initialTableColumns: { field: keyof IProduct; header: string }[] = [
  { field: 'is_purchased', header: 'Приобретено' },
  { field: 'name', header: 'Наименование' },
  { field: 'price', header: 'Цена' },
  { field: 'model', header: 'Модель' },
  { field: 'buy_date', header: 'Дата покупки' },
  { field: 'guarantee', header: 'Гарантийный срок' },
  { field: 'guarantee_end_date', header: 'Окончание гарантии' },
  { field: 'receipt', header: 'Чек' },
  { field: 'shop', header: 'Магазин' },
  { field: 'tags', header: 'Тэги' },
  { field: 'priority', header: 'Приоритет' }
];

export const initialProduct: IProduct = {
  id: 0,
  name: '',
  price: null,
  model: '',
  is_purchased: false,
  buy_date: null,
  guarantee: null,
  guarantee_end_date: null,
  receipt: '',
  shop: '',
  priority: 1,
  tags: null
};
