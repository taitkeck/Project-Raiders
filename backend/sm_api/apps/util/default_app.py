from sm_api.apps.models.app import Service, App
from .api_key import key_gen
import os
import json


async def get_default_app():
    """
    The default app is for the docs, testing, and same-origin requests.
    The api key of the app is written to ~/fake_data/.env.
    """
    app = await App.find_one(App.name == "default")
    if app is None:
        app = App(
            name="default", domains=[], services=Service.get_all(), api_key=key_gen()
        )
        await app.create()
    if len(app.services) != Service.get_all():
        app.services = Service.get_all()
        await app.save()

    with open(f"{os.getcwd()}/fake_data/.env", "w") as f:
        f.write(f"API_KEY={app.api_key}")
    with open(f"{os.getcwd()}/default_app.json", "w") as f:
        f.write(app.json())
    return app
