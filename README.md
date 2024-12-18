# AI-Powered Light Curve Similarity Search

Zachary R. Claytor, Space Telescope Science Institute

This is a proof-of-concept (POC) for a tool that returns light curves that are similar to a user-specified light curve, where similarity is determined by artificial intelligence (AI). Think Google Lens, but for light curves. 

When browsing light curves in the MAST portal, a user might find a light curve with interesting morphology. They might want to retrieve similar light curves, but can't define or use any metadata to effectively find similar targets. Instead, they could use a similarity search, which uses data-driven similarity metrics, eliminating the need for the user to know external information about the light curve.

The similarity search will rely on a vector database that is lightweight and rapidly queryable. Each light curve will have an embedding vector, determined by AI and composed of floating point values. For the POC, the embedding is a probability vector with 64 weights, extracted from the last hidden layer of a convolutional neural network classifier. The similarity of two light curves is simply the euclidean distance between their two points in that vector space.

## Contents

- `catalogs`: four CSVs containing training set metadata
- `runs`: the output folders related to training and evaluating the CNN. Listed in chronological order:
   - classes_0: the first successful test run
   - batchnorm1_0: added batch normalization and changed embeddings to be the output of last hidden layer.
- `mastDownload`: the test set light curves
- `wavelets`: the wavelet power spectra of the light curves (used as CNN input)
- `model.py`: the python code containing the CNN model
- [`1-read-and-transform-lightcurves.ipynb`](#transform)
- [`2-train-and-evaluate-cnn.ipynb`](#train)
- [`3-check-cnn-performance.ipynb`](#performance)
- [`3.5-download-test-lightcurves.ipynb`](#download)
- [`4-lightcurve-similarity.ipynb`](#similarity)

## Read and Transform Light Curves <a name="transform"></a>

## Train and Evaluate CNN <a name="train"></a>

## Check CNN Performance <a name="performance"></a>

## Download Test Light Curves <a name="download"></a>

## Light Curve Similarity <a name="similarity"></a>