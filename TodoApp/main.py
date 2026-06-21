from fastapi import FastAPI, Request, status
from .models import Base
from .database import engine
from .routers import auth, todos, admin, users
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

app = FastAPI()

# Instantiate DB and table(s); only runs if xx.db does not yet exist!
Base.metadata.create_all(bind=engine)

# Set static file use (CSS, JS)
app.mount("/static", StaticFiles(directory="TodoApp/static"), name="static")

# test endpoint
@app.get("/")
def test(request: Request):
    return RedirectResponse(url="/todos/todo-page", status_code=status.HTTP_302_FOUND)
  

# Test endpoint
@app.get("/health")
def health_check():
    return { "status": "Healthy"}


# Use router for auth endpoint
app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)