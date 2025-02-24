import paramiko
import os
from dotenv import load_dotenv
import pandas as pd

class Server:
    def __init__(self):
        load_dotenv()
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(os.getenv("server_ip"), port=22, username=os.getenv("user"), password=os.getenv("password"))
    
    @property
    def schedule_task(self):
        self.client.exec_command(f"nmap -p- {os.getenv("server_ip")} >> nmap.txt")

    @property
    def download_file(self):
        sftp = self.client.open_sftp()
        sftp.get("nmap.txt", "nmap.txt")

    @property
    def clean_data(self):
        with open("nmap.txt", mode="r") as file:
            lines = file.read()
            datas = lines.split("(conn-refused)")[1]
            datas = datas.split("Nmap done")[0].split()
            count = 0
            df_data = [datas[:3]]
            del datas[:3]
            for num in range(3, len(datas) + 1, 3):
                df_data.append(datas[count:num])
                count = num
     
    @property
    def clean_data(self):
        with open("nmap.txt", mode="r") as file:
            lines = file.read()
            datas = lines.split("(conn-refused)")[1]
            datas = datas.split("Nmap done")[0].split()
            count = 0
            clean_datas = [datas[:3]]
            del datas[:3]
            for num in range(3, len(datas) + 1, 3):
                clean_datas.append(datas[count:num])
                count = num

        def excel_files(df_data):

            df = pd.DataFrame(df_data)
            df.to_excel("server_listen_ports.xlsx")

        excel_files(clean_datas)

    def main(self):
        
        self.schedule_task
        self.download_file
        self.clean_data

