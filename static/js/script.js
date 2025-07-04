document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const chatMessages = document.getElementById('chat-messages');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');
    const loadingIndicator = document.getElementById('loading-indicator');
    const historyBtn = document.getElementById('history-btn');
    const historyModal = new bootstrap.Modal(document.getElementById('historyModal'));
    const historyList = document.getElementById('history-list');
    
    // Session management
    const sessionId = 'user_' + Math.random().toString(36).substr(2, 9);
    
    // Auto-expand textarea
    userInput.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = (this.scrollHeight) + 'px';
    });
    
    // Send message on Enter (but allow Shift+Enter for new lines)
    userInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
    
    // Send button click handler
    sendBtn.addEventListener('click', sendMessage);
    
    // History button click handler
    historyBtn.addEventListener('click', showHistory);
    
    function sendMessage() {
        const message = userInput.value.trim();
        if (!message) return;
        
        // Add user message to chat
        addMessage('user', message);
        userInput.value = '';
        userInput.style.height = 'auto';
        
        // Show loading indicator
        loadingIndicator.classList.remove('d-none');
        
        // Scroll to bottom
        scrollToBottom();
        
        // Send to server
        fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: message,
                session_id: sessionId
            })
        })
        .then(response => response.json())
        .then(data => {
            // Hide loading indicator
            loadingIndicator.classList.add('d-none');
            
            if (data.type === 'error') {
                addMessage('assistant', data.message, [], true);
            } else if (data.type === 'response') {
                addMessage('assistant', data.message, data.properties);
            }
            
            scrollToBottom();
        })
        .catch(error => {
            console.error('Error:', error);
            loadingIndicator.classList.add('d-none');
            addMessage('assistant', 'Sorry, an error occurred while processing your request.', [], true);
            scrollToBottom();
        });
    }
    
    function addMessage(sender, message, properties = [], isError = false) {
        const messageDiv = document.createElement('div');
        messageDiv.className = sender + '-message';
        
        if (isError) {
            messageDiv.classList.add('error-message');
        }
        
        messageDiv.innerHTML = `<p>${message}</p>`;
        
        if (properties && properties.length > 0) {
            const propertiesDiv = document.createElement('div');
            propertiesDiv.className = 'properties-container mt-3';
            
            properties.forEach(prop => {
                const propertyCard = document.createElement('div');
                propertyCard.className = 'property-card mb-3';
                
                let thumbnail = '';
                if (prop.thumbnail) {
                    thumbnail = `<img src="${prop.thumbnail}" alt="${prop.title}" class="img-thumbnail float-end" style="max-height: 100px;">`;
                }
                
                propertyCard.innerHTML = `
                    <h5>${prop.title}</h5>
                    ${thumbnail}
                    <p><strong>Price:</strong> $${prop.price.toLocaleString()}</p>
                    <p><strong>Location:</strong> ${prop.location}</p>
                    <p><strong>Bedrooms:</strong> ${prop.bedrooms}, <strong>Bathrooms:</strong> ${prop.bathrooms}</p>
                    <p>${prop.description}</p>
                    <small class="text-muted">Source: ${prop.source}</small>
                `;
                
                propertiesDiv.appendChild(propertyCard);
            });
            
            messageDiv.appendChild(propertiesDiv);
        }
        
        chatMessages.appendChild(messageDiv);
    }
    
    function scrollToBottom() {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    function showHistory() {
        // Fetch history from server
        fetch(`/api/history?session_id=${sessionId}`)
            .then(response => response.json())
            .then(history => {
                historyList.innerHTML = '';
                
                if (history.length === 0) {
                    historyList.innerHTML = '<li class="list-group-item">No history yet</li>';
                    return;
                }
                
                history.forEach(item => {
                    const li = document.createElement('li');
                    li.className = 'list-group-item';
                    
                    if (item.sender === 'user') {
                        li.innerHTML = `
                            <div class="d-flex justify-content-between">
                                <strong>You:</strong>
                                <small class="text-muted">${formatTime(item.timestamp)}</small>
                            </div>
                            <p>${item.message}</p>
                        `;
                    } else {
                        let propertiesInfo = '';
                        if (item.properties && item.properties.length > 0) {
                            propertiesInfo = `<p class="text-success">Found ${item.properties.length} properties</p>`;
                        }
                        
                        li.innerHTML = `
                            <div class="d-flex justify-content-between">
                                <strong>Assistant:</strong>
                                <small class="text-muted">${formatTime(item.timestamp)}</small>
                            </div>
                            <p>${item.message}</p>
                            ${propertiesInfo}
                        `;
                    }
                    
                    historyList.appendChild(li);
                });
                
                historyModal.show();
            });
    }
    
    function formatTime(timestamp) {
        return new Date(timestamp * 1000).toLocaleString();
    }
});