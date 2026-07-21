document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');
    const chatMessages = document.getElementById('chat-messages');
    const typingIndicator = document.getElementById('typing-indicator');
    const agentList = document.getElementById('agent-list');
    const themeToggle = document.getElementById('theme-toggle');
    const mobileMenuBtn = document.getElementById('mobile-menu-btn');
    const sidebar = document.getElementById('sidebar');
    const sidebarOverlay = document.getElementById('sidebar-overlay');
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

    // Mobile Sidebar Toggle
    function toggleSidebar() {
        sidebar.classList.toggle('active');
        sidebarOverlay.classList.toggle('active');
    }

    if (mobileMenuBtn) {
        mobileMenuBtn.addEventListener('click', toggleSidebar);
    }

    if (sidebarOverlay) {
        sidebarOverlay.addEventListener('click', toggleSidebar);
    }

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
                    
                    // Close sidebar on mobile after selecting an agent
                    if (window.innerWidth <= 768) {
                        sidebar.classList.remove('active');
                        sidebarOverlay.classList.remove('active');
                    }
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

    function formatToolName(toolName) {
        return (toolName || 'Tool')
            .replace(/_tool$/, '')
            .replace(/_/g, ' ')
            .replace(/\b\w/g, c => c.toUpperCase());
    }

    function truncateText(text, sentences = 2) {
        const sentencePattern = /[^.!?]*[.!?]+/g;
        const matches = text.match(sentencePattern);
        if (!matches || matches.length <= sentences) return { text, isTruncated: false };
        return {
            text: matches.slice(0, sentences).join(' ').trim(),
            remainder: matches.slice(sentences).join(' ').trim(),
            isTruncated: true
        };
    }

    function addMessage(content, type, agentName = null, sources = [], errors = []) {
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
            // For agent responses, check if content is long and truncate if needed
            const plainText = content.replace(/<[^>]*>/g, '');
            const truncated = truncateText(plainText, 2);

            if (truncated.isTruncated) {
                contentDiv.innerHTML = marked.parse(truncated.text);

                const expandBtn = document.createElement('button');
                expandBtn.className = 'expand-response-btn';
                expandBtn.textContent = 'Show more';

                const hiddenContent = document.createElement('div');
                hiddenContent.className = 'expanded-content hidden';
                hiddenContent.innerHTML = marked.parse(truncated.remainder);

                expandBtn.addEventListener('click', () => {
                    hiddenContent.classList.toggle('hidden');
                    expandBtn.textContent = hiddenContent.classList.contains('hidden') ? 'Show more' : 'Show less';
                });

                contentDiv.appendChild(expandBtn);
                contentDiv.appendChild(hiddenContent);
            } else {
                contentDiv.innerHTML = marked.parse(content);
            }
        } else {
            contentDiv.textContent = content;
        }

        messageDiv.appendChild(contentDiv);
        
        if (sources && sources.length > 0) {
            const sourcesContainer = document.createElement('div');
            sourcesContainer.className = 'sources-container';
            
            const sourcesHeader = document.createElement('div');
            sourcesHeader.className = 'sources-header';
            sourcesHeader.innerHTML = `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="2" y1="12" x2="22" y2="12"></line><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path></svg> Sources: (${sources.length} citations)`;
            sourcesContainer.appendChild(sourcesHeader);
            
            const cardsWrapper = document.createElement('div');
            cardsWrapper.className = 'source-cards-wrapper';
            
            sources.forEach(source => {
                const card = document.createElement('a');
                card.className = 'source-card';
                card.href = source.url;
                card.target = '_blank';
                card.rel = 'noopener noreferrer';
                
                let iconChar = source.domain ? source.domain.charAt(0).toUpperCase() : 'W';
                
                card.innerHTML = `
                    <div class="source-card-icon">${iconChar}</div>
                    <div class="source-card-title">${source.title}</div>
                    <div class="source-card-domain">${source.domain || 'Link'}</div>
                `;
                cardsWrapper.appendChild(card);
            });
            
            sourcesContainer.appendChild(cardsWrapper);
            messageDiv.appendChild(sourcesContainer);
        }

        if (errors && errors.length > 0) {
            const errorsContainer = document.createElement('div');
            errorsContainer.className = 'tool-errors-container';

            const errorsHeader = document.createElement('div');
            errorsHeader.className = 'tool-errors-header';
            const label = errors.length > 1 ? `${errors.length} issues` : '1 issue';
            errorsHeader.innerHTML = `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path><line x1="12" y1="9" x2="12" y2="13"></line><line x1="12" y1="17" x2="12.01" y2="17"></line></svg> ${label} while gathering results`;
            errorsContainer.appendChild(errorsHeader);

            const errorsList = document.createElement('ul');
            errorsList.className = 'tool-errors-list';

            errors.forEach(err => {
                const li = document.createElement('li');
                li.className = 'tool-error-item';

                const toolLabel = document.createElement('span');
                toolLabel.className = 'tool-error-tool';
                toolLabel.textContent = formatToolName(err.tool);
                li.appendChild(toolLabel);
                li.appendChild(document.createTextNode(` ${err.message}`));

                errorsList.appendChild(li);
            });

            errorsContainer.appendChild(errorsList);
            messageDiv.appendChild(errorsContainer);
        }

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
                addMessage(data.response, 'agent', data.agent_name, data.sources, data.errors);
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
