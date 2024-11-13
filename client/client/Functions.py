import time, requests

class Functions(object):
  def __init__(self, ConfigObj):
    self.ConfigObj = ConfigObj

  def set_cookie(self, cookies, response):
    for cookie in cookies:
      response.set_cookie(cookie["name"], cookie["value"], max_age=60*60*24*365)
    return response
  
  def delete_cookie(self, cookies, response):
    for cookie in cookies:
      response.delete_cookie(cookie)
    return response
  
  def sendRequestPost(self, url, data):
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
  
  def get_client_ip(self, request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip