
# =============================================================================
# COMPLETE AYIKABOT PIPELINE - TRAINED MODEL + DOMAIN INTELLIGENCE
# =============================================================================

import re
import time
import numpy as np
from typing import List, Tuple, Optional
from transformers import TFT5ForConditionalGeneration, T5Tokenizer

# Domain Detection Keywords
CLIMATE_KEYWORDS = {
    'core_climate': [
        'climate', 'global warming', 'greenhouse', 'carbon dioxide', 'co2', 
        'emissions', 'temperature', 'warming', 'cooling', 'weather patterns',
        'climate change', 'greenhouse effect', 'greenhouse gas', 'carbon emissions'
    ],
    'environmental': [
        'environment', 'pollution', 'sustainability', 'renewable energy', 
        'fossil fuels', 'deforestation', 'biodiversity', 'ecosystem', 'conservation',
        'sustainable', 'green energy', 'clean energy', 'environmental impact'
    ],
    'climate_impacts': [
        'sea level', 'ice caps', 'glaciers', 'drought', 'flooding', 'storms', 
        'hurricanes', 'extreme weather', 'ocean acidification', 'coral bleaching',
        'rising seas', 'melting ice', 'heat waves', 'climate disasters'
    ],
    'climate_science': [
        'greenhouse effect', 'carbon cycle', 'methane', 'ozone', 'atmosphere', 
        'albedo', 'feedback', 'tipping points', 'climate models', 'ipcc',
        'carbon footprint', 'carbon sink', 'atmospheric co2', 'climate data'
    ],
    'climate_solutions': [
        'renewable', 'solar', 'wind', 'electric vehicles', 'carbon capture', 
        'reforestation', 'energy efficiency', 'carbon footprint', 'offsetting',
        'solar panels', 'wind turbines', 'green technology', 'carbon offsets',
        'climate action', 'mitigation', 'adaptation'
    ],
    'climate_education': [
        'learn climate', 'teach climate', 'climate facts', 'climate science',
        'climate education', 'explain climate', 'climate knowledge', 'climate awareness'
    ]
}

NON_CLIMATE_TOPICS = {
    'technology': ['computer', 'software', 'programming', 'coding', 'internet', 'smartphone', 'app'],
    'sports': ['football', 'basketball', 'soccer', 'tennis', 'olympics', 'sports', 'game'],
    'entertainment': ['movie', 'music', 'celebrity', 'actor', 'singer', 'netflix', 'youtube'],
    'food_cooking': ['recipe', 'cooking', 'restaurant', 'food', 'meal', 'dinner', 'breakfast'],
    'health_medical': ['medicine', 'doctor', 'hospital', 'disease', 'symptoms', 'treatment'],
    'finance': ['money', 'investment', 'stocks', 'banking', 'loan', 'cryptocurrency'],
    'personal_life': ['relationship', 'dating', 'marriage', 'family', 'personal'],
    'general_knowledge': ['capital', 'country', 'geography', 'population', 'language']
}

SCIENCE_CONNECTIONS = {
    'photosynthesis': 'Photosynthesis is directly related to climate through the carbon cycle. Plants absorb CO2 during photosynthesis, making them important carbon sinks in climate regulation.',
    'ocean currents': 'Ocean currents play a crucial role in climate regulation by distributing heat around the globe and affecting regional weather patterns.',
    'water cycle': 'The water cycle is intimately connected to climate, with warming temperatures affecting evaporation, precipitation, and weather patterns.',
    'chemistry': 'Chemistry is fundamental to understanding greenhouse gases, atmospheric reactions, and ocean acidification in climate science.',
    'biology': 'Biology connects to climate through ecosystem responses, species adaptation, and the role of living organisms in carbon cycles.'
}

class AyikaBot:
    """Complete AyikaBot with trained model and domain intelligence"""
    
    def __init__(self, model_path):
        """Initialize with trained model"""
        print("Loading AyikaBot...")
        self.tokenizer = T5Tokenizer.from_pretrained(model_path)
        self.model = TFT5ForConditionalGeneration.from_pretrained(model_path)
        print("AyikaBot loaded successfully!")
    
    def is_climate_related(self, question: str) -> Tuple[bool, float, str]:
        """Check if question is climate-related"""
        question_lower = question.lower().strip()
        cleaned_question = re.sub(r'\b(what|how|why|when|where|who|can|is|are|do|does|will|would|could|should|please|tell|me|about)\b', '', question_lower)
        cleaned_question = re.sub(r'[^\w\s]', ' ', cleaned_question)
        cleaned_question = ' '.join(cleaned_question.split())
        
        total_score = 0
        matched_categories = []
        keyword_matches = []
        
        weights = {'core_climate': 4.0, 'climate_science': 3.0, 'climate_impacts': 2.5, 
                  'climate_solutions': 2.5, 'climate_education': 2.0, 'environmental': 1.5}
        
        for category, keywords in CLIMATE_KEYWORDS.items():
            category_matches = 0
            category_keywords = []
            
            for keyword in keywords:
                if keyword in cleaned_question:
                    category_matches += 1
                    category_keywords.append(keyword)
                    
            if category_matches > 0:
                weight = weights.get(category, 1.0)
                total_score += category_matches * weight
                matched_categories.append(category)
                keyword_matches.extend(category_keywords)
        
        max_possible_score = sum(len(keywords) * weights.get(category, 1.0) 
                               for category, keywords in CLIMATE_KEYWORDS.items())
        confidence_score = min(total_score / max_possible_score * 10, 1.0)
        
        is_climate = confidence_score > 0.08
        
        if matched_categories:
            reason = f"Keywords: {', '.join(keyword_matches[:3])} | Categories: {', '.join(matched_categories[:2])}"
        else:
            reason = "No climate keywords detected"
        
        return is_climate, confidence_score, reason
    
    def detect_non_climate_topics(self, question: str) -> Tuple[bool, str, List[str]]:
        """Detect non-climate topics"""
        question_lower = question.lower()
        topic_scores = {}
        all_matches = {}
        
        for topic, keywords in NON_CLIMATE_TOPICS.items():
            matches = [kw for kw in keywords if kw in question_lower]
            if matches:
                topic_scores[topic] = len(matches)
                all_matches[topic] = matches
        
        if topic_scores:
            primary_topic = max(topic_scores.items(), key=lambda x: x[1])
            climate_check, confidence, _ = self.is_climate_related(question)
            
            if confidence < 0.15:
                return True, primary_topic[0], all_matches[primary_topic[0]]
        
        return False, "", []
    
    def handle_science_questions(self, question: str) -> Optional[str]:
        """Handle science questions with climate connections"""
        question_lower = question.lower()
        
        for topic, connection in SCIENCE_CONNECTIONS.items():
            if topic in question_lower:
                return f"While {topic} isn't exclusively a climate topic, it connects to climate science: {connection}"
        
        return None
    
    def generate_answer(self, question: str, max_length=100, temperature=0.7) -> str:
        """Generate domain-specific climate education answer"""
        # Domain analysis
        is_climate, confidence, reason = self.is_climate_related(question)
        is_non_climate, non_climate_topic, non_climate_keywords = self.detect_non_climate_topics(question)
        science_connection = self.handle_science_questions(question)
        
        # Handle non-climate questions
        if is_non_climate and confidence < 0.2:
            topic_display = non_climate_topic.replace('_', ' ').title()
            examples = ', '.join(non_climate_keywords[:3])
            return (f"I'm a climate education chatbot and can only answer questions about climate change, "
                    f"environment, and sustainability. Your question appears to be about {topic_display} "
                    f"(detected: {examples}). \n\n"
                    f"Try asking about: global warming, renewable energy, carbon footprint, "
                    f"climate impacts, or environmental solutions!")
        
        # Handle science connections
        if science_connection and not is_climate:
            return f"{science_connection}\n\nWould you like to know more about the climate aspects of this topic?"
        
        # Handle low confidence questions
        if not is_climate or confidence < 0.05:
            return (f"I specialize in climate education and can help with questions about:\n"
                    f"   Climate science (greenhouse effect, global warming)\n"
                    f"   Environmental impacts (sea level rise, extreme weather)\n"
                    f"   Climate solutions (renewable energy, sustainability)\n"
                    f"   Climate education and awareness\n\n"
                    f"Could you please ask a climate-related question?")
        
        # Generate answer using trained model
        try:
            prompt = f"question: {question.strip()}"
            inputs = self.tokenizer(prompt, return_tensors="tf")
            
            output_ids = self.model.generate(
                inputs.input_ids,
                attention_mask=inputs.attention_mask,
                max_length=max_length,
                min_length=20,
                temperature=temperature,
                do_sample=True,
                top_p=0.9,
                top_k=50,
                repetition_penalty=1.2,
                num_beams=2,
                early_stopping=True,
                pad_token_id=self.tokenizer.pad_token_id,
                eos_token_id=self.tokenizer.eos_token_id
            )
            
            answer = self.tokenizer.decode(output_ids[0], skip_special_tokens=True)
            
            # Clean response
            if answer.lower().startswith(question.lower()):
                answer = answer[len(question):].strip()
            
            prefixes = ["question:", "answer:", "response:"]
            for prefix in prefixes:
                if answer.lower().startswith(prefix):
                    answer = answer[len(prefix):].strip()
            
            if len(answer.split()) < 8:
                answer = f"This is an important climate topic. {answer}"
            
            return answer
            
        except Exception as e:
            return f"I can help with this climate question, but encountered a technical issue. Please try rephrasing your question."
    
    def chat(self):
        """Interactive chat interface"""
        print("\nAYIKABOT - CLIMATE EDUCATION CHATBOT")
        print("Powered by fine-tuned T5 model + domain intelligence!")
        print("Ask me anything about climate change and sustainability.")
        print("Type 'quit' to exit, 'help' for examples")
        print("-" * 60)
        
        session_stats = {'climate_questions': 0, 'rejected_questions': 0, 'total_time': 0}
        
        while True:
            try:
                user_input = input("\nYour question: ").strip()
                
                if user_input.lower() == 'quit':
                    avg_time = session_stats['total_time'] / max(session_stats['climate_questions'], 1)
                    print(f"\nSession Summary:")
                    print(f"   Climate questions answered: {session_stats['climate_questions']}")
                    print(f"   Off-topic questions redirected: {session_stats['rejected_questions']}")
                    print(f"   Average response time: {avg_time:.1f}s")
                    print("Thanks for learning about climate with AyikaBot!")
                    break
                    
                elif user_input.lower() == 'help':
                    print(f"\nTry asking about:")
                    print(f"   • What is global warming?")
                    print(f"   • How do renewable energy sources work?")
                    print(f"   • What can individuals do about climate change?")
                    print(f"   • How does deforestation affect the climate?")
                    continue
                    
                elif not user_input:
                    continue
                
                # Analyze and respond
                is_climate, confidence, _ = self.is_climate_related(user_input)
                
                start_time = time.time()
                response = self.generate_answer(user_input)
                gen_time = time.time() - start_time
                
                # Update stats
                if is_climate:
                    session_stats['climate_questions'] += 1
                    session_stats['total_time'] += gen_time
                    print(f"Climate topic detected (confidence: {confidence:.2f})")
                else:
                    session_stats['rejected_questions'] += 1
                    print(f"Non-climate topic (confidence: {confidence:.2f})")
                
                print(f"\nAyikaBot: {response}")
                print(f"Response time: {gen_time:.1f}s")
                
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"Error occurred. Please try rephrasing your question.")

# Usage functions
def load_ayikabot(model_path="/content/climate_chatbot_BEST_exp4c"):
    """Load complete AyikaBot system"""
    return AyikaBot(model_path)

def quick_test(bot):
    """Quick test of the system"""
    test_questions = [
        "What is global warming?",
        "How do solar panels work?", 
        "How do I cook pasta?"
    ]
    
    print("TESTING COMPLETE AYIKABOT SYSTEM...")
    print("=" * 50)
    
    for i, q in enumerate(test_questions, 1):
        print(f"\n{i}. Question: {q}")
        response = bot.generate_answer(q)
        print(f"   Response: {response}")

# Auto-load instructions
print("COMPLETE AYIKABOT PIPELINE READY!")
print("\nTo use after runtime restart:")
print("1. Run this cell to load all functions")
print("2. bot = load_ayikabot()")
print("3. bot.chat()  # Start interactive chat")
print("4. quick_test(bot)  # Run quick test")
