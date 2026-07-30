from astroquery.simbad import Simbad
import numpy as np
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from homepage import Homepage
from lookup_codes import constellations
import rate_limiter as rl
import asyncio, redis, json, os

app = FastAPI(docs_url=None, redoc_url=None)
@app.get("/healthz")
def health_check():
    return {
            "status": "ok",
            "details": "Service is running.",
        }


app.mount("/fonts", StaticFiles(directory="fonts"), name="fonts")

r_url = os.getenv("REDIS_URL")
if r_url != None:
    r = redis.Redis.from_url(r_url)
else:
    r = redis.Redis(host="redis", decode_responses=True)

r.get("test connection")

home = Homepage(constellations)


@app.get("/", response_class=HTMLResponse)
def read_root():
    return home.build()

@app.get("/robots.txt", response_class=PlainTextResponse)
def robots():
    return """User-agent: *\nDisallow: /"""


@app.get("/{item_key}")
async def get_data(item_key: str):
    SELECTED = item_key.lower()
    if SELECTED not in constellations:
        return {"status": "error", "details": "Requested key not found."}

    c = r.get("constellation:" + SELECTED)
    if c != None:
        return json.loads(c)

    if rl.allowed("SIMBAD_calls", r) == 1:
        loop = asyncio.get_running_loop()
        res = await loop.run_in_executor(None, call_SIMBAD, item_key)
        if res["status"] == "ok":
            r.set("constellation:" + SELECTED, json.dumps(res), 1209600)
        return res

    return {
        "status": "error",
        "details": "Too many recent requests. Please wait a few seconds and then try again.",
    }


def call_SIMBAD(item_key: str):
    SELECTED = item_key

    STAR_CODE = constellations[SELECTED.lower()]
    
    try:
        simbad = Simbad(timeout=2000)

        simbad.add_votable_fields(
            "otype", "mesDistance", "plx_value", "plx_qual", "plx_err", "plx_err_prec",  "V", "G"
        )
        
        info_simbad = simbad.query_object(
            STAR_CODE, wildcard=True, criteria="otype = 'star..'", async_job=True
        )
    except:
        return {"status": "error", "details": "Error connecting to SIMBAD. Wait a moment and try again."}

    found_ids = {}
    data_formatted = {
        "status": "ok", 
        "stars": []
    }

    for row in info_simbad:
        if row["main_id"] in found_ids:
            continue

        if row["ra"] is np.ma.masked:
            continue
        if row["dec"] is np.ma.masked:
            continue
        if row["otype"] is np.ma.masked:
            continue

        found_ids[row["main_id"]] = True

        data = {
            "main_id": row["main_id"],
            "ra": row["ra"],
            "dec": row["dec"],
            "otype": row["otype"],
        }

        if row["plx_value"] is not np.ma.masked:
            data["plx_value"] = row["plx_value"]

        if row["mesdistance.dist"] is not np.ma.masked:
            data["dist"] = row["mesdistance.dist"]
            data["dist_unit"] = row["mesdistance.unit"].strip()
            data["dist_method"] = row["mesdistance.method"].strip()

        if row["V"] is not np.ma.masked:
                data["V"] = row["V"]
        
        if row["G"] is not np.ma.masked:
            data["G"] = row["G"]

        data_formatted["stars"].append(data)

    return data_formatted