import os
import logging

from pandas import read_csv
import dask
import numpy as np

import core

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


def process_one(uri, catname):
    """Process a single light curve.
    """
    logging.warning(f"Processing {uri}.")
    outname = os.path.basename(uri).replace("lc.fits", "wt")

    core.lc_to_wps(uri,
        lc_kw=dict(flux_column="sap_flux", quality_bitmask="hard"),
        wp_kw=dict(minimum_period=0.01, maximum_period=12, output_size=64),
        save_path=f"wavelets/{catname}/{outname}.npy",
    )


def process(catname, load=False):
    """Process the light curves from the catalog.
    """

    if load:
        uris = np.loadtxt(f"catalogs/{catname}-uris.txt", dtype=str)
    else:
        # Read the catalog
        cat = core.read_catalog(f"catalogs/{catname}.csv")

        # Get light curve URIs
        uris = core.query_observations(cat, uris_path=f"catalogs/{catname}-uris.txt")

    # Process light curves into wavelet power spectra and save
    lazy_results = []
    for uri in uris:
        lazy_result = dask.delayed(process_one)(uri, catname)
        lazy_results.append(lazy_result)
    
    dask.compute(*lazy_results)


if __name__ == "__main__":
    import argparse

    # Create an argument parser
    parser = argparse.ArgumentParser(description='Set logging level from command line')

    # Add an argument for log level
    parser.add_argument(
        '--log',
        dest='log_level',
        default='WARNING',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        type=str.upper,
        help='Set the logging level'
    )

    # Parse the arguments
    args = parser.parse_args()

    # Get the log level from arguments
    log_level = args.log_level

    # Set up logger
    numeric_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % log_level)
    logging.basicConfig(level=numeric_level, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

    catname = "tess-ebs"
    #read(save_path=f"catalogs/{catname}.csv")
    process(catname, load=True)