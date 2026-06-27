document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');
    const chatMessages = document.getElementById('chat-messages');
    const typingIndicator = document.getElementById('typing-indicator');
    const agentList = document.getElementById('agent-list');
    const themeToggle = document.getElementById('theme-toggle');
    const root = document.documentElement;

    // Load saved theme
    if (localStorage.getItem('theme') === 'light') {
        root.setAttribute('data-theme', 'light');
    }

    themeToggle.addEventListener('click', () => {
        if (root.getAttribute('data-theme') === 'light') {
            root.removeAttribute('data-theme');
            localStorage.setItem('theme', 'dark');
        } else {
            root.setAttribute('data-theme', 'light');
            localStorage.setItem('theme', 'light');
        }
    });

    let currentSelectedAgent = 'NovaAssist'; // Default to orchestrator

    async function loadAgents() {
        try {
            const response = await fetch('/api/agents');
            const agents = await response.json();
            
            agentList.innerHTML = '';
            
            agents.forEach(agent => {
                const li = document.createElement('li');
                li.className = `agent-item ${agent.name === currentSelectedAgent ? 'active' : ''}`;
                li.innerHTML = `
                    <div class="agent-name">${agent.name}</div>
                    <div class="agent-desc">${agent.description}</div>
                `;
                
                li.addEventListener('click', () => {
                    document.querySelectorAll('.agent-item').forEach(el => el.classList.remove('active'));
                    li.classList.add('active');
                    currentSelectedAgent = agent.name;
                    addMessage(`Now talking directly to: ${agent.name}`, 'system');
                });
                
                agentList.appendChild(li);
            });
        } catch (error) {
            console.error('Failed to load agents:', error);
        }
    }

    // Load agents on startup
    loadAgents();

    function scrollToBottom() {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function addMessage(content, type, agentName = null) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}`;

        if (agentName && type === 'agent') {
            const label = document.createElement('div');
            label.className = 'agent-label';
            label.textContent = agentName;
            messageDiv.appendChild(label);
        }

        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        
        if (type === 'agent') {
            contentDiv.innerHTML = marked.parse(content);
        } else {
            contentDiv.textContent = content;
        }

        messageDiv.appendChild(contentDiv);
        chatMessages.appendChild(messageDiv);
        scrollToBottom();
    }

    let lastAgent = null;

    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const message = userInput.value.trim();
        if (!message) return;

        // Add user message to chat
        addMessage(message, 'user');
        userInput.value = '';
        userInput.disabled = true;

        // Show typing indicator
        typingIndicator.classList.remove('hidden');
        scrollToBottom();

        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ 
                    message,
                    agent_name: currentSelectedAgent 
                })
            });

            const data = await response.json();

            // Hide typing indicator
            typingIndicator.classList.add('hidden');

            if (data.status === 'success') {
                if (lastAgent !== data.agent_name) {
                    addMessage(`Switched context to ${data.agent_name}`, 'context-switch');
                    lastAgent = data.agent_name;
                }
                // Add agent response
                addMessage(data.response, 'agent', data.agent_name);
            } else {
                addMessage(data.error || 'An error occurred.', 'system');
            }
        } catch (error) {
            typingIndicator.classList.add('hidden');
            addMessage('Network error. Please try again.', 'system');
        } finally {
            userInput.disabled = false;
            userInput.focus();
        }
    });
});
