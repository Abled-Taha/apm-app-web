import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def encrypt(salt, password, masterPassword):
  kdf = PBKDF2HMAC(
      algorithm=hashes.SHA256(),
      length=32,
      salt=salt.encode(),
      iterations=390000,
  )
  password = password.encode()
  masterPassword = masterPassword.encode()
  key = base64.urlsafe_b64encode(kdf.derive(masterPassword))
  f = Fernet(key)
  passwordEncrypt = f.encrypt(password)

  return str(passwordEncrypt)

def decryptor(salt, masterPassword, passwordEncrypt):
  kdf = PBKDF2HMAC(
      algorithm=hashes.SHA256(),
      length=32,
      salt=salt.encode(),
      iterations=390000,
  )
  masterPassword = masterPassword.encode()
  key = base64.urlsafe_b64encode(kdf.derive(masterPassword))
  f = Fernet(key)
  passwordEncrypt = passwordEncrypt.removeprefix("b").encode()
  passwordDecrypt = f.decrypt(passwordEncrypt)
  return passwordDecrypt.decode('utf-8')