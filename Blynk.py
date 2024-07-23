import time
import requests
from create_datastream_dict import createBlynkDatastreams
from influxdb_client_3 import Point

class Blynk:
	def __init__(self, db, send_to_influx):
		self.db = db
		self.send_to_influx = send_to_influx
		self.endpoint = "https://blynk.cloud/external/api/"
		self.rv_brain_token = "fkY_GzSnp2MVq31eh4iSj6UIne4-RFY0"
		self.rv_battery_token = "a58EO0MExXyF1byGFDbb-WmtsQw71bdW"
		self.house_lights_token = "dWl-flniQB-bG9NC7p2hIl-H4OiNUpp7"
		# self.read_rv_brain_pins = [0,1,2,3,4,5,6,7,8,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79]
		# self.read_rv_battery_pins = [5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40]
		# self.read_house_lights_pins = [0,1,2,3]
		# self.rv_brain_pin_vals = {}
		# self.rv_battery_pin_vals = {}
		# self.house_lights_pin_vals = {}
		self.read_interval = 750
		self.read_timer = 0
		ds = createBlynkDatastreams()
  
		# generate from create_datastream_dict.py		
		# when changing datastreams, need to update html in datastream_html.py
		self.rv_brain_datastreams = ds.process_html(1)
		self.rv_battery_datastreams = ds.process_html(2)
		self.house_lights_datastreams = ds.process_html(3)

	def virtual_write(self, pin, value, device="rv_brain"):
		if device == "rv_brain":
			token = self.rv_brain_token
		elif device == "rv_battery":
			token = self.rv_battery_token
		else:
			token = self.house_lights_token
   
		url = self.endpoint + "update?token=" + token + "&" + str(pin) + "=" + str(value)
		# print(1)
		response = requests.get(url=url)
		# print(2)

		# print(response.status_code)
		return response.status_code
		if response.status_code == 200:
			return 1
		else:
			return 0
		
	def virtual_write_batch(self, pins, values, device="rv_brain"):
		if device == "rv_brain":
			token = self.rv_brain_token
		elif device == "rv_battery":
			token = self.rv_battery_token
		else:
			token = self.house_lights_token
   
		url = self.endpoint + "batch/update?token=" + token
		for i in range(len(pins)):
			pin_str = ""
			if isinstance(pins[i], int):
				pin_str = f"V{pins[i]}"
			elif not pins[i].__contains__('V'):
				pin_str = f"V{pins[i]}"
			else:
				pin_str = pins[i]
			url += "&" + pin_str + "=" + str(values[i])
	
		try:
			response = requests.get(url=url, timeout=3)
			return response.status_code
		except requests.Timeout as e:
			print(e)
			return 500
		except requests.RequestException as e:
			print(e)
			return 500
	

	def virtual_read(self, datastreams, device="rv_brain"):
		if device == "rv_brain":
			token = self.rv_brain_token
		elif device == "rv_battery":
			token = self.rv_battery_token
		else:
			token = self.house_lights_token
   
		pin_list = ""
		# for pin in pins:
		# 	pin_list += "&V" + str(pin)
		for pin, props in datastreams.items():
			pin_list += "&" + pin
   
		# print(pin_list)
			

		url = self.endpoint + "get?token=" + token + str(pin_list)
		# print(url)
		# print(3)
		try:
			response = requests.get(url=url, timeout=3)
			status = response.status_code
			if status == 200:
				vals = response.json()
				# print(vals)
				vals = {k:v for k,v in vals.items()}
				# print(vals)
				# add value to datastreams dict
				return vals
				# for dict in self.rv_brain_datastreams:
				# 	print(dict)
				# 	dict.val = vals[dict.pin]
				# print(self.rv_brain_datastreams)
				# return self.rv_brain_datastreams

				# add vals to datastreams
				# return vals
			else:
				return False
		except requests.Timeout as e:
			print(e)
			return False
		except requests.RequestException as e:
			print(e)
			return False
		# print(4)

	
	def get_pin_vals(self, pins, device="rv_battery"):
		output = []
		for pin in pins:
			pin_str = ""
			if isinstance(pin, int):
				pin_str = f"V{pin}"
			elif not pin.__contains__('V'):
				pin_str = f"V{pin}"
			else:
				pin_str = pin
			# print(pin_str, self.pin_vals)
			try:
				if device == "rv_battery":
					# output.append(self.rv_battery_pin_vals[pin_str])
					output.append(self.rv_battery_datastreams[pin_str]['val'])
				elif device == "rv_brain":
					# output.append(self.rv_brain_pin_vals[pin_str])
					output.append(self.rv_brain_datastreams[pin_str]['val'])
				else:
					# output.append(self.house_lights_pin_vals[pin_str])
					output.append(self.house_lights_datastreams[pin_str]['val'])
			except IndexError:
				return False

		return output
	
	
	def get_pin_val(self, pin, device="rv_battery"):
		pin_str = ""
		if isinstance(pin, int):
			pin_str = f"V{pin}"
		elif not pin.__contains__('V'):
			pin_str = f"V{pin}"
		else:
			pin_str = pin
		# print(pin_str, self.pin_vals)
 
		try:
			if device == "rv_battery":
				# print(self.rv_battery_pin_vals)
				# return self.rv_battery_pin_vals[pin_str]
				return self.rv_battery_datastreams[pin_str]['val']
			elif device == "rv_brain":
				# print(self.rv_brain_pin_vals)
				# return self.rv_brain_pin_vals[pin_str]
				return self.rv_brain_datastreams[pin_str]['val']
			else:
				# return self.house_lights_pin_vals[pin_str]
				return self.house_lights_datastreams[pin_str]['val']
		except IndexError:
			print(False)
			return False


	def run(self):
		while True:
			t = time.time_ns() // 1000000

			if (t - self.read_timer) >= self.read_interval:
				try:
					# vals = self.virtual_read(self.read_rv_brain_pins, "rv_brain")
					vals = self.virtual_read(self.rv_brain_datastreams, "rv_brain")
					if vals != False:
						data = []
						for pin,value in vals.items():
							self.rv_brain_datastreams[pin]['val'] = value
							if self.send_to_influx:
								column = self.rv_brain_datastreams[pin]['name']
								column = "dc_dc_currentF" if column == "dc_dc_current" else column
								table = "rv_brain"
								point = (
									Point(table).field(column, value)
								)
								data.append(point)								

						# print(self.rv_brain_datastreams)
						# print(data)
						if self.send_to_influx:
							self.db.write(data)


					vals = self.virtual_read(self.rv_battery_datastreams, "rv_battery")
					if vals != False:
						data = []
						for pin,value in vals.items():
							self.rv_battery_datastreams[pin]['val'] = value
							if self.send_to_influx:
								column = self.rv_battery_datastreams[pin]['name']
								table = "rv_battery"
								point = (
									Point(table).field(column, value)
								)
								data.append(point)	

						# print(self.rv_battery_datastreams)
						# print(data)
						if self.send_to_influx:
							self.db.write(data)

					vals = self.virtual_read(self.house_lights_datastreams, "house_lights")
					if vals != False:
						data = []
						for pin,value in vals.items():
							self.house_lights_datastreams[pin]['val'] = value
							column = self.house_lights_datastreams[pin]['name']
							table = "rv_battery"
							if self.send_to_influx:
								point = (
									Point(table).field(column, value)
								)
								data.append(point)	

						# print(self.house_lights_datastreams)
						# print(data)
						if self.send_to_influx:
							self.db.write(data)
						
					self.read_timer = t
					# print(self.pin_vals)

					print("Read Blynk Values")

				except Exception as e:
					print(e)


if __name__ == "__main__":
	from influxDB import InfluxDB
	db = InfluxDB()
 
	blynk = Blynk(db=db, send_to_influx=True)
	blynk.run()