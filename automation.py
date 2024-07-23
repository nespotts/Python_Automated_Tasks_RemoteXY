from datetime import datetime, timezone, timedelta
import time
# import pytz

class Automation:
    def __init__(self, blynk, bms, solar, nm):
        self.blynk = blynk
        self.bms = bms
        self.solar = solar
        self.nm = nm
        self.water_heater_state = 0  # 0-off 3-on
        self.inverter_state = 0  # 0-off 1-starting 2-waiting on inverter 3-on
        self.state = 0  # 0-inverter & WH off, 1-invert on WH off, 2-inverter on WH on, 3-inverter starting
        self.inverter_start_timer = 0
        self.state_timer = 0
        self.state_interval = 500

        self.load_timer = 0
        self.load_interval = 750
        
        self.fan_timer = 0
        self.fan_interval = 750

        self.house_lights_timer = 0
        self.house_lights_interval = 1000

        # setup timezone hours offset
        self.tz = timezone(timedelta(hours=-5))
        self.now = datetime.now(self.tz)

    def run(self):
        # if time of day is corrrect a
        # and if battery is above 95%
        # 
        while True:
            t = time.time_ns() // 1000000
            self.now = datetime.now(self.tz)

            if (t - self.state_timer) > self.state_interval:
                self.state_timer = t

                try:
                    automation_en = self.blynk.get_pin_val('V78', "rv_brain")
                    if automation_en == 1:
                        print('automation enabled')
                        # self.manage_inverter()
                        # self.manage_water_heater()
                        # print('a')
                        self.syncState()
                        # print('b')
                        self.stateMachine()
                        # print(2)
                    else:
                        print('automation disabled')
                        pass
                except Exception as e:
                    print(e)

            if (t - self.load_timer) > self.load_interval:
                self.load_timer = t
                try:
                    self.calc_load_current()
                    print("Calculating Load")
                except Exception as e:
                    print(e)
                    
            # add automation for solar fans and exhaust fan
            if (t - self.fan_timer) > self.fan_interval:
                self.fan_timer = t
                try:
                    # get max of the solar controller temperatures
                    self.controlSolarFan()
                    self.controlExhaustFan()                    
                except Exception as e:
                    print(e)

            # automate house lights
            if (t - self.house_lights_timer) > self.house_lights_interval:
                self.house_lights_timer = t
                try:
                    if self.now.hour == 7 and self.now.minute == 0:
                        print("turning house light on")
                        self.blynk.virtual_write('V1', 0, "house_lights")
                    elif self.now.hour == 8 and self.now.minute == 0:
                        print("turning house light off")
                        self.blynk.virtual_write('V1', 1, "house_lights")
                    elif self.now.hour == 5 and self.now.minute == 0:
                        print("turning house light on")
                        self.blynk.virtual_write('V1', 0, "house_lights")
                    elif self.now.hour == 8 and self.now.minute == 0:
                        print("turning house light off")
                        self.blynk.virtual_write('V1', 1, "house_lights")
                        

                except Exception as e:
                    print(e)
                    # pass
                    
                    
    def controlSolarFan(self):
        fan_temp = 115.0
        temp_deadband = 1
        
        temp1 = self.blynk.get_pin_val('V53', "rv_brain")
        temp2 = self.blynk.get_pin_val('V60', "rv_brain")
        temp3 = self.blynk.get_pin_val('V67', "rv_brain")
        current_fan_state = self.blynk.get_pin_val('V75', "rv_brain")
        
        max_temp = max([temp1, temp2, temp3])
        
        if max_temp >= (fan_temp + temp_deadband) and current_fan_state == 0:
            print("Turning on solar fans")
            # self.nm.send_message("Turning on solar fan")
            self.blynk.virtual_write('V75', 1, "rv_brain")
        elif max_temp < (fan_temp - temp_deadband) and current_fan_state == 1:
            print("Turning Off solar fans")
            # self.nm.send_message("Turning off solar fan")
            self.blynk.virtual_write('V75', 0, "rv_brain")
            
            
    def controlExhaustFan(self):
        on_temp = 90.0
        off_temp = 85.0
        
        electrical_temp = self.blynk.get_pin_val('V11', "rv_brain")
        current_fan_state = self.blynk.get_pin_val('V76', "rv_brain")
        
        if electrical_temp >= on_temp and current_fan_state == 0:
            print("Turning on exhaust fan")
            self.blynk.virtual_write('V76', 1, "rv_brain")
        elif electrical_temp <= off_temp and current_fan_state == 1:
            print("Turning Off exhaust fan")
            self.blynk.virtual_write('V76', 0, "rv_brain")
    

    def stateMachine(self):
        # print(4)
        schedule = self.blynk.get_pin_val('V77', "rv_brain").split("\x00")
        soc = self.blynk.get_pin_val('V45', "rv_brain")
        soc_range = self.blynk.get_pin_val('V79', "rv_brain").split("-")
        # print(5)
        min_hour = int(schedule[0]) // 3600
        max_hour = int(schedule[1]) // 3600
        inverter_off_time = self.blynk.get_pin_val('V5', "rv_brain").split("\x00")
        inverter_off_hour = int(inverter_off_time[0]) // 3600
        inverter_off_minute = (int(inverter_off_time[0]) % 3600) // 60
        # print(6)
        soc_turn_on = float(soc_range[1])
        soc_turn_off = float(soc_range[0])
        # print(7)
        # utc = datetime.datetime.now()  # UTC
        # print(8)
        # eastern = pytz.timezone('US/Eastern')  # eastern timezone info
        # print(9)
        # now = utc.astimezone(eastern)
        # self.now = datetime.now()
        # print(10)


        match self.state:
            case 0:  # inverter & WH off
                # check if it's time to turn on
                if (
                        soc >= soc_turn_on and self.now.hour >= min_hour and self.now.hour < max_hour and self.now.hour < inverter_off_hour):
                    self.state = 1
                    self.blynk.virtual_write('V74', 1)
                    self.inverter_start_timer = time.time()  # in seconds
                    print("Starting Inverter")
            case 1:  # inverter starting
                if (time.time() - self.inverter_start_timer >= 10):
                    self.state = 2
                    print("Inverter Running")
            case 2:  # inverter on, WH off
                if (
                        soc >= soc_turn_on and self.now.hour >= min_hour and self.now.hour < max_hour and self.now.hour < inverter_off_hour):
                    self.state = 3
                    self.blynk.virtual_write('V73', 1)
                    print("Turning Water Heater On")
                elif self.now.hour >= inverter_off_hour:
                    self.state = 0
                    self.blynk.virtual_write('V73', 0)
                    self.blynk.virtual_write('V74', 0)
                    print("Turning Inverter Off for the Night")
            case 3:  # inverter & WH on
                if (soc <= soc_turn_off or self.now.hour < min_hour or self.now.hour >= max_hour):
                    self.state = 2
                    self.blynk.virtual_write('V73', 0)
                    print("Turning Water Heater Off")

                if self.now.hour >= inverter_off_hour:
                    self.state = 0
                    self.blynk.virtual_write('V73', 0)
                    self.blynk.virtual_write('V74', 0)
                    print("Turning Inverter Off for the Night")

    def syncState(self):
        inverter_switch = self.blynk.get_pin_val('V74', "rv_brain")
        water_heater = self.blynk.get_pin_val('V73', "rv_brain")

        if inverter_switch == 0 and water_heater == 0:
            self.state = 0
        elif inverter_switch == 1 and water_heater == 0 and self.state != 1:
            self.state = 2
        elif inverter_switch == 0 and water_heater == 1:
            self.blynk.virtual_write('V73', 0)
            self.state = 0
        elif inverter_switch == 1 and water_heater == 1:
            self.state = 3

    def calc_load_current(self):
        battery_current = self.bms.battery['current']
        solar_current = self.solar.solar_data['battery_current']
        dc_dc_current = self.blynk.get_pin_val('V8', "rv_brain")
        inv_current = self.blynk.get_pin_val('V7', "rv_brain")

        # bucket inverter current as a dc load when it is not charging
        if (inv_current < 0):
            load_current = solar_current + dc_dc_current - battery_current
        else:
            load_current = solar_current + dc_dc_current + inv_current - battery_current
            
        res = self.blynk.virtual_write('V72', load_current, "rv_brain")
