import gspread,datetime
from oauth2client.service_account import ServiceAccountCredentials
from time import sleep

scope = ['https://spreadsheets.google.com/feeds']
credentials = ServiceAccountCredentials.from_json_keyfile_name('My Project 42524-9bf42c7441d1.json', scope) ## Temp-3914c1792c0b.json replace Your Json file
gc = gspread.authorize(credentials)

wks = gc.open("Temp").sheet1  ## Temp replace your Work sheet name

def main():
	sensor = 1 #DS18B20()
	
	while True:
		time = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
		temperatures = sensor.get_temperatures([1, 2, 3])
		
		print time
       		print("Degrees Celsius: %f" % temperatures[0])
       		print("Kelvin: %f" % temperatures[2])
	 	print("Degrees Fahrenheit: %f" % temperatures[1])
		print("Adding row please wait...")
		
		x = 0
		try:
			for values in wks.col_values(1):  ## loop count row
    				x = x + 1
			rowToAdd = [time, temperatures[0], temperatures[2], temperatures[1]] ## your data want to send
			wks.resize(x)
			wks.append_row(rowToAdd)
			print("Add row done !!!")
			print("==================================")
			sleep(5)
		except:
			print("Exit.")
			print("Bye...")
			break;

if __name__ == "__main__":
main()