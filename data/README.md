# Dataset Access and Preparation 

## Data source
This project uses Dataset 2, which is the Monash Smart Infrastructure occupancy and Environmental Dataset supplied for the MMA3001 project. More specifically, the environmental temperature measurements from this dataset were used for the analysis. Occupancy measurements were not needed for the reconstruction experiments.

## Required Input
The origional environmental sensor archive used in this project is: 
5EnvSensor_MayToDec2024_180kRows (1).zip

The notebook reads environmental sensor records, extracts the temperature measurements from the nested JSON files and then converts the associated timestamps into chronological measurements.
The sensor ID 6012002000869 was the focus of this analysis.

## Preparing Google Colab
1. Obtain the dataset through the official MMA3001 dataset materials.
2. Upload the environmental sensor ZIP archive to Google Drive.
3. Open Missing_Sensor_Data.ipynb in Google Colab.
4. Mount Google Drive when prompted.
5. Update the notebook's data_folder variable to the folder containing the ZIP archive.
6. Run the notebook cells in order

## Important Notes
The complete raw dataset is not redistributed via this repository.
The project creates artificial missing data blocks within observed temperature sequences and assesses reconstruction against the origional measurements.
Resampling to refular 10 minute intervales could introduce some naturally empty timeslots, these however, should not automatically be interpretaed as confimred sensor failures.

## Limitations
The notebook used currently depends on the source dataset and a configured Google Drive path. The users need to obtain the same dataset to reproduce the same results.
The reported results of this experiment were obtained using select continuous obsered segments from a single temperature sensor.
