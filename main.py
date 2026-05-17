from astroquery.simbad import Simbad


def main():
    simbad = Simbad()
    simbad.add_votable_fields("otype", "alltypes", "dim")
    info_simbad = simbad.query_object("NGC4038")
    print(info_simbad["main_id"][0])


if __name__ == "__main__":
    main()
