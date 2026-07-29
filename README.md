# Constellations API

## Run command

development:

```
docker compose up
```

production:

```
uv run fastapi run
```

## Fields returned

- main_id: Main identifier
- ra: Right ascension
- dec: Declination
- otype: Object type
- plx_value: Parallax
- dist: Measured distance
- dist_unit: Distance measurement unit
- dist_method: Distance measurement method
- V: Apparent visual magnitude in Johnson's 11-color system
- G: G-Band Magnitude from Gaia space observatory
