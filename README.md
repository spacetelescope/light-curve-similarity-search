# AI-Powered Light Curve Similarity Search

Zachary R. Claytor, Space Telescope Science Institute

This is a proof-of-concept (POC) for a tool that returns light curves that are similar to a user-specified light curve, where similarity is determined by artificial intelligence (AI). Think Google Lens, but for light curves. 

When browsing light curves in the MAST portal, a user might find a light curve with interesting morphology. They might want to retrieve similar light curves, but can't define or use any metadata to effectively find similar targets. Instead, they could use a similarity search, which uses data-driven similarity metrics, eliminating the need for the user to know external information about the light curve.

The similarity search will rely on a vector database that is lightweight and rapidly queryable. Each light curve will have an embedding, determined by AI and comprising a small handful of floating point values. For the POC, the embedding is a probability vector with four weights, one for each of four object classes. The similarity of two light curves is simply the euclidean distance between their two points in that vector space.

## Contents

- `catalogs`: four CSVs containing training set metadata
- `classes_0`: the output related to training and evaluating the CNN
- `mastDownload`: the test set light curves
- `wavelets`: the wavelet power spectra of the light curves (used as CNN input)
- `model.py`: the python code containing the CNN model
- [`1-read-and-transform-lightcurves.ipynb`][## Read and Transform Light Curves]
- [`2-train-and-evaluate-cnn.ipynb`][## Train and Evaluate CNN]
- [`3-check-cnn-performance.ipynb`][## Check CNN Performance]
- [`3.5-download-test-lightcurves.ipynb`][## Download Test Light Curves]
- [`4-lightcurve-similarity.ipynb`][## Light Curve Similarity]

## Read and Transform Light Curves

## Train and Evaluate CNN

## Check CNN Performance

## Download Test Light Curves

## Light Curve Similarity