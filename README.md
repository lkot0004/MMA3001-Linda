# Evaluating the Reliability of Missing Sensor Data Reconstruction in Smart Buildings
## Project Overview

This project investigates how reliable numerical methods are for reconstructing missing indoor temperature measurements in smart buildings.

Three methods are compared:
1. Forward fill: This uses the previous known temperature.
2. Linear interpolation: This estimates the temperatures using straight line interpolation between observations.
3. PCHIP: uses shape preserving piecewise cubic hermite interpolation.

The main objective is to assess the accuracy of the reconstructions, sensitivity to missing data duration, computational performance and Engineering limitations.

## Dataset
The data used for ths analysis was obtained from the Monash Smart Infrastructure Occupancy and Environmental Dataset. The temperature observations were taken from the environemntal sensor records, cleaned up and then arranged chronologically.
This investigation focuses on one sensor out of the several that were provided. Large raw datasets are not included in this repository.

## Numerical Methodology
Artificial gaps that contained 1,2,3,5 and 8 consecutinve observations were introduced into some observed temperature sequences. The three methods reconstructed the hidden measurements, which were then compared to the origional values using mean square error (MAE) and Root Mean Squared Error (RMSE).
The development experiments used a sequence that had 66 observations. Independent validation then used two additional sequences that had 65 and 55 observations.

## RESULTS
The independent valuation produced the following mean earror values:

1. Linear Interpolation -> mean mae (0.0787°C), mean rmse (0.0902°C)
2. PCHIP -> mean mae (0.0884°C), mean rmse (0.1019°C)
3. Forward fill ->  mean mae (0.1164°C), mean rmse (0.1389°C)

Linear interpolation had the lowest average errors in the independent validation, while PCHIP perfomed the best during the initial development stage but not as well in teh validation phase.
These results show us that recosntruction performance heavily depends on the properties of the temperature sequence and missing data gap.

## Installing and testing
we clone the repository:
git clone https://github.com/lkot0004/MMA3001-Linda.git
cd MMA3001-Linda

we install the dependencies:
python -m pip install -r requirements

then run the verification tests
python -m pytest tests/ -v

The automated test suite had 12 tests that cover knwon numerical solutions, input validation and reconstruction behaviour. All 12 of them passed int eh verification run recorded.

## Running the Notebook 
Open the document Missing_sensor_data in google colab. Provide access to the origional environmental sensor dataset to reproduce the processing, reconstruction experiments, sensitivity analysis and validation plots. The reusable numerical implementation is provided in src/reconstruction.py.

## Documentation 
There is HTML documentation for the reconstruction functions available in teh docs/directory. The documentation can be generated with:

pdoc ./src/reconstruction.py -o docs

## Limitataions
The analysis uses short sequences obtained from one environmental sensor. Artificial missing blocks may not be enough to capture how complex real sensor failures could be. Some of the test gaps overlap, which places a limitation on the independence of the trials that were run.

## AI Assistance
AI was used during programming, debugging and to double check interpretaion of the results. The process involved guiding the AI and any outputs it provided were checked against numerical comparisons, verification tests and examination of implementation errors. A more detailed discussion of AI use and verification is included in the project report.



