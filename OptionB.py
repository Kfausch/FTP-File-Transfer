import os
import shutil
from ftplib import FTP

#Site 1 will be receiving files
FTP_SERVER = "ftp.site1.com"
FTP_USERNAME = "usernamehere"
FTP_PASSWORD = "passwordhere"
FTP_DIRECTORY = 'diretoryhere'
#Site 2 will start with the files
FTP_SERVER2 = "ftp.site2.com"
FTP_PORT2 = 1234 #remove if port is not required
FTP_USERNAME2 = "domain\\username"
FTP_PASSWORD2 = "passwordhere"
FTP_DIRECTORY2 = 'directory1/folderA/subfolder'
#Local backup
BACKUP_DIRECTORY = "\\\\server\\Archive"


def handleDownload(block):
    file.write(block)
    print(".", end="")

#fuction to check connection status
def check_ftp_connection(ftp):
    try:
        ftp.voidcmd("NOOP")
        return True  # The connection is still active
    except:
        return False  # The connection has been lost

#function that keeps you connected
def reconnect_ftp_server(ftp_details):
    try:
        ftp_details['ftp_object'].quit()
    except:
        pass
    ftp_details['ftp_object'] = FTP()
    ftp_details['ftp_object'].connect(ftp_details['server'], ftp_details['port'])
    ftp_details['ftp_object'].login(ftp_details['username'], ftp_details['password'])
    ftp_details['ftp_object'].cwd(ftp_details['directory'])

# Define FTP connection details for FTP_SERVER2
ftp_details_ftp2 = {
    'ftp_object': FTP(),
    'server': FTP_SERVER2,
    'port': FTP_PORT2,
    'username': FTP_USERNAME2,
    'password': FTP_PASSWORD2,
    'directory': FTP_DIRECTORY2,
}

# Connect to FTP_SERVER2
reconnect_ftp_server(ftp_details_ftp2)
ftp2 = ftp_details_ftp2['ftp_object']

try:
    os.makedirs(BACKUP_DIRECTORY, exist_ok=True)
    entries = ftp2.nlst()

    # Filter out specific known placeholders or directories
    files = [f for f in entries if f.lower().endswith('.edi')]

    with FTP(FTP_SERVER) as ftp:
        ftp.login(FTP_USERNAME, FTP_PASSWORD)
        ftp.cwd(FTP_DIRECTORY)

        for filename in files:
            local_path = os.path.join(BACKUP_DIRECTORY, filename)

            # Download the file
            with open(local_path, 'wb') as file:
                ftp2.retrbinary(f"RETR {filename}", handleDownload)

            # Check connection and reconnect if necessary
            if not check_ftp_connection(ftp2):
                print(f"Reconnecting to FTP_SERVER2 to delete {filename}.")
                reconnect_ftp_server(ftp_details_ftp2)
                ftp2 = ftp_details_ftp2['ftp_object']

            # Upload the file
            with open(local_path, 'rb') as file:
                ftp.storbinary(f"STOR {filename}", file)

            # Delete the file
            ftp2.delete(filename)

  #Can remove after testing or you can comment it out for troubleshooting later
    print("Success: Files transferred.")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    # Ensure the connection is closed properly
    try:
        ftp2.quit()
    except:
        pass
