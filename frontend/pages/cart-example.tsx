import Layout from "../components/layout"
import { useEffect, useState } from "react"
import { Cart, CartProduct, Product, ProductList } from "../types/shop"

export default function CartExamplePage() {
  const [cart, setCart] = useState<Cart>()
  // How many products in the database. Used to get a random product.
  const [productCount, setProductCount] = useState(1)

  const addRandomItemToCart = async () => {
    async function getProduct() {
      const productIndex = Math.floor(Math.random() * productCount)
      // get one product
      const randProductRes = await fetch(
        `/api/shop/products?skip=${productIndex}&limit=1`
      )
      const randProductData = (await randProductRes.json()) as ProductList
      setProductCount(randProductData.count)
      return randProductData.products[0]
    }

    async function addToCart(product: Product) {
      const cartPost = `/api/shop/cart/add`
      const body = {
        id: cart && cart._id ? cart._id : undefined,
        product_id: product._id,
        quantity: Math.ceil(Math.random() * 3),
      }

      if (!body.id) {
        delete body.id
      }

      const addToCartRes = await fetch(cartPost, {
        method: "POST",
        body: JSON.stringify(body),
      })
      const newCart = (await addToCartRes.json()) as Cart

      if (newCart.products) {
        console.log(newCart)
        setCart(newCart)
      }
    }

    const product = await getProduct()
    await addToCart(product)
  }

  const deleteCart = async () => {
    localStorage.removeItem("cart")
    if (cart && cart._id) {
      await fetch(`/api/shop/cart/delete/${cart?._id}`)
      setCart(undefined)
    }
  }

  const deleteCartItem = async (product_id: string) => {
    if (cart && cart._id) {
      const cartRes = await fetch(
        `/api/shop/cart/delete/${cart?._id}/${product_id}`
      )
      const cartData = (await cartRes.json()) as Cart
      if (cartData) {
        if (cartData.total_quantity === 0) {
          await deleteCart()
        } else {
          setCart(cartData)
        }
      }
    }
  }

  const submitPurchase = () => {
    alert("You bought some stuff!")
    deleteCart()
  }

  useEffect(() => {
    const getCartDB = async () => {
      try {
        const cartRes = await fetch("/api/shop/cart")
        const cartData = (await cartRes.json()) as Cart
        if (cartData && cartData._id) {
          setCart(cartData)
        }
      } catch (e) {
        // no cart found
      }
    }

    if (cart) {
      localStorage.setItem("cart", JSON.stringify(cart))
    } else {
      // first load
      const cartDataJSON = localStorage.getItem("cart")
      if (cartDataJSON) {
        const cartData = JSON.parse(cartDataJSON) as Cart
        if (cartData && cartData._id) {
          setCart(cartData)
        }
      } else {
        getCartDB()
      }
    }
  }, [cart])

  return (
    <Layout>
      <h1>Cart Example</h1>
      <button onClick={addRandomItemToCart}>
        Add Random Product To Cart +
      </button>

      {cart && cart._id && (
        <>
          <button onClick={deleteCart}>Delete Cart</button>
          <ul>
            {cart.products &&
              Object.entries(cart.products).map((item, i) => (
                <li key={item[1].name + i}>
                  <h3>{item[1].name}</h3>
                  <p>
                    Quantity: {item[1].quantity}
                    <br />
                    Price Per Item: {cart.currency}
                    {item[1].price}
                  </p>
                  <button
                    style={{ float: "right" }}
                    onClick={() => deleteCartItem(item[0])}
                  >
                    Remove From Cart
                  </button>
                </li>
              ))}
          </ul>
          <div>
            <h2>Total</h2>
            <p>
              {cart.currency}
              {cart.total_price}
            </p>
            <button onClick={submitPurchase}>BUY NOW!</button>
          </div>
        </>
      )}
    </Layout>
  )
}
