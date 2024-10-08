# AI Text Summarization Model

## Table of Contents
- [Introduction](#introduction)
- [Setup and Run](#setup-and-run)
- [Models and Libraries Used](#models-and-libraries-used)
- [Use Case](#use-case)
- [Additional Features](#additional-features)

## Introduction
The project aims to develop an AI model for text summarization using open-source models, addressing the challenge of condensing large volumes of information into concise summaries. Key features include multi-language summarization to support a diverse user base, customizable word length to meet specific needs, text classification for context understanding, and the inclusion of links to the original content for further exploration. Together, these features enhance the tool's usability, making it an invaluable resource for users seeking efficient information retrieval across various languages and topics.

## Setup and Run
This section will guide you through setting up the environment and running the text summarization model.

### Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.7+
- Pip (Python package installer)

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/text-summarization.git
   cd text-summarization
   
2. Install the required packages:
   ```bash
   pip install -r requirements.txt

3. Run the application:
   ```bash
   python main.py
 

## Models and Libraries used

### Models Used
1. facebook/bart-large-cnn
Description: A transformer-based model by Facebook designed for text summarization, capable of generating concise summaries while preserving key information and context.
2. Helsinki-NLP/opus-mt-hi-en
Description: A translation model that translates text from Hindi to English, providing state-of-the-art translation capabilities.
3. Helsinki-NLP/opus-mt-en-hi
Description: A translation model that translates text from English to Hindi, enhancing communication between speakers of both languages.

### Libraries and Modules Used
1. **PyPDF2**
**Description**: A Python library for reading PDF files, allowing for text and metadata extraction from PDF documents.
**Installation**: pip install PyPDF2

2. **python-docx**
**Description**: A library for creating and modifying Microsoft Word (.docx) files, useful for handling text and formatting in Word documents.
**Installation**: pip install python-docx

3. **Transformers**
**Description**: Developed by Hugging Face, this library provides pre-trained models for natural language processing tasks, including text summarization.
**Installation**: pip install transformers

4. **Torch**
**Description**: A deep learning framework used for building and training neural networks, often used in conjunction with the Transformers library.
**Installation**: Follow the instructions on the official PyTorch website.

5. **Flask**
**Description**: A lightweight web framework for Python to create web applications easily.
**Installation**: pip install Flask

6. **Flask-SocketIO**
**Description**: An extension for Flask that enables real-time communication between the server and clients using WebSockets.
**Installation**: pip install flask-socketio

7. **Flask-CORS**
**Description**: A Flask extension that allows enabling Cross-Origin Resource Sharing (CORS) in Flask applications.
**Installation**: pip install flask-cors

8. **OS and Time**
**Description**: Built-in Python modules for interacting with the operating system and handling time-related tasks.

## Use Cases
- **News Aggregation**: Summarizing news articles in multiple languages for users to quickly grasp current events.
- **Academic Research**: Helping researchers and students summarize lengthy papers or articles, facilitating quicker comprehension across various languages.
- **Content Curation**: Enabling content creators and marketers to summarize and translate blog posts, reviews, or other content for broader audiences.
- **E-learning**: Summarizing educational materials in multiple languages to support diverse student populations.

## Additional Features

- **Multi-language Support**: Summarizes text in various languages.
- **Multi-format Support**: Accepting various input formats (text, PDF, docx) for summarization.
- **Customizable Summary Length**: Allowing users to specify the desired length of the summary
- **Keyword Highlighting**: Highlighting key terms or concepts in the summary for enhanced understanding


