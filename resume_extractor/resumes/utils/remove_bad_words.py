import re

def load_bad_words(path='bad_words.txt'):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            words = [w.strip().lower() for w in f if w.strip()]
        return set(words)
    except FileNotFoundError:
        return {'fuck', 'shit', 'bitch'}

BAD_WORDS = load_bad_words()

def censor_text(text, placeholder='***'):
    def repl(m):
        w = m.group(0)
        return placeholder
    if not text:
        return text
    pattern = re.compile(r'\b(' + '|'.join(re.escape(w) for w in BAD_WORDS) + r')\b', flags=re.IGNORECASE) #creating pattren form txt
    print(pattern)
    return pattern.sub(repl, text)
