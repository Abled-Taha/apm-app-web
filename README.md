## APM, The Password Manager You Need

# Pre-requisites
1. Downloading & Installing [APM-SERVER](https://github.com/Abled-Taha/apm-server)

# Setting up APM-APP-WEB
1. Clone the repository
2. Open the directory
3. Make ".env" file
4. Set all the variables in that file from the "config.json" file
5. Open a terminal in "./apm-app-web"
6. Run ```pip install -r ./requirements.txt ; cd ./client ; python manage.py collectstatic ; cd .. ; python main.py```
7. Visit http://127.0.0.1:8080 and see it running

### Todo
1. Import, Export Vault, Encrypted and Decrypted
2. Master Password Changing
3. Email Verification
4. Forgot Password
5. Extension
6. Mobile App
7. Password Generator Config
8. 2FA
9.  Auto Fill
10. Password Strength Analysis
11. Emergency Contact Access
12. Password History
13. Biometric Access
14. Offline Access
15. Logs