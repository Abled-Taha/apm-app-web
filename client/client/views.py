import json, time, requests, base64, datetime
from django.shortcuts import redirect, render
from django.contrib import messages
from django.http.response import HttpResponse, JsonResponse
from .settings import ConfigObj
from . import forms, encryptor

base_url = f"http://{ConfigObj.server_host}:{ConfigObj.server_port}"



def home(request):
  if request.method != "GET":
    return(JsonResponse({"errorCode":1, "errorMessage":"Method not Allowed."}))
  else:
    if request.COOKIES.get("sessionId") is None:
      return redirect("signin", permanent=True)
    else:
      return redirect("vault", permanent=True)



def sendRequestPost(url, data):
  attempt_num = 0
  while attempt_num < ConfigObj.max_retries:
    try:
      response = requests.post(url, json=data)
      dict_response = response.json()

      if dict_response["errorCode"] == 0:
        return True, dict_response
          
      else:
        return False, dict_response
    except:
      attempt_num += 1
      time.sleep(2)
  return None, {}



def signin(request):
  if request.method == "POST":
    form = forms.Signin(request.POST)
    if form.is_valid():
      try:
        sessionName = form.cleaned_data["sessionName"]
      except:
        sessionName = ""
      data = {
        "email":form.cleaned_data["email"],
        "password":form.cleaned_data["password"],
        "sessionName":sessionName
      }
      url = f'{base_url}/signin/'

      success, dict_response = sendRequestPost(url, data)
      if success:
        response = redirect("home", permanent=True)
        response.set_cookie("sessionId", dict_response["sessionId"], max_age=60*60*24*365)
        response.set_cookie("email", data["email"], max_age=60*60*24*365)
        response.set_cookie("password", data["password"], max_age=60*60*24*365)
        response.set_cookie("salt", dict_response["salt"], max_age=60*60*24*365)
        response.set_cookie("username", dict_response["username"], max_age=60*60*24*365)
        return response
      elif success == None:
        response = redirect("signin", permanent=True)
        messages.error(request, "Connection Error")
        return response
      else:
        response = redirect("signin", permanent=True)
        messages.error(request, dict_response["errorMessage"])
        # response.set_cookie("errorMessage", dict_response["errorMessage"])
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

      success, dict_response = sendRequestPost(url, data)
      if success:
        response = redirect("signin", permanent=True)
        messages.success(request, "Account Created")
        return response
      elif success == None:
        response = redirect("signup", permanent=True)
        messages.error(request, "Connection Error")
        return response
      else:
        response = redirect("signup", permanent=True)
        messages.error(request, dict_response["errorMessage"])
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
      success, dict_response = sendRequestPost(url, data)

      if success:
        for value in dict_response["passwords"]:
          noteDecrypt = encryptor.decryptor(request.COOKIES.get("salt"), request.COOKIES.get("password"), value["note"])
          value["note"] = noteDecrypt
          passwordDecrypt = encryptor.decryptor(request.COOKIES.get("salt"), request.COOKIES.get("password"), value["password"])
          value["password"] = passwordDecrypt
        url = f'{base_url}/session-get/'
        success, dict_response1 = sendRequestPost(url, data)
        if success:
          sessions = dict_response1["sessionIds"]
          url = f'{base_url}/pp-get/'
          data["username"] = request.COOKIES.get("username")
          success, dict_response2 = sendRequestPost(url, data)
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
        response.delete_cookie("sessionId")
        response.delete_cookie("email")
        response.delete_cookie("password")
        response.delete_cookie("salt")
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
      success, dict_response = sendRequestPost(url, data)

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

      success, dict_response = sendRequestPost(url, data)
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

      success, dict_response = sendRequestPost(url, data)
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
    success, dict_response = sendRequestPost(url, data)

    if success:
      response = redirect("signin", permanent=False)
      response.delete_cookie("email")
      response.delete_cookie("sessionId")
      response.delete_cookie("password")
      return response
    elif success == None:
      response = redirect("vault", permanent=True)
      response.set_cookie("errorMessage", "Connection Error")
      return response
    else:
      response = redirect("signin", permanent=True)
      response.set_cookie("errorMessage", dict_response["errorMessage"])
      response.delete_cookie("sessionId")
      response.delete_cookie("email")
      response.delete_cookie("salt")
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

      success, dict_response = sendRequestPost(url, data)
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

      success, dict_response = sendRequestPost(url, data)
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

      success, dict_response = sendRequestPost(url, data)
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
      messages.error(request, form.errors["image"][0])
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
    success, dict_response = sendRequestPost(url, data)

    if success:
      for value in dict_response["passwords"]:
        noteDecrypt = encryptor.decryptor(request.COOKIES.get("salt"), request.COOKIES.get("password"), value["note"])
        value["note"] = noteDecrypt
        passwordDecrypt = encryptor.decryptor(request.COOKIES.get("salt"), request.COOKIES.get("password"), value["password"])
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
      response.set_cookie("pGConfigLength", form.cleaned_data["length"], max_age=365*24*60*60)
      response.set_cookie("pGConfigCapitalLetters", form.cleaned_data["capitalLetters"], max_age=365*24*60*60)
      response.set_cookie("pGConfigSmallLetters", form.cleaned_data["smallLetters"], max_age=365*24*60*60)
      response.set_cookie("pGConfigNumbers", form.cleaned_data["numbers"], max_age=365*24*60*60)
      response.set_cookie("pGConfigSymbols", form.cleaned_data["symbols"], max_age=365*24*60*60)
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

        email = request.COOKIES.get("email")
        sessionId = request.COOKIES.get("sessionId")
        salt = request.COOKIES.get("salt")
        password = request.COOKIES.get("password")

        url = f'{base_url}/vault-new/'
        
        for entry in data_dict["items"]:
          entry["email"] = email
          entry["sessionId"] = sessionId
          entry["password"] = encryptor.encrypt(salt, entry["password"], password)
          entry["note"] = encryptor.encrypt(salt, entry["note"], password)

          success, dict_response = sendRequestPost(url, entry)
          if success:
            pass
          elif success == None:
            response = redirect("vault", permanent=True)
            messages.error(request, "Connection Error")
            return response
          else:
            response = redirect("vault", permanent=True)
            messages.error(request, dict_response["errorMessage"])
            return response
          
        response = redirect("vault", permanent=True)
        messages.success(request, "Vault Imported")
        return response
      except Exception as e:
        response = redirect("vault", permanent=True)
        messages.error(request, "Invalid JSON file")
        return response
    else:
      print(form.errors)
      response = redirect("vault", permanent=True)
      messages.error(request, form.errors["file"][0])
      return response
  else:
    return HttpResponse("method not allowed")