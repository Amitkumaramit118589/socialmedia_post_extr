# Automatic Hashtag Generator (Simple)

live site link: https://socialmedia-post-extr.onrender.com/

## Overview
Simple project that extracts keywords from a text post and converts them into readable CamelCase hashtags.

## Files
- `hashtag_generator.py` : Core logic for cleaning text and generating hashtags.
- `app.py` : Streamlit UI to paste text and generate hashtags.
- `requirements.txt` : Python dependencies.

## Setup (Windows)
1. Make sure Python 3.8+ is installed.
2. Create and activate virtual environment:
   ```powershell
   python -m venv venv
   # If PowerShell blocks activation, run as admin:
   Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
   venv\Scripts\activate
   ```
3. Upgrade pip (optional but recommended):
   ```powershell
   python -m pip install --upgrade pip
   ```
4. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
5. Download NLTK data (run Python once):
   ```python
   import nltk
   nltk.download('punkt')
   nltk.download('averaged_perceptron_tagger')
   nltk.download('stopwords')
   ```

## Run
- Run demo script in terminal:
  ```powershell
  python hashtag_generator.py
  ```
- Run Streamlit app:
  ```powershell
  streamlit run app.py
  ```

## Notes / Troubleshooting
- If NLTK downloads fail due to no internet, the script falls back to a frequency-based extractor (still works).
- To improve quality, install spaCy and use noun-phrase extraction (not included in this basic project).
