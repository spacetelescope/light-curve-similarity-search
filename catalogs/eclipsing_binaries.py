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
    core.process(catname, load=True)