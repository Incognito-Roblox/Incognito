import os
import requests
import hashlib
import zipfile
import subprocess
import uuid
import wmi
import misc.app_info as IncognitoApp

class SystemInfo:
    def __init__(self):
        self.wmi = wmi.WMI()
    
    def returnSerials(self):
        macAddress = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(0, 2 * 6, 8)][::-1])
        cpuID = subprocess.check_output("wmic cpu get ProcessorId").decode().strip().split('\n')[1]
        motherboardSerial = self.wmi.Win32_BaseBoard()[0].SerialNumber
        diskSerial = self.wmi.Win32_DiskDrive()[0].SerialNumber
        biosSerial = self.wmi.Win32_BIOS()[0].SerialNumber
        windowsID = self.wmi.Win32_OperatingSystem()[0].SerialNumber
        sysUUID = subprocess.check_output("wmic csproduct get UUID").decode().strip().split('\n')[1]
        gpuID = self.wmi.Win32_VideoController()[0].DeviceID
        windowsUserID = os.getlogin()
        networkCardIDs = [interface.MACAddress for interface in self.wmi.Win32_NetworkAdapter() if interface.MACAddress]

        return macAddress, cpuID, motherboardSerial, diskSerial, biosSerial, windowsID, sysUUID, gpuID, windowsUserID, networkCardIDs

    def hashSerials(self):
        serials = self.returnSerials()
        hash = hashlib.sha256(''.join(str(serial).replace(' ', '') for serial in serials).encode()).hexdigest()
        return hash

class Bootstrapper:
    def __init__(self):
        self.baseURL = 'http://127.0.0.1:8000/api' # temp: use 'fastapi dev main.py' to run api in dev mode ( we will replace this once we get VPS )
        self.currentVersion = IncognitoApp.VERSION
        self.cwd = os.getcwd()

    def calculateHash(self, filePath):
        hash256 = hashlib.sha256()
        with open(filePath, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                hash256.update(chunk)
        return hash256.hexdigest()

    def ensureDirectory(self):
        folders = ['workspace', 'scripts', 'bin', 'autoexecute']

        for folder in folders:
            folderPath = os.path.join(self.cwd, folder)

            if not os.path.exists(folderPath):
                os.makedirs(folderPath)

    def checkUpdates(self):
        statusURL = requests.get(self.baseURL + '/status')

        if statusURL.status_code == 200:
            data = statusURL.json()

            apiStatus = data.get('status')
            latestVersion = data.get('version')

            if apiStatus and latestVersion:
                if apiStatus == "True":
                    if latestVersion == self.currentVersion:
                        return 'Files are up to date!'
                    else:
                        downloadURL = requests.get(self.baseURL + '/download', stream=True, headers={'Content-Type': 'application/zip', 'x-secret-key': 'QfTGYQU8WiR0OTNbCBkRoYP2cMTuYGwF'})

                        if downloadURL.status_code == 200:
                            updateFilePath = os.path.join(self.cwd, 'update.zip')

                            with open(updateFilePath, 'wb') as file:
                                for chunk in downloadURL.iter_content(chunk_size=8192):
                                    file.write(chunk)

                            fileHash = downloadURL.headers.get('File-Hash')
                            calculatedHash = self.calculateHash(updateFilePath)

                            if fileHash == calculatedHash:
                                try:
                                    with zipfile.ZipFile(updateFilePath, 'r') as zipRef:
                                        zipRef.extractall(self.cwd)
                                except Exception as e:
                                    os.remove(updateFilePath)
                                    return 'Failed to extract update.'
                                finally:
                                    if os.path.exists(updateFilePath):
                                        os.remove(updateFilePath)

                                return 'File updated successfully to:'
                            else:
                                os.remove(updateFilePath)
                                return 'File hash mismatch.'
                        else:
                            return 'Failed to contact download endpoint.'
                else:
                    return 'Incognito is currently down!'
            else:
                return 'Failed to get status or latest version.'
        else:
            return 'Failed to contact version endpoint.'

    def checkKey(self):
        """
        TODO::

        [?] check if file storing key is in /bin folder 
            [NO] prompt them for the linkvertise process then store key they enter in bin folder
            [YES] move to next step

        [?] check if the key is still valid from time it was registered to currentime
            [NO] delete key from file and prompt for linkvertise
            [YES] move to next step

        [?] calculate device hash and check it matches with one stored in database
            [NO] accuse them of key sharing and bomb their pc
            [YES] launch
        """ 

        

    def run(self):
        self.ensureDirectory()
        message = self.checkUpdates()

        return message

