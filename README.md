* This is a Python application to find the location which received highest rainfall over a month.
* The dataset is obtained from "ncdc.noaa.gov" for the year 1981-2010.

rain_month.py
* The rainfall and locaion data files are retrieved from the website.
* The mly-prcp-filled.txt file is parsed for Station  ID, Year, Month of highest Rainfall data.
* The ghcnd-stations.txt file is parsed for location of the Station with highest rainfall.
* The data is printed in Json Format.

{
    "Station ID": "USC00511880",
    "Rain Fall": 23.89,
    "Year": 1996,
    "Month": "DECEMBER",
    "Location": "HI HONOKOHAU HARBOR 68.14"
}

Dockerfile
* Dockerfile is to contanerize the application and execute it.
* Includes Python version  and application file to be executed.

The application can be forked from following Github link: https://github.com/samyuktas/Samyukta_Rain_Data_App.git

Commands to execute:
docker build https://github.com/samyuktas/Samyukta_Rain_Data_App.git#container:docker
docker run "image_name"
