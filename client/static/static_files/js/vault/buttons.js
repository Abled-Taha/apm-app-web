function openPopup(website, username, password, url, id) {
  document.getElementById("popup-website").textContent = website;
  document.getElementById("popup-username").textContent = username;
  document.getElementById("popup-password").textContent = password;
  document.getElementById("popup-url").textContent = url;
  document.getElementById("popup-id").textContent = id;
  document.getElementById("popup-button").onclick = function() {
    copyPassword(password)
  }
  document.getElementById("popup").style.display = "flex";
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

function filterVault() {
  const searchValue = document.getElementById('search').value.toLowerCase();
  const vaultItems = document.querySelectorAll('.vault-item');

  vaultItems.forEach(item => {
      const itemName = item.querySelector('h3').textContent.toLowerCase();
      const itemUsername = item.querySelector('p').textContent.toLowerCase();
      
      if (itemName.includes(searchValue) || itemUsername.includes(searchValue)) {
          item.style.display = ''; // Show
      } else {
          item.style.display = 'none'; // Hide
      }
  });
}
