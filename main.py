import paramiko
import os
from dotenv import load_dotenv

class Server:
    def __init__(self):
        load_dotenv()
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(os.getenv("server_ip"), port=22, username=os.getenv("user"), password=os.getenv("password"))
    
    @property
    def schedule_task(self):
        self.client.exec_command(f"nmap -p- {os.getenv("server_ip")} >> nmap.txt")
