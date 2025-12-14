
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

function Str_To_List(str) {
    // récupère uniquement les nombres dans la chaîne
    const match = str.match(/\d+/g);
    if (!match || match.length !== 3) {
        throw new Error("Format RGB invalide : " + str);
    }
    return match.map(Number);
}

function rgb_To_Hsl(r, g, b) {
    r /= 255;
    g /= 255;
    b /= 255;

    const max = Math.max(r, g, b);
    const min = Math.min(r, g, b);
    let h, s;
    const l = (max + min) / 2;

    if (max === min) {
        h = 0;
        s = 0; // achromatique
    } else {
        const d = max - min;
        s = l > 0.5
            ? d / (2 - max - min)
            : d / (max + min);

        switch (max) {
            case r:
                h = ((g - b) / d + (g < b ? 6 : 0)) * 60;
                break;
            case g:
                h = ((b - r) / d + 2) * 60;
                break;
            case b:
                h = ((r - g) / d + 4) * 60;
                break;
        }
    }

    return [
        Math.round(h),
        Math.round(s * 100),
        Math.round(l * 100)
    ];
}

function hsl_To_Rgb(h, s, l) {
    s /= 100;
    l /= 100;

    const k = n => (n + h / 30) % 12;
    const a = s * Math.min(l, 1 - l);
    const f = n =>
        l - a * Math.max(-1, Math.min(k(n) - 3, Math.min(9 - k(n), 1)));

    const r = Math.round(255 * f(0));
    const g = Math.round(255 * f(8));
    const b = Math.round(255 * f(4));

    return `(${r},${g},${b})`
}


const preview = document.getElementById("preview");

const hue = document.getElementById("hue");
const sat = document.getElementById("sat");
const light = document.getElementById("light");

// update la couleur quand modifié
function updateColor() {
  const h = hue.value;
  const s = sat.value;
  const l = light.value;

  preview.style.backgroundColor = `hsl(${h}, ${s}%, ${l}%)`;

  rgb = hsl_To_Rgb(h, s, l);
  console.log("rgb : ", rgb)

  fetch('/couleur', {
    method: 'POST',
    headers: { 'Content-Type': 'text/plain' },
    body: rgb // rgb = hsl_To_Rgb(h,s,l) -> "(238,238,93)"
});
}

hue.addEventListener("input", updateColor);
sat.addEventListener("input", updateColor);
light.addEventListener("input", updateColor);

// update la bonne couleur quand lance page
window.addEventListener('DOMContentLoaded', async () => {
    try {
        const response = await fetch('/couleur');  // GET
        const data = await response.text();        // récupère "(238,238,93)"

        console.log("Réponse brute du serveur :", data);

        const rgb_liste = Str_To_List(data);       // [238,238,93]

        const hsl = rgb_To_Hsl(rgb_liste[0], rgb_liste[1], rgb_liste[2]);

        hue.value = hsl[0];
        sat.value = hsl[1];
        light.value = hsl[2];

        preview.style.backgroundColor = `hsl(${hue.value}, ${sat.value}%, ${light.value}%)`;
    } catch (err) {
        console.error("Erreur lors du fetch GET :", err);
    }
});


// ------------effets bouton selection----------------------

const effet_select = document.getElementById('animation')

const envoyer_effet = () => {
    const valeur = effet_select.value;

    console.log("Effet choisi :", valeur);

    fetch('/animation', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: 'effet=' + valeur
    });
};

// Déclenche à chaque changement de sélection
effet_select.addEventListener('change', envoyer_effet);

// Update au lancement
window.addEventListener('DOMContentLoaded', async () => {
        const response = await fetch('/animation');  // GET
        const data = await response.json();
        const display = document.getElementById('animation')
        display.value = data.effet; // met à jour le texte du h5
});
