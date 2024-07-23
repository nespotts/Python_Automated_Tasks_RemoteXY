import requests
import json

headers = {"accept": "application/json"}




class TomorrowAPI:
    key = "BCuIasKaoGFaKF4HLIl7Yq7TT7NHbGMI"
    location = "43567%20US"
    api = "https://api.tomorrow.io/v4/weather/"
    
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
        
        
        
        # print(self.getLocalTime())
        
        # print("\n\n")

        self.getHistoricalWeather()
        
        # print("\n\n")

        # self.getForecastWeather(1)
        
        
    def getHistoricalWeather(self):
        url = f"{self.api}/history/recent?location={self.location}&units=imperial&apikey={self.key}"
        response = requests.get(url=url)
        data = json.loads(response.text)
        
        # print(json.dumps(data, indent=4))
        
        print(json.dumps(data['timelines']['daily'], indent=4))
        
        
    # def getForecastWeather(self, num_days):
    #     url = f"{self.api}forecast.json?key={self.key}&q={self.location}&days={num_days}&aqi=no&alerts=no"
    #     response = requests.get(url=url)
    #     data = json.loads(response.text)
        
    #     print(json.dumps(data['forecast']['forecastday'][0]['hour'], indent=4))
        
        
    # def getLocalTime(self):
    #     url = f"{self.api}timezone.json?key={self.key}&q={self.location}"
    #     response = requests.get(url=url)
    #     data = json.loads(response.text)
        
    #     # print(json.dumps(data, indent=4))
        
    #     return response.json()['location']['localtime']
        
        
    # def getLocalDate(self):
    #     datetime = self.getLocalTime()
    #     date = datetime.split(' ')[0]
    #     return date

        

if __name__ == "__main__":
    # from influxDB import InfluxDB
    # db = InfluxDB()

    # from Blynk import Blynk
    # blynk = Blynk(db, False)

    from notification_manager import NotificationManager
    nm = NotificationManager()

    ma = TomorrowAPI(nm)
    ma.run()