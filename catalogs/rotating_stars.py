import logging

from astropy.io import ascii


catalog_url = "https://content.cld.iop.org/journals/1538-3881/164/4/137/revision1/ajac866dt1_mrt.txt"


def read(save_path=None):
    """Download the stellar rotation catalog and process it.

    Currently sourced from Marina Kounkel et al. (2022).
    https://ui.adsabs.harvard.edu/abs/2022AJ....164..137K/abstract
    """
    
    logging.info(f"Reading catalog from {catalog_url}.")
    rot = ascii.read(catalog_url).to_pandas()

    # Drop rows with NaN period
    rot = rot.dropna(subset="Period")
    
    # Group sectors of TIC IDs together
    rot = rot.groupby("TIC")["Sec"].apply(lambda x: ",".join(map(str, sorted(x)))).reset_index()

    # Rename columns and save
    rot = rot[["TIC", "Sec"]].rename(columns={"Sec": "sectors"})
    rot = rot.set_index("TIC").sort_index()
    if save_path:
        logging.info(f"Saving catalog to {save_path}.")
        rot.to_csv(save_path)
    
    return rot


if __name__ == "__main__":
    read(save_path="catalogs/tess-rot.csv")