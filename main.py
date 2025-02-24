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
    def server_port_lister(self):
        """
        Executes an Nmap scan on the target server and saves the output to a .txt file.

        This function runs the Nmap command with the '-p-' option (scanning all ports)
        on the specified server IP and appends the results to 'nmap.txt' on the remote server.

        """
        server_ip = os.getenv("server_ip")
        server_path = os.getenv("server_path")

        if server_ip and server_path:
            self.client.exec_command(f"nmap -p- {server_ip} >> {server_path}/nmap.txt")
        else:
            print("Error: 'server_ip' enviroment variable is not set or the 'server_path' is not set")

    @property
    def download_file(self):
        """
        Download the nmap.txt from the remote server and save the file on 'local_path' locally
        """
        sftp = self.client.open_sftp()
        local_path = os.getenv("local_path")
        server_path = os.getenv("server_path")
        if local_path:
            sftp.get(f"{server_path}/nmap.txt", f"{local_path}/nmap.txt")

    @property
    def clean_data(self):
        """
        This function will read the nmap.txt file and clean the datas for create a .xlsx file utilizing pandas
        """

        with open(f"{os.getenv("local_path")}/nmap.txt", mode="r") as file:
            lines = file.read()
            datas = lines.split("(conn-refused)")[1]
            datas = datas.split("Nmap done")[0].split()
            count = 0
            clean_datas = [datas[:3]]
            del datas[:3]
            for num in range(3, len(datas) + 1, 3):
                clean_datas.append(datas[count:num])
                count = num

        def excel_files(df_data: list[list]):
            """
            This nested function will create the .xlsx file utilizing pandas

            df_data >>> list
            """
            df = pd.DataFrame(df_data)
            df.to_excel("server_listen_ports.xlsx")

        excel_files(clean_datas)

    def main(self):
        self.server_port_lister
        self.server_port_lister
        self.download_file
        self.clean_data

