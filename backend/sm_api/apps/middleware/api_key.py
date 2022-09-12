from starlette.middleware.base import BaseHTTPMiddleware
from starlette.routing import Match
from fastapi import Request, HTTPException, Response

from sm_api.apps.models.app import App
from sm_api.routers import routers

# extends BaseHTTPMiddleware filter.
class APIKeyMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        # TODO: Check for api key and route permissions
        try:
            api_key = request.headers.get("x-api-key")
            app = await App.find_one(App.api_key == api_key)
            if api_key is None or app is None:
                # If it's a same origin request
                if f"{request.url.hostname}:{request.url.port}" == "localhost:8080":
                    app = await App.find_one(App.name == "default")
                # TODO: If the domain is not allowed
                # elif not request.url in app.domains:
                #   raise HTTPException(403, "Domain not authorized")
                else:
                    raise HTTPException(403, "API Key missing or invalid")
            # Store the app in the request state
            request.state.app = app

            # Check request url
            if app.name == "default":
                # success
                response = await call_next(request)
                return response

            for service in app.services:
                # print(service.name)
                for router in routers[service.name]:
                    for route in router.routes:
                        if route.matches(request.scope)[0] == Match.FULL:
                            # success
                            response = await call_next(request)
                            return response

            raise HTTPException(403, "Access denied")
        except HTTPException as e:
            return Response(e.detail, e.status_code)
