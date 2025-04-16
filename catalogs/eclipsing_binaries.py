from pandas import read_csv


catalog_url = "https://archive.stsci.edu/hlsps/tess-ebs/hlsp_tess-ebs_tess_lcf-ffi_s0001-s0026_tess_v1.0_cat.csv"


def read(save=False):
    """Download the EB catalog and process it.

    Currently sourced from the TESS Eclipsing Binaries Catalog produced by Prša et al. (2022).
    https://archive.stsci.edu/hlsps/tess-ebs
    """
    
    ebs = read_csv(catalog_url)

    # Remove rows with no sectors
    ebs = ebs.dropna(subset="sectors")

    # Rename columns and save
    ebs = ebs[["tess_id", "sectors"]].rename(columns={"tess_id": "TIC"})
    ebs = ebs.set_index("TIC").sort_index()
    if save:
        ebs.to_csv("tess-ebs.csv")

    return ebs