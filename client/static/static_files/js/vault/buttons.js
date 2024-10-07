function openPopup(website, username, password, url, id) {
  document.getElementById("popup-website").textContent = website;
  document.getElementById("popup-username").textContent = username;
  document.getElementById("popup-password").textContent = password;
  document.getElementById("popup-url").textContent = url;
  document.getElementById("popup-id").textContent = id;
  document.getElementById("popup-button").onclick = function() {
    copyPassword(password)
  }
  document.getElementById("popup").style.display = "block";
  document.addEventListener('keydown', handleKeyDown);
}

function closePopup() {
  document.getElementById("popup").style.display = "none";
  document.removeEventListener('keydown', handleKeyDown);
}

function copyPassword(password) {
navigator.clipboard.writeText(password).then(function() {
    alert("Password copied!");
}, function(err) {
    console.error("Could not copy password: ", err);
});
}

function deletePassword() {
  alert("Password deleted!");
}

function handleKeyDown(event) {
  if (event.key === "Escape") {
    closePopup();
  }
}