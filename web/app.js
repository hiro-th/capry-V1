const chatMessages = document.getElementById('chatMessages');
const form = document.getElementById('chatForm');
const input = document.getElementById('messageInput');
const sessionIdInput = document.getElementById('sessionId');
const activationInput = document.getElementById('activationCode');

if (!activationInput.value) {
  activationInput.value = 'hiro';
}

function addMessage(role, text) {
  const message = document.createElement('div');
  message.className = `message ${role}`;
  message.textContent = text;
  chatMessages.appendChild(message);
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

form.addEventListener('submit', async (event) => {
  event.preventDefault();
  const text = input.value.trim();
  if (!text) return;

  addMessage('user', text);
  input.value = '';

  const payload = {
    message: text,
    session_id: sessionIdInput.value || 'default',
    activation_code: activationInput.value,
    history: []
  };

  try {
    const response = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.detail || 'Request failed');
    }

    if (!sessionIdInput.value) {
      sessionIdInput.value = data.session_id;
    }

    addMessage('assistant', data.reply);
  } catch (error) {
    addMessage('assistant', `CAPRI error: ${error.message}`);
  }
});
