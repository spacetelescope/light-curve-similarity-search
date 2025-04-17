import os
import logging

from astroquery.mast import Observations
from pandas import read_csv
import numpy as np
from scipy import signal # scipy<1.15
import torch
import s3fs
import lightkurve # lightkurve>=2.5


Observations.enable_cloud_dataset() # use cloud data when possible
fs = s3fs.S3FileSystem(anon=True)   # read cloud data as though local


def read_catalog(filepath):
    logging.info(f"Reading catalog from {filepath}.")
    cat = read_csv(
        filepath,
        index_col="TIC", 
        converters={"sectors": lambda x: x.replace("'","").split(",")},
    )
    return cat


def query_observations(
    catalog,
    uris_path=None,
    obs_collection="TESS",
    dataproduct_type="timeseries",
    **kw
):
    """Query MAST light curves for a specified catalog.
    """
    ids = catalog.index.astype(str)
    logging.info("Querying observations.")
    obs = Observations.query_criteria(
        target_name=ids, 
        obs_collection=obs_collection, 
        dataproduct_type=dataproduct_type, 
        **kw)

    logging.info("Filtering observations.")
    filtered_obs = obs[[str(row["sequence_number"]) in catalog.loc[int(row["target_name"]), "sectors"] for row in obs]]

    # Get associated science products for each Observation
    logging.info("Getting list of data products.")
    data_products = Observations.get_product_list(filtered_obs) 

    # Keep only the science products
    logging.info("Filtering the list of data products.")
    lc_prod = Observations.filter_products(data_products, extension="s_lc.fits", productType="SCIENCE")

    # Query the light curve URIs, optionally save
    logging.info("Getting product URIs.")
    lc_uri = Observations.get_cloud_uris(lc_prod)
    if uris_path:
        logging.info(f"Saving list of URIs to {uris_path}.")
        np.savetxt(uris_path, lc_uri, fmt="%s")

    return lc_uri


def read_lightcurve(uri, flux_column="sap_flux", **kw):
    """Read a light curve given a URI, and remove NaN values.

    Parameters:
        uri (str): the cloud URI of the light curve file.
        flux_column (str, "sap_flux"): the flux column to select
        **kw: keyword arguments to be passed to `lightkurve.read`

    Returns:
        lc (lightkurve.LightCurve): the light curve.
    """
    logging.info(f"Reading light curve from {uri}.")
    with fs.open(uri, "rb") as f:
        lc = lightkurve.read(uri, flux_column=flux_column, **kw).remove_nans()

    return lc
        

def wavelet_power(
    lc,
    wavelet=signal.morlet2,
    w=6,
    period=None,
    minimum_period=None,
    maximum_period=None,
    period_samples=512,
    output_size=None,
):
    """Compute the wavelet power spectrum of a light curve.

    By default, this computes the Morlet wavelet transform as implemented in scipy.
    Optionally bin the power array to a user-specified shape.
    """
    logging.info("Computing wavelet power spectrum.")
    time = lc.time.value
    flux = lc.flux.value

    # Mean-normalize the flux
    flux -= flux.mean()

    # Compute the nyquist frequency
    nyquist = 0.5 / np.median(np.diff(time))

    # If `period` is not specified, infer the periods at which to evaluate the power
    if period is None:
        if minimum_period is None:
            minimum_period = 1/nyquist
        if maximum_period is None:
            maximum_period = time[-1] - time[0]
        period = np.geomspace(minimum_period, maximum_period, period_samples)

    # Calculate the wavelet widths
    widths = w * nyquist * period / np.pi

    # Calculate the continuous wavelet transform
    cwtm = signal.cwt(flux, wavelet, widths, w=w)

    # Compute the wavelet power and scale by the widths (as per Liu et al. 2007).
    power = np.abs(cwtm)**2 / widths[:, np.newaxis]

    # If `output_size` is specified, scale down the power array
    if output_size:
        # If `output_size` is an integer, convert it to a tuple
        if isinstance(output_size, int):
            output_size = (output_size, output_size)

        power = torch.tensor(np.expand_dims(power, 0))
        power = torch.nn.functional.adaptive_avg_pool2d(power, output_size=output_size)
        power = np.squeeze(power.numpy())

    return power


def lc_to_wps(uri, lc_kw=None, wp_kw=None, save_path=None):
    """Given a URI, read the light curve and compute the wavelet power.

    Wraps `read_lightcurve` and `wavelet_power`.

    Accepts dictionaries `lc_kw` and `wp_kw` for kwargs to the two functions.
    """

    # Initialize empty dicts if no kwargs are provided
    if not lc_kw:
        lc_kw = {}
    if not wp_kw:
        wp_kw = {}

    # Read light curve and compute wavelet power spectrum
    lc = read_lightcurve(uri, **lc_kw)
    power = wavelet_power(lc, **wp_kw)

    # Rescale power spectrum
    power -= power.min()
    power *= 255/power.max()
    power = power.astype(np.uint8)

    # Optionally save wavelet power spectrum
    if save_path:
        np.save(save_path, power)

    return power