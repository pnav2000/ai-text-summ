import os
import warnings
from googletrans import Translator
from transformers import pipeline

# Suppress TensorFlow logs (set to '3' to ignore INFO and WARNING logs)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# Suppress warnings in Python
warnings.filterwarnings("ignore")

import wikipedia
from transformers import pipeline
import torch
class chatbot:
    def __init__(self) -> None:
        # Check if GPU is available and set the device
        device = 0 if torch.cuda.is_available() else -1
        
        # Load a reliable summarization model
        self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=device)
        self.classifier = pipeline("zero-shot-classification", device=device)  
        self.sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
        self.translator = Translator()

    def categorize_text(self, input_text):
        # Define potential categories
        categories = [
            "Artificial Intelligence",
            "Healthcare",
            "Finance",
            "Technology",
            "Education",
            "Transportation",
            "Environment",
            "Politics",
            "Sports",
            "Entertainment"
        ]
        result = self.classifier(input_text, categories)
        return result['labels'][0], result['scores'][0]
    
    def summarize_text(self, input_text, min_words=20, max_words=100, do_sample=False):
        max_tokens = 768  # Increased chunk size for better context
        words = input_text.split()
        chunks = [' '.join(words[i:i + max_tokens]) for i in range(0, len(words), max_tokens)]
    
        # Summarize all chunks in one batch with sampling
        summaries = self.summarizer(chunks, max_length=max_words, min_length=min_words, do_sample=do_sample, top_k=50, top_p=0.95)
        combined_summary = ' '.join([summary['summary_text'] for summary in summaries])
        return combined_summary

    def search_wikipedia_articles(self, query):
        search_results = wikipedia.search(query, results=5)
        articles = []
        for title in search_results:
            try:
                page = wikipedia.page(title)
                articles.append({'title': page.title, 'url': page.url})
            except (wikipedia.exceptions.DisambiguationError, wikipedia.exceptions.PageError):
                continue
        return articles
    
    def get_related_articles(self, text):
        max_length = 300
        text = text[:max_length]
        articles = self.search_wikipedia_articles(text)
        if not articles:
            keywords = text.split()[:3]  # Use first three words as keywords
            fallback_query = " ".join(keywords)
            articles = self.search_wikipedia_articles(fallback_query)
        return articles
    
    def analyze_sentiment(self, text):
        # Get sentiment analysis results
        result = self.sentiment_pipeline(text)[0]
    
        label = result['label']
        score = result['score']
    
        # Interpret the results based on the score
        if label == 'POSITIVE':
            if score > 0.9:
                return "Very Happy"
            elif score > 0.7:
                return "Happy"
            else:
                return "Neutral"
        else:  # 'NEGATIVE'
            if score < 0.1:  # Close to neutral
                return "Neutral"
            elif score < 0.3:
                return "Sad"
            elif score < 0.5:
                return "Frustrated"
            else:
                return "Very Sad"
            
    def translat_msg(self, text, src, dest):
        translation = self.translator.translate(text, src=src, dest=dest)
        return translation.text
        
    def detect_language(self, text):
        language_map = {'af': 'Afrikaans', 'ar': 'Arabic', 'bn': 'Bengali', 'en': 'English', 'fr': 'French', 'de': 'German', 'gu': 'Gujarati', 'hi': 'Hindi', 'kn': 'Kannada', 'ml': 'Malayalam', 'mr': 'Marathi', 'ne': 'Nepali', 'or': 'Odia', 'pa': 'Punjabi', 'ta': 'Tamil', 'te': 'Telugu', 'ur': 'Urdu', 'as': 'Assamese', 'bh': 'Bhojpuri', 'sd': 'Sindhi', 'si': 'Sinhala', 'th': 'Thai', 'ja': 'Japanese', 'zh-cn': 'Chinese (Simplified)', 'ru': 'Russian', 'es': 'Spanish', 'it': 'Italian', 'pt': 'Portuguese', 'ko': 'Korean'}
        detected = self.translator.detect(text)
        language_name = language_map.get(detected.lang, "Unknown language")

        return detected.lang, language_name
