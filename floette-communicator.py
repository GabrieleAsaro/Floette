import serial
import hashlib
import os.path
import time
import requests
import json

port = serial.Serial('YOUR_PORT', 9600)
path = "YOUR_DIRECTORY"
already_scanned = []
index = 0

while os.path.exists(path):
    directories = os.listdir( path )
    for file in directories:
        time.sleep(1)
        new_file = path + file
        if os.path.isfile(new_file):
            with open(new_file, "rb") as f:
                file_hash = hashlib.md5()
                while chunk := f.read(8192):
                    file_hash.update(chunk)

                if file_hash.hexdigest() not in already_scanned :
                    request = requests.get('https://www.virustotal.com/vtapi/v2/file/report?apikey=YOUR_API&resource=' + file_hash.hexdigest())
                    virustotal_content = json.loads(request.content)
                    index += 1
                    already_scanned.insert(index, file_hash.hexdigest())

                    if virustotal_content['response_code'] == 0 :
                        print('Cannot retrieve infos about the file.')
                    else:
                        total_detections = sum(1 for antivirus in virustotal_content['scans'] if virustotal_content['scans'][antivirus]['detected'])
                        if total_detections > 15:
                            print('detected')
                            port.write('detected'.encode())
                        else:
                            print("legit")