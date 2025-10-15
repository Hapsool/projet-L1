
// Maquette front seule : simulation de données + callbacks UI.
// À connecter ensuite à l'API Flask (endpoints /api/state, /api/on, /api/off, /api/mode, /api/seuil)

const luxEl = document.getElementById('lux');
const presenceEl = document.getElementById('presence');
const ledEl = document.getElementById('led');
const modeEl = document.getElementById('mode');
const logEl = document.getElementById('log');
const seuil = document.getElementById('seuil');
const seuilVal = document.getElementById('seuilVal');

let MODE = 'MANUEL';
let LED = 'OFF';
let PRESENCE = 'non';
let LUX = 200;

function log(msg){
  const ts = new Date().toLocaleTimeString();
  logEl.textContent = `[${ts}] ${msg}\n` + logEl.textContent;
}

function render(){
  luxEl.textContent = LUX;
  presenceEl.textContent = PRESENCE;
  ledEl.textContent = LED;
  modeEl.textContent = MODE;
  seuilVal.textContent = seuil.value;
}

function simulateStep(){
  // bruit + pseudo-événements
  const daylight = 500 + 200*Math.sin(Date.now()/5000);
  const noise = (Math.random()-0.5)*40;
  LUX = Math.max(30, Math.floor(daylight + noise));

  // présence aléatoire 10%
  PRESENCE = Math.random() < 0.1 ? 'oui' : 'non';

  if(MODE === 'AUTO'){
    const seuilLux = parseInt(seuil.value, 10);
    if(PRESENCE === 'oui' && LUX < seuilLux){ 
      if(LED !== 'ON'){ LED='ON'; log('AUTO → LED ON'); }
    } else {
      if(LED !== 'OFF'){ LED='OFF'; log('AUTO → LED OFF'); }
    }
  }
  render();
}

// Handlers UI
document.getElementById('btn-on').addEventListener('click', () => {
  LED = 'ON';
  MODE = 'MANUEL';
  log('MANUEL → LED ON');
  render();
});

document.getElementById('btn-off').addEventListener('click', () => {
  LED = 'OFF';
  MODE = 'MANUEL';
  log('MANUEL → LED OFF');
  render();
});

document.getElementById('btn-auto').addEventListener('click', () => {
  MODE = (MODE === 'AUTO') ? 'MANUEL' : 'AUTO';
  log(`Mode basculé → ${MODE}`);
  render();
});

seuil.addEventListener('input', () => {
  seuilVal.textContent = seuil.value;
});

// Simulation
render();
setInterval(simulateStep, 1000);
