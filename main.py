from labpack.storage.google.drive import driveClient

import RPi.GPIO as GPIO  # Import Raspberry Pi GPIO library
from time import sleep  # Import the sleep function from the time module
import os
import time
import datetime
import urllib2

def generate():
    GPIO.setwarnings(False)  # Ignore warning for now
    GPIO.setmode(GPIO.BOARD)  # Use physical pin numbering

    LEDPIN = 8
    MAGNETPIN = 7
    SWITCHPIN = 12

    GPIO.setup(LEDPIN, GPIO.OUT, initial=GPIO.LOW)  # Set pin 8 to be an output pin and set initial value to low (off)
    GPIO.setup(MAGNETPIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # magnet switch. Default is CLOSED
    GPIO.setup(SWITCHPIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # tactile switch. Default is OPEN

    # GPIO.setup(8, GPIO.OUT, initial=GPIO.LOW) # Set pin 8 to be an output pin and set initial value to low (off)
    # GPIO.setup(7, GPIO.IN, pull_up_down = GPIO.PUD_UP) #magnet switch. Default is CLOSED
    # GPIO.setup(12, GPIO.IN, pull_up_down = GPIO.PUD_UP) #tactile switch. Default is OPEN


    lastSensorReading = 1  # use this to stop multiple recordings for the same event
    lastButtonReading = 0
    buttonPushed = 0  # make sure button push isn't registerd multiple times
    stringStatus = "NA"  #

    # on start up create a .csv file with time stamp(so you know how long it's been running)
    now = datetime.datetime.now()  # get time
    namestr = now.strftime("%Y-%m-%d_%H-%M-%S")
    filename = '/home/pi/Desktop/data/' + namestr + '.csv'
    f = open(filename, 'a+')
    if os.stat(filename).st_size == 0:
        f.write('Date,Time,DoorStatus\r\n')

    # input first reading - is door open or closed?
    if GPIO.input(MAGNETPIN) == 1:  # Reading is HIGH (1), so open
        stringStatus = "DOOR-OPEN"
    else:
        stringStatus = "DOOR-CLOSED"

    f.write('{0},{1},{2}%\r\n'.format(time.strftime('%m/%d/%y'), time.strftime('%H:%M'), stringStatus))
    f.flush()
    f.close()  # close the file until time to write again

    # Declare File name
    # file_name = '{}.{}'.format(time.strftime('%m.%d.%y'), time.strftime('%H.%M'))

    # Run forever to take the rest of the readings
    while True:
        sleep(0.5)  # Sleep for 0.5 seconds
        if buttonPushed == 0:  # button has not been pushed
            # check if button is pushed
            if GPIO.input(SWITCHPIN) == 1:  # Reading is HIGH (1), so button is NOT pushed
                buttonPushed = 0
            else:
                if lastButtonReading != GPIO.input(SWITCHPIN):
                    # stop the bouncing effect so button pushed is registered ONCE
                    buttonPushed = 1
            lastButtonReading = GPIO.input(SWITCHPIN)  # update it so new reading is saved
            # check if sensor status has changed
            if GPIO.input(MAGNETPIN) != lastSensorReading:  # current reading does not equal last reading
                if GPIO.input(MAGNETPIN) == 1:  # Reading is HIGH (1), so open
                    stringStatus = "DOOR-OPEN"
                    # print("Switch Open!")
                    GPIO.output(LEDPIN, GPIO.HIGH)  # Turn on LED for testing
                else:
                    stringStatus = "DOOR-CLOSED"
                    # print("Switch Closed!")
                    GPIO.output(LEDPIN, GPIO.LOW)  # Turn off LED
                lastSensorReading = GPIO.input(MAGNETPIN)  # update it so new reading is saved
                now = datetime.datetime.now()  # get time
                print(now)


                # append the csv file
                with open(filename, "a") as f:
                    f.write('{0},{1},{2}%\r\n'.format(time.strftime('%m/%d/%y'), time.strftime('%H:%M'), stringStatus))
                    # don't need to flush & close here because of the 'with'

            # else GPIO.input(7) == lastSensorReading:  # current reading equals last reading

        else:  # button pushed, so file is being read to USB.
            # write to USB
            print("Button pushed!")

            buttonPushed = 0
            sleep(1)
            # set buttn push to 0
        print("******************")

'''
    Access Token is permanent, so be careful where you use it!
    file_path = filename
    drive_space = 'drive'
'''
def migrate(file_path, access_token, drive_space='drive'):

    '''
        a method to save a posix file architecture to google drive

    NOTE:   to write to a google drive account using a non-approved app,
            the oauth2 grantee account must also join this google group
            https://groups.google.com/forum/#!forum/risky-access-by-unreviewed-apps

    :param file_path: string with path to local file
    :param access_token: string with oauth2 access token grant to write to google drive
    :param drive_space: string with name of space to write to (drive, appDataFolder, photos)
    :return: string with id of file on google drive
    '''

# construct drive client
    import httplib2
    from googleapiclient import discovery
    from oauth2client.client import AccessTokenCredentials
    google_credentials = AccessTokenCredentials(access_token, 'my-user-agent/1.0')
    google_http = httplib2.Http()
    google_http = google_credentials.authorize(google_http)
    google_drive = discovery.build('drive', 'v3', http=google_http)
    drive_client = google_drive.files()

# prepare file body
    from googleapiclient.http import MediaFileUpload
    media_body = MediaFileUpload(filename=file_path, resumable=True)

# determine file modified time
    import os
    from datetime import datetime
    modified_epoch = os.path.getmtime(file_path)
    modified_time = datetime.utcfromtimestamp(modified_epoch).isoformat()

# determine path segments
    path_segments = file_path.split(os.sep)

# construct upload kwargs
    create_kwargs = {
        'body': {
            'name': path_segments.pop(),
            'modifiedTime': modified_time
        },
        'media_body': media_body,
        'fields': 'id'
    }

# walk through parent directories
    parent_id = ''
    if path_segments:

    # construct query and creation arguments
        walk_folders = True
        folder_kwargs = {
            'body': {
                'name': '',
                'mimeType' : 'application/vnd.google-apps.folder'
            },
            'fields': 'id'
        }
        query_kwargs = {
            'spaces': drive_space,
            'fields': 'files(id, parents)'
        }
        while path_segments:
            folder_name = path_segments.pop(0)
            folder_kwargs['body']['name'] = folder_name

    # search for folder id in existing hierarchy
            if walk_folders:
                walk_query = "name = '%s'" % folder_name
                if parent_id:
                    walk_query += "and '%s' in parents" % parent_id
                query_kwargs['q'] = walk_query
                response = drive_client.list(**query_kwargs).execute()
                file_list = response.get('files', [])
            else:
                file_list = []
            if file_list:
                parent_id = file_list[0].get('id')

    # or create folder
    # https://developers.google.com/drive/v3/web/folder
            else:
                if not parent_id:
                    if drive_space == 'appDataFolder':
                        folder_kwargs['body']['parents'] = [ drive_space ]
                    else:
                        del folder_kwargs['body']['parents']
                else:
                    folder_kwargs['body']['parents'] = [parent_id]
                response = drive_client.create(**folder_kwargs).execute()
                parent_id = response.get('id')
                walk_folders = False

# add parent id to file creation kwargs
    if parent_id:
        create_kwargs['body']['parents'] = [parent_id]
    elif drive_space == 'appDataFolder':
        create_kwargs['body']['parents'] = [drive_space]

# send create request
    file = drive_client.create(**create_kwargs).execute()
    file_id = file.get('id')

    return file_id


# Output
file_name = generate()
access_token = "#########"
migrate(file_name,access_token)