from fastapi import FastAPI

import hobby_tracker_api.routers as routers

app = FastAPI()

app.include_router(routers.auth_router)
