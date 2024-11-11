import os
from dotenv import load_dotenv

class Config(object):
  def __init__(self, BASE_DIR):
    self.BASE_DIR = BASE_DIR
  
  # Loading Config File
  def readConfig(self):
    try:
      load_dotenv(f'{self.BASE_DIR}/../.env')
    except:
      pass
      
    self.debug = os.getenv("debug")
    if self.debug == "True":
      self.debug = True
    else:
      self.debug = False
    self.secret_key = os.getenv("secret_key")
    self.server_host = os.getenv("server_host")
    self.server_port = int(os.getenv("server_port"))
    self.client_host = os.getenv("client_host")
    self.client_port = int(os.getenv("client_port"))
    self.allowed_hosts = os.getenv("allowed_hosts").split(",")
    self.max_retries = int(os.getenv("max_retries"))
    self.api_token = os.getenv("api_token")