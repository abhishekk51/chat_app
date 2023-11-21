from fastapi import APIRouter

from server.views.chat import conversation_router


router = APIRouter()
router.include_router(conversation_router)