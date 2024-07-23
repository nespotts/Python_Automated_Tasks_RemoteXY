import time

class BMS:
    def __init__(self, blynk, nm):
        self.blynk = blynk
        self.nm = nm
        self.blynk_bms_pins = {
            'voltage': [5,17,29],
            'current': [6,18,30],
            'state_of_charge_percent': [7,19,31],
            'discharge_status': [8,20,32],
            'charge_status': [9,21,33],
            'state_of_charge': [12,24,36],
            'capacity': [13,25,37]
        }
        self.battery = {
            'voltage': 0,
            'current': 0,
            'state_of_charge': 0,
            'state_of_charge_percent': 0,
            'capacity': 0,
            'power': 0,
        }
        self.cell_voltages = [
            {
                "cells": [14,0,15,16],
                "delta_pin": 38,
                "delta": 0
                
            },
            {
                "cells": [49,50,51,52],
                "delta_pin": 39,
                "delta": 0
            },
            {
                "cells": [26,63,27,64],
                "delta_pin": 40,
                "delta": 0
            }
        ]
        self.send_timer = 0
        self.send_interval = 750
        
        self.sms_discharge_interval = 60000
        self.sms_timer = 0

    def sendToBlynk(self):
        # print(7)
        self.blynk.virtual_write_batch(['V41','V42','V43','V44','V45','V46'], [self.battery['voltage'], self.battery['current'], self.battery['capacity'], self.battery['state_of_charge'], self.battery['state_of_charge_percent'], self.battery['power']], "rv_brain")
        self.blynk.virtual_write_batch(['V41','V42','V43','V44','V45','V46'], [self.battery['voltage'], self.battery['current'], self.battery['capacity'], self.battery['state_of_charge'], self.battery['state_of_charge_percent'], self.battery['power']], "rv_battery")
        # print(8)
        # print(self.battery)
        self.blynk.virtual_write_batch(['V38','V39','V40'], [self.cell_voltages[0]["delta"], self.cell_voltages[1]["delta"], self.cell_voltages[2]["delta"]], "rv_battery")
    

    def run(self):
        while True:
            t = time.time_ns() // 1000000

            try:
                if (t - self.send_timer) >= self.send_interval:
                    print("Calculating Battery Totals")
                    self.calcBatteryStats()
                    self.send_timer = t
                    self.sendToBlynk()
                    # print(self.battery)
                    
                discharge_status = self.blynk.get_pin_vals(["V8","V20","V32"], "rv_battery")
                if 0 in discharge_status:
                    if (t - self.sms_timer) >= self.sms_discharge_interval:
                        self.sms_timer = t
                        self.nm.send_message("A battery discharge mosfet is turned off")
                        
            except Exception as e:
                # print(e)
                pass

    def calcBatteryStats(self):
        self.calcVoltage()
        self.calcCurrent()
        self.calcStateOfCharge()
        self.calcStateOfChargePercent()
        self.calcBatteryCapacity()
        self.calcBatteryPower()
        self.calcMaxCellDeltas()
        
    def calcMaxCellDeltas(self):
        # loop thru batteries
        # find difference between max and min cell voltages
        
        for battery in self.cell_voltages:
            voltages = self.blynk.get_pin_vals(battery["cells"], "rv_battery")
            # print(voltages)
            battery["delta"] = round(max(voltages) - min(voltages), 3)
            # print(battery["delta"])
            
            
                

    def calcVoltage(self):
        voltages = self.blynk.get_pin_vals(self.blynk_bms_pins['voltage'], "rv_battery")
        sum = 0
        for voltage in voltages:
            sum += voltage
        self.battery['voltage'] = round(sum/3, 3)

    def calcCurrent(self):
        currents = self.blynk.get_pin_vals(self.blynk_bms_pins['current'], "rv_battery")
        sum = 0
        for current in currents:
            sum += current
        self.battery['current'] = round(sum, 3)

    def calcStateOfCharge(self):
        SOCs = self.blynk.get_pin_vals(self.blynk_bms_pins['state_of_charge'], "rv_battery")
        sum = 0
        for SOC in SOCs:
            sum += SOC
        self.battery['state_of_charge'] = round(sum, 3)

    def calcStateOfChargePercent(self):
        SOCs = self.blynk.get_pin_vals(self.blynk_bms_pins['state_of_charge_percent'], "rv_battery")
        sum = 0
        for SOC in SOCs:
            sum += SOC
        self.battery['state_of_charge_percent'] = round(sum/3, 3)

    def calcBatteryCapacity(self):
        capacities = self.blynk.get_pin_vals(self.blynk_bms_pins['capacity'], "rv_battery")
        sum = 0
        for capacity in capacities:
            sum += capacity
        self.battery['capacity'] = round(sum, 3)

    def calcBatteryPower(self):
        power = self.battery['voltage'] * self.battery['current']
        # print(f"----{power}----")
        self.battery['power'] = round(power, 3)


        