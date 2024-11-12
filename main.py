import sys

# Non-Argument function
def setupConfig():
    from client.Config import Config as ConfigClass
    
    # Setting up Config
    global ConfigObj
    BASE_DIR = "./client"
    ConfigObj = ConfigClass(BASE_DIR)
    ConfigObj.readConfig()
  
  

# Argument function
def run_client():
    import os, subprocess

    # Running wsgi server
    setupConfig()
    
    os.chdir("./client")
    subprocess.call(["waitress-serve", f"--listen={ConfigObj.client_host}:{ConfigObj.client_port}", "client.wsgi:application"])

      
def help():
  print("Use run-client flag to run the client")
  print("Use help flag to get help")



if __name__ == "__main__":
    try:
      if sys.argv[1] == "run-client":
        run_client()
      elif sys.argv[1] == "help":
        help()
      else:
          print("Invalid arguments")
    except Exception as e:
      print(e)
      print("Provide a valid argument")
      print("Use help for more information")