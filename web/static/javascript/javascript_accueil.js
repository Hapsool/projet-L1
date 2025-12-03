
/* --------------boutton ON/OFF----------*/

const checkbox = document.getElementById('toggleSwitch');
checkbox.checked = false;
checkbox.addEventListener('change', async () => {
  const body = `etat=${checkbox.checked ? 1 : 0}`;
  try {
    const res = await fetch('/led/state', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: body
    });
    const data = await res.json();
    console.log("Réponse back:", data);
  } catch (e) {
    console.error("Erreur fetch:", e);
  }
});

/* ------------- recup l'etat ON ou OFF au chargement de la page ------------*/
window.addEventListener('DOMContentLoaded', async () => {
    try {
        const response = await fetch('/led/state');  // GET
        const data = await response.json();
        checkbox.checked = Boolean(data.etat)
        console.log("Etat au chargement : ", data.etat)
    } catch (err) {
        console.error("Erreur lors du fetch GET :", err);
    }
});


// ---------------verifier si mode manuel activé, sinon rendre invisible le bouton On/Off------------

async function verif_mode(mode) {
  console.log("mode :", mode)
  if (mode == "manual") {
    // Récupérer tous les divs avec la classe switch-container
    const boutons = document.querySelectorAll(".switch-container");

    // Supprimer tous les éléments
    boutons.forEach(b => b.classList.remove('invisible'));
      }
  console.log(checkbox.classList)
}

window.addEventListener('DOMContentLoaded', async () => {
    const response = await fetch('/led/mode');  // GET
    const data = await response.json();
    verif_mode(data.mode)
});

/* --------------test pour verif que le fichier js fonctionne----------*/
console.log("JavaScript fonctionne !");
