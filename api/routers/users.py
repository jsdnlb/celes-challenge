from fastapi import APIRouter
from firebase_admin import auth
from api.models.user import UserSchema
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from config.firebase_config import firebase


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
