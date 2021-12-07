from ftplib import FTP
from pathlib import Path
import os.path
import re
import json
 

def get_ftp_file(remotefile):
    basename = os.path.basename(remotefile)
    dirpath = os.path.dirname(remotefile)
    my_check = Path(basename)
    if my_check.is_file():
        return
    ftp = FTP('ftp.ncdc.noaa.gov')
    ftp.login()
    print(ftp.getwelcome())
    ftp.cwd(dirpath)
    ftp.retrlines('LIST')
    with open(basename, 'wb') as fp:
        ftp.retrbinary('RETR ' + basename, fp.write)
    ftp.quit()
 
# NOTE: data details can be found in /pub/data/normals/1981-2010/readme.txt


# Map name of month to the rain_month value
def find_month_name(num):
    month_dict = {'1': 'JANUARY', '2': 'FEBRUARY', '3': 'MARCH', '4': 'APRIL', '5': 'MAY', '6': 'JUNE',
                  '7': 'JULY', '8': 'AUGUST', '9': 'SEPTEMBER', '10': 'OCTOBER', '11': 'NOVEMBER', '12': 'DECEMBER'}
    return month_dict[str(num)]


# Function to retrieve the Station ID,Year, Month and highest rainfall value from given data set
def find_greatest_rain_fall():
    # When parsing the data. Ignore any negative number.
    # Filter out extra char( example 3132F should be 3132 )
    # Convert data to inch. 3132 = 31.32 inches
    rain_data_file = open('mly-prcp-filled.txt', 'r')
    rain_list = []  # List with [station ID, year, Month and highest rainfall] data for each row of file
    max_rain = 0
    rain_data = {}  # Dictionary with data of highest rainfall location
    rain_month = 0  # Month with highest rainfall in each row of file
    rain_value_inches = 0

    # Iterate through the file to generate a list with data of the highest rainfall in each row of the file.
    # Search for valid data ending with invalid characters and correct them.
    for line in rain_data_file:
        temp_list = line.split()           # Store data in every row as a list
        rain_value = -1
        pattern1 = r'^\d{1,5}[a-zA-Z]$'    # Regex to search values ending with alphabets
        pattern2 = r'^\W\d{1,5}[A-Za-z]$'  # Regex to search invalid values such as "-9999F"

        # Iterate through the rainfall data columns of all months
        for i in range(2, len(temp_list)):
            # If valid pattern was found, remove extra characters(if any) and update the list entry
            # If invalid pattern was found, store "-1" in place of it
            if re.match(pattern1, temp_list[i]):
                temp_list[i] = re.sub('[A-Za-z]', '', temp_list[i])
            elif re.match(pattern2, temp_list[i]):
                temp_list[i] = "-1"

            # Check for the highest rainfall and store corresponding month for every row .
            if int(temp_list[i]) >= rain_value:
                rain_value = int(temp_list[i])
                rain_value_inches = rain_value / 100  # Convert the rainfall data to inches
                rain_month = i-1

        # Check if the rainfall value is valid and append to rain_list
        # The list has Station ID, Year, Month of highest rainfall and Rainfall in inches
        if rain_value != -1:
            rain_list_row = [temp_list[0], temp_list[1], rain_month, rain_value_inches]
            rain_list.append(rain_list_row)

    # Iterate through rain_list to find the highest rainfall in the entire data set
    max_index = 0
    for i in range(0, len(rain_list)):
        if rain_list[i][3] >= max_rain:
            max_index = i  # Store the list index with highest data
            max_rain = rain_list[i][3]

    # Retrieve the name of the month with highest rainfall
    max_rain_month = find_month_name(rain_list[max_index][2])

    # Update the rain_data dictionary with Station ID, Rainfall, Year and Month
    rain_data['Station ID'] = rain_list[max_index][0]
    rain_data['Rain Fall'] = max_rain
    rain_data['Year'] = int(rain_list[max_index][1])
    rain_data['Month'] = max_rain_month
    return rain_data


# Function to retrieve location of the station with highest rainfall from ID
def find_weather_station(station_id):
    loc_file = open('ghcnd-stations.txt', 'r')
    loc_list = []  # List to store the location data
    for line in loc_file:
        if station_id in line:
            loc_list = line.split()
    location = " ".join(loc_list[4::])  # Parse the location data for state and city name only
    return location


# Print the rain data in Json format
def print_json(data):
    json_data = json.dumps(data, indent=4)
    print(json_data)
    return
 

def main():
    get_ftp_file("/pub/data/normals/1981-2010/source-datasets/mly-prcp-filled.txt")
    get_ftp_file("/pub/data/normals/1981-2010/source-datasets/ghcnd-stations.txt")

    # Parse the data file mly-prcp-filled.txt to find the month, year, weather station of the greatest rain fall.
    big_rain = find_greatest_rain_fall()

    # Retrieve the location of station with highest rainfall recorded
    station_loc = find_weather_station(big_rain['Station ID'])
    big_rain['Location'] = station_loc  # Update the Dictionary with station location

    # print data in json format
    print_json(big_rain)


if __name__ == '__main__':
    main()
