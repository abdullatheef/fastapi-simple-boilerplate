from fastapi import APIRouter

from .auth_sample import router as sample_auth_router
from .sample_posts import router as sample_posts_router

router = APIRouter(prefix="/v1")


router.include_router(sample_auth_router)
router.include_router(sample_posts_router)

