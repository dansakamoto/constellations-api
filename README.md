# Parallax

## Run command

development:

```
uv run fastapi dev
```

production:

```
uv run fastapi run
```

## To Do

- Add html default output with links to currently supported constellations
- Connect to Redis
- Add rate limiter - max 4 concurrent SIMBAD calls
- Cache SIMBAD responses for 2 weeks
