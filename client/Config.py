import os, json
from dotenv import load_dotenv

class Config(object):
  def __init__(self, BASE_DIR):
    self.BASE_DIR = BASE_DIR
  
  # Loading Config File
  def readConfig(self):
    try:
      load_dotenv(f'{self.BASE_DIR}/../.env')
    except:
      print("Warning: .env File Not Found! Trying to load default session values")
      pass
    try:
      with open(f'{self.BASE_DIR}/../config.json', 'r') as f:
        self.config = json.load(f)
    except:
      raise Exception("Critical: Config File Not Found!")
      
    self.secret_key = os.getenv("secret_key", "django-insecure-#s7(mccb@usp4x*%dne+60q7$o61vtkivsua^a(lx9w8vk!w=w")
    self.api_token = os.getenv("api_token", "")

    self.debug = self.config["debug"]
    self.server_host = self.config["server_host"]
    self.server_port = self.config["server_port"]
    self.client_host = self.config["client_host"]
    self.client_port = self.config["client_port"]
    self.allowed_hosts = self.config["allowed_hosts"]
    self.max_retries = self.config["max_retries"]