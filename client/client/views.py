import time
from django.shortcuts import redirect, render
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
        response = requests.post(url, json=data)
        if response.status_code == 200:
          dict_response = response.json()
          if dict_response["errorCode"] == 0:
            return True, dict_response
            
          else:
            return False, dict_response
        else:
          attempt_num += 1
          time.sleep(5)
      return None, {}



def signin(request):
  if request.method == "POST":
    form = forms.Signin(request.POST)
    if form.is_valid():
      data = {
        "email":form.cleaned_data["email"],
        "password":form.cleaned_data["password"]
      }
      url = f'{base_url}/signin/'

      success, dict_response = sendRequestPost(url, data)
      if success:
        response = redirect("home", permanent=True)
        response.set_cookie("sessionId", dict_response["sessionId"])
        response.set_cookie("email", data["email"])
        return response
      elif success == None:
        response = redirect("signin", permanent=True)
        response.set_cookie("errorMessage", "Connection Error")
        return response
      else:
        response = redirect("signin", permanent=True)
        response.set_cookie("errorMessage", dict_response["errorMessage"])
        return response

  else:
    form = forms.Signin()
    return(render(request, "signin/index.html", {'title':'APM - Signin','form':form}))



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
        return JsonResponse(dict_response)
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
      

      
def signup(request):
  return HttpResponse("signup")