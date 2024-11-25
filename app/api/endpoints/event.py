from fastapi import APIRouter

router = APIRouter(prefix="/events", tags=["События"])


@router.get("")
async def get_events():
    pass


@router.post("/create")
async def create_event():
    pass
