import threading, json, base64, datetime
from django.shortcuts import redirect, render
from django.contrib import messages
from django.http.response import HttpResponse, JsonResponse
from .settings import ConfigObj, LogHandlerObj
from . import forms, encryptor
from .Functions import Functions

base_url = f"http://{ConfigObj.server_host}:{ConfigObj.server_port}"
functions = Functions(ConfigObj)

def home(request):
  if request.method != "GET":
    return(JsonResponse({"errorCode":1, "errorMessage":"Method not Allowed."}))
  else:
    if request.COOKIES.get("sessionId") is None:
      return redirect("signin", permanent=True)
    else:
      return redirect("vault", permanent=True)



def signin(request):
  if request.method == "POST":
    form = forms.Signin(request.POST)
    if form.is_valid():
      if form.cleaned_data["sessionName"] == "":
        form.cleaned_data["sessionName"] = functions.get_client_ip(request)
      data = {
        "email":form.cleaned_data["email"],
        "password":form.cleaned_data["password"],
        "sessionName":form.cleaned_data["sessionName"]
      }
      url = f'{base_url}/signin/'

      success, dict_response = functions.sendRequestPost(url, data)
      if success:
        response = redirect("home", permanent=True)
        cookies = [
          {
            "name": "email",
            "value": data["email"],
          },
          {
            "name": "sessionId",
            "value": dict_response["sessionId"],
          },
          {
            "name": "password",
            "value": data["password"],
          },
          {
            "name": "salt",
            "value": dict_response["salt"],
          },
          {
            "name": "username",
            "value": dict_response["username"],
          },
          {
            "name": "pGConfigLength",
            "value": 16,
          },
          {
            "name": "pGConfigCapitalLetters",
            "value": True,
          },
          {
            "name": "pGConfigSmallLetters",
            "value": True,
          },
          {
            "name": "pGConfigNumbers",
            "value": True,
          },
          {
            "name": "pGConfigSymbols",
            "value": True,
          }
        ]
        response = functions.set_cookie(cookies, response)

        LogHandlerObj.write(f"Signin | OK | {data['email']} | {functions.get_client_ip(request)}")
        return response
      elif success == None:
        response = redirect("signin", permanent=True)
        messages.error(request, "Connection Error")

        LogHandlerObj.write(f"Signin | FAILED | {data['email']} | {functions.get_client_ip(request)} | Connection Error")
        return response
      else:
        response = redirect("signin", permanent=True)
        messages.error(request, dict_response["errorMessage"])
        
        LogHandlerObj.write(f"Signin | FAILED | {data['email']} | {functions.get_client_ip(request)} | {dict_response['errorMessage']}")
        return response
    else:
      response = redirect("signin", permanent=True)
      messages.error(request, "Invalid Form")
      return response

  else:
    if request.COOKIES.get("sessionId") != None:
      return(redirect("vault", permanent=True))
    else:
      form = forms.Signin()
      return(render(request, "signin/index.html", {'title':'APM - Signin','form':form}))



def signup(request):
  if request.method == "POST":
    form = forms.Signup(request.POST)
    if form.is_valid():
      data = {
        "email":form.cleaned_data["email"],
        "username":form.cleaned_data["username"],
        "password":form.cleaned_data["password"],
        "rePassword":form.cleaned_data["rePassword"]
      }
      url = f'{base_url}/signup/'

      success, dict_response = functions.sendRequestPost(url, data)
      if success:
        # response = redirect("signin", permanent=True)
        messages.success(request, "Account Created")

        LogHandlerObj.write(f"Signup | OK | {data['email']} | {functions.get_client_ip(request)}")
        # return response
        return(signin(request))
      elif success == None:
        response = redirect("signup", permanent=True)
        messages.error(request, "Connection Error")

        LogHandlerObj.write(f"Signup | FAILED | {data['email']} | {functions.get_client_ip(request)} | Connection Error")
        return response
      else:
        response = redirect("signup", permanent=True)
        messages.error(request, dict_response["errorMessage"])

        LogHandlerObj.write(f"Signup | FAILED | {data['email']} | {functions.get_client_ip(request)} | {dict_response['errorMessage']}")
        return response
    else:
      response = redirect("signup", permanent=True)
      messages.error(request, "Invalid Form")
      return response

  else:
    if request.COOKIES.get("sessionId") != None:
      return(redirect("vault", permanent=True))
    else:
      form = forms.Signup()
      return(render(request, "signup/index.html", {'title':'APM - Signup','form':form}))



def vault(request):
  if request.method != "GET":
    return(JsonResponse({"errorCode":1, "errorMessage":"Method not Allowed."}))
  else:
    if request.COOKIES.get("sessionId") == None:
      return redirect("signin")
    else:
      url = f'{base_url}/vault-get/'
      data = {
        "email":request.COOKIES.get("email"),
        "sessionId":request.COOKIES.get("sessionId")
      }
      success, dict_response = functions.sendRequestPost(url, data)

      if success:
        salt = request.COOKIES.get("salt")
        password = request.COOKIES.get("password")

        def handle_item(item):
          item["note"] = encryptor.decrypt(salt, password, item["note"])
          item["password"] = encryptor.decrypt(salt, password, item["password"])

        threads = []
        for value in dict_response["passwords"]:
          t = threading.Thread(target=handle_item, args=(value,))
          t.start()
          threads.append(t)

        for t in threads:
          t.join()

        url = f'{base_url}/session-get/'
        success, dict_response1 = functions.sendRequestPost(url, data)
        if success:
          sessions = dict_response1["sessionIds"]
          url = f'{base_url}/pp-get/'
          data["username"] = request.COOKIES.get("username")
          success, dict_response2 = functions.sendRequestPost(url, data)
          if success:
            pp = dict_response2["pp"].removeprefix("b'").removesuffix("'")
          else:
            pp = ""
        else:
          sessions = []
        return render(request, "vault/index.html", {'title':'APM - Vault', 'passwords':dict_response["passwords"], 'formVaultDelete':forms.VaultDelete(), 'formVaultNew':forms.VaultNew(), 'formVaultEdit':forms.VaultEdit(), 'formSessionEdit':forms.SessionEdit(), 'formSessionDelete':forms.SessionDelete(), 'formImageUpdate':forms.ImageUpdate(), 'formPGConfig':forms.PGConfig(), 'formImportVault':forms.ImportVault(), 'sessions':sessions, 'pp':pp})
      elif success == None:
        response = redirect("vault", permanent=True)
        messages.error(request, "Connection Error")
        return response
      else:
        response = redirect("signin", permanent=True)
        messages.error(request, dict_response["errorMessage"])
        cookies = [
          "email",
          "password",
          "salt",
          "sessionId"
        ]
        response = functions.delete_cookie(cookies, response)
        return response
      


def vaultNew(request):
  if request.method == "POST":
    form = forms.VaultNew(request.POST)
    if form.is_valid():

      if form.cleaned_data.get("name") == None:
        form.cleaned_data["name"] = ""
      if form.cleaned_data.get("username") == None:
        form.cleaned_data["username"] = ""
      if form.cleaned_data.get("password") == None:
        form.cleaned_data["password"] = ""
      if form.cleaned_data.get("url") == None:
        form.cleaned_data["url"] = ""
      if form.cleaned_data.get("note") == None:
        form.cleaned_data["note"] = ""

      passwordEncrypt = encryptor.encrypt(request.COOKIES.get("salt"), form.cleaned_data["password"], request.COOKIES.get("password"))
      noteEncrypt = encryptor.encrypt(request.COOKIES.get("salt"), form.cleaned_data["note"], request.COOKIES.get("password"))
      data = {
        "email":request.COOKIES.get("email"),
        "sessionId":request.COOKIES.get("sessionId"),
        "name":form.cleaned_data["name"],
        "username":form.cleaned_data["username"],
        "password":passwordEncrypt,
        "url":form.cleaned_data["url"],
        "note":noteEncrypt
      }
      url = f'{base_url}/vault-new/'
      success, dict_response = functions.sendRequestPost(url, data)

      if success:
        response = redirect("vault", permanent=True)
        messages.success(request, "Password Added")
        return response
      elif success == None:
        response = redirect("vault", permanent=True)
        messages.error(request, "Connection Error")
        return response
      else:
        response = redirect("vault", permanent=True)
        messages.error(request, dict_response["errorMessage"])
        return response
    else:
      response = redirect("vault", permanent=True)
      messages.error(request, "Invalid Form")
      return response

  else:
    # form = forms.VaultNew()
    # return(render(request, "vault/vaultNew.html", {'title':'APM - New','form':form}))
    return HttpResponse("method not allowed")



def vaultEdit(request):
  if request.method == "POST":
    form = forms.VaultEdit(request.POST)
    if form.is_valid():

      if form.cleaned_data.get("newName") == None:
        form.cleaned_data["newName"] = ""
      if form.cleaned_data.get("newUsername") == None:
        form.cleaned_data["newUsername"] = ""
      if form.cleaned_data.get("newPassword") == None:
        form.cleaned_data["newPassword"] = ""
      if form.cleaned_data.get("newUrl") == None:
        form.cleaned_data["newUrl"] = ""
      if form.cleaned_data.get("newNote") == None:
        form.cleaned_data["newNote"] = ""

      passwordEncrypt = encryptor.encrypt(request.COOKIES.get("salt"), form.cleaned_data["newPassword"], request.COOKIES.get("password"))
      noteEncrypt = encryptor.encrypt(request.COOKIES.get("salt"), form.cleaned_data["newNote"], request.COOKIES.get("password"))
      data = {
        "email":request.COOKIES.get("email"),
        "sessionId":request.COOKIES.get("sessionId"),
        "newName":form.cleaned_data["newName"],
        "newUsername":form.cleaned_data["newUsername"],
        "newPassword":passwordEncrypt,
        "newUrl":form.cleaned_data["newUrl"],
        "newNote":noteEncrypt,
        "id":form.cleaned_data["id"]
      }
      url = f'{base_url}/vault-edit/'

      success, dict_response = functions.sendRequestPost(url, data)
      if success:
        response = redirect("vault", permanent=True)
        messages.success(request, "Password Saved")
        return response
      elif success == None:
        response = redirect("vault", permanent=True)
        messages.error(request, "Connection Error")
        return response
      else:
        response = redirect("vault", permanent=True)
        messages.error(request, dict_response["errorMessage"])
        return response
    else:
      response = redirect("vault", permanent=True)
      messages.error(request, "Invalid Form")
      return response

  else:
    # form = forms.VaultNew()
    # return(render(request, "vault/vaultNew.html", {'title':'APM - New','form':form}))
    return HttpResponse("method not allowed")



def vaultDelete(request):
  if request.method == "POST":
    form = forms.VaultDelete(request.POST)
    if form.is_valid():
      data = {
        "id" : form.cleaned_data["id"],
        "email" : request.COOKIES.get("email"),
        "sessionId" : request.COOKIES.get("sessionId")
      }

      url = f'{base_url}/vault-delete/'

      success, dict_response = functions.sendRequestPost(url, data)
      if success:
        response = redirect("vault")
        return response
      elif success == None:
        response = redirect("vault", permanent=True)
        messages.error(request, "Connection Error")
        return response
      else:
        response = redirect("vault", permanent=True)
        messages.error(request, dict_response["errorMessage"])
        return response
    else:
      response = redirect("vault", permanent=True)
      messages.error(request, "Invalid Form")
      return response
  else:
    return HttpResponse("Method not allowed")



def logout(request):
  if request.method != "GET":
    return(JsonResponse({"errorCode":1, "errorMessage":"Method not Allowed."}))
  else:
    url = f'{base_url}/session-delete/'
    data = {
      "email":request.COOKIES.get("email"),
      "sessionId":request.COOKIES.get("sessionId"),
      "sessionIdW":request.COOKIES.get("sessionId")
    }
    success, dict_response = functions.sendRequestPost(url, data)

    cookies = [
        "csrftoken",
        "email",
        "sessionId",
        "password",
        "salt",
        "username",
        "pGConfigLength",
        "pGConfigCapitalLetters",
        "pGConfigSmallLetters",
        "pGConfigNumbers",
        "pGConfigSymbols"
      ]

    if success:
      response = redirect("signin", permanent=False)
      response = functions.delete_cookie(cookies, response)

      LogHandlerObj.write(f"Logout | OK | {request.COOKIES.get('email')} | {functions.get_client_ip(request)}")
      return response
    elif success == None:
      response = redirect("vault", permanent=True)
      messages.error(request, "Connection Error")

      LogHandlerObj.write(f"Logout | FAILED | {request.COOKIES.get('email')} | {functions.get_client_ip(request)} | Connection Error")
      return response
    else:
      response = redirect("signin", permanent=True)
      messages.error(request, dict_response["errorMessage"])

      response = functions.delete_cookie(cookies, response)

      LogHandlerObj.write(f"Logout | FAILED | {request.COOKIES.get('email')} | {functions.get_client_ip(request)} | {dict_response['errorMessage']}")
      return response



def sessionEdit(request):
  if request.method == "POST":
    form = forms.SessionEdit(request.POST)
    if form.is_valid():
      data = {
        "email":request.COOKIES.get("email"),
        "sessionId":request.COOKIES.get("sessionId"),
        "newName":form.cleaned_data["newSessionName"],
        "sessionIdW":form.cleaned_data["sessionIdW"]
      }
      url = f'{base_url}/session-edit/'

      success, dict_response = functions.sendRequestPost(url, data)
      if success:
        response = redirect("vault", permanent=True)
        messages.success(request, "Session Saved")
        return response
      elif success == None:
        response = redirect("vault", permanent=True)
        messages.error(request, "Connection Error")
        return response
      else:
        response = redirect("vault", permanent=True)
        messages.error(request, dict_response["errorMessage"])
        return response
    else:
      response = redirect("vault", permanent=True)
      messages.error(request, "Invalid Form")
      return response

  else:
    return HttpResponse("method not allowed")
  


def sessionDelete(request):
  if request.method == "POST":
    form = forms.SessionDelete(request.POST)
    if form.is_valid():
      data = {
        "email" : request.COOKIES.get("email"),
        "sessionId" : request.COOKIES.get("sessionId"),
        "sessionIdW" : form.cleaned_data["SessionDeleteSessionIdW"]
      }

      url = f'{base_url}/session-delete/'

      success, dict_response = functions.sendRequestPost(url, data)
      if success:
        response = redirect("vault")
        return response
      elif success == None:
        response = redirect("vault", permanent=True)
        messages.error(request, "Connection Error")
        return response
      else:
        response = redirect("vault", permanent=True)
        messages.error(request, dict_response["errorMessage"])
        return response
    else:
      response = redirect("vault", permanent=True)
      messages.error(request, "Invalid Form")
      return response
  else:
    return HttpResponse("Method not allowed")
  


def ppNew(request):
  if request.method == "POST":
    form = forms.ImageUpdate(request.POST, request.FILES)
    if form.is_valid():
      data = {
        "email":request.COOKIES.get("email"),
        "sessionId":request.COOKIES.get("sessionId"),
        "username":request.COOKIES.get("username"),
        "image":""
      }
      url = f'{base_url}/pp-new/'
      image64 = base64.standard_b64encode(request.FILES["image"].read())
      image64 = f"{image64}"
      data["image"] = image64

      success, dict_response = functions.sendRequestPost(url, data)
      if success:
        response = redirect("vault", permanent=True)
        messages.success(request, "Profile Picture Updated")
        return response
      elif success == None:
        response = redirect("vault", permanent=True)
        messages.error(request, "Connection Error")
        return response
      else:
        response = redirect("vault", permanent=True)
        messages.error(request, dict_response["errorMessage"])
        return response
    else:
      print(form.errors)
      response = redirect("vault", permanent=True)
      messages.error(request, str(form.errors["image"][0]))
      return response
  else:
    return HttpResponse("method not allowed")



def exportApmJson0(request):
  if request.method != "GET":
    return(JsonResponse({"errorCode":1, "errorMessage":"Method not Allowed."}))
  else:
    url = f'{base_url}/vault-get/'
    data = {
      "email":request.COOKIES.get("email"),
      "sessionId":request.COOKIES.get("sessionId")
    }
    success, dict_response = functions.sendRequestPost(url, data)

    if success:
      for value in dict_response["passwords"]:
        noteDecrypt = encryptor.decrypt(request.COOKIES.get("salt"), request.COOKIES.get("password"), value["note"])
        value["note"] = noteDecrypt
        passwordDecrypt = encryptor.decrypt(request.COOKIES.get("salt"), request.COOKIES.get("password"), value["password"])
        value["password"] = passwordDecrypt

      export = {
        "items":[

        ]
      }
      for value in dict_response["passwords"]:
        export["items"].append(value)
      
      response = JsonResponse(export, safe=False)
      response['Content-Disposition'] = f'attachment; filename=export-apm-json-0_{datetime.datetime.now(datetime.timezone.utc).isoformat()}.json'
      return response
    elif success == None:
      response = redirect("vault", permanent=True)
      messages.error(request, "Connection Error")
      return response
    else:
      response = redirect("vault", permanent=True)
      messages.error(request, dict_response["errorMessage"])
      return response
    


def pGConfig(request):
  if request.method == "POST":
    form = forms.PGConfig(request.POST)
    if form.is_valid():
      response = redirect("vault", permanent=True)
      cookies = [
        {
          "name": "pGConfigLength",
          "value": form.cleaned_data["length"],
        },
        {
          "name": "pGConfigCapitalLetters",
          "value": form.cleaned_data["capitalLetters"],
        },
        {
          "name": "pGConfigSmallLetters",
          "value": form.cleaned_data["smallLetters"],
        },
        {
          "name": "pGConfigNumbers",
          "value": form.cleaned_data["numbers"],
        },
        {
          "name": "pGConfigSymbols",
          "value": form.cleaned_data["symbols"],
        }
      ]
      response = functions.set_cookie(cookies, response)

      messages.success(request, "Password Generation Config Saved")
      return response
    else:
      response = redirect("vault", permanent=True)
      messages.error(request, "Invalid Form")
      return response
  else:
    return HttpResponse("method not allowed")
  


def importVault(request):
  if request.method == "POST":
    form = forms.ImportVault(request.POST, request.FILES)
    if form.is_valid():
      try:
        json_file = request.FILES['file']
        json_data = json_file.read()

        data_dict = json.loads(json_data)
        data_dict["email"] = request.COOKIES.get("email")
        data_dict["sessionId"] = request.COOKIES.get("sessionId")

        salt = request.COOKIES.get("salt")
        password = request.COOKIES.get("password")

        url = f'{base_url}/vault-import/'
        
        for entry in data_dict["items"]:
          entry["password"] = encryptor.encrypt(salt, entry["password"], password)
          entry["note"] = encryptor.encrypt(salt, entry["note"], password)

        success, dict_response = functions.sendRequestPost(url, data_dict)
        if success:
          response = redirect("vault", permanent=True)
          messages.success(request, "Vault Imported")
          return response
        elif success == None:
          response = redirect("vault", permanent=True)
          messages.error(request, "Connection Error")
          return response
        else:
          response = redirect("vault", permanent=True)
          messages.error(request, dict_response["errorMessage"])
          return response
      except Exception as e:
        response = redirect("vault", permanent=True)
        messages.error(request, "Invalid JSON file")
        return response
    else:
      print(form.errors)
      response = redirect("vault", permanent=True)
      messages.error(request, str(form.errors["file"][0]))
      return response
  else:
    return HttpResponse("method not allowed")