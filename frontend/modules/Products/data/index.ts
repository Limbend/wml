import type { IProduct } from '~/types/Products/Products.types.ts';

export const initialTableColumns: {
    field: keyof IProduct;
    header: string;
    sortable?: Boolean;
}[] = [
    { field: 'name', header: 'Наименование', sortable: true },
    { field: 'model', header: 'Модель' },
    { field: 'price', header: 'Цена, ₽' },
    { field: 'buy_date', header: 'Дата покупки', sortable: true },
    { field: 'guarantee', header: 'Гарантийный срок, месяц', sortable: true },
    { field: 'guarantee_end_date', header: 'Окончание гарантии', sortable: true },
    // { field: 'receipt', header: 'Чек' },
    { field: 'shop', header: 'Магазин', sortable: true },
    // { field: 'tags', header: 'Тэги' },
    { field: 'priority', header: 'Приоритет', sortable: true },
];

export const initialProduct: IProduct = {
    id: undefined,
    name: 'Стаканчик',
    model: 'Пластиковый',
    price: 123,
    is_purchased: false,
    buy_date: undefined,
    guarantee: undefined,
    guarantee_end_date: undefined,
    // receipt: '',
    shop: { name: 'Магазин Стаканчиков' },
    product_link: 'https://stakunchiki.cum/samiy-luchshiy-stackunchik',
    priority: 5,
    /* tags: undefined // строка любая */
};
