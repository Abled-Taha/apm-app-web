function togglePasswordVisibility() {
  const passwordField = document.getElementById("id_password");
  const toggleIconPassword = document.getElementById("togglePassword");

  if (passwordField.type === "password") {
      passwordField.type = "text";
      toggleIconPassword.classList.remove("fa-eye");
      toggleIconPassword.classList.add("fa-eye-slash");
  } else {
      passwordField.type = "password";
      toggleIconPassword.classList.remove("fa-eye-slash");
      toggleIconPassword.classList.add("fa-eye");
  }
}