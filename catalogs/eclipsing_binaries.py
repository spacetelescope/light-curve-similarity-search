import logging

from pandas import read_csv


catalog_url = "https://archive.stsci.edu/hlsps/tess-ebs/hlsp_tess-ebs_tess_lcf-ffi_s0001-s0026_tess_v1.0_cat.csv"


def read(save_path=None):
    """Download the EB catalog and process it.

    Currently sourced from the TESS Eclipsing Binaries Catalog produced by Prša et al. (2022).
    https://archive.stsci.edu/hlsps/tess-ebs
    """
    
    logging.info(f"Reading catalog from {catalog_url}.")
    ebs = read_csv(catalog_url)

    # Remove rows with no sectors
    ebs = ebs.dropna(subset="sectors")

    # Rename columns and save
    ebs = ebs[["tess_id", "sectors"]].rename(columns={"tess_id": "TIC"})
    ebs = ebs.set_index("TIC").sort_index()
    if save_path:
        logging.info(f"Saving catalog to {save_path}.")
        ebs.to_csv(save_path)

    return ebs


if __name__ == "__main__":
    read(save_path="catalogs/tess-ebs.csv")