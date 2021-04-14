# Importing important libraries
import requests
import bs4
import re
import matplotlib.pyplot as plt
import csv

# Creating class of important functions
class Weather():
    
    def __init__(self,hiiweather_obj,lowweather_obj):
        
        # Passes in the html website code
        
        self.hiiweather_obj = hiiweather_obj
        self.lowweather_obj = lowweather_obj
        
    def get_days(self):
        
        # Gets the next 14 days from the url 
        
        date = []
        for i in range(1,len(self.lowweather_obj)):
            date.append(soup.select('.DetailsSummary--daypartName--1Mebr'))
            
        date = date[0]
        days = []
        for day in date:
            days.append(day.text)
        
        return days[1:len(date)]
         
    def get_day_weather(self):
        
        # Gets the projected temperature data for the morning and noon
        
        self.hiiweather_obj = hiiweather_obj   
        day_temp_str = re.findall(r'\d\d',str(self.hiiweather_obj))
        day_temp = []
        for i in day_temp_str:
            day_temp.append(float(i))
        
        return day_temp
    
    def get_night_weather(self):
        
        # Gets the projected temperature data for the night
        
        self.lowweather_obj = lowweather_obj
        night_temp_str = re.findall(r'\d\d',str(self.lowweather_obj))
        night_temp = []
        
        for i in night_temp_str:
            night_temp.append(float(i))
        
        return night_temp
    

    def get_weather_detail(self):
        
        # Gets projected weather detail such as if it rains, sunny, snowing, cloudy, etc. 
        
        weather_detail = []
        for i in soup.select('.Icon--icon--2AbGu.Icon--fullTheme--3jU2v.DailyContent--weatherIcon--2tnL5'):
            weather_detail.append(i.text)
            
        if len(weather_detail) == 30:
            return weather_detail[2:len(weather_detail)]
        elif len(weather_detail) == 29:
            return weather_detail[1:len(weather_detail)]
        
    def get_temp_csv_data(self,days,night_temp,day_temp,weather_details):
        
        # Saving the information into a csv file
        
        self.days = days
        self.night_temp = night_temp
        self.day_temp = day_temp
        self.weather_details = weather_details
        
        day_weather_details = []
        night_weather_details = []
        for i in range(0,len(self.weather_details)):
            if i % 2 == 0:
                day_weather_details.append(self.weather_details[i])
            else:
                night_weather_details.append(self.weather_details[i])
            
        
        
        # Creates CSV file
        create_file = open('weather_data.csv','w',newline='')
        weather_data = csv.writer(create_file,delimiter=',')
        weather_data.writerow(['Day','Day Temperature [\N{DEGREE SIGN}F]','Night Temperature [\N{DEGREE SIGN}F]','Day Weather Information','Night Weather Information'])
        create_file.close()
        
        # Appends days and temperature details
        for i in range(0,len(self.days)):
            f = open('weather_data.csv','a',newline='')
            weather_data = csv.writer(f)
            weather_data.writerow([self.days[i],self.day_temp[i],self.night_temp[i],day_weather_details[i],night_weather_details[i]])
            f.close()
        
    

# Getting the url and website html code
url = requests.get("https://weather.com/weather/tenday/l/2e5da9e3a4d6ad00aaf8bdeb907999bbed62f07c7f02226ef84189690daa2215")
soup = bs4.BeautifulSoup(url.text,"lxml")
hiiweather_obj = soup.select('.DetailsSummary--highTempValue--3x6cL')
lowweather_obj = soup.select('.DetailsSummary--lowTempValue--1DlJK')

# Extracting data 
temperature = Weather(hiiweather_obj,lowweather_obj)
day_temp = temperature.get_day_weather()
night_temp = temperature.get_night_weather()
days = temperature.get_days()
weather_detail = temperature.get_weather_detail()

# Fail-safe to ensure the list length remains the same
if len(day_temp) != len(days):
    day_temp.pop(0)

if len(night_temp) != len(days):
    night_temp.pop(0)

# Plotting temperatures with respect to days
fig = plt.figure(figsize=(15,15))
plt.subplot(2,1,1)
plt.plot(days, day_temp,'r')
plt.legend(['Daytime Temperature'])
plt.ylabel("Temperature [\N{DEGREE SIGN}F]")
plt.title('Temperature Forcast [\N{DEGREE SIGN}F]')
plt.grid()

plt.subplot(2,1,2)
plt.plot(days, night_temp,'b')
plt.legend(['Nighttime Temperature'])
plt.xlabel("Dates")
plt.ylabel("Temperature [\N{DEGREE SIGN}F]")
plt.grid()
fig.savefig('Temperature Forcast')



# Getting the information into CSV file
temperature.get_temp_csv_data(days,night_temp,day_temp,weather_detail)

    
        
