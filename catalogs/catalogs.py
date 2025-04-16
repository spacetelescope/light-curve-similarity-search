import pandas as pd
from astropy.io import ascii
from astroquery.mast import Catalogs


def eclipsing_binaries(save=False):
    """Download the EB catalog and process it.

    Currently sourced from the TESS Eclipsing Binaries Catalog produced by Prša et al. (2022).
    https://archive.stsci.edu/hlsps/tess-ebs
    """
    
    catalog_url = "https://archive.stsci.edu/hlsps/tess-ebs/hlsp_tess-ebs_tess_lcf-ffi_s0001-s0026_tess_v1.0_cat.csv"
    ebs = pd.read_csv(catalog_url)

    # Remove rows with no sectors
    ebs = ebs.dropna(subset="sectors")

    # Rename columns and save
    ebs = ebs[["tess_id", "sectors"]].rename(columns={"tess_id": "TIC"})
    ebs = ebs.set_index("TIC").sort_index()
    if save:
        ebs.to_csv("tess-ebs.csv")

    return ebs


def exoplanet_transits(save=False):
    """Download the exoplanet catalog and process it.

    Currently sourced from the Exoplanet Follow-up Observing Program (ExoFOP).
    https://exofop.ipac.caltech.edu/tess
    """

    catalog_url = "https://exofop.ipac.caltech.edu/tess/download_toi.php?sort=toi&output=pipe"
    exo = pd.read_csv(catalog_url, delimiter="|")

    # Filter down to confirmed planets
    exo = exo.query("`TFOPWG Disposition` == 'KP' or `TFOPWG Disposition` == 'CP'")
    
    # Rename columns and save
    exo = exo[["TIC ID", "TOI", "Sectors"]].rename(columns={"TIC ID": "TIC", "Sectors": "sectors"})
    exo = exo.set_index("TIC").sort_index()
    if save:
        exo.to_csv("tess-exo.csv")

    return exo


def flaring_stars(save=False):
    """Download the flare catalog and process it.

    Currently sourced from Maximilian Günther et al. (2020).
    https://ui.adsabs.harvard.edu/abs/2020AJ....159...60G/abstract
    """

    catalog_url = "https://content.cld.iop.org/journals/1538-3881/159/2/60/revision1/ajab5d3at1_mrt.txt"
    flares = ascii.read(catalog_url).to_pandas()

    # Drop duplicate sectors; we only need the sector in which a flare occurs
    flares = flares[["TESS", "sector"]].drop_duplicates()

    # Group sectors of TIC IDs together
    flares = flares.groupby("TESS")["sector"].apply(lambda x: ",".join(map(str, sorted(x)))).reset_index()

    # Rename columns and save
    flares = flares.rename(columns={"TESS": "TIC", "sector": "sectors"})
    flares = flares.set_index("TIC").sort_index()
    if save:
        flares.to_csv("tess-flares.csv")
    
    return flares


def rotating_stars(save=False):
    """Download the stellar rotation catalog and process it.

    Currently sourced from Marina Kounkel et al. (2022).
    https://ui.adsabs.harvard.edu/abs/2022AJ....164..137K/abstract
    """
    
    catalog_url = "https://content.cld.iop.org/journals/1538-3881/164/4/137/revision1/ajac866dt1_mrt.txt"
    rot = ascii.read(catalog_url).to_pandas()

    # Drop rows with NaN period
    rot = rot.dropna(subset="Period")
    
    # Group sectors of TIC IDs together
    rot = rot.groupby("TIC")["Sec"].apply(lambda x: ",".join(map(str, sorted(x)))).reset_index()

    # Rename columns and save
    rot = rot[["TIC", "Sec"]].rename(columns={"Sec": "sectors"})
    rot = rot.set_index("TIC").sort_index()
    if save:
        rot.to_csv("tess-rot.csv")
    
    return rot


def seismic_stars(save=False):
    """Download the asteroseismology catalog and process it.

    Currently sourced from Marc Hon et al. (2021).
    https://ui.adsabs.harvard.edu/abs/2021ApJ...919..131H/abstract
    """
    
    catalog_url = "https://content.cld.iop.org/journals/0004-637X/919/2/131/revision1/apjac14b1t1_mrt.txt"
    seis = ascii.read(catalog_url).to_pandas()

    raise NotImplementedError(
        """
        Seismic stars are not yet fully implemented. You can get the list of TIC IDs,
        but the sectors in which those targets were observed is harder to get. Astroquery times out,
        so consider using a smaller subsample.
        """
    )
    return seis


def supernovae(save=False):
    """Download the supernovae catalog and process it.

    Currently sourced from the TESSTransients page at MIT.
    https://tess.mit.edu/public/tesstransients
    """

    catalog_url = "https://tess.mit.edu/public/tesstransients/lc_bulk/count_transients.txt"
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


def dipper_stars(save=False):
    """Download the dipper stars catalog and process it.

    Currently sourced from Ben Capistrant et al. (2022).
    https://ui.adsabs.harvard.edu/abs/2022ApJS..263...14C/abstract
    """

    # catalog_url = "https://content.cld.iop.org/journals/0067-0049/263/1/14/revision2/apjsac9125t1_mrt.txt"
    catalog_url = "apjsac9125t1_mrt.txt" # MRT has a bad character, so source from the local version for now.
    dip = ascii.read(catalog_url).to_pandas()

    # Rename columns and save
    dip = dip[["TIC", "Sector"]].rename(columns={"Sector": "sectors"})
    dip = dip.set_index("TIC").sort_index()
    if save:
        dip.to_csv("tess-dip.csv")
    return dip


if __name__ == "__main__":
    from sys import argv
    try:
        save = argv[1].lower() == "save"
    except IndexError as e:
        save = False

    eclipsing_binaries(save=save)
    exoplanet_transits(save=save)
    flaring_stars(save=save)
    rotating_stars(save=save)
    dipper_stars(save=save)