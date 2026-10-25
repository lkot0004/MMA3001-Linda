# Examiner Dataset and Run Instructions

## Project Overview

This repository contains the MMA3001 project evaluating three numerical methods for reconstructing missing smart-building temperature measurements: forward fill, linear interpolation and PCHIP.

## 1. Dataset Requirements

The project uses **Dataset 2: Monash Smart Infrastructure Occupancy and Environmental Data**, which is supplied via the MMA3001 course materials.

**Required file:** `5EnvSensor_MayToDec2024_180kRows (1).zip`

The environmental sensor archive can be obtained from the MMA3001 project dataset materials.

Only the environmental archive is required; the occupancy dataset was not used for this experiment.

The analysis only examines the first 20,000 CSV records from the environmental archive and selects temperature measurements from sensor `6012002000869` solely.

The raw dataset is not stored in this public repository because I could not find any information on the redistribution permissions for this dataset.

## 2. Running the Notebook in Google Colab

1. Open `Missing_Sensor_Data.ipynb` from this repository in Google Colab.
2. Select **Runtime → Run all**.
3. Once prompted, upload the original environmental sensor **ZIP** file.
4. The notebook will automatically load and processes the environmental data.
5. The notebook performs the reconstruction experiments, sensitivity analysis, held-out validation and computational runtime comparison.

## 3. Numerical Methods

The notebook compares:
- Forward fill
- Linear interpolation using NumPy
- PCHIP using SciPy

Reconstruction accuracy is evaluated using MAE and RMSE for artificially hidden temperature measurements.

## 4. Reusable Code and Verification

Reusable numerical functions are stored in `src/reconstruction.py`.

Automated tests are provided in `tests/test_reconstruction.py`.

To run the tests locally, install the dependencies and execute:

`pip install -r requirements.txt`

`python -m pytest -q`

The recorded verification run completed with 12 passing tests.

## 5. Reproducibility Notes

- The environmental ZIP must be supplied by the examiner.
- The original dataset is not modified during the analysis.
- Numerical experiments use artificially hidden observations with known reference temperatures.
- Runtime measurements may vary depending on the execution environment.
- The investigation is limited to one sensor and the first 20,000 CSV records, rather than the complete environmental archive.

## 6. Repository Contents

- `Missing_Sensor_Data.ipynb` — Main analysis notebook
- `src/reconstruction.py` — Reusable numerical methods
- `tests/test_reconstruction.py` — Automated verification tests
- `docs/reconstruction.html` — Generated source-code documentation
- `results/` — Recorded test results
- `requirements.txt` — Software dependencies
- `README.md` — Project overview and instructions
