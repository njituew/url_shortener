from fastapi import FastAPI, Body, status, HTTPException, Depends
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

from src.lifespan import lifespan
from src.service import make_urls_pair, get_url_by_slug
from src.exception import (
    NoOriginalUrlFoundError,
    SlugAlreadyExistsError,
    InvalidURL_Error,
)
from src.dependencies import get_session
from db.crud import delete_all_pairs, get_all_pairs, delete_pair_by_slug

from sqlalchemy.ext.asyncio import AsyncSession

from typing import Annotated


app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/slug")
async def process_url_pair(
    original_url: Annotated[str, Body(embed=True)],
    session: Annotated[AsyncSession, Depends(get_session)],
):
    try:
        slug = await make_urls_pair(original_url, session)
    except InvalidURL_Error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid URL",
        )
    except SlugAlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Try one more time :(",
        )

    return {"slug": slug, "original_url": f"{original_url}"}


@app.get("/slugs")
async def get_all_slugs(session: Annotated[AsyncSession, Depends(get_session)]):
    pairs = await get_all_pairs(session)
    return [{"slug": p.slug, "original_url": p.original_url} for p in pairs]


@app.get("/{slug}")
async def redirect_on_original(
    slug: str, session: Annotated[AsyncSession, Depends(get_session)]
):
    try:
        original_url = await get_url_by_slug(slug, session)
    except NoOriginalUrlFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No original URL found for this short URL",
        )
    return RedirectResponse(url=original_url, status_code=status.HTTP_302_FOUND)


@app.delete("/slugs/{slug}")
async def delete_url(
    slug: str, session: Annotated[AsyncSession, Depends(get_session)]
):
    deleted = await delete_pair_by_slug(slug, session)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Slug not found",
        )
    return {"message": f"Slug '{slug}' deleted successfully."}


@app.delete("/slugs")
async def delete_all_urls(session: Annotated[AsyncSession, Depends(get_session)]):
    await delete_all_pairs(session)
    return {"message": "All URL pairs have been deleted from the database."}
