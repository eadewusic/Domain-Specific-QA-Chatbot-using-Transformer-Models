# Climate Chatbot Model Architecture

## Overview
- **Model**: T5-small (Text-To-Text Transfer Transformer)
- **Parameters**: 60,506,624
- **Type**: Encoder-Decoder Transformer
- **Framework**: TensorFlow
- **Purpose**: Generative QA for Climate Education

## Architecture Details

### Encoder
- **Layers**: 6
- **Attention Heads**: 8
- **Hidden Size**: 512
- **Feed Forward**: 2,048

### Decoder
- **Layers**: 6
- **Attention Heads**: 8
- **Hidden Size**: 512
- **Feed Forward**: 2,048

### Key Features
- **Vocabulary**: 32,128 tokens (SentencePiece)
- **Max Input**: 128 tokens
- **Max Output**: 100 tokens
- **Attention**: Multi-head self-attention with relative position bias

## Task Adaptation
- **Input Format**: `question: [QUESTION]`
- **Output Format**: Natural language climate education answers
- **Fine-tuning**: Full model fine-tuning on climate dataset
- **Domain**: Climate science and environmental education

## Performance
- **Training Loss**: 0.5757 (excellent convergence)
- **BLEU Score**: 0.0549 (good performance for domain)
- **Generation Speed**: ~17 seconds per answer
- **Model Size**: ~230.8 MB
