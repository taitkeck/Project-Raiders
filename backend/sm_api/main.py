"""
Server main runtime
"""

# pylint: disable=unused-import

from sm_api.app import app
from sm_api.routers import routers

for r_list in routers.values():
    for r in r_list:
        app.include_router(r)
