import json
import time
from django.shortcuts import redirect, render
from django.contrib import messages
from django.http.response import HttpResponse, JsonResponse
import requests
from .settings import ConfigObj
from . import forms

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
        return render(request, "vault/index.html", {'title':'APM - Vault', 'passwords':dict_response["passwords"], 'formVaultDelete':forms.VaultDelete()})
      elif success == None:
        response = redirect("vault", permanent=True)
        messages.error(request, "Connection Error")
        return response
      else:
        response = redirect("signin", permanent=True)
        messages.error(request, dict_response["errorMessage"])
        response.delete_cookie("sessionId")
        response.delete_cookie("email")
        return response
      


def vaultNew(request):
  if request.method == "POST":
    form = forms.VaultNew(request.POST)
    if form.is_valid():
      try:
        url = form.cleaned_data["url"]
      except:
        url = ""
      data = {
        "email":request.COOKIES.get("email"),
        "sessionId":request.COOKIES.get("sessionId"),
        "name":form.cleaned_data["name"],
        "username":form.cleaned_data["username"],
        "password":form.cleaned_data["password"],
        "url":url
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
    form = forms.VaultNew()
    return(render(request, "vault/vaultNew.html", {'title':'APM - New','form':form}))
  


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
      return response