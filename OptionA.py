import os
#import shutil
from ftplib import FTP

#FTP site you want to get files from
FTP_SERVER = "ftp.site.com"
FTP_USERNAME = "usernamehere"
FTP_PASSWORD = "passwordhere"
FTP_DIRECTORY = 'ftpfolderhere'
#FTP site you want to move files to
FTP_SERVER2 = "ftp.site2.com"
FTP_PORT2 = 1234 #remove is port is not required
FTP_USERNAME2 = "domain\\username"
FTP_PASSWORD2 = "passwordhere"
FTP_DIRECTORY2 = 'folder1/folder2'
#Local backup
BACKUP_DIRECTORY = "\\\\servername\\FTP-Archive"


def handleDownload(block):
    file.write(block)
    print(".", end="")

try:
    # Connect to the first FTP server
    with FTP(FTP_SERVER) as ftp:
        ftp.login(FTP_USERNAME, FTP_PASSWORD)
        ftp.cwd(FTP_DIRECTORY)
        files = ftp.nlst()

        # Ensure BACKUP_DIRECTORY exists
        os.makedirs(BACKUP_DIRECTORY, exist_ok=True)

        # Connect to the second FTP server
        with FTP() as ftp2:
            ftp2.connect(FTP_SERVER2, FTP_PORT2)
            ftp2.login(FTP_USERNAME2, FTP_PASSWORD2)
            ftp2.cwd(FTP_DIRECTORY2)

            for filename in files:
                local_path = os.path.join(BACKUP_DIRECTORY, filename)
                # Download the file from the first server
                with open(local_path, 'wb') as file:
                    ftp.retrbinary(f"RETR {filename}", handleDownload)
                
                # Upload the file to the second server
                with open(local_path, 'rb') as file:
                    ftp2.storbinary(f'STOR {filename}', file)
                
                # Delete the file from the first server
                ftp.delete(filename)

            print("Success: Files transferred and archived in BACKUP_DIRECTORY.")
except Exception as e:
    print(f"An error occurred: {e}")
