# My Tensorflow model is 356.58 MB which exceeds GitHub's file
# size limit of 100.00 MB and I've used up LFS storage
# Hence using Hugging Face Hub approach

from transformers import T5Tokenizer, TFT5ForConditionalGeneration
import tensorflow as tf

"""
Climate Education QA Chatbot - Trained Model Access

Model Details:
- Model: T5-small fine-tuned for climate education QA
- Size: ~240MB (too large for GitHub)
- Performance: 0.0549 BLEU score, ~17s generation, 55x improvement from baseline
- Training: 4 experiments with systematic optimization
- Best Configuration: Experiment 4c (balanced quality + speed)
- Framework: TensorFlow
- Architecture Type: Encoder-Decoder Transformer
- Layers: 6 Encoder + 6 Decoder
- Parameters: 60,506,624 (60M)
- Attention Mechanism: Multi-Head Self-Attention
- Position Encoding: Relative Position Bias
- Activation Function: ReLU

Hugging Face Repository: https://huggingface.co/Climi/Climate-Education-QA-Chatbot
"""

def download_model_from_huggingface():
    """
    Download the climate chatbot model from Hugging Face
    """
    print("Climate Education QA Chatbot - Model Download")
    print("=" * 60)
    print("Repository: https://huggingface.co/Climi/Climate-Education-QA-Chatbot")
    print("Model size: ~240MB")
    print("=" * 60)
    
    try:
        from transformers import T5Tokenizer, TFT5ForConditionalGeneration
        
        print("Downloading model from Hugging Face...")
        print("This may take a few minutes depending on your internet connection.")
        
        # Download tokenizer
        print(" Downloading tokenizer...")
        tokenizer = T5Tokenizer.from_pretrained("Climi/Climate-Education-QA-Chatbot")
        print("Tokenizer downloaded successfully")
        
        # Download model
        print(" Downloading model weights...")
        model = TFT5ForConditionalGeneration.from_pretrained("Climi/Climate-Education-QA-Chatbot")
        print(" Model downloaded successfully")
        
        print(f"\nMODEL READY FOR USE!")
        print(f"   Model parameters: {model.num_parameters():,}")
        print(f"   Architecture: T5-small (Encoder-Decoder Transformer)")
        print(f"   Task: Climate Education Question Answering")
        
        return model, tokenizer
        
    except ImportError:
        print("Error: transformers library not installed")
        print("Please install it using:")
        print("   pip install transformers tensorflow")
        return None, None
    
    except Exception as e:
        print(f"Error downloading model: {e}")
        print("Please check your internet connection and try again.")
        return None, None

def quick_test_model(model, tokenizer):
    """
    Quick test of the downloaded model
    """
    if model is None or tokenizer is None:
        print("Model not available for testing")
        return
    
    print("\nQUICK MODEL TEST:")
    print("-" * 40)
    
    # Test question
    test_question = "What is climate change?"
    print(f"Question: {test_question}")
    
    try:
        # Generate answer
        input_text = f"question: {test_question}"
        input_ids = tokenizer.encode(input_text, return_tensors='tf')
        
        outputs = model.generate(
            input_ids,
            max_length=100,
            temperature=0.7,
            do_sample=True,
            pad_token_id=tokenizer.pad_token_id,
            eos_token_id=tokenizer.eos_token_id
        )
        
        answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
        print(f"Answer: {answer}")
        print("Model working correctly!")
        
    except Exception as e:
        print(f"Error during testing: {e}")

def interactive_demo(model, tokenizer):
    """
    Interactive demo of the climate chatbot
    """
    if model is None or tokenizer is None:
        print("Model not available for demo")
        return
    
    print("\nINTERACTIVE CLIMATE EDUCATION CHATBOT")
    print("Ask questions about climate change! (type 'quit' to exit)")
    print("-" * 60)
    
    while True:
        try:
            question = input("\nYour question: ").strip()
            
            if question.lower() == 'quit':
                print("Thanks for learning about climate change!")
                break
            
            if not question:
                continue
            
            # Generate answer
            input_text = f"question: {question}"
            input_ids = tokenizer.encode(input_text, return_tensors='tf')
            
            outputs = model.generate(
                input_ids,
                max_length=100,
                temperature=0.7,
                do_sample=True,
                repetition_penalty=1.2,
                pad_token_id=tokenizer.pad_token_id,
                eos_token_id=tokenizer.eos_token_id
            )
            
            answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
            print(f"\nAnswer: {answer}")
            
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")

# Alternative download methods
def alternative_download_methods():
    """
    Show alternative ways to access the model
    """
    print("\nALTERNATIVE DOWNLOAD METHODS:")
    print("=" * 50)
    
    print("\nCOMMAND LINE (using git):")
    print("   git clone https://huggingface.co/Climi/Climate-Education-QA-Chatbot")
    
    print("\nHUGGING FACE CLI:")
    print("   # Install huggingface-hub")
    print("   pip install huggingface-hub")
    print("   # Download model")
    print("   huggingface-cli download Climi/Climate-Education-QA-Chatbot")
    
    print("\nPYTHON SCRIPT (this method):")
    print("   from transformers import T5Tokenizer, TFT5ForConditionalGeneration")
    print("   tokenizer = T5Tokenizer.from_pretrained('Climi/Climate-Education-QA-Chatbot')")
    print("   model = TFT5ForConditionalGeneration.from_pretrained('Climi/Climate-Education-QA-Chatbot')")
    
    print("\nDIRECT BROWSER ACCESS:")
    print("   Visit: https://huggingface.co/Climi/Climate-Education-QA-Chatbot")
    print("   Click 'Files and versions' tab to browse/download individual files")

def show_model_details():
    """
    Display detailed information about the model
    """
    print("\nMODEL DETAILS:")
    print("=" * 40)
    print("Architecture: T5-small (Text-To-Text Transfer Transformer)")
    print("Parameters: ~60 million")
    print("Model Size: ~240MB")
    print("Task: Generative Question Answering")
    print("Domain: Climate Education")
    print("Performance: 0.0549 BLEU score")
    print("Generation Speed: ~17 seconds")
    print("Framework: TensorFlow")
    
    print("\nEXPERIMENT PROGRESSION:")
    experiments = [
        "Baseline: 9.04 loss, 0.0001 BLEU (severe underfitting)",
        "Exp 2: 0.93 loss, 0.0012 BLEU (major breakthrough)", 
        "Exp 3: 1.26 loss, 0.0392 BLEU (quality optimization)",
        "Exp 4: 0.58 loss, 0.0392 BLEU (best training)",
        "Exp 4c: OPTIMAL - 0.0549 BLEU (best balanced performance)"
    ]
    
    for i, exp in enumerate(experiments, 1):
        marker = " !BEST!" if "OPTIMAL" in exp else ""
        print(f"   {i}. {exp}{marker}")

# Main execution
if __name__ == "__main__":
    print("Starting Climate Education QA Chatbot Setup...")
    
    # Show model details
    show_model_details()
    
    # Show alternative download methods
    alternative_download_methods()
    
    # Ask user what they want to do
    print("\nWHAT WOULD YOU LIKE TO DO?")
    print("1. Download and test model")
    print("2. Download and run interactive demo") 
    print("3. Just show information")
    
    try:
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == "1":
            model, tokenizer = download_model_from_huggingface()
            if model and tokenizer:
                quick_test_model(model, tokenizer)
                
        elif choice == "2":
            model, tokenizer = download_model_from_huggingface()
            if model and tokenizer:
                quick_test_model(model, tokenizer)
                interactive_demo(model, tokenizer)
                
        elif choice == "3":
            print("\nInformation displayed above!")
            print("Visit the Hugging Face repository for more details:")
            print("https://huggingface.co/Climi/Climate-Education-QA-Chatbot")
            
        else:
            print("Invalid choice. Please run the script again.")
            
    except KeyboardInterrupt:
        print("\n\nSetup cancelled. Goodbye!")
    except Exception as e:
        print(f"\nError: {e}")
        print("Please check the repository and try again.")
    
    print(f"\nREPOSITORY LINKS:")
    print(f"   Hugging Face: https://huggingface.co/Climi/Climate-Education-QA-Chatbot")
    print(f"   Documentation: Check the model card for training details")
    print(f"   Issues: Report any problems in the repository discussions")