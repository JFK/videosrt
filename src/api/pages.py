from fastapi import APIRouter, Depends, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_session
from src.models import Job
from src.templating import templates

router = APIRouter()


@router.get("/")
async def upload_page(request: Request):
    return templates.TemplateResponse(request, "upload.html", {"active_page": "upload"})


@router.get("/history")
async def history_page(request: Request, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Job).order_by(Job.created_at.desc()).limit(100))
    jobs = result.scalars().all()
    return templates.TemplateResponse(request, "history.html", {"active_page": "history", "jobs": jobs})


@router.get("/meta/{job_id}")
async def meta_editor_page(job_id: str, request: Request, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Job).where(Job.id == job_id))
    job = result.scalar_one_or_none()
    if not job:
        from fastapi.responses import RedirectResponse
        return RedirectResponse("/history")
    return templates.TemplateResponse(request, "meta_editor.html", {"active_page": "history", "job": job})


@router.get("/costs")
async def costs_page(request: Request):
    return templates.TemplateResponse(request, "costs.html", {"active_page": "costs"})


@router.get("/settings")
async def settings_page(request: Request):
    return templates.TemplateResponse(request, "settings.html", {"active_page": "settings"})
