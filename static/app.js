const luxEl = document.getElementById('lux');
const presenceEl = document.getElementById('presence');
const ledEl = document.getElementById('led');
const modeEl = document.getElementById('mode');
const seuil = document.getElementById('seuil');
const seuilVal = document.getElementById('seuilVal');
const intensityBar = document.getElementById('intensityBar');
const intensityText = document.getElementById('intensityText');
const tbody = document.getElementById('historyBody');

async function getJSON(url){ const r = await fetch(url); return r.json(); }
async function postJSON(url, body){ 
  const r = await fetch(url,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body||{})}); 
  return r.json(); 
}

async function refreshState(){
  try{
    const s = await getJSON('/api/state');
    luxEl.textContent = s.lux?.toFixed ? s.lux.toFixed(0) : s.lux;
    presenceEl.textContent = s.presence ? 'oui' : 'non';
    ledEl.textContent = s.led ? 'ON' : 'OFF';
    modeEl.textContent = s.mode;
    seuil.value = s.seuil; seuilVal.textContent = s.seuil;
    const pct = Math.round((s.intensity||0)*100);
    intensityBar.style.width = pct + '%';
    intensityText.textContent = pct + '%';
  }catch(e){ console.error(e); }
}

async function refreshHistory(){
  const data = await getJSON('/api/history');
  tbody.innerHTML = '';
  for(const [ts, led, lux, pres, mode, reason, intensity] of data){
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td>${ts}</td>
      <td>${led}</td>
      <td>${Math.round(lux)}</td>
      <td>${pres ? 'oui':'non'}</td>
      <td>${mode}</td>
      <td>${reason||''}</td>
      <td>${Math.round((intensity||0)*100)}%</td>
    `;
    tbody.appendChild(tr);
  }
}

// Actions
document.getElementById('btn-on').addEventListener('click', async ()=>{
  await postJSON('/api/on'); refreshState(); refreshHistory();
});
document.getElementById('btn-off').addEventListener('click', async ()=>{
  await postJSON('/api/off'); refreshState(); refreshHistory();
});
document.getElementById('btn-man').addEventListener('click', async ()=>{
  await postJSON('/api/mode',{mode:'MANUEL'}); refreshState();
});
document.getElementById('btn-auto').addEventListener('click', async ()=>{
  await postJSON('/api/mode',{mode:'AUTO'}); refreshState();
});
document.getElementById('btn-clap').addEventListener('click', async ()=>{
  await postJSON('/api/mode',{mode:'CLAP'}); refreshState();
});
seuil.addEventListener('input', ()=>{
  seuilVal.textContent = seuil.value;
});
seuil.addEventListener('change', async ()=>{
  await postJSON('/api/seuil',{seuil: parseInt(seuil.value,10)});
});

document.getElementById('refreshHistory').addEventListener('click', refreshHistory);

// Boucle
refreshState(); refreshHistory();
setInterval(refreshState, 1000);
