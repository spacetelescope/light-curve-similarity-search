import logging

from astropy.io import ascii


catalog_url = "https://content.cld.iop.org/journals/1538-3881/159/2/60/revision1/ajab5d3at1_mrt.txt"
    

def read(save_path=None):
    """Download the flare catalog and process it.

    Currently sourced from Maximilian Günther et al. (2020).
    https://ui.adsabs.harvard.edu/abs/2020AJ....159...60G/abstract
    """

    logging.info(f"Reading catalog from {catalog_url}.")
    flares = ascii.read(catalog_url).to_pandas()

    # Drop duplicate sectors; we only need the sector in which a flare occurs
    flares = flares[["TESS", "sector"]].drop_duplicates()

    # Group sectors of TIC IDs together
    flares = flares.groupby("TESS")["sector"].apply(lambda x: ",".join(map(str, sorted(x)))).reset_index()

    # Rename columns and save
    flares = flares.rename(columns={"TESS": "TIC", "sector": "sectors"})
    flares = flares.set_index("TIC").sort_index()
    if save_path:
        logging.info(f"Saving catalog to {save_path}.")
        flares.to_csv(save_path)
    
    return flares

        
if __name__ == "__main__":
    read(save_path="catalogs/tess-flares.csv")