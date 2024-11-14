## APM, The Password Manager You Need

# Pre-requisites
1. Downloading & Installing [APM-SERVER](https://github.com/Abled-Taha/apm-server)

# Setting up APM-APP-WEB
1. Clone the repository
2. Open the directory
3. Make ".env" file
4. Set all the variables in that file from the "config.json" file
5. Open a terminal in "./apm-app-web"
6. Run ```pip install -r ./requirements.txt ; cd ./client ; python manage.py collectstatic ; cd .. ; python main.py run-client```
7. Visit http://127.0.0.1:8080 and see it running

### Todo
1. Support BitWarden Imports
2. Master Password Changing
3. Forgot Password
4. Extension
5. Mobile App
6. 2FA
7.  Auto Fill
8.  Password Strength Analysis
9.  Emergency Contact Access
10. Password History
11. Biometric Access
12. Offline Access
13. Logs