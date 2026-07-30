from astroquery.simbad import Simbad

simbad = Simbad()

simbad.add_votable_fields(
    "coordinates"
)

info_simbad = simbad.query_object("beta librae")

print(info_simbad[0])