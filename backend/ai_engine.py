import json
import os
import re
from datetime import datetime

class AyuAI:
    def __init__(self, data_dir):
        self.data_dir = data_dir
        self.kb_path = os.path.join(data_dir, 'knowledge_base.json')
        self.training_path = os.path.join(data_dir, 'training_data.json')
        self.logs_path = os.path.join(data_dir, 'chat_logs.json')
        self.learned_path = os.path.join(data_dir, 'learned_knowledge.json')
        
        self.load_data()
        
    def load_data(self):
        with open(self.kb_path, 'r') as f:
            self.kb = json.load(f)
        with open(self.training_path, 'r') as f:
            self.training = json.load(f)
        
        if os.path.exists(self.learned_path):
            with open(self.learned_path, 'r') as f:
                self.learned_knowledge = json.load(f)
        else:
            self.learned_knowledge = {}

        if os.path.exists(self.logs_path):
            with open(self.logs_path, 'r') as f:
                self.logs = json.load(f)
        else:
            self.logs = []

    def preprocess(self, text):
        return re.sub(r'[^\w\s]', '', text.lower()).strip()

    def _get_bigrams(self, word):
        """Custom helper to generate character bigrams for fuzzy matching."""
        return set(word[i:i+2] for i in range(len(word)-1))

    def _calculate_similarity(self, word1, word2):
        """Custom Sorensen-Dice coefficient implementation for string similarity."""
        if word1 == word2: return 1.0
        if len(word1) < 2 or len(word2) < 2: return 0.0
        
        bigrams1 = self._get_bigrams(word1)
        bigrams2 = self._get_bigrams(word2)
        
        common = len(bigrams1 & bigrams2)
        return (2.0 * common) / (len(bigrams1) + len(bigrams2))

    def fuzzy_match(self, token, keywords, threshold=0.6):
        """Custom fuzzy matcher without using external libraries.
        Ignores very short tokens to avoid false positives with common words.
        """
        if len(token) < 4:
            return False
            
        for keyword in keywords:
            if self._calculate_similarity(token, keyword) >= threshold:
                return True
        return False

    def detect_intent(self, text):
        clean_text = self.preprocess(text)
        tokens = clean_text.split()
        scores = {intent: 0 for intent in self.training['intents']}
        
        for token in tokens:
            for intent, keywords in self.training['intents'].items():
                # Check for direct keyword matches or custom fuzzy matches
                if token in keywords or self.fuzzy_match(token, keywords):
                    scores[intent] += 1
        
        best_intent = max(scores, key=scores.get)
        
        # New Logic: If no intent found but emotion is present, return 'emotion_only'
        if scores[best_intent] == 0:
            emotion = self.detect_emotion(text)
            if emotion != "neutral":
                return "emotion_only"
            return "unknown"
            
        return best_intent

    def detect_emotion(self, text):
        clean_text = self.preprocess(text)
        tokens = clean_text.split()
        scores = {emotion: 0 for emotion in self.training['emotions']}
        
        for token in tokens:
            for emotion, keywords in self.training['emotions'].items():
                # Increased threshold to 0.8 for emotions to avoid false positives
                if token in keywords or self.fuzzy_match(token, keywords, threshold=0.8):
                    scores[emotion] += 1
        
        best_emotion = max(scores, key=scores.get)
        if scores[best_emotion] == 0:
            return "neutral"
        return best_emotion

    def log_query(self, query, intent):
        if intent == "unknown":
            self.logs.append({
                "timestamp": datetime.now().isoformat(),
                "query": query,
                "status": "unrecognized"
            })
            with open(self.logs_path, 'w') as f:
                json.dump(self.logs, f, indent=2)

    def get_response(self, text):
        clean_text = self.preprocess(text)
        
        # 1. Check if this is a "Teaching" command
        if text.lower().startswith("ayu learn:"):
            try:
                content = text[10:].split('=')
                if len(content) == 2:
                    q = self.preprocess(content[0])
                    a = content[1].strip()
                    self.learned_knowledge[q] = a
                    with open(self.learned_path, 'w') as f:
                        json.dump(self.learned_knowledge, f, indent=2)
                    return f"Thank you! I have learned that for '{content[0].strip()}', the answer is: {a} 🧠✨"
            except:
                return "To teach me, please use the format: 'Ayu learn: [question] = [answer]' 📝"

        # 2. Check persistent "learned" memory first
        if clean_text in self.learned_knowledge:
            return "Based on what I've learned: " + self.learned_knowledge[clean_text] + " 📚"

        # 3. Normal processing
        intent = self.detect_intent(text)
        emotion = self.detect_emotion(text)
        self.log_query(text, intent)
        
        # Base responses based on emotion
        emotion_prefix = {
            "happy": "I'm so glad to hear that! It sounds like you're having a wonderful time planning! 😊 ",
            "stressed": "I can feel that you're under a lot of pressure. Please don't worry, I'm here to handle the details for you. Take a deep breath. 🌸 ",
            "sad": "I'm truly sorry to hear you're feeling this way. Wedding planning should be joyful, so let's see how I can make things easier for you. 🫂 ",
            "angry": "I sincerely apologize if I've upset you or if things aren't going as planned. Please tell me how I can fix this. 🥺 ",
            "neutral": ""
        }
        
        prefix = emotion_prefix.get(emotion, "")
        
        # Handle Emotion-Only venting (No "Please teach me" trigger)
        if intent == "emotion_only":
            if emotion == "stressed" or emotion == "sad":
                return prefix + "I'm here to support you. Would you like to talk about your budget, venues, or maybe explore some cultural traditions to take your mind off things? 🕊️"
            if emotion == "happy":
                return prefix + "Your happiness makes me happy too! What's the most exciting thing you're working on right now? 🌟"
            return prefix + "I hear you. I'm here to help with whatever you need for your big day. 💖"

        # Culture Detection (High Priority)
        culture = None
        buddhist_keywords = ["buddhist", "poruwa", "temple", "nilame", "osariya"]
        hindu_keywords = ["hindu", "tamil", "kovil", "thali", "kanchipuram", "veshti"]
        christian_keywords = ["christian", "church", "vows", "gown", "tuxedo"]
        muslim_keywords = ["muslim", "islam", "nikah", "walima", "sherwani"]

        tokens = clean_text.split()
        for token in tokens:
            if token in buddhist_keywords or self.fuzzy_match(token, buddhist_keywords):
                culture = "buddhist"
                break
            if token in hindu_keywords or self.fuzzy_match(token, hindu_keywords):
                culture = "hindu"
                break
            if token in christian_keywords or self.fuzzy_match(token, christian_keywords):
                culture = "christian"
                break
            if token in muslim_keywords or self.fuzzy_match(token, muslim_keywords):
                culture = "muslim"
                break

        # If a culture is detected, check for specific sub-topics
        if culture:
            if any(k in intent or k in clean_text for k in ["ritual", "tradition", "custom", "ceremony", "thali", "poruwa", "nikah", "walima"]):
                return prefix + self.kb[culture]["rituals"] + " ✨"
            if any(k in intent or k in clean_text for k in ["attire", "dress", "clothes", "wear", "suit", "saree", "gown", "veshti", "osariya", "kanchipuram", "sherwani"]):
                return prefix + self.kb[culture]["attire"] + " 👗👔"
            if any(k in intent or k in clean_text for k in ["food", "catering", "eat", "menu", "dinner", "briyani", "kiribath", "sweet"]):
                return prefix + self.kb[culture]["food"] + " 🍛"
            if any(k in intent or k in clean_text for k in ["package", "deal", "offer", "price", "cost"]):
                return prefix + self.kb[culture]["packages"] + " 📦"
            
            # Default culture response
            return prefix + f"What specifically would you like to know about {culture.capitalize()} weddings? I can help with rituals, attire, food, or packages! 💍"

        # General info (If no culture specified)
        if any(k in intent or k in clean_text for k in ["venues", "places", "decoration"]):
            return prefix + self.kb["general"]["venues"] + " 🏛️"
        if intent == "photography":
            return prefix + self.kb["general"]["photography"] + " 📸"
        if intent == "budget":
            return prefix + self.kb["general"]["budget"] + " 💰"
        if intent == "packages" or any(k in clean_text for k in ["package", "deal", "offer"]):
             return prefix + "We offer specialized wedding packages (Budget, Standard, and Premium) for Buddhist, Hindu, Christian, and Muslim traditions. Which cultural tradition are you planning for? 📦✨"
        if intent == "catering":
             return prefix + "Sri Lankan wedding menus vary by culture! For example, Buddhist weddings feature Kiribath, while Muslim weddings are famous for Briyani. Which tradition are you interested in? 🍛"
        if intent == "attire":
             return prefix + "From Kandyan Osariyas to South Indian Kanchipuram sarees, Sri Lankan wedding attire is stunning! Which cultural tradition would you like to know about? 👗"

        # Greetings/Farewells/Help (Lower priority if other info found)
        if intent == "greeting":
            return prefix + "Ayubowan! I am Ayu, your Sri Lankan wedding planner assistant. How can I help you today? 🇱🇰"
        
        if intent == "farewell":
            return prefix + "Goodbye! Wishing you all the best with your wedding planning! 👋"

        if intent == "Thank You":
            return prefix + "You're Welcome! i always here for you wedding plan support & Wishing you all the best with your wedding planning! 👋"

        if intent == "help":
            return prefix + "I can help you plan Buddhist, Hindu, Christian, or Muslim weddings in Sri Lanka. Ask me about rituals, attire, food, venues, or packages! 💍"

        if intent == "unknown":
            return prefix + "I'm not quite sure I understand. Could you please rephrase that or ask about specific cultures like Buddhist, Hindu, Christian, or Muslim weddings? 🤔"
        
        return prefix + "I can help you with wedding rituals, attire, food, venues, and packages for various Sri Lankan traditions. What would you like to explore? 🌟"

# Active Learning helper
def update_training(new_keyword, intent):
    # In a real app, this would be an admin feature
    pass
