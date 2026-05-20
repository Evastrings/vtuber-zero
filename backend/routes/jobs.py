from fastapi import APIRouter

router = APIRouter()

@router.get('/jobs/{job_id}')
async def jobs(job_id: str):
    pass