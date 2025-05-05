import logging

from pandas import read_csv


catalog_url = "https://exofop.ipac.caltech.edu/tess/download_toi.php?sort=toi&output=pipe"


def read(save_path=None):
    """Download the exoplanet catalog and process it.

    Currently sourced from the Exoplanet Follow-up Observing Program (ExoFOP).
    https://exofop.ipac.caltech.edu/tess
    """

    logging.info(f"Reading catalog from {catalog_url}.")
    exo = read_csv(catalog_url, delimiter="|")

    # Filter down to confirmed planets
    exo = exo.query("`TFOPWG Disposition` == 'KP' or `TFOPWG Disposition` == 'CP'")
    
    # Rename columns and save
    exo = exo[["TIC ID", "TOI", "Sectors"]].rename(columns={"TIC ID": "TIC", "Sectors": "sectors"})
    exo = exo.set_index("TIC").sort_index()
    if save_path:
        logging.info(f"Saving catalog to {save_path}.")
        exo.to_csv(save_path)

    return exo

    
if __name__ == "__main__":
    read(save_path="catalogs/tess-exo.csv")