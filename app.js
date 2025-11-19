// Простой frontend для WebApp. Подключается к backend API.
const API_BASE = (location.hostname === 'localhost' || location.hostname === '127.0.0.1') ? 'http://localhost:8000/api' : `${location.origin}/api`;

const screens = {
  home: document.getElementById('home'),
  profile: document.getElementById('profile'),
  economy: document.getElementById('economy'),
  casino: document.getElementById('casino')
};

function show(name){ Object.values(screens).forEach(s=>s.classList.add('hidden')); screens[name].classList.remove('hidden'); }

// init
document.getElementById('btnProfile').addEventListener('click', ()=>{
  fetchProfile(); show('profile');
});

document.getElementById('btnBackFromProfile').addEventListener('click', ()=> show('home'));

document.getElementById('btnEconomy').addEventListener('click', ()=>{ fetchEconomy(); show('economy'); });
document.getElementById('btnBackFromEconomy').addEventListener('click', ()=> show('home'));

document.getElementById('btnCasino').addEventListener('click', ()=>{ fetchCasinoBalance(); show('casino'); });
document.getElementById('btnBackFromCasino').addEventListener('click', ()=> show('home'));

// Economy actions
document.getElementById('btnBuildFactory').addEventListener('click', async ()=>{
  const res = await apiPost('/build', {type:'factories', amount:1}); alert(res.message || JSON.stringify(res)); fetchEconomy();
});

document.getElementById('btnCollect').addEventListener('click', async ()=>{ const res = await apiPost('/collect'); alert(res.message || JSON.stringify(res)); fetchEconomy(); fetchProfile(); });

// Casino
document.getElementById('btnRoulette').addEventListener('click', async ()=>{
  const bet = Number(document.getElementById('casinoBet').value) || 10;
  const res = await apiPost('/casino/roulette', {bet}); appendCasinoLog(res.message || JSON.stringify(res)); fetchCasinoBalance(); fetchProfile();
});

document.getElementById('btnDice').addEventListener('click', async ()=>{
  const bet = Number(document.getElementById('casinoBet').value) || 20;
  const res = await apiPost('/casino/dice', {bet}); appendCasinoLog(res.message || JSON.stringify(res)); fetchCasinoBalance(); fetchProfile();
});

document.getElementById('btnLottery').addEventListener('click', async ()=>{
  const bet = Number(document.getElementById('casinoBet').value) || 50;
  const res = await apiPost('/casino/lottery', {bet}); appendCasinoLog(res.message || JSON.stringify(res)); fetchCasinoBalance(); fetchProfile();
});

function appendCasinoLog(text){ const el = document.getElementById('casinoLog'); el.textContent = (text || '') + '\n' + el.textContent; }

async function fetchProfile(){ const r = await fetch(API_BASE + '/profile', {method:'GET'}); const data = await r.json(); document.getElementById('profileName').textContent = data.username || 'Профиль'; document.getElementById('profileData').textContent = JSON.stringify(data, null, 2); document.getElementById('userShort').textContent = `${data.username || '-'} • ${data.comm_coins || 0}💰`; }

async function fetchEconomy(){ const r = await fetch(API_BASE + '/economy'); const data = await r.json(); document.getElementById('econData').innerHTML = `Фабрик: ${data.factories}/${data.factory_limit}<br>Ферм: ${data.farms}/${data.farm_limit}<br>Доход при сборе: ${data.income}`; }

async function fetchCasinoBalance(){ const r = await fetch(API_BASE + '/profile'); const data = await r.json(); document.getElementById('casinoBalance').textContent = `Баланс: ${data.comm_coins}💰`; }

// helper
async function apiPost(path, body={}){
  const res = await fetch(API_BASE + path, {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(body)});
  return await res.json();
}

// On load
show('home');
// Try to fetch profile to show short user data
fetchProfile().catch(()=>{});

// Telegram WebApp integration (optional): send init data to server
if(window.Telegram && window.Telegram.WebApp){
  const tg = window.Telegram.WebApp;
  // example: send auth data to backend
  // fetch(API_BASE + '/tg_init', {method:'POST', body: JSON.stringify(tg.initDataRaw)});
}
