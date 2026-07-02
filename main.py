from astroquery.simbad import Simbad
import numpy as np
import json, sys


def main():

    SELECTED = input("Enter key to lookup: ")
    FORMAT = "json"

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
        print("Requested key not found.")
        sys.exit(1)

    STAR_CODE = constellations[SELECTED.lower()]

    simbad = Simbad()

    simbad.add_votable_fields(
        "otype", "mesDistance", "plx_value", "plx_qual", "plx_err", "plx_err_prec"
    )

    info_simbad = simbad.query_object(
        "* Lib", wildcard=True, criteria="otype = 'star..'"
    )

    data_raw = info_simbad.pformat()
    data_formatted = {}

    for row in info_simbad:
        if row["main_id"] in data_formatted:
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

    fName = f"data/results.json"
    with open(fName, "w") as f:
        print("\nWriting results to file " + fName)
        f.write(json.dumps(data_formatted, indent=2, ensure_ascii=False))
        f.close()


#    np.savetxt("data/results.csv", info_simbad.pformat(), delimiter=",", fmt="%s")


if __name__ == "__main__":
    main()
