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
      
    self.debug = os.getenv("debug", "False")
    if self.debug == "True":
      self.debug = True
    else:
      self.debug = False
    self.secret_key = os.getenv("secret_key", "django-insecure-#s7(mccb@usp4x*%dne+60q7$o61vtkivsua^a(lx9w8vk!w=w")
    self.server_host = os.getenv("server_host", "127.0.0.1")
    self.server_port = int(os.getenv("server_port", "8000"))
    self.client_host = os.getenv("client_host", "127.0.0.1")
    self.client_port = int(os.getenv("client_port", "8080"))
    self.allowed_hosts = os.getenv("allowed_hosts", "*").split(",")
    self.max_retries = int(os.getenv("max_retries", "3"))
    self.api_token = os.getenv("api_token", "")