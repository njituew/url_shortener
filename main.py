from fastapi import FastAPI, Body
from src.lifespan import lifespan
from src.service import process_url

app = FastAPI(lifespan=lifespan)


@app.post("/short_url")
async def generate_short_url(original_url: str = Body(embed=True)):
    slug = await process_url(original_url)
    return {"slug": slug, "original_url": f"{original_url}"}


@app.get("/{slug}")
async def redirect(slug: str):
    return ...  # redirect
