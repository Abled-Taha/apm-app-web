import json

class Config(object):
  def __init__(self, BASE_DIR):
    self.BASE_DIR = BASE_DIR
  
  # Loading Config File
  def readConfig(self):
    with open(f'{self.BASE_DIR}/../config.json', 'r') as f:
      self.config = json.load(f)
      
      self.server_host = self.config["server_host"]
      self.server_port = self.config["server_port"]
      self.secret_key = self.config["secret_key"]
      self.debug = self.config["debug"]
      self.client_host = self.config["client_host"]
      self.client_port = self.config["client_port"]
      self.allowed_hosts = self.config["allowed_hosts"]
      self.max_retries = self.config["max_retries"]