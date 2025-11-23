
/* --------------boutton ON/OFF----------*/

const checkbox = document.getElementById('toggleSwitch');
checkbox.checked = false; /* met le bouton sur false*/
checkbox.addEventListener('change', () => {
    console.log("Click");
    fetch('/led/state', {
        method: 'POST',
        headers: {'Content-Type': 'application/x-www-form-urlencoded'},
        body: (checkbox.checked ? 1 : 0)
    });
});



console.log("JavaScript fonctionne !");