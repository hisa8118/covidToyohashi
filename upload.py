import pprint
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from pydrive.files import GoogleDriveFile
import yaml
# upload csv file to GoogleDriveFile
with open('settings.yaml') as file:
    config = yaml.safe_load(file)
file_name = config['drive_file_name']
directory_name = config['drive_directory_id']
file_id = config['drive_file_id']

gauth = GoogleAuth()
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)

f = drive.CreateFile({"parents": [{"id": directory_name}],"id":file_id,"title":file_name})
f.SetContentFile('data/dataAll.csv')
f.Upload()
# print(f)
# pprint.pprint(f)