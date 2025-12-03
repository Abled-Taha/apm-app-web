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
3. Rename ".env.example""file to ".env"
4. Open a terminal in "./apm-app-web"
5. Run ```pip install -r ./requirements.txt ; cd ./client ; python manage.py collectstatic ; cd .. ; python main.py run-client```
6. Visit http://127.0.0.1:8080 and see it running

# Todo
1. Support BitWarden Imports
2. Extension
3. Mobile App
4. 2FA
5. Auto Fill
6. Emergency Contact Access
7. Password History
8. Biometric Access
9. Offline Access