from ftplib import FTP
import time
import os

ftp = FTP('drakeliu.hostedftp.com')   # connect to host, default port

ftp.login("redscare3", "redscare3")

ftp.retrlines('LIST')     # list directory contents 

#with open('falcon0.txt', 'rb') as f:  
    #ftp.storlines('STOR %s' % 'falcon0.txt', f)
	
def clearFile(filename):
	open(filename, 'wb').close()

# realstuff
cleanDB = {'printers.txt', 'users.txt', 'password.txt'}
database = open('database.txt', 'r+b')
password = 'hellosleepwalker'
duckvar = 0
count = 0
while True:
	filesToRead = set(ftp.nlst())
	if cleanDB == filesToRead:
		print('waiting.', end='')
		if count > 500:
			time.sleep(5)
			print('..')
		if count > 100:
			time.sleep(1)
			print('.')
		else:
			print('')
		count += 1
	else:
		ftp.retrbinary('RETR printers.txt', database.write, 1024)
		filesToRead = list(filesToRead - cleanDB)		
		for file in filesToRead:
			clearFile('printers.txt')
			newDB = open('printers.txt', 'wb')
			database = open('database.txt', 'r+b')
			ofile = open(file, 'wb')
			ftp.retrbinary('RETR ' + file, ofile.write, 1024)
			ofile.close()
			ifile = open(file, 'rb')
			currData = ifile.read()
			dorm = currData[:3].decode()
			cnt = 0
			for line in database:
				nln = line.decode()
				nln = nln[:3]
				if nln == dorm:
					val = currData
					print(val)
					newDB.write(val)
				else:
					#print(line)
					newDB.write(line)
			clearFile("database.txt")
			database = open('database.txt', 'r+b')
			newDB.close()
			temp = open('printers.txt', 'rb')
			database.write(temp.read())
			ftp.delete(file)
		try:
			newDB = open('printers.txt', 'rb')
			ftp.delete('printers.txt')
			#os.remove(file)
			ftp.storlines('STOR %s' % 'printers.txt', newDB)
			d = 1/0
		except Exception:
			duckvar = 1
		count = 0
		#replace database with newDB on server