import gspread,datetime
import smbus			#import SMBus module of I2C
from oauth2client.service_account import ServiceAccountCredentials
from time import sleep


#some MPU6050 Registers and their Address
PWR_MGMT_1   = 0x6B
SMPLRT_DIV   = 0x19
CONFIG       = 0x1A
GYRO_CONFIG  = 0x1B
INT_ENABLE   = 0x38
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H  = 0x43
GYRO_YOUT_H  = 0x45
GYRO_ZOUT_H  = 0x47

def MPU_Init():
	#write to sample rate register
	bus.write_byte_data(Device_Address, SMPLRT_DIV, 7)
	
	#Write to power management register
	bus.write_byte_data(Device_Address, PWR_MGMT_1, 1)
	
	#Write to Configuration register
	bus.write_byte_data(Device_Address, CONFIG, 0)
	
	#Write to Gyro configuration register
	bus.write_byte_data(Device_Address, GYRO_CONFIG, 24)
	
	#Write to interrupt enable register
	bus.write_byte_data(Device_Address, INT_ENABLE, 1)

def read_raw_data(addr):
	#Accelero and Gyro value are 16-bit
        high = bus.read_byte_data(Device_Address, addr)
        low = bus.read_byte_data(Device_Address, addr+1)
    
        #concatenate higher and lower value
        value = ((high << 8) | low)
        
        #to get signed value from mpu6050
        if(value > 32768):
                value = value - 65536
        return value

bus = smbus.SMBus(1) 	# or bus = smbus.SMBus(0) for older version boards
Device_Address = 0x68   # MPU6050 device address
		
MPU_Init()
		
##scope = ['https://spreadsheets.google.com/feeds']
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('mydemoproject.json', scope) ## Temp-3914c1792c0b.json replace Your Json file
gc = gspread.authorize(credentials)

wks = gc.open("DataToSheet").sheet1  ## Temp replace your Work sheet name
##wks = gc.open_by_key("1Ia0IuL5x0OmphS0mOi5LNzI99OQpY6nXMW1mqQyu6to").sheet1  ## Temp replace your Work sheet name
wks.update_acell('A1', "Data from Raspberry-pi/ESP32 to Google Sheet")
wks.update_acell('A2', "By Ankit Maurya")
wks.update_acell('A3', "Time")
wks.update_acell('B3', "Gyro-X")
wks.update_acell('C3', "Gyro-Y")
wks.update_acell('D3', "Gyro-Z")
wks.update_acell('E3', "Accel-X")
wks.update_acell('F3', "Accel-Y")
wks.update_acell('G3', "Accel-Z")

def main():

        while True:
                time = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
                gyro = [read_raw_data(GYRO_XOUT_H), read_raw_data(GYRO_YOUT_H), read_raw_data(GYRO_ZOUT_H)]
				accl = [read_raw_data(ACCEL_XOUT_H),read_raw_data(ACCEL_YOUT_H), read_raw_data(ACCEL_ZOUT_H)]
			   print("Adding row please wait...")

                x = 0
                try:
                        for values in wks.col_values(1):  ## loop count row
                                x = x + 1
                        rowToAdd = [time, gyro[0], gyro[1], gyro[2],accl[0], accl[1], accl[2] ] ## your data want to send
                        wks.resize(x)
                        wks.append_row(rowToAdd)
                        sleep(1)
                except:
                        break;

if __name__ == "__main__":
			main()