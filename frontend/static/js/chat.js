(function () {
    const chatToggle = document.getElementById('chat-toggle');
    const chatWindow = document.getElementById('chat-window');
    const closeChat = document.getElementById('close-chat');
    const maximizeChat = document.getElementById('maximize-chat');
    const collapseChat = document.getElementById('collapse-chat');
    const sendBtn = document.getElementById('send-button');
    const userInput = document.getElementById('user-input');
    const chatMessages = document.getElementById('chat-messages');
    const langSelector = document.getElementById('language-selector');

    const emojiBtn = document.getElementById('emoji-btn');
    const emojiPanel = document.getElementById('emoji-panel');
    const ayuMood = document.getElementById('ayu-mood');

    let isLearning = false;
    let pendingQuestion = "";

    // Emoji Picker Logic (Panel)
    emojiBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        emojiPanel.classList.toggle('hidden');
    });

    emojiPanel.addEventListener('click', (e) => {
        if (e.target.tagName === 'SPAN') {
            userInput.value += e.target.textContent;
            userInput.focus();
            emojiPanel.classList.add('hidden');
        }
    });

    // Close emoji panel if clicking elsewhere
    document.addEventListener('click', (e) => {
        if (!emojiBtn.contains(e.target) && !emojiPanel.contains(e.target)) {
            emojiPanel.classList.add('hidden');
        }
    });

    // Toggle Chat Window (Open/Close)
    chatToggle.addEventListener('click', () => {
        chatWindow.classList.toggle('hidden');
        chatToggle.classList.toggle('hidden');
    });

    closeChat.addEventListener('click', () => {
        chatWindow.classList.add('hidden');
        chatToggle.classList.remove('hidden');
    });

    // Maximize/Restore Logic
    maximizeChat.addEventListener('click', () => {
        chatWindow.classList.toggle('maximized');
        chatWindow.classList.remove('collapsed'); // Restore if collapsed
        const icon = maximizeChat.querySelector('i');
        if (chatWindow.classList.contains('maximized')) {
            icon.className = 'fas fa-compress-alt';
        } else {
            icon.className = 'fas fa-expand-alt';
        }
    });

    // Collapse Logic
    collapseChat.addEventListener('click', () => {
        chatWindow.classList.toggle('collapsed');
        const icon = collapseChat.querySelector('i');
        if (chatWindow.classList.contains('collapsed')) {
            icon.className = 'fas fa-plus';
        } else {
            icon.className = 'fas fa-minus';
        }
    });

    // Update Mood Indicator
    function updateMood(emotion) {
        const moods = {
            'happy': '😊',
            'stressed': '😟',
            'sad': '🥺',
            'angry': '😡',
            'neutral': '😇'
        };
        ayuMood.textContent = moods[emotion] || '😊';
    }

    // Append Image Logic
    function appendImage(type) {
        const images = {
            'decoration': 'static/images/wedding_deco.png',
            'beach_deco': 'static/images/beach_deco.png',
            'dress': 'static/images/wedding_dress.png',
            'venue': 'static/images/wedding_venue.png'
        };
        const imgPath = images[type];
        if (imgPath) {
            const msgDiv = document.createElement('div');
            msgDiv.className = 'message bot';
            msgDiv.innerHTML = `<div class="text"><img src="${imgPath}" alt="${type}" class="bot-image"><br>I have generated this visual for your ${type.replace('_', ' ')}! ✨</div>`;
            chatMessages.appendChild(msgDiv);
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
    }

    async function generateDynamicImage(type) {
        const typingId = appendMessage('bot', '🎨 Ayu is generating your visual...', true);
        setTimeout(() => {
            const typingEl = document.getElementById(typingId);
            if (typingEl) typingEl.remove();
            appendImage(type);
        }, 2500);
    }

    // Send Message Logic
    async function sendMessage() {
        const message = userInput.value.trim();
        const lang = langSelector.value;

        if (!message) return;

        // Append User Message
        appendMessage('user', message);
        userInput.value = '';

        // Check if we are in learning mode
        if (isLearning) {
            localStorage.setItem('ayu_learned_' + pendingQuestion.toLowerCase(), message);
            isLearning = false;
            pendingQuestion = "";
            appendMessage('bot', "Thank you! 🙏 I have learned about this now. I will remember it for next time! 🧠✨");
            return;
        }

        // Check Local Storage for learned answers first
        const learnedAnswer = localStorage.getItem('ayu_learned_' + message.toLowerCase());
        if (learnedAnswer) {
            const typingId = appendMessage('bot', 'Ayu is thinking...', true);
            setTimeout(() => {
                const typingEl = document.getElementById(typingId);
                if (typingEl) typingEl.remove();
                appendMessage('bot', "Based on what you taught me: " + learnedAnswer + " 📚");
                if (window.voiceAssistant) window.voiceAssistant.speak(learnedAnswer);
            }, 600);
            return;
        }

        // Check for Image Generation Request
        const lowMsg = message.toLowerCase();
        const isGenRequest = lowMsg.includes('generate') || lowMsg.includes('visual') || lowMsg.includes('show me') || lowMsg.includes('provide');
        
        if (isGenRequest) {
            if (lowMsg.includes('beach')) {
                generateDynamicImage('beach_deco');
                return;
            }
            if (lowMsg.includes('decoration')) {
                generateDynamicImage('decoration');
                return;
            }
            if (lowMsg.includes('dress') || lowMsg.includes('attire')) {
                generateDynamicImage('dress');
                return;
            }
            if (lowMsg.includes('venue')) {
                generateDynamicImage('venue');
                return;
            }
        }

        // Typing Indicator
        const typingId = appendMessage('bot', 'Ayu is thinking...', true);

        try {
            const response = await fetch('http://127.0.0.1:5000/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message, lang })
            });

            const data = await response.json();

            // Remove typing indicator
            const typingEl = document.getElementById(typingId);
            if (typingEl) typingEl.remove();

            // Update Ayu's Mood
            updateMood(data.emotion_detected);

            // Append Bot Response
            appendMessage('bot', data.response);

            // Image Generation Support (Smart Suggestion)
            const lowMsg = message.toLowerCase();
            if (lowMsg.includes('decoration') || lowMsg.includes('idea')) appendImage('decoration');
            if (lowMsg.includes('dress') || lowMsg.includes('wear') || lowMsg.includes('clothes')) appendImage('dress');
            if (lowMsg.includes('venue') || lowMsg.includes('place')) appendImage('venue');

            // Check if backend doesn't know the answer
            if (data.intent_detected === "unknown") {
                isLearning = true;
                pendingQuestion = message;
                setTimeout(() => {
                    appendMessage('bot', "Actually, I'm still learning about this. Could you please teach me? What should I say when someone asks this? 📝");
                }, 1000);
            }

            // Trigger Voice if enabled
            if (window.voiceAssistant && data.response) {
                window.voiceAssistant.speak(data.response);
            }

        } catch (error) {
            console.error('Error:', error);
            const typingEl = document.getElementById(typingId);
            if (typingEl) typingEl.remove();
            appendMessage('bot', 'Sorry, I am having trouble connecting to my brain. Please try again later! 😅');
        }
    }

    function appendMessage(sender, text, isTyping = false) {
        const id = 'msg-' + Date.now();
        const msgDiv = document.createElement('div');
        msgDiv.className = `message ${sender}`;
        msgDiv.id = id;
        msgDiv.innerHTML = `<div class="text">${text}</div>`;
        chatMessages.appendChild(msgDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        return id;
    }

    sendBtn.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage();
    });

    // Auto-focus input when opening
    chatToggle.addEventListener('click', () => {
        setTimeout(() => userInput.focus(), 300);
    });
})();
