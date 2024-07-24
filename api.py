import requests
import time

class API:
  def __init__(self):
    self.read_interval = 1000
    self.read_timer = 0
    self.url = "http://192.168.8.148"
    
    self.datastreams = {}
    
  def get_all_data(self):
    url = f"{self.url}/get_all"
    response = requests.get(url=url)

    if response.status_code == 200:
      self.datastreams = response.json()
      # print(self.datastreams)


  def run(self):
    while True:
      t = time.time_ns() // 1000000
      
      if (t - self.read_timer) >= self.read_interval:
        self.get_all_data()
        self.read_timer = t
        
  def get_value(self, key):
    return self.datastreams[key]
  
  
  def set_value(self, key, value):
    url = f"{self.url}/set_value/{key}/{value}"
    response = requests.get(url=url)
    # print(response.status_code)
    
  def set_solar_params(self, solar_id, voltage, current, power, battery_voltage, battery_current, state_of_charge, controller_temp):
    url = f"{self.url}/set_solar_params/{solar_id}/{voltage}/{current}/{power}/{battery_voltage}/{battery_current}/{state_of_charge}/{controller_temp}"
    response = requests.get(url=url)
    # print(response.status_code)
    
    
    
    
    
    
if __name__ == "__main__":
  api = API()
  # api.set_value("solar_power", 0)
  # api.set_solar_params(1, 0, 0, 0, 0, 0, 0, 0)
  # api.run()

