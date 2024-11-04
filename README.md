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
3. Email Changing
4. Email Verification
5. Forgot Password
6. Extension
7. Mobile App
8. Password Generator Config
9. 2FA
10. Auto Fill
11. Password Strength Analysis
12. Secure Notes
13. Emergency Contact Access
14. Password History
15. Biometric Access
16. Offline Access
17. Logs