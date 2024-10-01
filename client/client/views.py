from django.shortcuts import redirect, render
from django.http.response import HttpResponse, JsonResponse
import json
from .settings import ConfigObj

def home(request):
  if request.method != "GET":
    return(JsonResponse({"errorCode":1, "errorMessage":"Method not Allowed."}))
  else:
    if request.COOKIES.get("sessionId") is None:
      return redirect("signin/")
    else: 
      return redirect("vault/")

def signin(request):
  return(render(request, "signin/index.html", {'title':'APM - Signin'}))

def vault(request):
  return HttpResponse("vault")