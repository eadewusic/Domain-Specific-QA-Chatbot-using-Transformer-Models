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

# Add the current directory to Python path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Try to import transformers, install if needed
try:
    from transformers import TFT5ForConditionalGeneration, T5Tokenizer
except ImportError:
    st.error("Please install transformers: pip install transformers tensorflow")
    st.stop()

# Page configuration
st.set_page_config(
    page_title="AyikaBot - Climate Education Bot",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
/* Header & layout */
.main-header {
    text-align: left;
    padding: 1rem 0;
    color: #fff;
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
    color: #fff;
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

</style>
""", unsafe_allow_html=True)

# Domain Detection Constants
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

COMPLIMENT_KEYWORDS = [
    'thank you', 'thanks', 'great', 'awesome', 'excellent', 'amazing', 'wonderful',
    'fantastic', 'brilliant', 'helpful', 'nice', 'good job', 'well done', 
    'impressive', 'perfect', 'love it', 'appreciate', 'grateful', 'cool',
    'nice response', 'good response', 'that was helpful', 'very helpful',
    'thx', 'ty', 'good answer', 'great answer', 'smart', 'clever'
]

GREETING_RESPONSES = [
    "Hello! I'm AyikaBot, your climate education companion. I'm here to help you learn about climate change, environmental impacts, and sustainability solutions. What would you like to explore today?",
    "Hi there! Great to meet you! I'm passionate about helping people understand climate science and environmental issues. What climate topic can I help you with?",
    "Hey! Welcome to AyikaBot. I'm excited to share knowledge about our planet's climate and how we can protect it. What would you like to learn about?",
    "Hello! I'm AyikaBot, and I love talking about climate science, renewable energy, and environmental solutions. What climate question is on your mind?",
    "Hi! Nice to see you here. I'm your friendly climate education bot, ready to explore topics like global warming, sustainability, and environmental protection with you. What interests you most?"
]

COMPLIMENT_RESPONSES = [
    "Thank you so much! I'm glad I could help you learn about climate science. What other climate topic would you like to explore?",
    "You're very welcome! I love sharing knowledge about our planet's climate. Is there another environmental question I can help you with?",
    "I appreciate your kind words! Climate education is my passion. What else would you like to know about sustainability or environmental protection?",
    "Thank you! It makes me happy to help people understand climate change better. What other climate topic interests you?",
    "I'm so glad that was helpful! There's so much to learn about climate science. What would you like to explore next?",
    "Thank you for the feedback! I'm here to make climate education accessible and engaging. What other questions do you have about our environment?"
    "I'm thrilled to hear that! Climate education is so important, and I'm here to help. What other topics would you like to discuss?",
    "Thanks! I'm passionate about making climate science understandable. Is there another aspect of climate change you're curious about?"
]

@st.cache_resource
def load_ayikabot_model(model_path):
    """Load the AyikaBot model and tokenizer"""
    try:
        tokenizer = T5Tokenizer.from_pretrained(model_path)
        model = TFT5ForConditionalGeneration.from_pretrained(model_path)
        return tokenizer, model
    except Exception as e:
        st.error(f"Error loading model from {model_path}: {str(e)}")
        return None, None

def is_greeting(question: str) -> bool:
    """Check if the input is a greeting"""
    question_lower = question.lower().strip()
    # Remove punctuation for better matching
    cleaned = re.sub(r'[^\w\s]', '', question_lower)
    
    # Check for exact matches or greetings at the start of the message
    for greeting in GREETING_KEYWORDS:
        if cleaned == greeting or cleaned.startswith(greeting + ' ') or cleaned.endswith(' ' + greeting):
            return True
    
    # Check for very short inputs that are likely greetings
    if len(cleaned.split()) <= 2 and any(greeting in cleaned for greeting in ['hi', 'hello', 'hey']):
        return True
        
    return False

def log_user_interaction(question: str, response: str, metadata: Dict[str, Any], session_id: str = None):
    """
    Log user interactions for future model training and analysis
    """
    try:
        # Create logs directory if it doesn't exist
        logs_dir = "/content/ayikabot_logs"
        os.makedirs(logs_dir, exist_ok=True)
        
        # Generate session ID if not provided
        if session_id is None:
            session_id = st.session_state.get('session_id', f"session_{int(time.time())}")
            st.session_state.session_id = session_id
        
        # Create log entry
        log_entry = {
            'timestamp': datetime.now().isoformat(),
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
        
        # Log to JSON file (for detailed analysis)
        json_log_file = os.path.join(logs_dir, f"interactions_{datetime.now().strftime('%Y%m%d')}.json")
        with open(json_log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
        
        # Log to CSV file (for easy spreadsheet analysis)
        csv_log_file = os.path.join(logs_dir, f"interactions_{datetime.now().strftime('%Y%m%d')}.csv")
        file_exists = os.path.isfile(csv_log_file)
        
        with open(csv_log_file, 'a', newline='', encoding='utf-8') as f:
            fieldnames = ['timestamp', 'session_id', 'user_question', 'bot_response', 
                         'response_type', 'is_climate_related', 'confidence_score', 
                         'detection_reason', 'generation_time', 'question_length', 'response_length']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            
            # Write header if file is new
            if not file_exists:
                writer.writeheader()
            
            writer.writerow(log_entry)
            
    except Exception as e:
        # Don't break the app if logging fails
        print(f"Logging error: {str(e)}")

def log_session_summary():
    """
    Log session summary when chat is cleared or session ends
    """
    try:
        if st.session_state.get('chat_history') and len(st.session_state.chat_history) > 0:
            logs_dir = "/content/ayikabot_logs"
            os.makedirs(logs_dir, exist_ok=True)
            
            session_id = st.session_state.get('session_id', f"session_{int(time.time())}")
            stats = st.session_state.session_stats
            
            summary = {
                'timestamp': datetime.now().isoformat(),
                'session_id': session_id,
                'total_questions': stats['questions_asked'],
                'climate_questions': stats['climate_questions'],
                'rejected_questions': stats['rejected_questions'],
                'total_time': stats['total_time'],
                'avg_response_time': stats['total_time'] / max(stats['climate_questions'], 1),
                'session_duration': len(st.session_state.chat_history),
                'engagement_score': stats['climate_questions'] / max(stats['questions_asked'], 1)
            }
            
            # Log session summary
            summary_file = os.path.join(logs_dir, f"session_summaries_{datetime.now().strftime('%Y%m%d')}.json")
            with open(summary_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(summary, ensure_ascii=False) + '\n')
                
    except Exception as e:
        print(f"Session summary logging error: {str(e)}")

def export_training_data():
    """
    Export logged data in format suitable for model training
    """
    try:
        logs_dir = "/content/ayikabot_logs"
        if not os.path.exists(logs_dir):
            return None
            
        training_data = []
        
        # Read all JSON log files
        for filename in os.listdir(logs_dir):
            if filename.startswith('interactions_') and filename.endswith('.json'):
                filepath = os.path.join(logs_dir, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    for line in f:
                        try:
                            entry = json.loads(line.strip())
                            # Only include climate-related Q&A for training
                            if entry.get('is_climate_related') and entry.get('response_type') == 'climate_answer':
                                training_data.append({
                                    'input': f"question: {entry['user_question']}",
                                    'output': entry['bot_response'],
                                    'metadata': {
                                        'confidence': entry['confidence_score'],
                                        'timestamp': entry['timestamp']
                                    }
                                })
                        except json.JSONDecodeError:
                            continue
        
        # Save training data
        if training_data:
            training_file = os.path.join(logs_dir, f"training_data_{datetime.now().strftime('%Y%m%d')}.json")
            with open(training_file, 'w', encoding='utf-8') as f:
                json.dump(training_data, f, ensure_ascii=False, indent=2)
            
            return len(training_data)
        
    except Exception as e:
        print(f"Training data export error: {str(e)}")
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
        
        # Clean up response prefixes
        for prefix in ["question:", "answer:", "response:"]:
            if answer.lower().startswith(prefix):
                answer = answer[len(prefix):].strip()
        
        return answer if len(answer.split()) >= 8 else f"I can provide information about this climate topic: {answer}"
    except Exception as e:
        return "I encountered an issue generating a response. Please try rephrasing your question."

def process_user_question(question: str, tokenizer, model) -> Tuple[str, dict]:
    """Process user question and return response with metadata"""
    start = time.time()
    
    # First check if it's a greeting
    if is_greeting(question):
        response = get_greeting_response()
        return response, {
            'is_climate': False,
            'confidence': 0.0,
            'reason': "Greeting detected",
            'response_type': "greeting",
            'generation_time': time.time() - start
        }
    
    # Then check climate relevance
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
    with st.sidebar:
        st.markdown("<div style='text-align:center; margin-bottom:20px;'>"
                    "<img src='https://cdn-icons-png.flaticon.com/512/6057/6057198.png' width='80'>"
                    "</div>", unsafe_allow_html=True)
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
        st.subheader("📊 Data & Training")
        
        # Add logging info and export functionality
        if st.button("📥 Export Training Data", help="Export logged interactions for model improvement"):
            with st.spinner("Exporting training data..."):
                count = export_training_data()
                if count:
                    st.success(f"✅ Exported {count} training examples!")
                else:
                    st.info("No training data available yet.")
        
        st.markdown("""
        <small>
        <em>AyikaBot logs interactions to improve climate education responses. 
        Only climate-related Q&A pairs are used for training.</em>
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

    # Load model
    tokenizer, model = load_ayikabot_model("/content/ayikabot_clean")
    if not tokenizer or not model:
        st.error("Failed to load the climate education model. Please check the model path.")
        return

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
            # Store the question and start thinking
            question_to_process = user_question.strip()
            st.session_state.pending_question = question_to_process
            st.session_state.is_thinking = True
            st.session_state.input_key_counter += 1  # Clear input immediately
            st.rerun()
        
        # Process pending question if we're thinking
        if st.session_state.is_thinking and st.session_state.get("pending_question"):
            question_to_process = st.session_state.pending_question
            
            # Process the question
            response, metadata = process_user_question(question_to_process, tokenizer, model)
            stats = st.session_state.session_stats
            stats['questions_asked'] += 1
            
            if metadata['response_type'] == 'climate_answer':
                stats['climate_questions'] += 1
                stats['total_time'] += metadata['generation_time']
            else:
                stats['rejected_questions'] += 1
                
            # Add to chat history
            st.session_state.chat_history.append({'question': question_to_process, 'response': response, 'metadata': metadata})
            st.session_state.last_processed_input = question_to_process
            
            # Log the interaction
            log_user_interaction(question_to_process, response, metadata)
            
            # Clear thinking state
            st.session_state.is_thinking = False
            st.session_state.pending_question = ""
            st.rerun()

        # Display metrics if there are questions asked
        if st.session_state.session_stats['questions_asked'] > 0:
            st.markdown('<div class="metrics-container">', unsafe_allow_html=True)
            cols = st.columns(4)
            stats = st.session_state.session_stats
            avg_time = stats['total_time'] / max(stats['climate_questions'], 1)
            cols[0].metric("Questions", stats['questions_asked'])
            cols[1].metric("Climate Topics", stats['climate_questions'])
            cols[2].metric("Redirected", stats['rejected_questions'])
            cols[3].metric("Avg Time", f"{avg_time:.1f}s")
            st.markdown('</div>', unsafe_allow_html=True)

        # Handle clear chat button
        if clear_button:
            # Log session summary before clearing
            log_session_summary()
            
            for key, default_value in session_keys.items():
                st.session_state[key] = default_value
            st.session_state.input_key_counter += 1  # Force new input widget
            
            # Generate new session ID for next session
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