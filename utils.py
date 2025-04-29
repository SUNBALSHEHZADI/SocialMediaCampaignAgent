import torch
from transformers import pipeline
from diffusers import StableDiffusionPipeline
import streamlit as st
from accelerate import Accelerator

accelerator = Accelerator()

# Cache models for better performance
@st.cache_resource(show_spinner=False)
def load_models():
    """Load all ML models once and cache them"""
    models = {}
    
    # Text Generation (Faster GPT-2 variant)
    models['text_gen'] = pipeline(
        'text-generation', 
        model='gpt2',
        device=accelerator.device
    )
    
    # Image Generation (Optimized SD 2.1 Base)
    models['sd_pipe'] = StableDiffusionPipeline.from_pretrained(
        "stabilityai/stable-diffusion-2-1-base",
        torch_dtype=torch.float32,
        safety_checker=None  # Disable for faster generation
    ).to(accelerator.device)
    
    # Sentiment Analysis
    models['sentiment'] = pipeline(
        "sentiment-analysis",
        model="distilbert-base-uncased-finetuned-sst-2-english",
        device=accelerator.device
    )
    
    return models

def generate_content(prompt, models):
    """Handle all content generation in optimized way"""
    # Text Generation
    text_result = models['text_gen'](
        prompt,
        max_length=150,
        num_return_sequences=1,
        do_sample=True,
        temperature=0.7
    )
    
    # Image Generation (Faster settings)
    image = models['sd_pipe'](
        prompt,
        num_inference_steps=25,  # Reduced from default 50
        guidance_scale=7.5
    ).images[0]
    
    # Sentiment Analysis
    sentiment = models['sentiment'](text_result[0]['generated_text'][:512])
    
    return {
        'text': text_result[0]['generated_text'],
        'image': image,
        'sentiment': sentiment
    }
