from fastapi import FastAPI, Body, status, HTTPException
from fastapi.responses import RedirectResponse
from src.lifespan import lifespan
from src.service import process_url, get_url_by_slug
from src.exception import NoOriginalUrlFoundError
from db.crud import clear_all_pairs

app = FastAPI(lifespan=lifespan)


@app.get("/")
async def index_page():
    return {"message": "hello world"}


@app.post("/short_url")
async def generate_short_url(original_url: str = Body(embed=True)):
    slug = await process_url(original_url)
    return {"slug": slug, "original_url": f"{original_url}"}


@app.get("/{slug}")
async def redirect(slug: str):
    try:
        original_url = await get_url_by_slug(slug)
    except NoOriginalUrlFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No original URL found for this short URL",
        )
    return RedirectResponse(url=original_url, status_code=status.HTTP_302_FOUND)


@app.delete("/clear_urls")
async def clear_urls():
    await clear_all_pairs()
    return {"message": "All URL pairs have been deleted from the database."}
