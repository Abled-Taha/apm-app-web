function getCookie(cookieName) {
  let cookies = document.cookie;
  let cookieArray = cookies.split("; ");

  for (let i = 0; i < cookieArray.length; i++) {
     let cookie = cookieArray[i];
     let [name, value] = cookie.split("=");
    
     if (name === cookieName) {
        return decodeURIComponent(value);
     }
  }
  
  return null;
}

let errorMessage = getCookie("errorMessage");

if (errorMessage != null) {
  alert(errorMessage)
  document.cookie = "errorMessage=;path=/;Max-Age=0"
}