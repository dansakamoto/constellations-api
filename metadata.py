from astroquery.simbad import Simbad


def main():
    simbad = Simbad()
    simbad.list_votable_fields().pprint_all()


if __name__ == "__main__":
    main()
