from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.routers import user, post, auth, auth2

app = FastAPI()

origin = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origin,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    )



app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(auth2.router)

app.openapi = lambda: None

@app.get("/")
def root(request: Request):
    return {"messege": "MNSM"}






###uvicorn app.main:app --reload
##uvicorn --host 0.0.0.0 app.main:app
##uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 2 --reload
#pip freeze > requirements.txt
#pip install -r requirements.txt
