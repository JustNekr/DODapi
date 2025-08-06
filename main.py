import uvicorn
from fastapi import FastAPI
# from auth.views import router as auth_router
from test.views import router as test_router

app = FastAPI(title="DOD", docs_url="/")

# app.include_router(auth_router)
app.include_router(test_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
