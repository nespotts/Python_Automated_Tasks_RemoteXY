import time
from renogymodbus import RenogyChargeController
from notification_manager import NotificationManager
from api import *


class ChargeController:
    def __init__(self, api, nm):
        self.api = api
        self.nm = nm
        self.COM_port = "/dev/ttyUSB0"
        
        self.read_timer = 0
        self.read_interval = 1000
        self.min_read_time_gap = 250
        self.send_timer = 0
        self.send_interval = 1000

        self.controllers = {}
        self.controller1 = None
        self.controller2 = None
        self.controller3 = None
        self.create_controller_data()

        self.controller_efficiency = 0.94

        self.solar_data = {
            'battery_current': 0,
            'battery_voltage': 0,
            'solar_current': 0,
            'solar_power': 0,
        }
        
        self.msg_interval = 15 * 60000
        self.msg_timer = 0
        
    def create_controller_data(self):
        # self.controller_data = {addr: {} for position: addr in self.controller_addresses}
        try:
            self.controller1 = RenogyChargeController(self.COM_port, 17)
            self.controller2 = RenogyChargeController(self.COM_port, 18)
            self.controller3 = RenogyChargeController(self.COM_port, 16)
            self.controllers = [{}, {}, {}]
        except Exception as e:
            print(e)

        # print(self.controllers)

    def calc_combined_solar_data(self):
        self.solar_data['battery_current'] = self.calcCombinedBatteryCurrent()
        self.solar_data['battery_voltage'] = self.calcAverageBatteryVoltage()
        self.solar_data['solar_current'] = self.calcCombinedSolarCurrent()
        self.solar_data['solar_power'] = self.calcCombinedSolarPower()


    def calcCombinedBatteryCurrent(self):
        sum = 0
        for controller in self.controllers:
            sum += controller['battery_current']
        return round(sum, 3)
    
    def calcCombinedSolarCurrent(self):
        sum = 0
        for controller in self.controllers:
            sum += controller['solar_current']
        return round(sum, 3)

    def calcCombinedSolarPower(self):
        sum = 0
        for controller in self.controllers:
            sum += controller['solar_power']
        return round(sum, 3)

    def calcAverageBatteryVoltage(self):
        sum = 0
        for controller in self.controllers:
            sum += controller['battery_voltage']
        return round(sum/3, 3)

    def send_to_api(self):

        # need to write individual solar controller values
        try:
            for i in range(3):
                # set_solar_params(solar_id, voltage, current, power, battery_voltage, battery_current, state_of_charge, controller_temp)
                self.api.set_solar_params(i, self.controllers[i]['solar_voltage'], self.controllers[i]['solar_current'], self.controllers[i]['solar_power'], self.controllers[i]['battery_voltage'], self.controllers[i]['battery_current'], self.controllers[i]['state_of_charge'], self.controllers[i]['controller_temperature'])

            # send combined data
            self.api.set_val("solar_battery_current", self.solar_data['battery_current'])
            self.api.set_val("solar_battery_voltage", self.solar_data['battery_voltage'])
            self.api.set_val("solar_current", self.solar_data['solar_current'])
            self.api.set_val("solar_power", self.solar_data['solar_power'])
        except Exception as e:
            print(f"Exception in send_to_api: {e}")


    def run(self):
        while True:
            t = time.time_ns() // 1000000

            try:
                if (t - self.read_timer) >= self.read_interval:
                    # testing
                    # pass
                    print("Getting Solar Info")
                    self.get_charge_controller_info()
                    now = time.time_ns() // 1000000

                    next_time = t + self.read_interval
                    if next_time - now < self.min_read_time_gap:
                    # if (now - self.min_read_time_gap - self.read_interval) >= t:
                        print('waiting')
                        self.read_timer = now + self.min_read_time_gap
                    else:
                        print('not waiting')
                        self.read_timer = t

                if (t - self.send_timer) >= self.send_interval:
                    self.send_to_api()
                    self.send_timer = t
            except Exception as e:
                # pass
                print(e)

    def get_charge_controller_info(self):
        for i in range(len(self.controllers)):
            if i == 0:
                controller = self.controller1
            elif i == 1:
                controller = self.controller2
            elif i == 2:
                controller = self.controller3
            try:
                # print(i)
                # get current values and assign to dictionary
                self.controllers[i]['solar_voltage'] = controller.get_solar_voltage()
                self.controllers[i]['solar_current'] = controller.get_solar_current()
                self.controllers[i]['solar_power'] = controller.get_solar_power()
                self.controllers[i]['battery_voltage'] = controller.get_battery_voltage()
                self.controllers[i]['battery_current'] = round((self.controllers[i]['solar_power'] / self.controllers[i]['battery_voltage']) * self.controller_efficiency, 3)
                # self.controllers[i]['max_solar_power_today'] = controller.get_maximum_solar_power_today()
                # self.controllers[i]['min_solar_power_today'] = controller.get_minimum_solar_power_today()
                self.controllers[i]['state_of_charge'] = controller.get_battery_state_of_charge()
                self.controllers[i]['controller_temperature'] = round(controller.get_controller_temperature()*1.8 + 32.0, 3)
                
                # necessary time delay to prevent communication issues
                time.sleep(0.05)
            except Exception as e:
                print(e)
                t = time.time_ns() // 1000000
                if (t - self.msg_timer) >= self.msg_interval:
                    self.msg_timer = t
                    self.nm.send_message(f"Failed to get solar charge controller info from controller {i+1}")
                

        # print(self.controllers[0])
        # print(self.controllers[1])
        # print(self.controllers[2])




if __name__ == "__main__":
    api = API()
    nm = NotificationManager()
    controller = ChargeController(api, nm)
    while True:
        controller.run()
