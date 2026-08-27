# Final Project Report: Ayu AI Wedding Planner 🇱🇰💍

## 1. Project Overview
Ayu AI is a premium, multi-cultural Sri Lankan wedding planning assistant designed to provide expert guidance for Buddhist, Hindu, Christian, and Muslim traditions. The system leverages zero-dependency Natural Language Processing (NLP) to offer an empathetic and intelligent user experience.

## 2. Tools & Technologies
- **Frontend**: HTML5, CSS3 (Vanilla), JavaScript (ES6+).
- **Backend**: Python 3.x, Flask (Lightweight Web Framework).
- **Inference Engine**: Custom Fuzzy Matching (Dice's Similarity Coefficient).
- **NLP**: Character-level N-gram analysis for typo tolerance.
- **Voice**: Web Speech API (Recognition & Synthesis).
- **Data Storage**: JSON-based Knowledge Base and Training Data.
- **Packaging**: PyInstaller (for .exe generation).

## 3. Features & Functions
- **Multi-Cultural Intelligence**: Specialized knowledge for 4 major Sri Lankan wedding traditions.
- **Emotional Intelligence 2.0**: Real-time sentiment detection (Happy, Stressed, Sad, Angry) with visual mood indicators.
- **Active Learning**: Ability to learn new information from users in real-time via local storage.
- **Typo Tolerance**: High-performance fuzzy matching for resilient query understanding.
- **Voice Assistant**: Full voice-to-text input (with real-time display) and text-to-speech output.
- **Smart Image Generation**: Automated visual inspiration for decorations, attire, and venues.
- **Glassmorphism UI**: Premium, draggable, and responsive interface design.

## 4. Methodology & Approach
The project follows a **Modular 3-Tier Architecture**:
1. **Presentation Layer**: Responsive web interface.
2. **Logic Layer**: Python AI engine for intent and emotion classification.
3. **Data Layer**: Structured JSON knowledge repository.

### AI Approach
Instead of heavy external ML libraries, Ayu uses a **Custom Scoring Algorithm** that combines keyword matching with bigram similarity. This ensures the app is lightweight, privacy-focused, and extremely fast.

## 5. Requirements Analysis
### Functional Requirements
- Identify user intent and culture from natural language.
- Provide factual wedding information from the KB.
- Recognize and respond to user emotions empathetically.
- Support voice input and real-time speech feedback.

### Non-Functional Requirements
- **Performance**: Response time < 500ms.
- **Robustness**: Handles misspelled inputs (e.g., "budjet").
- **Accessibility**: Support for Sinhala, Tamil, and English.
- **Portability**: Standalone executable with no dependencies.

## 6. Testing & Results
- **Unit Testing**: Verified custom fuzzy matching logic (100% pass rate).
- **Emotional Testing**: Validated empathy prefixes for mixed-text sentences.
- **System Testing**: End-to-end verification of voice and image features.
- **Typo Resilience**: Successfully handled variations like "angery", "budhist", and "nikha".

## 7. User Manual
1. **Open the App**: Run the generated `AyuAI.exe`.
2. **Chat**: Type or use the **Mic icon** to speak.
3. **Emoji Picker**: Click the 😊 icon to add emojis to your message.
4. **Learn Mode**: If Ayu doesn't know an answer, follow the prompt to teach her!
5. **Mute/Unmute**: Click the **Speaker icon** to toggle voice output instantly.
6. **Move Ayu**: Click and drag **anywhere** on the chat window to reposition it.

## 8. Limitations & Future Enhancements
### Limitations
- Currently relies on a local KB; not connected to live APIs for vendor prices.
- Voice recognition depends on browser/OS support.

### Future Enhancements
- Integration with live Sri Lankan wedding vendor APIs.
- Vector database integration for full-sentence semantic search.
- Advanced Admin Dashboard for KB management.

## 9. Conclusion
Ayu AI demonstrates the power of a customized, lightweight AI engine tailored for a specific cultural niche. It provides a seamless, empathetic, and visually stunning solution for modern Sri Lankan wedding planning.
