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
2. Forgot Password
3. Extension
4. Mobile App
5. 2FA
6.  Auto Fill
7.  Password Strength Analysis
8.  Emergency Contact Access
9.  Password History
10. Biometric Access
11. Offline Access
12. Logs