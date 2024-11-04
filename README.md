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
1. User Details Changing
2. Import, Export Vault, Encrypted and Decrypted
3. Master Password Changing
4. Email Changing
5. Email Verification
6. Forgot Password
7. Extension
8. Mobile App
9. Password Generator
10. 2FA
11. Auto Fill
12. Password Strength Analysis
13. Secure Notes
14. Emergency Contact Access
15. Password History
16. Biometric Access
17. Offline Access
18. Logs