export interface IProduct {
  id: number;
  name: string;
  price?: number | null;
  model?: string | null;
  is_purchased?: boolean;
  buy_date?: Date | null;
  guarantee?: number | null;
  guarantee_end_date?: Date | null;
  receipt?: string | null;
  shop?: string | null;
  priority?: number | null;
  tags?: string[] | null;
}
