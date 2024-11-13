import time, requests
from typing import List, Dict, Any, Union, Tuple, Optional
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect

class Functions(object):
  def __init__(self, ConfigObj):
    """
    Initialize the class with the given ConfigObj
    @param ConfigObj: The Config Class Object
    @type ConfigObj: Config
    """
    
    self.ConfigObj = ConfigObj

  def set_cookie(self, cookies: List[Dict[str, Any]], response: Union[Union[HttpResponseRedirect, HttpResponsePermanentRedirect], HttpResponse]) -> Union[Union[HttpResponseRedirect, HttpResponsePermanentRedirect], HttpResponse]:
    """
    Set a list of cookies on the given response

    @param cookies: List of dictionaries, each containing the name and value of the cookie
    @type cookies: list
    @param response: The response to set the cookies on
    @type response: HttpResponse
    @return: The response with the cookies set
    @rtype: HttpResponse
    """

    for cookie in cookies:
      response.set_cookie(cookie["name"], cookie["value"], max_age=60*60*24*365)
    return response
  
  def delete_cookie(self, cookies: List[str], response: Union[Union[HttpResponseRedirect, HttpResponsePermanentRedirect], HttpResponse]) -> Union[Union[HttpResponseRedirect, HttpResponsePermanentRedirect], HttpResponse]:
    """
    Delete a list of cookies from the given response
    
    @param cookies: List of strings, each containing the name of the cookie
    @type cookies: list
    @param response: HttpResponse object to delete the cookies from
    @type response: HttpResponse
    @return: The modified HttpResponse with the cookies deleted
    @rtype: HttpResponse
    """
    
    for cookie in cookies:
      response.delete_cookie(cookie)
    return response
  
  def sendRequestPost(self, url: str, data: Dict[str, Any]) -> Tuple[Optional[bool], Dict[str, Any]]:
    """
    Send a POST request to the given URL with the given data, and return the JSON response

    @param url: The URL to send the request to
    @type url: str
    @param data: A dictionary containing the data to send in the request body
    @type data: dict
    @return: A tuple containing a boolean or none indicating the success of the request and the JSON response
    @rtype: tuple
    """

    data["apiToken"] = self.ConfigObj.api_token
    attempt_num = 0
    while attempt_num < self.ConfigObj.max_retries:
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
  
  def get_client_ip(self, request: HttpRequest) -> str:
    """
    Get the client's IP from the request object
    @param request: the request object
    @type request: HttpRequest
    @return: the client's IP
    @rtype: str
    """

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
      ip = x_forwarded_for.split(',')[0]
    else:
      ip = request.META.get('REMOTE_ADDR') or ""
    return ip