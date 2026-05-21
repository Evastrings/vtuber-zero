from fastapi import APIRouter, File, UploadFile, Depends, BackgroundTasks, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = "my-secret-key"
ALGORITHM = "HS256"

async def get_current_user_id(token: str = Depends(oauth2_scheme)) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        user_id: str = payload.get("sub")

        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Out of Token")
        
        return user_id

    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )

def run_comfyui_pipeline(job_id: str, background_task: BackgroundTasks):
    pass

@router.post('/process_image')
async def process_image(file: UploadFile = File(...), user_id: str = Depends(get_current_user_id)):
    print(f"The user making this request is: {user_id}")
    return {"status": "processing", "user_id": user_id}




