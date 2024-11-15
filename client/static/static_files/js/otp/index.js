function onChange() {
  otpForm = document.getElementById('otp-form');

  otp1 = document.getElementById('otp1');
  otp2 = document.getElementById('otp2');
  otp3 = document.getElementById('otp3');
  otp4 = document.getElementById('otp4');
  otp5 = document.getElementById('otp5');
  otp6 = document.getElementById('otp6');

  otp1.onchange = function() {
    otp2.focus();
  }
  otp2.onchange = function() {
    otp3.focus();
  }
  otp3.onchange = function() {
    otp4.focus();
  }
  otp4.onchange = function() {
    otp5.focus();
  }
  otp5.onchange = function() {
    otp6.focus();
  }
  otp6.onchange = function() {
    otpForm.submit();
  }
}

onChange()