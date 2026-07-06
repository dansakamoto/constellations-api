from astroquery.simbad import Simbad
import numpy as np
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from homepage import Homepage
from dotenv import load_dotenv
import ratelimiter as rl
import asyncio, redis, json, os

load_dotenv()

app = FastAPI()
app.mount("/style", StaticFiles(directory="static"), name="static")

if os.getenv("REDIS_MODE") == "DEV":
    r = redis.Redis(host="localhost", decode_responses=True)
else:
    r = redis.Redis.from_url(os.getenv("REDIS_URL"))
r.get("test connection")

constellations = {
    "orion": "* Ori",
    "ursamajor": "* UMa",
    "ursaminor": "* UMi",
    "aries": "* Ari",
    "taurus": "* Tau",
    "gemini": "* Gem",
    "cancer": "* Cnc",
    "leo": "* Leo",
    "virgo": "* Vir",
    "libra": "* Lib",
    "scorpio": "* Sco",
    "sagittarius": "* Sgr",
    "capricorn": "* Cap",
    "aquarius": "* Aqr",
    "pisces": "* Psc",
}

home = Homepage(constellations)


@app.get("/", response_class=HTMLResponse)
def read_root():
    return home.build()


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
        r.set("constellation:" + SELECTED, json.dumps(res), 1209600)
        return res

    return {
        "status": "error",
        "details": "Too many recent requests. Please wait a few seconds and then try again.",
    }


def call_SIMBAD(item_key: str):
    SELECTED = item_key

    STAR_CODE = constellations[SELECTED.lower()]

    simbad = Simbad(timeout=2000)

    simbad.add_votable_fields(
        "otype", "mesDistance", "plx_value", "plx_qual", "plx_err", "plx_err_prec"
    )

    info_simbad = simbad.query_object(
        STAR_CODE, wildcard=True, criteria="otype = 'star..'", async_job=True
    )

    data_formatted = {}

    for row in info_simbad:
        if row["main_id"] in data_formatted:
            continue

        if row["ra"] is np.ma.masked:
            continue
        if row["dec"] is np.ma.masked:
            continue
        if row["otype"] is np.ma.masked:
            continue

        data = {
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

        data_formatted[row["main_id"]] = data

    return data_formatted


def all_votable_fields():
    simbad = Simbad()
    simbad.list_votable_fields().pprint_all()
