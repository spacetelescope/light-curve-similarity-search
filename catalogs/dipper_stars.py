from astropy.io import ascii


catalog_url = "https://content.cld.iop.org/journals/0067-0049/263/1/14/revision3/apjsac9125t1_mrt.txt"
    

def read(save=False):
    """Download the dipper stars catalog and process it.

    Currently sourced from Ben Capistrant et al. (2022).
    https://ui.adsabs.harvard.edu/abs/2022ApJS..263...14C/abstract
    """

    dip = ascii.read(catalog_url).to_pandas()

    # Rename columns and save
    dip = dip[["TIC", "Sector"]].rename(columns={"Sector": "sectors"})
    dip = dip.set_index("TIC").sort_index()
    if save:
        dip.to_csv("tess-dip.csv")
    return dip