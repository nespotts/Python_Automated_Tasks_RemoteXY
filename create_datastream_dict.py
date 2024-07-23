import requests
from bs4 import BeautifulSoup
from datastream_html import rv_brain_html, rv_battery_html, home_lights_html


	# response = requests.get("https://blynk.cloud/dashboard/52834/templates/edit/288956/datastreams")
class createBlynkDatastreams:
	rv_brain_datastreams = []
	rv_battery_datastreams = []
	house_lights_datastreams = []
	
	def __init__(self) -> None:
		pass

	def process_html(self, selector):
		if selector == 1:
			html = rv_brain_html
		elif selector == 2:
			html = rv_battery_html
		elif selector == 3:
			html = home_lights_html
   
		soup = BeautifulSoup(html, features="html.parser")
		rows = soup.select("#datastreams-table > div > div.ant-table-body > table > tbody > tr.ant-table-row")

		datastreams = {}
		# print(rows)
		for row in rows:
			name = row.select_one("td.ant-table-cell.table-cell-name.ant-table-cell-fix-left.ant-table-cell-fix-left-last.ant-table-cell-ellipsis > span > span")
			pin = row.select_one("td:nth-child(5)")
			# datastreams.append(name.text)

			datastreams[pin.text] = {
				"name": name.text,
				"pin": pin.text
			}


		print(datastreams)
		return datastreams
     



# print(response.text)

if __name__ == "__main__":
  d = createBlynkDatastreams()
  d.process_html(1)