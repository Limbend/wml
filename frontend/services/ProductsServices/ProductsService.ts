import { get } from '~/api';
import type { AsyncData } from 'nuxt/app';
import type { FetchError } from 'ofetch';

import type { IProduct } from '~/types/Products/Products.types.ts';

export interface IProductApiParams {
  limit?: string;
  offset?: string;
}

const launchApi = {
  async get(params: IProductApiParams) {
    return await get('/products', params);
  }
};

export default class LaunchService {
  static async getAll(params: IProductApiParams) {
    try {
      const products = await launchApi.get(params);

      if (products.error.value) {
        throw products;
      }

      return products as AsyncData<{ products?: IProduct[] }, FetchError | null>;
    } catch (products) {
      console.log('products getAll error', products);
      return products as AsyncData<{ products?: IProduct[] }, FetchError | null>;
    }
  }
}
