# hashtag_generator.py
import re
from collections import Counter

# Try to use NLTK if available (optional). If not, fallback to simple extractor.
use_nltk = False
try:
    import nltk
    from nltk.corpus import stopwords
    from nltk import word_tokenize, pos_tag
    try:
        nltk.data.find('tokenizers/punkt')
        nltk.data.find('taggers/averaged_perceptron_tagger')
        nltk.data.find('corpora/stopwords')
        use_nltk = True
    except LookupError:
        # try to download quietly (may fail in restricted env)
        try:
            nltk.download('punkt', quiet=True)
            nltk.download('averaged_perceptron_tagger', quiet=True)
            nltk.download('stopwords', quiet=True)
            use_nltk = True
        except Exception:
            use_nltk = False
except Exception:
    use_nltk = False

FALLBACK_STOPWORDS = {
    'the','and','is','in','to','a','of','for','on','with','that','this','it','as','are',
    'was','be','by','an','at','from','or','we','our','you','your','but','not','have','has',
    'i','me','my','so','will','can','its','they','their','new','made','line'
}

def clean_text(text):
    text = re.sub(r'https?://\S+',' ', text)
    text = re.sub(r'@\w+',' ', text)
    text = re.sub(r'#\w+',' ', text)
    text = re.sub(r'[^A-Za-z0-9\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip().lower()
    return text

def phrase_to_hashtag(phrase):
    words = re.findall(r"[A-Za-z0-9]+", phrase)
    if not words:
        return None
    return '#' + ''.join(w.capitalize() for w in words)

def extract_keywords_nltk(text, top_n=8):
    tokens = word_tokenize(text)
    tokens = [t for t in tokens if t.isalnum()]
    sw = set(stopwords.words('english')) | FALLBACK_STOPWORDS
    tags = pos_tag(tokens)
    candidates = [w for w,tag in tags if (tag.startswith('NN') or tag.startswith('JJ')) and w.lower() not in sw and len(w)>2]
    counts = Counter([w.lower() for w in candidates])
    return [p for p,c in counts.most_common(top_n)]

def extract_keywords_fallback(text, top_n=8):
    tokens = re.findall(r"[A-Za-z0-9]+", text.lower())
    sw = FALLBACK_STOPWORDS
    tokens = [t for t in tokens if t not in sw and len(t)>2 and not t.isdigit()]
    counts = Counter(tokens)
    return [p for p,c in counts.most_common(top_n)]

def generate_hashtags(text, top_n=8):
    cleaned = clean_text(text)
    if not cleaned:
        return []
    if use_nltk:
        try:
            keywords = extract_keywords_nltk(cleaned, top_n=top_n)
        except Exception:
            keywords = extract_keywords_fallback(cleaned, top_n=top_n)
    else:
        keywords = extract_keywords_fallback(cleaned, top_n=top_n)

    hashtags = []
    for kw in keywords:
        h = phrase_to_hashtag(kw)
        if h:
            hashtags.append(h)

    # If too few, fill from most common single words
    if len(hashtags) < top_n:
        more = extract_keywords_fallback(cleaned, top_n=top_n*2)
        for m in more:
            h = phrase_to_hashtag(m)
            if h and h not in hashtags:
                hashtags.append(h)
            if len(hashtags) >= top_n:
                break

    return hashtags[:top_n]
