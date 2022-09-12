from sm_api.accounts.routes.auth import router as AuthRouter
from sm_api.accounts.routes.mail import router as MailRouter
from sm_api.accounts.routes.register import router as RegisterRouter
from sm_api.accounts.routes.user import router as UserRouter
from sm_api.apps.routes.app import router as AppsRouter
from sm_api.shop.routes.cart import router as CartRouter
from sm_api.shop.routes.product import router as ProductRouter
from sm_api.shop.routes.paypal import router as PayPalRouter

routers = {
    "accounts": [
        AuthRouter,
        MailRouter,
        RegisterRouter,
        UserRouter,
    ],
    "apps": [AppsRouter],
    "shop": [
        CartRouter,
        PayPalRouter,
        ProductRouter,
    ],
}
