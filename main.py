from astroquery.simbad import Simbad
import numpy as np
from fastapi import FastAPI
from time import sleep

app = FastAPI()


@app.get("/")
def read_root():
    return {"status": "running"}


@app.get("/{item_key}")
def read_item(item_key: str):

    SELECTED = item_key

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

    data_raw = info_simbad.pformat()
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
