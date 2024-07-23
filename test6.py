import requests
import json
from datetime import date, timedelta

class MowingAutomation:
    key = "8d2baeda83354e7abcd123415241705"
    location = "Wauseon,OH"
    api = "http://api.weatherapi.com/v1/"
    date = None
    time = None
    hours = None # 24 hr clock
    minutes = None
    
    historical_data = None
    forecast_data = None
    
    def __init__(self, nm):
        # self.blynk = blynk  # might not need blynk here
        self.nm = nm

    def run(self):
        # Main Logic
        '''
        if the time is 10:00 AM ohio time, do historical checks and current day forecast
            Historical Checks
                - past day precipitation
                - past two day precipitation
                - past 3 day precipitation
                - past 10 hour rainfall
            Forecast Checks
                - Current condition (raining / humidity / condition code)
                - chance of rain (will_it_rain today / hourly)
        '''
        
        self.getLocalTime()
        
        print(self.date)
        print(self.time_str)
        print(self.hours)
        print(self.minutes)
        
        # if self.hours == 9 and self.minutes >= 55 or self.hours == 10 and self.minutes <= 5:
        # testing
        if True:
            # its about 10:00 AM
            # get todays precipitation thus far
            self.getHistoricalWeather(self.time_str)

            
            
            # get yesterday's date
            yesterday = date.today() - timedelta(days=1)
            
            print(yesterday)
            # self.getHistoricalWeather()
            
        
        # print("\n\n")

        # self.getHistoricalWeather('2024-05-18')
        
        # print("\n\n")

        # self.getForecastWeather(1)
        
        
    def getHistoricalWeather(self, date):
        url = f"{self.api}history.json?key={self.key}&q={self.location}&dt={date}"
        response = requests.get(url=url)
        # data = json.loads(response.text)
        # print(json.dumps(data, indent=4))
        
        self.historical_data = response.json()['forecast']['forecastday']
        
        
    def getForecastWeather(self, num_days):
        url = f"{self.api}forecast.json?key={self.key}&q={self.location}&days={num_days}&aqi=no&alerts=no"
        response = requests.get(url=url)
        # data = json.loads(response.text)
        # print(json.dumps(data['forecast']['forecastday'][0]['hour'], indent=4))
        
        self.forecast_data = response.json()['forecast']['forecastday']
        
        
        
    def getLocalTime(self):
        url = f"{self.api}timezone.json?key={self.key}&q={self.location}"
        response = requests.get(url=url)
        # data = json.loads(response.text)
        # print(json.dumps(data, indent=4))
        
        datetime = response.json()['location']['localtime'].split(' ')
        self.date = datetime[0]
        self.time_str = datetime[1]
        time_nums = self.time_str.split(":")
        self.hours = time_nums[0]
        self.minutes = time_nums[1]

        

if __name__ == "__main__":
    # from influxDB import InfluxDB
    # db = InfluxDB()

    # from Blynk import Blynk
    # blynk = Blynk(db, False)

    from notification_manager import NotificationManager
    nm = NotificationManager()

    ma = MowingAutomation(nm)
    ma.run()