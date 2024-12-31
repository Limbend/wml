import { get, post, patch, del } from '~/api';
import type { AsyncData } from 'nuxt/app';
import type { FetchError } from 'ofetch';

import type { IProduct, IProductResponse } from '~/types/Products/Products.types.ts';
import type { TEmptyObject, TStatus } from '~/types/index.types';
import { messageHandler } from '~/api/messageHandler/messageHandler';

export interface IProductApiParams {
    by?: number;
    chunk?: number;
    product_id?: number;
    field?: keyof IProduct;
    desc?: boolean;
    search_query?: string;
}

const launchApi = {
    async get(params: IProductApiParams) {
        return await get('/products', params);
    },

    async post(body: IProduct) {
        return await post('/products', body);
    },

    async patch(body: IProduct) {
        return await patch('/products', body);
    },

    async delete(params: IProductApiParams) {
        return await del('/products', params);
    },
};

export default class ProductService {
    static async getAll(
        params: IProductApiParams,
        loading: Ref<TStatus> | TEmptyObject = {},
    ) {
        loading.value = 'loading';
        try {
            const products = await launchApi.get(params);

            if (products.error.value) {
                throw products;
            }

            return products as AsyncData<
                { content: IProduct[]; total_count: number },
                FetchError | null
            >;
        } catch (products) {
            messageHandler({
                message: 'Ошибка при получении списка покупок',
                type: 'error',
            });
            console.log('products getAll error', products);
            return products as AsyncData<
                { content: IProduct[]; total_count: number },
                FetchError | null
            >;
        } finally {
            loading.value = 'success';
        }
    }

    static async createProduct(
        body: IProduct,
        loading: Ref<TStatus> | TEmptyObject = {},
    ) {
        loading.value = 'loading';
        try {
            const product = await launchApi.post(body);

            if (product.error.value) {
                throw product;
            }

            messageHandler({
                message: `Покупка: ${body.name}, успешно создана`,
                type: 'success',
            });

            return product as AsyncData<IProductResponse, FetchError | null>;
        } catch (product) {
            messageHandler({
                message: 'Ошибка при создании покупки',
                type: 'error',
            });
            console.log('products createProduct error', product);
            return product as AsyncData<IProductResponse, FetchError | null>;
        } finally {
            loading.value = 'success';
        }
    }

    static async editProduct(body: IProduct, loading: Ref<TStatus> | TEmptyObject = {}) {
        loading.value = 'loading';
        try {
            const product = await launchApi.patch(body);

            if (product.error.value) {
                throw product;
            }

            messageHandler({
                message: `Покупка: ${body.name}, отредактирована`,
                type: 'success',
            });

            return product as AsyncData<IProductResponse, FetchError | null>;
        } catch (product) {
            console.log('products editProduct error', product);
            messageHandler({
                message: 'Ошибка при редактировании покупки',
                type: 'error',
            });
            return product as AsyncData<IProductResponse, FetchError | null>;
        } finally {
            loading.value = 'success';
        }
    }

    static async deleteProduct(params: IProductApiParams, name: string) {
        try {
            const product = await launchApi.delete(params);

            if (product.error.value) {
                throw product;
            }

            messageHandler({
                message: `Покупка: ${name} была удалена`,
                type: 'success',
            });

            return product as AsyncData<{ content: IProduct[] }, FetchError | null>;
        } catch (product) {
            console.log('products delProduct error', product);
            messageHandler({
                message: 'Ошибка при удалении покупки',
                type: 'error',
            });
            return product as AsyncData<{ content: IProduct[] }, FetchError | null>;
        }
    }
}
