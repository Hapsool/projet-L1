
/* --------------infos base de donnée pour afficher sur page information----------*/

fetch("/led/luminosite")
  .then(res => res.json())
  .then(data => {
        const display = document.getElementById('info_luminosite');
        console.log(data.luminosite);
        display.innerText = data.luminosite; // met à jour le texte du h5
  });


/* --------------test pour verif que le fichier js fonctionne----------*/
console.log("JavaScript fonctionne !");

/* --------------graphe test------------------------------*/
// Initialisation du graphique vide
const chart = Highcharts.chart('graphe', {
    chart: { type: 'spline' },
    title: { text: 'Luminosité en temps réel' },
    xAxis: {
        type: 'datetime', // affiche le temps en abscisse
        tickPixelInterval: 150
    },
    yAxis: {
        title: { text: 'Luminosité' },
        min: 0
    },
    series: [{
        name: 'Luminosité LED',
        data: [] // vide au départ
    }]
});

async function chargerDonnees() {
    const response = await fetch("/capteur_lumiere/luminosite");
    const data = await response.json();
    console.log(data);
}

chargerDonnees();

/* raffraichissement des données en temps réel */
setInterval(() => {
  chart.series[0].addPoint(Math.random() * 100, true, true);
}, 1000);