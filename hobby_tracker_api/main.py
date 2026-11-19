from fastapi import FastAPI

import hobby_tracker_api.routers as routers

app = FastAPI(title="Hobby Tracker API")

app.include_router(routers.activity_router)
app.include_router(routers.auth_router)
app.include_router(routers.hobby_router)
