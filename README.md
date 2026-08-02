# Constellations API

An endpoint for getting JSON-formatted lists of stars by constellation region from the [SIMBAD Astronomical Database](https://simbad.cds.unistra.fr/simbad/). Created to support artistic projects, this tool retrieves position and brightness data but may not include all of the error/precision details necessary for scientific research.

## Fields returned

- main_id: Main identifier
- ra: [Right Ascension](https://en.wikipedia.org/wiki/Right_ascension) (ICRS coord, ep=J2000)
- dec: [Declination](https://en.wikipedia.org/wiki/Declination) (ICRS coord, ep=J2000)
- otype: [Object type](https://simbad.cds.unistra.fr/guide/otypes.htx)
- plx_value: [Parallax](https://en.wikipedia.org/wiki/Stellar_parallax) in milliarcseconds
- dist: [Measured distance](https://simbad.cds.unistra.fr/simbad/sim-display?data=meas#distance) (Note: this is a single-item query for now, and it's unclear whether this results in the most accurate available data. This might be good enough for artistic applications, but it also might be worth doing a deeper dive into available options.)
- dist_unit: Distance measurement unit
- dist_method: Distance measurement method
- V: Apparent visual magnitude in [Johnson's 11-color system](https://en.wikipedia.org/wiki/UBV_photometric_system_)
- G: G-Band Magnitude from Gaia space observatory (note: not a clean substitute for a V value, but included as a backup in case an entry lacks a V value.)

## Run command

run in a development environment with a test redis instance:

```
docker compose up
```

run in production mode:

```
uv run fastapi run
```

## To Do

- Research the range of options returned in SIMBAD's mesDistance field, and figure out if there's a way to ensure we're getting the most accurate measurement available.
- Is it useful to add precision/error data for parallax values?
- Is there a way to meaningfully filter results down to just the most recognizeable parts of a constellation?
- Add a way to filter to just the brightest objects (and would this help with the previous item, or is it a separate concern?)
