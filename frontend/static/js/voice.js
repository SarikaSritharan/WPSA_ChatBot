(function() {
    class VoiceAssistant {
        constructor() {
            this.recognition = null;
            this.synth = window.speechSynthesis;
            this.isSpeaking = true;
            this.isListening = false;
            
            this.micBtn = document.getElementById('voice-input');
            this.speakerBtn = document.getElementById('speaker-toggle');
            this.cancelBtn = document.getElementById('cancel-voice');
            this.waveContainer = document.getElementById('wave-container');
            this.langSelector = document.getElementById('language-selector');
            this.userInput = document.getElementById('user-input');

            this.isCancelled = false;

            this.initRecognition();
            this.attachEvents();
        }

        initRecognition() {
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            if (SpeechRecognition) {
                this.recognition = new SpeechRecognition();
                this.recognition.continuous = false;
                this.recognition.interimResults = true;

                this.recognition.onstart = () => {
                    this.isListening = true;
                    this.isCancelled = false;
                    this.micBtn.classList.add('active');
                    this.waveContainer.classList.remove('hidden');
                };

                this.recognition.onend = () => {
                    this.isListening = false;
                    this.micBtn.classList.remove('active');
                    this.waveContainer.classList.add('hidden');
                };

                this.recognition.onresult = (event) => {
                    if (this.isCancelled) return;
                    
                    let interimTranscript = '';
                    for (let i = event.resultIndex; i < event.results.length; ++i) {
                        if (event.results[i].isFinal) {
                            this.userInput.value = event.results[i][0].transcript;
                            document.getElementById('send-button').click();
                        } else {
                            interimTranscript += event.results[i][0].transcript;
                            this.userInput.value = interimTranscript;
                        }
                    }
                };
            } else {
                console.warn("Speech recognition not supported in this browser.");
                this.micBtn.style.display = 'none';
            }
        }

        attachEvents() {
            this.micBtn.addEventListener('click', () => {
                if (this.isListening) {
                    this.recognition.stop();
                } else {
                    this.recognition.lang = this.getLangCode();
                    this.recognition.start();
                }
            });

            this.cancelBtn.addEventListener('click', () => {
                this.isCancelled = true;
                this.recognition.abort(); // Immediately stop and discard
                this.userInput.value = '';
                this.waveContainer.classList.add('hidden');
            });

            this.speakerBtn.addEventListener('click', () => {
                this.isSpeaking = !this.isSpeaking;
                this.speakerBtn.innerHTML = this.isSpeaking ? 
                    '<i class="fas fa-volume-up"></i>' : 
                    '<i class="fas fa-volume-mute"></i>';
                
                // Immediately stop current speech if muting
                if (!this.isSpeaking) {
                    this.synth.cancel();
                }
            });
        }

        getLangCode() {
            const lang = this.langSelector.value;
            if (lang === 'si') return 'si-LK';
            if (lang === 'ta') return 'ta-LK';
            return 'en-US';
        }

        speak(text) {
            if (!this.isSpeaking) return;

            // Cancel existing speech
            this.synth.cancel();

            const utterance = new SpeechSynthesisUtterance(text);
            utterance.lang = this.getLangCode();
            
            // Find a suitable voice if possible
            const voices = this.synth.getVoices();
            const langCode = this.getLangCode();
            const voice = voices.find(v => v.lang.startsWith(langCode));
            if (voice) utterance.voice = voice;

            this.synth.speak(utterance);
        }
    }

    const voiceAssistant = new VoiceAssistant();
    window.voiceAssistant = voiceAssistant;
})();
