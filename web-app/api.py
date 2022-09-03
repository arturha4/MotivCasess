from fastapi import FastAPI

from server.db import get_web_site_by_hash
app = FastAPI()


@app.get("/web_sites/{site_hash}")
async def root(site_hash):
    dict = get_web_site_by_hash(int(site_hash,16))
    return dict
