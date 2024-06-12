from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from firebase_admin import auth
from api.models.user import UserSchema
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from config.firebase_config import firebase
from security.authentication import verify_token

router = APIRouter()


@router.post("/signup", tags=["Users"])
def create_account(user: UserSchema):
    email = user.email
    password = user.password

    try:
        user = auth.create_user(email=email, password=password)
        return JSONResponse(
            content={
                "status_code": 201,
                "message": f"User account created successfully for user {user.uid}",
            }
        )
    except auth.EmailAlreadyExistsError:
        raise HTTPException(status_code=400, detail="An error occurred")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/token", tags=["Users"])
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    email = form_data.username
    password = form_data.password

    try:
        user = firebase.auth().sign_in_with_email_and_password(
            email=email, password=password
        )
        token = user["idToken"]

        return {"access_token": token, "token_type": "bearer"}
    except:
        raise HTTPException(status_code=400, detail="Invalid credentials")


@router.get("/me", tags=["Users"])
def my_user(uid: str = Depends(verify_token)):
    return JSONResponse(
        content={
            "message": f"Welcome, your user ID is {uid}",
        },
        status_code=200,
    )
