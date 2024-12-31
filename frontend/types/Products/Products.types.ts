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
    priority?: number;
    shop?: {
        id?: number;
        name: string;
    };
    product_link?: string;
}

export interface IProductResponse extends IBaseResponse {
    content:
        | IProduct
        | { product_id: number; auto_generated_fields?: Record<string, string> }
        | IProduct[];
}
