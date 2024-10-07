function openPopup(website, username, password, url, id) {
  document.getElementById("popup-website").textContent = website;
  document.getElementById("popup-username").textContent = username;
  document.getElementById("popup-password").textContent = password;
  document.getElementById("popup-url").textContent = url;
  document.getElementById("popup-id").textContent = id;
  document.getElementById("popup-button").onclick = function() {
    copyPassword(password)
  }
  document.getElementById("popup-details").style.display = "flex";
  document.addEventListener('keydown', handleKeyDown);
}

function closePopup() {
  document.getElementById("popup-details").style.display = "none";
  document.removeEventListener('keydown', handleKeyDown);
}

function copyPassword(password) {
navigator.clipboard.writeText(password).then(function() {
    alert("Password copied!");
}, function(err) {
    console.error("Could not copy password: ", err);
});
}

function openPopupDelete(id) {
  document.getElementById("id_id").setAttribute('value', id)
  document.getElementById("popup-delete").style.display = "flex";
  document.addEventListener('keydown', handleKeyDown);
}

function closePopupDelete() {
  document.getElementById("popup-delete").style.display = "none";
  document.removeEventListener('keydown', handleKeyDown);
}

function openPopupAdd() {
  document.getElementById("popup-add").style.display = "flex";
  document.addEventListener('keydown', handleKeyDown);
}

function closePopupAdd() {
  document.getElementById("popup-add").style.display = "none";
  document.removeEventListener('keydown', handleKeyDown);
}

function handleKeyDown(event) {
  if (event.key === "Escape") {
    closePopup();
    closePopupDelete();
    closePopupAdd();
  }
}

function filterVault() {
  const searchValue = document.getElementById('search').value.toLowerCase();
  const vaultItems = document.querySelectorAll('.vault-item');

  vaultItems.forEach(item => {
      const itemName = item.querySelector('h3').textContent.toLowerCase();
      const itemUsername = item.querySelector('p').textContent.toLowerCase();
      
      if (itemName.includes(searchValue) || itemUsername.includes(searchValue)) {
          item.style.display = '';
      } else {
          item.style.display = 'none';
      }
  });
}

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
