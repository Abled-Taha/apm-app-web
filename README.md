## APM, The Password Manager You Need

# About
The Project [APM-SERVER](https://github.com/Abled-Taha/apm-server),
[APM-APP](https://github.com/Abled-Taha/apm-app) & [APM-APP-WEB](https://github.com/Abled-Taha/apm-app-web) are of a larger project known as **APM** which serves to be a Password Manager.
None of these repositores or single projects can and should be used just on their own unless stated otherwise. They are meant to be used together.

# How To Get Working
## Pre-requisites
1. Downloading & Installing [APM-SERVER](https://github.com/Abled-Taha/apm-server)

## Setting up APM-APP-WEB
1. Clone the repository
2. Open the directory
3. Make ".env" file
4. Set all the variables in that file from the "config.json" file
5. Open a terminal in "./apm-app-web"
6. Run ```pip install -r ./requirements.txt ; cd ./client ; python manage.py collectstatic ; cd .. ; python main.py run-client```
7. Visit http://127.0.0.1:8080 and see it running

# Todo
1. Support BitWarden Imports
2. Forgot Password
3. Extension
4. Mobile App
5. 2FA
6.  Auto Fill
7.  Emergency Contact Access
8.  Password History
9.  Biometric Access
10. Offline Access
11. Logs