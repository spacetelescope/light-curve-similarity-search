from astropy.io import ascii


catalog_url = "https://tess.mit.edu/public/tesstransients/lc_bulk/count_transients.txt"


def read(save=False):
    """Download the supernovae catalog and process it.

    Currently sourced from the TESSTransients page at MIT.
    https://tess.mit.edu/public/tesstransients
    """

    sne = ascii.read(catalog_url).to_pandas()

    # Select only supernova light curves
    sne = sne.query("t1 == 'SN'")

    raise NotImplementedError(
        """
        Supernovae are not yet fully implemented. Since they are not associated with TIC
        objects, FFI light curves must be created from the coordinate information, unless
        there exists some external database of supernova light curves.
        """
    )