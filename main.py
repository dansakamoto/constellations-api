from astroquery.simbad import Simbad
import numpy as np
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import asyncio

app = FastAPI()

app.mount("/style", StaticFiles(directory="static"), name="static")

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


@app.get("/", response_class=HTMLResponse)
def read_root():
    links = ""
    for c in constellations:
        links += '<li><a href="' + c + '">' + c + "</a></li>"

    return (
        """
    <html>
        <head>
            <title>Constellations</title>
            <link rel="preconnect" href="https://fonts.googleapis.com">
            <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
            <link href="https://fonts.googleapis.com/css2?family=Inter:ital,opsz,wght@0,14..32,100..900;1,14..32,100..900&display=swap" rel="stylesheet">
            <link rel="stylesheet" type="text/css" href="style/main.css">
        </head>
        <body>
            <div class="header">
            <h1>Constellations API</h1>
            <p>Returns a JSON-formatted list of position data for all stars within a constellation - from <a href="https://simbad.cds.unistra.fr/simbad/">SIMBAD</a>
            </div>
            <div class="content">
            <p>supported keys:</p>
            <ul>
                """
        + links
        + """
            </u>
            </div>
        </body>
    </html>
    """
    )


@app.get("/{item_key}")
async def get_data(item_key: str):
    loop = asyncio.get_running_loop()
    res = await loop.run_in_executor(None, call_SIMBAD, item_key)
    return res


def call_SIMBAD(item_key: str):
    SELECTED = item_key

    if SELECTED.lower() not in constellations:
        return {"status": "error", "details": "Requested key not found."}

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
