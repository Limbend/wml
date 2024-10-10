import type { IBaseResponse } from '~/types/responses/Responses.types';

export interface IProduct {
  id?: number;
  name: string;
  price?: number;
  model?: string;
  is_purchased?: boolean;
  buy_date?: Date | string;
  guarantee?: number;
  guarantee_end_date?: Date;
  receipt?: string;
  shop?: string;
  priority?: number;
  tags?: string[];
}

export interface IProductResponse extends IBaseResponse {
  content:
    | IProduct
    | { product_id: number; auto_generated_fields?: Record<string, string> }
    | IProduct[];
}
