import { get, post, patch, del } from '~/api';
import type { AsyncData } from 'nuxt/app';
import type { FetchError } from 'ofetch';

import type { IProduct, IProductResponse } from '~/types/Products/Products.types.ts';

export interface IProductApiParams {
  limit?: string;
  offset?: string;
  product_id?: number;
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
  }
};

export default class ProductService {
  static async getAll(params: IProductApiParams) {
    try {
      const products = await launchApi.get(params);

      if (products.error.value) {
        throw products;
      }

      return products as AsyncData<{ content: IProduct[] }, FetchError | null>;
    } catch (products) {
      console.log('products getAll error', products);
      return products as AsyncData<{ content: IProduct[] }, FetchError | null>;
    }
  }

  static async createProduct(body: IProduct) {
    try {
      const product = await launchApi.post(body);

      if (product.error.value) {
        throw product;
      }

      return product as AsyncData<IProductResponse, FetchError | null>;
    } catch (product) {
      console.log('products createProduct error', product);
      return product as AsyncData<IProductResponse, FetchError | null>;
    }
  }

  static async editProduct(body: IProduct) {
    try {
      const product = await launchApi.patch(body);

      if (product.error.value) {
        throw product;
      }

      return product as AsyncData<IProductResponse, FetchError | null>;
    } catch (product) {
      console.log('products editProduct error', product);
      return product as AsyncData<IProductResponse, FetchError | null>;
    }
  }

  static async deleteProduct(params: IProductApiParams) {
    try {
      const product = await launchApi.delete(params);

      if (product.error.value) {
        throw product;
      }

      return true;
    } catch (product) {
      console.log('products delProduct error', product);
      return false;
    }
  }
}
