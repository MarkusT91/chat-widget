const toggle = document.getElementById('toggle');
const box    = document.getElementById('box');
const msgs   = document.getElementById('messages');
const inp    = document.getElementById('input');
const send   = document.getElementById('send');

const TOKEN  = 'X8f71aBzX78zuvJK$k';
const API    = 'fa-chat-widget.azurewebsites.net';

toggle.onclick = () =>
  box.style.display = box.style.display === 'none' ? 'flex' : 'none';

send.onclick = async () => {
  const text = inp.value.trim();
  if (!text) return;
  msgs.innerHTML += `<div>User: ${text}</div>`;
  inp.value = '';
  msgs.innerHTML += `<div id="loading">…</div>`;
  try {
    const res = await fetch(API, {
      method: 'POST',
      headers: { 'Content-Type':'application/json','X-Chat-Token':TOKEN },
      body: JSON.stringify({ message: text })
    });
    const { reply } = await res.json();
    document.getElementById('loading').remove();
    msgs.innerHTML += `<div>Bot: ${reply}</div>`;
    msgs.scrollTop = msgs.scrollHeight;
  } catch {
    document.getElementById('loading').remove();
    msgs.innerHTML += `<div style="color:red">Fehler</div>`;
  }
};
