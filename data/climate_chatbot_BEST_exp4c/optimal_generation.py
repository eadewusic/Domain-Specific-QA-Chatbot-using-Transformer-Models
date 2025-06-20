# OPTIMAL GENERATION FUNCTION FOR CLIMATE CHATBOT
# Experiment 4c - Balanced parameters for best performance

def generate_answer_optimal(question, max_length=70, temperature=0.5):
    """
    OPTIMAL generation function for climate chatbot
    Balanced for quality, speed, and factual accuracy
    """
    # Clean input
    input_text = f"question: {question.strip()}"
    
    # Tokenize
    input_ids = tokenizer.encode(
        input_text,
        return_tensors='tf',
        max_length=110,
        truncation=True,
        add_special_tokens=True
    )
    
    # OPTIMAL PARAMETERS (Experiment 4c)
    outputs = model.generate(
        input_ids,
        max_length=max_length,        # 70 tokens for focused answers
        min_length=18,               # Ensure substantial content
        temperature=temperature,      # 0.5 for balanced creativity
        do_sample=True,
        top_p=0.8,                   # Nucleus sampling
        top_k=40,                    # Vocabulary restriction
        repetition_penalty=2.0,      # Anti-repetition
        no_repeat_ngram_size=3,      # Prevent 3-gram repetition
        num_beams=1,                 # Single beam for speed
        pad_token_id=tokenizer.pad_token_id,
        eos_token_id=tokenizer.eos_token_id
    )
    
    # Decode
    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    # Post-processing
    answer = post_process_optimal(answer, question)
    
    return answer

def post_process_optimal(answer, question):
    """
    Optimal post-processing for factual accuracy
    """
    # Remove input echo
    if answer.lower().startswith(question.lower()):
        answer = answer[len(question):].strip()
    
    # Remove prefixes
    prefixes = ["question:", "answer:", "response:", "a:", "q:"]
    for prefix in prefixes:
        if answer.lower().startswith(prefix):
            answer = answer[len(prefix):].strip()
    
    # Fix critical factual errors only
    critical_fixes = {
        'sea levels falling': 'sea levels rising',
        'sea level falling': 'sea level rising',
        'temperature decreasing': 'temperature increasing'
    }
    
    for error, correction in critical_fixes.items():
        if error in answer.lower():
            answer = answer.lower().replace(error, correction)
    
    # Remove immediate word repetition
    words = answer.split()
    if len(words) > 1:
        cleaned_words = [words[0]]
        for i in range(1, len(words)):
            if words[i].lower() != words[i-1].lower():
                cleaned_words.append(words[i])
        answer = ' '.join(cleaned_words)
    
    # Ensure proper ending
    if answer and not answer.endswith('.') and not answer.endswith('?'):
        answer += '.'
    
    # Quality check
    if len(answer.split()) < 6:
        return "I can provide information about this climate topic. What specific aspect interests you?"
    
    return answer

def interactive_climate_chat_optimal():
    """
    OPTIMAL interactive climate chat
    """
    print("CLIMATE EDUCATION CHATBOT - OPTIMAL VERSION")
    print("Best performing model from comprehensive experiments")
    print("Commands: 'quit' to exit, 'stats' for performance info")
    print("-" * 70)
    
    while True:
        try:
            user_input = input("\nYour climate question: ").strip()
            
            if user_input.lower() == 'quit':
                print("Thanks for learning about climate change!")
                break
            elif user_input.lower() == 'stats':
                print(f"\nOPTIMAL MODEL PERFORMANCE:")
                print(f"   Experiment: 4c (Balanced)")
                print(f"   BLEU Score: 0.0549 (Best balanced performance)")
                print(f"   Generation Speed: ~17s (Good speed)")
                print(f"   Training Loss: 0.5757 (Excellent)")
                print(f"   Validation Loss: 0.8844 (Stable)")
                continue
            elif not user_input:
                continue
            
            # Generate with optimal function
            import time
            start_time = time.time()
            answer = generate_answer_optimal(user_input)
            gen_time = time.time() - start_time
            
            print(f"\nAnswer: {answer}")
            print(f"Generated in {gen_time:.2f} seconds")
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")
