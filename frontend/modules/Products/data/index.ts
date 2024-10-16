import type { IProduct } from '~/types/Products/Products.types.ts';

export const initialTableColumns: { field: keyof IProduct; header: string }[] = [
  { field: 'name', header: 'Наименование' },
  { field: 'price', header: 'Цена, ₽' },
  { field: 'model', header: 'Модель' },
  { field: 'buy_date', header: 'Дата покупки' },
  { field: 'guarantee', header: 'Гарантийный срок, месяц' },
  { field: 'guarantee_end_date', header: 'Окончание гарантии' },
  { field: 'receipt', header: 'Чек' },
  { field: 'shop', header: 'Магазин' },
  { field: 'tags', header: 'Тэги' },
  { field: 'priority', header: 'Приоритет' }
];

export const initialProduct: IProduct = {
  id: undefined,
  name: 'Стаканчик',
  price: 123,
  model: 'Пластиковый',
  is_purchased: false,
  buy_date: undefined,
  guarantee: undefined,
  guarantee_end_date: undefined,
  receipt: '',
  shop: '',
  priority: 5
  /* tags: undefined // строка любая */
};
