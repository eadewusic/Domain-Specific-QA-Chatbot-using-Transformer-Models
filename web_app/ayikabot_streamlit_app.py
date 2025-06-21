import streamlit as st
import time
import re
import random
import json
import csv
from datetime import datetime
from typing import Tuple, Dict, Any
import sys
import os

# Firebase Imports
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Add the current directory to Python path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Try to import transformers, install if needed
try:
    from transformers import TFT5ForConditionalGeneration, T5Tokenizer
except ImportError:
    st.error("Please install transformers: pip install transformers tensorflow")
    st.stop()

# Define your Hugging Face Hub model ID
HUGGING_FACE_MODEL_ID = "Climi/Climate-Education-QA-Chatbot"

# Firebase Initialization
# Use st.cache_resource to initialize Firebase only once
@st.cache_resource
def initialize_firestore():
    try:
        # Streamlit Secrets store the JSON as a string
        # We need to parse it back to a dictionary
        firebase_config_json = json.loads(st.secrets["FIREBASE_CONFIG"])
        
        # Initialize Firebase Admin SDK
        cred = credentials.Certificate(firebase_config_json)
        if not firebase_admin._apps: # Check if app is already initialized
            firebase_admin.initialize_app(cred)
        
        db = firestore.client()
        # Removed the UI success message; logging to console instead.
        print("Firebase Firestore initialized successfully (backend log).")
        return db
    except Exception as e:
        st.error(f"Error initializing Firebase Firestore: {e}. "
                 "Please ensure your 'FIREBASE_CONFIG' secret is correctly set in Streamlit Cloud.")
        return None

# Page configuration
st.set_page_config(
    page_title="AyikaBot - Climate Education Bot",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS (existing CSS remains the same)
st.markdown("""
<style>
/* Header & layout */
.main-header {
    text-align: left;
    padding: 1rem 0;
    color: #fff; /* Assuming a dark background for readability */
    font-size: 2.5rem;
    font-weight: bold;
    margin-bottom: 0.5rem;
}

/* Multicolored Ayika styling */
.ayika-multicolor {
    background: linear-gradient(45deg, #2E7D32, #D32F2F, #2E7D32, #D32F2F);
    background-size: 400% 400%;
    background-clip: text;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: gradient-shift 3s ease-in-out infinite;
    display: inline;
}

@keyframes gradient-shift {
    0%, 100% { background-position: 0% 50%; }
    25% { background-position: 100% 50%; }
    50% { background-position: 100% 100%; }
    75% { background-position: 0% 100%; }
}

.subtitle {
    color: #fff; /* Assuming a dark background for readability */
    font-size: 1.1rem;
    margin-bottom: 2rem;
    text-align: left;
}
.chat-container {
    max-width: 800px;
    margin: 0 auto;
}
.user-message, .bot-message {
    padding: 1rem;
    border-radius: 15px;
    margin: 0.5rem;
    word-wrap: break-word; /* Ensure long words wrap */
}
.user-message {
    background-color: #1976D220;
    margin-left: 2rem;
    text-align: right;
}
.bot-message {
    background-color: #2E7D3220;
    margin-right: 2rem;
    text-align: left;
}
.message-author {
    font-weight: bold;
    font-size: 0.9rem;
    margin-bottom: 0.3rem;
}
.input-container, .metrics-container {
    max-width: 800px;
    margin: 2rem auto;
}
.thinking-indicator {
    color: white;
    font-size: 0.95rem;
    margin-bottom: 10px;
    font-weight: 500;
}

/* Main green button: Ask AyikaBot */
div[data-testid="stButton"]:nth-of-type(1) > button {
    background-color: #2E7D32 !important;
    color: white !important;
    font-weight: bold;
    border: 2px solid #2E7D32 !important;
    border-radius: 8px;
    padding: 0.6em 1.2em;
    height: 3em;
    transition: 0.3s ease-in-out;
}

/* Hover effect for green button */
div[data-testid="stButton"]:nth-of-type(1) > button:hover {
    background-color: transparent !important;
    color: white !important;
    border: 2px solid #2E7D32 !important;
}

/* Clear Chat button (light gray) */
div[data-testid="stButton"]:nth-of-type(2) > button {
    background-color: #E0E0E0 !important;
    color: #333 !important;
    font-weight: bold;
    border-radius: 8px;
    border: none;
    height: 3em;
}

/* Ensure main content is centered and has max width */
.st-emotion-cache-z5fcl4 { 
    max-width: 800px;
    margin: 0 auto;
}

/* Sidebar styling for better contrast */
.st-emotion-cache-1wp42u4 { 
    background-color: #1a1a1a; 
    color: #f0f0f0; 
    padding: 20px;
    border-right: 1px solid #333;
}

.st-emotion-cache-1ym3sml { 
    background-color: #1a1a1a;
}
</style>
""", unsafe_allow_html=True)


# Domain Detection Constants (remain unchanged)
CLIMATE_KEYWORDS = {
    'core_climate': ['climate', 'global warming', 'greenhouse', 'carbon dioxide', 'co2', 'emissions', 'temperature'],
    'environmental': ['environment', 'pollution', 'sustainability', 'renewable energy', 'fossil fuels', 'deforestation'],
    'climate_impacts': ['sea level', 'glaciers', 'drought', 'flooding', 'extreme weather', 'ocean acidification'],
    'climate_solutions': ['renewable', 'solar', 'wind', 'electric vehicles', 'carbon capture', 'reforestation']
}

NON_CLIMATE_TOPICS = {
    'technology': ['computer', 'software', 'programming', 'coding'],
    'sports': ['football', 'basketball', 'soccer', 'tennis'],
    'entertainment': ['movie', 'music', 'celebrity', 'actor'],
    'food': ['recipe', 'cooking', 'restaurant', 'food'],
    'general': ['capital', 'country', 'geography', 'population']
}

GREETING_KEYWORDS = [
    'hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening', 
    'greetings', 'howdy', 'what\'s up', 'whats up', 'sup', 'yo', 'hiya'
]

GREETING_RESPONSES = [
    "Hello! I'm AyikaBot, your climate education companion. I'm here to help you learn about climate change, environmental impacts, and sustainability solutions. What would you like to explore today?",
    "Hi there! Great to meet you! I'm passionate about helping people understand climate science and environmental issues. What climate topic can I help you with?",
    "Hey! Welcome to AyikaBot. I'm excited to share knowledge about our planet's climate and how we can protect it. What would you like to learn about?",
    "Hello! I'm AyikaBot, and I love talking about climate science, renewable energy, and environmental solutions. What climate question is on your mind?",
    "Hi! Nice to see you here. I'm your friendly climate education bot, ready to explore topics like global warming, sustainability, and environmental protection with you. What interests you most?"
]

@st.cache_resource
def load_ayikabot_model(model_id): # Changed from model_path to model_id
    """Load the AyikaBot model and tokenizer from Hugging Face Hub"""
    try:
        tokenizer = T5Tokenizer.from_pretrained(model_id)
        model = TFT5ForConditionalGeneration.from_pretrained(model_id)
        return tokenizer, model
    except Exception as e:
        st.error(f"Error loading model from Hugging Face Hub ({model_id}): {str(e)}. Please check your model ID and internet connection.")
        return None, None

def is_greeting(question: str) -> bool:
    """Check if the input is a greeting"""
    question_lower = question.lower().strip()
    cleaned = re.sub(r'[^\w\s]', '', question_lower)
    
    for greeting in GREETING_KEYWORDS:
        if cleaned == greeting or cleaned.startswith(greeting + ' ') or cleaned.endswith(' ' + greeting):
            return True
    
    if len(cleaned.split()) <= 2 and any(greeting in cleaned for greeting in ['hi', 'hello', 'hey']):
        return True
        
    return False

# Firestore Logging Functions
def log_user_interaction(db, question: str, response: str, metadata: Dict[str, Any], session_id: str = None):
    """
    Log user interactions to Firestore.
    """
    try:
        if session_id is None:
            session_id = st.session_state.get('session_id', f"session_{int(time.time())}")
            st.session_state.session_id = session_id
        
        log_entry = {
            'timestamp': datetime.now(), # Store as datetime object for Firestore
            'session_id': session_id,
            'user_question': question,
            'bot_response': response,
            'response_type': metadata.get('response_type', 'unknown'),
            'is_climate_related': metadata.get('is_climate', False),
            'confidence_score': metadata.get('confidence', 0.0),
            'detection_reason': metadata.get('reason', ''),
            'generation_time': metadata.get('generation_time', 0.0),
            'question_length': len(question),
            'response_length': len(response)
        }
        
        # Add document to 'interactions' collection
        db.collection('interactions').add(log_entry)
        # print(f"Logged interaction for session {session_id}") # For debugging in logs
            
    except Exception as e:
        st.warning(f"Failed to log interaction to Firestore: {e}")
        print(f"Firestore logging error (interaction): {e}")


def log_session_summary(db):
    """
    Log session summary to Firestore.
    """
    try:
        if st.session_state.get('chat_history') and len(st.session_state.chat_history) > 0:
            session_id = st.session_state.get('session_id', f"session_{int(time.time())}")
            stats = st.session_state.session_stats
            
            summary = {
                'timestamp': datetime.now(), # Store as datetime object
                'session_id': session_id,
                'total_questions': stats['questions_asked'],
                'climate_questions': stats['climate_questions'],
                'rejected_questions': stats['rejected_questions'],
                'total_time': stats['total_time'],
                'avg_response_time': stats['total_time'] / max(stats['climate_questions'], 1) if stats['climate_questions'] > 0 else 0,
                'session_duration_interactions': len(st.session_state.chat_history),
                'engagement_score': stats['climate_questions'] / max(stats['questions_asked'], 1) if stats['questions_asked'] > 0 else 0
            }
            
            # Add document to 'session_summaries' collection
            db.collection('session_summaries').add(summary)
            # print(f"Logged session summary for session {session_id}") # For debugging in logs
                
    except Exception as e:
        st.warning(f"Failed to log session summary to Firestore: {e}")
        print(f"Firestore logging error (summary): {e}")

def export_training_data(db):
    """
    Export logged data from Firestore in format suitable for model training.
    """
    try:
        training_data = []
        
        # Fetch all climate-related interactions from Firestore
        # For very large datasets, consider fetching in batches or filtering by date.
        interactions_ref = db.collection('interactions')
        query = interactions_ref.where('is_climate_related', '==', True).where('response_type', '==', 'climate_answer')
        
        docs = query.stream() # Get all documents matching the query
        
        for doc in docs:
            entry = doc.to_dict()
            training_data.append({
                'input': f"question: {entry.get('user_question', '')}",
                'output': entry.get('bot_response', ''),
                'metadata': {
                    'confidence': entry.get('confidence_score', 0.0),
                    'timestamp': entry.get('timestamp', datetime.now()).isoformat()
                }
            })
        
        if training_data:
            # For demonstration, we'll offer a download button.
            # In a real training pipeline, you'd integrate this with your ML workflow
            # (e.g., download, then process, then train).
            training_json = json.dumps(training_data, ensure_ascii=False, indent=2)
            st.download_button(
                label="Download Training Data (JSON)",
                data=training_json,
                file_name=f"ayikabot_training_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                help="Downloads all climate-related Q&A from Firestore for retraining."
            )
            return len(training_data)
        
        return None # Return None if no training data is found
            
    except Exception as e:
        st.error(f"Error exporting training data from Firestore: {e}")
        print(f"Firestore training data export error: {e}")
        return None

def get_greeting_response() -> str:
    """Get a random greeting response"""
    return random.choice(GREETING_RESPONSES)

def is_climate_related(question: str) -> Tuple[bool, float, str]:
    """
    Determine if a question is climate-related, return (is_climate, confidence, reason)
    """
    question_lower = question.lower().strip()
    # Remove common question words for better keyword matching
    cleaned = re.sub(r'\b(what|how|why|when|where|who|can|is|are|do|does|will|would|could|should)\b', '', question_lower)
    
    score, matches, keywords = 0, [], []
    weights = {'core_climate': 4.0, 'environmental': 2.0, 'climate_impacts': 2.5, 'climate_solutions': 2.5}
    
    for cat, kws in CLIMATE_KEYWORDS.items():
        found = [kw for kw in kws if kw in cleaned]
        if found:
            matches.append(cat)
            keywords.extend(found)
            score += len(found) * weights.get(cat, 1.0)
    
    max_score = sum(len(kws) * weights.get(cat, 1.0) for cat, kws in CLIMATE_KEYWORDS.items())
    confidence = min(score / max_score * 10, 1.0) if max_score > 0 else 0.0
    reason = f"Keywords: {', '.join(keywords[:3])}" if matches else "No climate keywords detected"
    
    return confidence > 0.08, confidence, reason

def detect_non_climate_topics(question: str) -> Tuple[bool, str]:
    """Detect if question is about non-climate topics"""
    q = question.lower()
    for topic, kws in NON_CLIMATE_TOPICS.items():
        if any(kw in q for kw in kws):
            return True, topic
    return False, ""

def generate_climate_response(question: str, tokenizer, model) -> str:
    """Generate response using the climate model"""
    try:
        prompt = f"question: {question.strip()}"
        inputs = tokenizer(prompt, return_tensors="tf") 
        output_ids = model.generate(
            inputs.input_ids,
            attention_mask=inputs.attention_mask,
            max_length=100,
            min_length=20,
            temperature=0.7,
            do_sample=True,
            top_p=0.9,
            top_k=50,
            repetition_penalty=1.2,
            num_beams=2,
            early_stopping=True,
            pad_token_id=tokenizer.pad_token_id,
            eos_token_id=tokenizer.eos_token_id
        )
        answer = tokenizer.decode(output_ids[0], skip_special_tokens=True)
        
        for prefix in ["question:", "answer:", "response:"]:
            if answer.lower().startswith(prefix):
                answer = answer[len(prefix):].strip()
        
        return answer if len(answer.split()) >= 8 else f"I can provide information about this climate topic: {answer}"
    except Exception as e:
        print(f"Error generating response: {e}") 
        return "I encountered an issue generating a response. Please try rephrasing your question."

def process_user_question(question: str, tokenizer, model) -> Tuple[str, dict]:
    """Process user question and return response with metadata"""
    start = time.time()
    
    if is_greeting(question):
        response = get_greeting_response()
        return response, {
            'is_climate': False,
            'confidence': 0.0,
            'reason': "Greeting detected",
            'response_type': "greeting",
            'generation_time': time.time() - start
        }
    
    is_climate, confidence, reason = is_climate_related(question)
    is_non_climate, topic = detect_non_climate_topics(question)
    
    if is_non_climate and confidence < 0.2:
        response = f"I'm a climate education chatbot. Your question appears to be about {topic.title()}. I'd love to help you learn about climate science instead! Try asking about global warming, renewable energy, or environmental impacts."
        response_type = "rejected"
    elif not is_climate or confidence < 0.05:
        response = "I specialize in climate education! Please ask a climate-related question about topics like global warming, sustainability, renewable energy, or environmental impacts."
        response_type = "redirect"
    else:
        response = generate_climate_response(question, tokenizer, model)
        response_type = "climate_answer"
    
    return response, {
        'is_climate': is_climate,
        'confidence': confidence,
        'reason': reason,
        'response_type': response_type,
        'generation_time': time.time() - start
    }

def main():
    # Initialize Firestore client
    db = initialize_firestore()
    if db is None: # If Firestore failed to initialize, stop the app
        st.stop()

    with st.sidebar:
        # Changed from external image URL to a local emoji
        st.markdown("<div style='text-align:center; margin-bottom:2px; font-size: 4.5rem;'>🌍</div>", unsafe_allow_html=True)
        st.subheader("🌿 About AyikaBot")
        st.write("I'm an AI chatbot specialized in climate education. Ask me anything about climate science, environmental impacts, or sustainability solutions!")
        st.markdown("---")
        st.subheader("How to Use")
        st.markdown("""
        - Type your climate-related question in the input box
        - Press Enter or click "Ask AyikaBot" to get your answer
        - Use "Clear Chat" to start a new conversation
        - Tip: Be specific about what you want to learn for best answers. Try asking about:
            - What is global warming?
            - How do solar panels work?
            - What can I do about climate change?
            - How does deforestation affect climate?
            - What are renewable energy sources?
        """)
        
        st.markdown("---")
        st.subheader("Data & Training")
        
        # Add logging info and export functionality
        if st.button("Export Training Data", help="Export logged interactions for model improvement"):
            with st.spinner("Fetching training data from Firestore..."):
                count = export_training_data(db) # Pass db to export function
                if count is not None: # Check for None explicitly for successful export (even if 0)
                    st.success(f"Exported {count} training examples! Click the 'Download Training Data (JSON)' button above.")
                else:
                    st.info("No training data available in Firestore or export failed.")
        
        st.markdown("""
        <small>
        <em>AyikaBot logs interactions to improve climate education responses. 
        Only climate-related Q&A pairs are used for training. 
        </small>
        """, unsafe_allow_html=True)
    
    # Initialize session state
    session_keys = {
        'chat_history': [],
        'session_stats': {'climate_questions': 0, 'rejected_questions': 0, 'total_time': 0, 'questions_asked': 0},
        'is_thinking': False,
        'last_processed_input': "",
        'input_key_counter': 0,
        'pending_question': ""
    }
    
    for key, default_value in session_keys.items():
        if key not in st.session_state:
            st.session_state[key] = default_value

    # Load model using the Hugging Face Hub ID
    tokenizer, model = load_ayikabot_model(HUGGING_FACE_MODEL_ID)
    if not tokenizer or not model:
        st.error("Failed to load the climate education model. Please ensure the model ID is correct and accessible on Hugging Face Hub.")
        st.stop() # Stop the app if model fails to load

    col1, col2, col3 = st.columns([1, 6, 1])
    with col2:
        st.markdown('<h1 class="main-header">🌿 <span class="ayika-multicolor">Ayika</span>Bot - Climate Education</h1>', unsafe_allow_html=True)
        st.markdown('<p class="subtitle">A cooler planet starts with informed minds. How can I help you learn about climate change today?</p>', unsafe_allow_html=True)

        # Chat history display
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        for chat in st.session_state.chat_history:
            st.markdown(f'<div class="user-message"><div class="message-author">You</div>{chat["question"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="bot-message"><div class="message-author">AyikaBot</div>{chat["response"]}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Show thinking indicator if bot is thinking
        if st.session_state.is_thinking:
            st.markdown("""
            <div class="thinking-indicator">
                🌿 AyikaBot is thinking...
            </div>
            """, unsafe_allow_html=True)

        # Input field with dynamic key to force clearing
        user_question = st.text_input(
            label="Your question:",
            placeholder="Ask me about climate change, environment, or sustainability...",
            key=f"user_input_{st.session_state.input_key_counter}",
            label_visibility="collapsed"
        )

        col_btn1, col_btn2 = st.columns(2)
        ask_button = col_btn1.button("Ask AyikaBot", use_container_width=True)
        clear_button = col_btn2.button("Clear Chat", use_container_width=True)

        # Handle input submission (Enter key or button click)
        if (ask_button and user_question.strip()) or (user_question and user_question.strip() and user_question != st.session_state.get("last_processed_input", "")):
            question_to_process = user_question.strip()
            st.session_state.pending_question = question_to_process
            st.session_state.is_thinking = True
            st.session_state.input_key_counter += 1   
            st.rerun()
        
        # Process pending question if we're thinking
        if st.session_state.is_thinking and st.session_state.get("pending_question"):
            question_to_process = st.session_state.pending_question
            
            response, metadata = process_user_question(question_to_process, tokenizer, model)
            stats = st.session_state.session_stats
            stats['questions_asked'] += 1
            
            if metadata['response_type'] == 'climate_answer':
                stats['climate_questions'] += 1
                stats['total_time'] += metadata['generation_time']
            else:
                stats['rejected_questions'] += 1
                
            st.session_state.chat_history.append({'question': question_to_process, 'response': response, 'metadata': metadata})
            st.session_state.last_processed_input = question_to_process
            
            # Log the interaction to Firestore
            log_user_interaction(db, question_to_process, response, metadata)
            
            st.session_state.is_thinking = False
            st.session_state.pending_question = ""
            st.rerun()

        # Display metrics if there are questions asked
        if st.session_state.session_stats['questions_asked'] > 0:
            st.markdown('<div class="metrics-container">', unsafe_allow_html=True)
            cols = st.columns(4)
            stats = st.session_state.session_stats
            avg_time = stats['total_time'] / max(stats['climate_questions'], 1) if stats['climate_questions'] > 0 else 0
            cols[0].metric("Questions", stats['questions_asked'])
            cols[1].metric("Climate Topics", stats['climate_questions'])
            cols[2].metric("Redirected", stats['rejected_questions'])
            cols[3].metric("Avg Time", f"{avg_time:.1f}s")
            st.markdown('</div>', unsafe_allow_html=True)

        # Handle clear chat button
        if clear_button:
            # Log session summary to Firestore before clearing
            log_session_summary(db)
            
            for key, default_value in session_keys.items():
                st.session_state[key] = default_value
            st.session_state.input_key_counter += 1   
            
            st.session_state.session_id = f"session_{int(time.time())}"
            st.rerun()

        # Footer
        st.markdown("---")
        st.markdown("""
        <div style='text-align: center; color: #888; padding: 1rem;'>
            <p>🌿 <strong>AyikaBot</strong> — AI for Climate Education</p>
            <p><em>© Built by Eunice Adewusi Climiradi - 2025</em></p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
