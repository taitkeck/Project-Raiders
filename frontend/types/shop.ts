export interface CartProduct {
  name: string
  description: string
  price: number
  quantity: number
  tags: Array<string>
}

export interface Product extends CartProduct {
  _id: string
  date_modified: Date
}

export interface ProductList {
  count: number
  products: Array<Product>
}

export type Cart = {
  _id: string
  currency: string
  products: Record<string, CartProduct>
  total_price: string
  total_quantity: number
}
