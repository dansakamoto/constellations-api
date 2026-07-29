from astroquery.simbad import Simbad

simbad = Simbad()
simbad.list_votable_fields().pprint_all()