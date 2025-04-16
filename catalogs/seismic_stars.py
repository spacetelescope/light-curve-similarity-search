from astropy.io import ascii


catalog_url = "https://content.cld.iop.org/journals/0004-637X/919/2/131/revision1/apjac14b1t1_mrt.txt"


def read(save=False):
    """Download the asteroseismology catalog and process it.

    Currently sourced from Marc Hon et al. (2021).
    https://ui.adsabs.harvard.edu/abs/2021ApJ...919..131H/abstract
    """
    
    seis = ascii.read(catalog_url).to_pandas()

    raise NotImplementedError(
        """
        Seismic stars are not yet fully implemented. You can get the list of TIC IDs,
        but the sectors in which those targets were observed is harder to get. Astroquery times out,
        so consider using a smaller subsample.
        """
    )
    return seis