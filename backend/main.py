from fastapi import FastAPI, Body, status, HTTPException
from fastapi.responses import RedirectResponse

from src.lifespan import lifespan
from src.service import make_urls_pair, get_url_by_slug
from src.exception import (
    NoOriginalUrlFoundError,
    SlugAlreadyExistsError,
    InvalidURL_Error,
)

from db.crud import clear_all_pairs


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def index_page():
    return {"message": "hello world"}


@app.post("/slug")
async def process_url_pair(original_url: str = Body(embed=True)):
    try:
        slug = await make_urls_pair(original_url)
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


@app.get("/redirect/{slug}")
async def redirect_on_original(slug: str):
    try:
        original_url = await get_url_by_slug(slug)
    except NoOriginalUrlFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No original URL found for this short URL",
        )
    return RedirectResponse(url=original_url, status_code=status.HTTP_302_FOUND)


# TODO: admin handler?
@app.delete("/clear_urls")
async def clear_all_urls():
    await clear_all_pairs()
    return {"message": "All URL pairs have been deleted from the database."}
