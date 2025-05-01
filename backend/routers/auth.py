from fastapi import APIRouter

router = APIRouter()

@router.post("/register")
def register(username: str, password: str):
    return {"message": f"User {username} registered successfully."}

@router.post("/login")
def login(username: str, password: str):
    return {"message": f"User {username} logged in successfully."}
