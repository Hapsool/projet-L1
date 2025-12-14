/* --------------infos base de donnée pour afficher sur page information----------*/

fetch("/led/luminosite")
  .then(res => res.json())
  .then(data => {
        const display = document.getElementById('info_luminosite');
        console.log(data.luminosite);
        display.innerText = data.luminosite; // met à jour le texte du h5
  });

fetch("/led/mode")
  .then(res => res.json())
  .then(data => {
        const display = document.getElementById('info_mode');
        console.log(data.mode);
        display.innerText = data.mode; // met à jour le texte du h5
  });

  fetch("/led/affichage")
  .then(res => res.json())
  .then(data => {
        const display = document.getElementById('info_affichage');
        console.log(data.jeu_de_lumiere);
        display.innerText = data.jeu_de_lumiere; // met à jour le texte du h5
  });

  fetch("/capteur/pir")
  .then(res => res.json())
  .then(data => {
        const display = document.getElementById('info_pir');
        console.log(data.pir);
        if (data.pir == 1) {
            display.innerText = "oui"
        }
        else {
            display.innerText = "non"
        }
  });

/* --------------test pour verif que le fichier js fonctionne----------*/
console.log("JavaScript fonctionne !");

/* --------------graphe test------------------------------*/
// Initialisation du graphique vide
const chart = Highcharts.chart('graphe', {
    chart: { type: 'spline', animation: Highcharts.svg },
    title: { text: 'Données captées en temps réel' },
    xAxis: {
        type: 'datetime',
        tickPixelInterval: 150
    },
    yAxis: {
        title: { text: 'Luminosité' },
        min: 0,
        max: 1023    // valeur maximale de l'axe
    },
    series: [{
        name: 'Luminosité LED',
        data: [] // vide au départ
    }],
    series: [
        {
            name: 'Luminosité ambiante',
            data: []
        },
        {
            name: 'seuil lumiere d\'activation de la led',
            data: [],            // vide au départ
            type: 'line',
            color: 'red',
            dashStyle: 'Dash',
            enableMouseTracking: false
        },
        {
            name: 'bruit ambiant',
            data: []
        },
        {
            name: 'seuil bruit d\'activation de la led',
            data: [],            // vide au départ
            type: 'line',
            color: 'red',
            dashStyle: 'Dash',
            enableMouseTracking: false
        },
    ]
});

async function updateSeuil() {
    try {
        const response = await fetch("/capteur/seuil_luminosite");
        const data = await response.json();

        const now = Date.now();
        const seriesSeuil = chart.series[1];

        console.log(data.lum_min)

        // On remplace les points pour que la droite soit toujours sur 5 secondes
        seriesSeuil.setData([
            [now - 5000, data.lum_min],  // 5 secondes avant
            [now, data.lum_min]          // maintenant
        ], true); // true pour redraw

    } catch (error) {
        console.error("Erreur lors du chargement des données :", error);
    }
}


// Fonction pour récupérer la dernière valeur
async function chargerDonnees() {
    try {
        const response = await fetch('/capteur/lumiere');
        const data = await response.json();

        // Créer le point : timestamp = maintenant, y = luminosité
        const point = [new Date().getTime(), Number(data.luminosite)];

        console.log('Ajout du point :', point);

        const series = chart.series[0];
        const serie_droite = chart.series[1]
        series.addPoint(point, true, false);

        // Supprimer les points trop anciens (plus de 5 secondes)
        const now = new Date().getTime();
        while (series.data.length > 0 && series.data[0].x < now - 5000) {
            series.data[0].remove(false);
        }

        updateSeuil()

        chart.redraw();
    } catch (error) {
        console.error("Erreur lors du chargement des données :", error);
    }
}

// ----------------pour capteur audio---------

async function updateSeuil_audio() {
    try {
        const response = await fetch("/capteur/seuil_audio");
        const data = await response.json();

        const now = Date.now();
        const seriesSeuil = chart.series[3];

        console.log(data.audio_min)

        // On remplace les points pour que la droite soit toujours sur 5 secondes
        seriesSeuil.setData([
            [now - 5000, data.audio_min],  // 5 secondes avant
            [now, data.audio_min]          // maintenant
        ], true); // true pour redraw

    } catch (error) {
        console.error("Erreur lors du chargement des données :", error);
    }
}


// Fonction pour récupérer la dernière valeur
async function chargerDonnees_audio() {
    try {
        const response = await fetch('capteur/audio');
        const data = await response.json();

        // Créer le point : timestamp = maintenant, y = luminosité
        const point = [new Date().getTime(), Number(data.sound)];

        console.log('Ajout du point :', point);

        const series = chart.series[2];
        const serie_droite = chart.series[3]
        series.addPoint(point, true, false);

        // Supprimer les points trop anciens (plus de 5 secondes)
        const now = new Date().getTime();
        while (series.data.length > 0 && series.data[0].x < now - 5000) {
            series.data[0].remove(false);
        }

        updateSeuil_audio()

        chart.redraw();
    } catch (error) {
        console.error("Erreur lors du chargement des données :", error);
    }
}


// Rafraîchissement toutes les 500 ms
setInterval(() => {
    chargerDonnees_audio();
    chargerDonnees();
    chargerDonnees_audio();
    chargerDonnees();
    chargerDonnees_audio();
    chargerDonnees();
    chargerDonnees_audio();
    chargerDonnees();
    chargerDonnees_audio();
    chargerDonnees();
    chargerDonnees_audio();
    chargerDonnees();
}, 500);

// Chargement initial
chargerDonnees();
chargerDonnees_audio();
