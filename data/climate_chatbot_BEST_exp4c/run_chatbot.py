#!/usr/bin/env python3
"""
Climate Education Chatbot - Optimal Deployment Script
Experiment 4c - Best performing configuration
"""

import sys
import os
from transformers import T5Tokenizer, TFT5ForConditionalGeneration

def load_optimal_chatbot():
    """Load the optimal climate chatbot"""
    print("Loading Climate Education Chatbot (Optimal)...")
    
    try:
        # Load model and tokenizer
        tokenizer = T5Tokenizer.from_pretrained("./", legacy=False)
        model = TFT5ForConditionalGeneration.from_pretrained("./")
        
        print("Model loaded successfully!")
        
        # Load optimal generation functions
        from optimal_generation import interactive_climate_chat_optimal
        
        print("Optimal generation functions loaded!")
        print("\nStarting interactive chat...")
        
        # Start interactive chat
        interactive_climate_chat_optimal()
        
    except Exception as e:
        print(f"Error loading chatbot: {e}")
        print("Make sure you're in the correct directory with model files.")

if __name__ == "__main__":
    load_optimal_chatbot()
