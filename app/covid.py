# this is the main python file that will conduct all of my CSV operations

# import statements
import os
from datetime import date
import csv
import urllib.request
from dotenv import load_dotenv
from app import APP_ENV
from app.email_service import send_email

load_dotenv()

STATE = os.getenv("STATE", default="California")
COUNTY = os.getenv("COUNTRY_CODE", default="Orange")
MY_NAME = os.getenv("MY_NAME", default="Hottest Person in the World")

def get_data()
    """
    WHAT IT DOES: 

    PARAMETERS: 

    RETURNS: 
    """
    # this is the url that contains all of the county information
    url = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv"

    # use the urllib.request (more information here: https://docs.python.org/3/howto/urllib2.html)
    response = urllib.request.urlopen(url)
    data = response.read()

    # using the nytdata in data folder to store information
    file_name = os.path.join(os.path.dirname(__file__),"..", "data", "nytdata.csv")

    # write the data to a file
    with open(file_name, 'wb') as f:
        f.write(data)

    return file_name

def data_validation()
    """
    WHAT IT DOES: 

    PARAMETERS: 

    RETURNS: 
    """
    #TODO: add in data validation

def average_deaths(deaths_array)
    """
    WHAT IT DOES: 

    PARAMETERS: 

    RETURNS: 
    """
    len_deaths = len(deaths_array)
    i = 1
    loop_deaths = 0
    while i < 15:
        loop_deaths = loop_deaths + deaths_array[len_deaths - i]
        i = i + 1
    average_deaths = round(loop_deaths/14,2)

    return average_deaths

def average_cases(cases_array)
    """
    WHAT IT DOES: 

    PARAMETERS: 

    RETURNS: 
    """
    len_cases = len(cases_array)
    i = 1
    loop_cases = 0
    while i < 15:
        loop_cases = loop_cases + cases_array[len_cases - i]
        i = i + 1
    average_cases = round(loop_cases/14,2)

    return average_cases

def death_change(average_deaths, new_deaths)
    """
    WHAT IT DOES: 

    PARAMETERS: 

    RETURNS: 
    """
    percent_deaths = 0
    message = " "
    
    # if statement to determine if percent of deaths has increased or decreased
    if average_deaths > int(new_deaths):
        percent_deaths = average_deaths - int(new_deaths)
        percent_deaths = percent_deaths/average_deaths
        percent_deaths = percent_deaths * 100
        percent_deaths = round(percent_deaths, 2)
        message += "Fortunately, this means that deaths have decreased by " + str(percent_deaths) + " percent"
    else:
        percent_deaths = int(new_deaths) - average_deaths
        percent_deaths = percent_deaths/average_deaths
        percent_deaths = percent_deaths * 100
        percent_deaths = round(percent_deaths, 2)
        message += "\nUnfortunately, this means that deaths have increased by " + str(percent_deaths) + " percent"

    return message

def cases_change(average_cases, new_cases)
    """
    WHAT IT DOES: 

    PARAMETERS: 

    RETURNS: 
    """

    percent_cases = 0
    message = " "

    # if statement to determine if percent of cases has increased or decreased
    if average_cases > int(new_cases):
        percent_cases = average_cases - int(new_cases)
        percent_cases = percent_cases/average_cases
        percent_cases = percent_cases * 100
        percent_cases = round(percent_cases, 2)
        message += "Cases have decreased by " + str(percent_cases) + " percent"
    else:
        percent_cases = int(new_cases) - average_cases
        percent_cases = percent_cases/average_cases
        percent_cases = percent_cases * 100
        percent_cases = round(percent_cases, 2)
        message += "Cases have increased by " + str(percent_cases) + " percent"
    
    return message


if __name__ == "__main__":

    if APP_ENV == "development":
        state_input = input("PLEASE INPUT A STATE (e.g. California): ")
        county_input = input("PLEASE INPUT A COUNTY (e.g. Orange): ")
        weather_results = get_hourly_forecasts(state=state_input, county=county_input) # invoke with custom params
    else:
        weather_results = get_hourly_forecasts() # invoke with default params

    # define variables and arrays
    total_deaths = 0 # int
    total_cases = 0 # int
    deaths_array = [] # array of ints
    cases_array = [] # array of ints
    states_array = []  # array of strings
    counties_array = [] # array of strings

    # parse through that data using the CSV module
    # headings ['date', 'county', 'state', 'fips', 'cases', 'deaths']
    with open(file_name, 'r') as f2:
        csv_file_reader = csv.DictReader(f2)
        for row in csv_file_reader:
            states_array.append(row["state"]) # for data validation
            if row["county"] == county_input and row["state"] == state_input:
                total_deaths = total_deaths + int(row["deaths"]) # calculate totals
                total_cases = total_cases + int(row["cases"]) 
                new_cases = row["cases"] # most recent case count
                new_deaths = row["deaths"] # most recent death count 
                recent_date = row["date"] # most recent date the CSV file has been updated for that county
                deaths_array.append(int(new_deaths)) # append to arrays
                cases_array.append(int(new_cases))


    html = ""
    html += f"<h3>Good Morning, {MY_NAME}!</h3>"

    html += "<h4>Today's Date</h4>"
    html += f"<p>{date.today().strftime('%A, %B %d, %Y')}</p>"

    html += f"<h4>COVID-19 COUNTY STATISTICS for {county_input} County, {state_input}.</h4>"
    html += "<ul>"
    for hourly in weather_results["hourly_forecasts"]:
        html += f"<li>{hourly['timestamp']} | {hourly['temp']} | {hourly['conditions'].upper()}</li>"
    html += "</ul>"

    # output message with summary of data
    print(f"As of " + recent_date + ", " + county_input + " County has had " + new_deaths + " new deaths due to COVID-19")
    print(f"Also, the number of new cases is " + new_cases + " cases")
    print("---------------------------------------")
    print(f"Total number of deaths: "+ str(total_deaths))
    print(f"Total number of cases: " + str(total_cases))
    print("---------------------------------------")
    
    print(f"The average number of deaths over these two weeks is " + str(average_deaths))
    print(f"The average number of cases is " + str(average_cases))
    print("---------------------------------------")

    # print a final goodbye message
    print("---------------------------------------")
    print("Thank you for using the COVID-19 County Tracker")

    send_email(subject="COVID-19 Daily County Report", html=html)
