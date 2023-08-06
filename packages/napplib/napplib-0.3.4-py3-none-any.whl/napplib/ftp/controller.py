import logging, ftplib

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(threadName)-11s %(levelname)-10s %(message)s")

class FTPController:
    
    @classmethod
    def download_ftp(self, host="", login="", password="", path="", 
                port=None, url="", extension="",move_downloaded_files=False):

        connection = ftplib.FTP(host, login, password)
        logging.info(f"Logged into {host} with user {login}")

        list_files = connection.nlst()
        files = list_files.copy()

        for file in files:
            if str(file.split('.')[-1]).lower() in extension:
                logging.info(f'Downloading {file}')
                with open(f'./files/{file}', 'wb') as f:
                    connection.retrbinary(f'RETR {file}', f.write)
            else:
                logging.warning(f'The file {file} has been ignored')
        
        if move_downloaded_files:
            logging.info('Moving files ... ')
            if 'processados' in files:
                files.pop(files.index('processados'))

        connection.close()