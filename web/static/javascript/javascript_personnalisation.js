
/* --------------test pour verif que le fichier js fonctionne----------*/
console.log("JavaScript fonctionne !");

/* --------------Modes + selection boutons------------------------------*/
const b_mode_couleur = document.getElementById('b_mode_couleur');
const b_mode_image = document.getElementById('b_mode_image');
const b_mode_animation = document.getElementById('b_mode_animation');

const boutons = document.querySelectorAll('.boutons_mode');
const fenetres_droite = document.querySelectorAll('.partie_droite_personnalisation')

boutons.forEach(btn => {
    btn.addEventListener('click', () => {
        // retirer la classe selected de tous les boutons
        boutons.forEach(b => b.classList.remove('selected'));

        // ajouter la classe selected au bouton cliqué
        btn.classList.add('selected');

        console.log(btn.classList);

        // récupérer le mode
        const mode = btn.dataset.mode;
        console.log("Mode sélectionné :", mode);
        fetch('/led/affichage', {
            method: 'POST',
            headers: { 'Content-Type': 'text/plain' },
            body: mode
        });

        // changer la fenetre de droite en fonction du mode

        update_fenetre(mode)

    });
});

/*------fonctions-------- */
function appliquerSelection(mode) {
    console.log("jeu de lumiere sauvegardé : ", mode)
    boutons.forEach(btn => {
        btn.classList.remove('selected');
        if (btn.dataset.mode === mode) {
            btn.classList.add('selected');
        }
    });
}

function update_fenetre(mode) {
    console.log(mode)
    fenetres_droite.forEach(f => {
        f.classList.add('invisible');
        if (f.dataset.mode === mode) {
            f.classList.remove('invisible');
        }
    });
}


// Au chargement de la page, récupérer le mode de jeu de lumiere actuel
window.addEventListener('DOMContentLoaded', async () => {
    try {
        const response = await fetch('/led/affichage');  // GET
        const data = await response.json();
        appliquerSelection(data.jeu_de_lumiere);
        update_fenetre(data.jeu_de_lumiere);

    } catch (err) {
        console.error("Erreur lors du fetch GET :", err);
    }
});


//--------------selection couleur -----------------------

const preview = document.getElementById("preview");

const hue = document.getElementById("hue");
const sat = document.getElementById("sat");
const light = document.getElementById("light");

function updateColor() {
  const h = hue.value;
  const s = sat.value;
  const l = light.value;

  preview.style.backgroundColor = `hsl(${h}, ${s}%, ${l}%)`;
}

hue.addEventListener("input", updateColor);
sat.addEventListener("input", updateColor);
light.addEventListener("input", updateColor);

updateColor();