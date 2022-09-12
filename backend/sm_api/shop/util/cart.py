from sm_api.shop.models.cart import Cart, CartRead


def get_cart_read(cart: Cart | None):
    if cart is None:
        return None
    return CartRead(
        **cart.dict(), total_price=cart.price(), total_quantity=cart.quantity()
    )
