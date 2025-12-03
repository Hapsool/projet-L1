
const sensibilite_audio_input = document.getElementById('sensibilite_audio');
const sensibilite_lumiere_input = document.getElementById('sensibilite_lumiere');
const intensite_luminosite_input = document.getElementById('intensite');
const mode_select = document.getElementById('mode')
//------------input luminosite--------------
const envoyerLuminosite = () => {
    const valeur = intensite_luminosite_input.value;

    console.log(valeur);

    fetch('/led/luminosite', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: 'luminosite=' + valeur
    });
    intensite_luminosite_input.blur();
};

// Quand on quitte le champ
intensite_luminosite_input.addEventListener('blur', envoyerLuminosite);

// Quand on appuie sur Entrée
// Quand on appuie sur Entrée
intensite_luminosite_input.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
        e.preventDefault(); // empêche le submit auto
        envoyerLuminosite();
    }
});

//------------input seuil lumi--------------
const envoyer_seuil_Luminosite = () => {
    const valeur_seuil_lumi = sensibilite_lumiere_input.value;

    console.log(valeur_seuil_lumi);

    fetch('/capteur/seuil_luminosite', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: valeur_seuil_lumi
    });
    sensibilite_lumiere_input.blur();
};

// Quand on quitte le champ
sensibilite_lumiere_input.addEventListener('blur', envoyer_seuil_Luminosite);

// Quand on appuie sur Entrée
// Quand on appuie sur Entrée
sensibilite_lumiere_input.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
        e.preventDefault(); // empêche le submit auto
        envoyer_seuil_Luminosite();
    }
});

//------------input seuil audio--------------
const envoyer_seuil_audio = () => {
    const valeur_seuil_audio = sensibilite_audio_input.value;

    console.log(valeur_seuil_audio);

    fetch('/capteur/seuil_audio', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: valeur_seuil_audio
    });
    sensibilite_audio_input.blur();
};

// Quand on quitte le champ
sensibilite_audio_input.addEventListener('blur', envoyer_seuil_audio);

// Quand on appuie sur Entrée
// Quand on appuie sur Entrée
sensibilite_audio_input.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
        e.preventDefault(); // empêche le submit auto
        envoyer_seuil_audio();
    }
});

//------------select mode--------------

const envoyermode = () => {
    const valeur = mode_select.value;

    console.log("Mode choisi :", valeur);

    fetch('/led/mode', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: 'mode=' + valeur
    });
};

// Déclenche à chaque changement de sélection
mode_select.addEventListener('change', envoyermode);


//------------reset button--------------
const btn = document.getElementById("reset")

async function recup_valeur_defaut() {
    const response = await fetch('/valeurs_par_defaut');  // GET
    const data = await response.json();

    const display = document.getElementById('intensite')
    display.value = data.luminosite; // met à jour le texte du h5

    const display2 = document.getElementById('sensibilite_lumiere')
    display2.value = data.lum_min; // met à jour le texte du h5

    const display3 = document.getElementById('sensibilite_audio')
    display3.value = data.audio_min; // met à jour le texte du h5


    fetch('/led/luminosite', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: 'luminosite=' + data.luminosite
    });

    fetch('/capteur/seuil_luminosite', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: data.lum_min
    });

        fetch('/capteur/seuil_audio', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: data.audio_min
    });
}

btn.addEventListener('click', () => {

    recup_valeur_defaut()

})


//----Met la valeur dans l'input au chargement de la page------
window.addEventListener('DOMContentLoaded', async () => {
        const response = await fetch('/led/luminosite');  // GET
        const data = await response.json();
        const display = document.getElementById('intensite')
        display.value = data.luminosite; // met à jour le texte du h5
});

window.addEventListener('DOMContentLoaded', async () => {
        const response = await fetch('/capteur/seuil_luminosite');  // GET
        const data = await response.json();
        const display = document.getElementById('sensibilite_lumiere')
        display.value = data.lum_min; // met à jour le texte du h5
});

window.addEventListener('DOMContentLoaded', async () => {
        const response = await fetch('/capteur/seuil_audio');  // GET
        const data = await response.json();
        const display = document.getElementById('sensibilite_audio')
        display.value = data.audio_min; // met à jour le texte du h5
});


window.addEventListener('DOMContentLoaded', async () => {
        const response = await fetch('/led/mode');  // GET
        const data = await response.json();
        const display = document.getElementById('mode')
        display.value = data.mode; // met à jour le texte du h5
});