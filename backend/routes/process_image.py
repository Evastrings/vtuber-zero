from fastapi import APIRouter

router = APIRouter()

@router.post('/process_image')
def process_image():
    pass