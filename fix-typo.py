#!/usr/bin/env python3
import subprocess
import urllib.request
import urllib.parse
import json
import sys
import os
import re
import time
import difflib

os.environ["DISPLAY"] = os.environ.get("DISPLAY", ":0")

# 1. Load English dictionary for high-precision spell check and layout detection
WORDS = set()
try:
    with open("/usr/share/dict/words", "r", encoding="utf-8", errors="ignore") as f:
        WORDS = set(line.strip().lower() for line in f)
except Exception:
    pass

# Common typo direct map for precision
COMMON_TYPOS = {
    "wnat": "want", "teh": "the", "amke": "make", "coroet": "correct", "coroect": "correct",
    "speieng": "spelling", "meistck": "mistake", "mistakc": "mistake", "shorcir": "shortcut",
    "prese": "precise", "pelae": "please", "exison": "extension", "exiosns": "extensions",
    "etx": "text", "past": "paste", "kb": "keyboard", "woneely": "wrongly", "mistyeneg": "mistyping",
    "punktuaion": "punctuation", "arbci": "Arabic", "wheil": "while", "thing": "think", "wokrirng": "working",
    "pls": "please", "plz": "please", "bc": "because", "cuz": "because", "idk": "I don't know",
    "imo": "in my opinion", "thx": "thanks", "ty": "thank you", "u": "you", "ur": "your", "r": "are",
    "hes": "he's", "shes": "she's", "cant": "can't", "wont": "won't", "dont": "don't", "didnt": "didn't",
    "isnt": "isn't", "arent": "aren't", "couldnt": "couldn't", "wouldnt": "wouldn't", "shouldnt": "shouldn't",
    "thats": "that's", "whats": "what's", "wheres": "where's", "hows": "how's", "whens": "when's"
}

# Arabic common words for layout detection
ARABIC_COMMON_WORDS = {
    "سلام", "عليكم", "مرحبا", "اهلا", "أهلا", "الان", "الآن", "كيف", "حالك", "شكرا", "شكراً",
    "نعم", "لا", "صباح", "مساء", "الخير", "النور", "الله", "انشاء", "إن", "شاء", "في", "من",
    "على", "عن", "مع", "الى", "إلى", "هذا", "هذه", "ذلك", "تلك", "هو", "هي", "هم", "نحن", "أنا", "انا",
    "انت", "أنت", "انتم", "أنتم", "كان", "يكون", "تكون", "تم", "تطبيق", "نظام", "برنامج", "ملف", "كتابة",
    "عايز", "محتاج", "ممكن", "فين", "ليه", "ازاي", "إزاي", "شغال", "مش", "كله", "تمام", "يا", "اخي", "أخي",
    "جميل", "حلو", "كويس", "شكر", "معك", "معي", "عندي", "عندك", "فيه", "فيها", "منك", "مني"
}

# Common English names and modern tech words
COMMON_NAMES_AND_TECH = {
    "ameen", "mohamed", "ahmed", "ali", "omar", "youssef", "mahmoud", "adham", "amr",
    "khaled", "mostafa", "hassan", "hussein", "sayed", "tarek", "fatima", "mariam", "nour",
    "youtuber", "youtube", "google", "facebook", "twitter", "github", "docker", "discord", "notion"
}
WORDS.update(COMMON_NAMES_AND_TECH)

# Keyboard layout character maps
EN_TO_AR = {
    "q": "ض", "w": "ص", "e": "ث", "r": "ق", "t": "ف", "y": "غ", "u": "ع", "i": "ه", "o": "خ", "p": "ح", "[": "ج", "]": "د",
    "a": "ش", "s": "س", "d": "ي", "f": "ب", "g": "ل", "h": "ا", "j": "ت", "k": "ن", "l": "م", ";": "ك", "'": "ط",
    "z": "ئ", "x": "ء", "c": "ؤ", "v": "ر", "b": "لا", "n": "ى", "m": "ة", ",": "و", ".": "ز", "/": "ظ", "`": "ذ",
    "~": "ّ", "Q": "َ", "W": "ً", "E": "ُ", "R": "ٌ", "T": "لإ", "Y": "إ", "U": "‘", "I": "÷", "O": "×", "P": "؛",
    "{": "<", "}": ">", "A": "ِ", "S": "ٍ", "D": "]", "F": "[", "G": "لأ", "H": "أ", "J": "ـ", "K": "،", "L": "/",
    ":": ":", "\"": "\"", "Z": "~", "X": "ْ", "C": "}", "V": "{", "B": "لآ", "N": "آ", "M": "'", "<": ",", ">": ".", "?": "؟"
}

AR_TO_EN = {v: k for k, v in EN_TO_AR.items()}
AR_TO_EN["لا"] = "b"
AR_TO_EN["لإ"] = "T"
AR_TO_EN["لأ"] = "G"
AR_TO_EN["لآ"] = "B"

def ar_to_en(text):
    t = text.replace("لإ", "T").replace("لأ", "G").replace("لآ", "B").replace("لا", "b")
    return "".join(AR_TO_EN.get(c, c) for c in t)

def en_to_ar(text):
    return "".join(EN_TO_AR.get(c, c) for c in text)

def detect_accidental_layout(text):
    has_ar = any('\u0600' <= c <= '\u06FF' for c in text)
    has_en = any(c.isascii() and c.isalpha() for c in text)

    # 1. Arabic text: check if it was typed accidentally instead of English
    if has_ar and not has_en:
        ar_words = [re.sub(r'[^\w]', '', w) for w in text.split()]
        real_ar_count = sum(1 for w in ar_words if w in ARABIC_COMMON_WORDS)
        
        converted = ar_to_en(text)
        en_words = [re.sub(r'[^a-zA-Z]', '', w) for w in converted.lower().split()]
        en_matches = sum(1 for w in en_words if w in WORDS or w in COMMON_TYPOS)

        if en_matches > 0 and (en_matches >= len(en_words) * 0.35 or real_ar_count == 0):
            return converted, "en", True
        return text, "ar", False

    # 2. English text: check if it was typed accidentally instead of Arabic
    if not has_ar:
        converted = en_to_ar(text)
        ar_words = [re.sub(r'[^\u0600-\u06FF]', '', w) for w in converted.split()]
        ar_matches = sum(1 for w in ar_words if w in ARABIC_COMMON_WORDS)

        en_words = [re.sub(r'[^a-zA-Z]', '', w) for w in text.lower().split()]
        en_matches = sum(1 for w in en_words if w in WORDS or w in COMMON_TYPOS or len(w) <= 2)

        if ar_matches > 0 and (ar_matches >= len(ar_words) * 0.35 or ar_matches > en_matches):
            return converted, "ar", True
        return text, "en", False

    return text, "auto", False

def run_cmd(cmd):
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=2)
        return res.stdout.strip()
    except Exception:
        return ""

def get_text():
    # Small pause to allow user to release Alt+Q modifier keys
    time.sleep(0.15)

    # 1. Try active primary selection (mouse-highlighted text)
    text = run_cmd(["xclip", "-o", "-selection", "primary"])
    if text and text.strip():
        return text.strip()

    # 2. Try copying highlighted text via synthetic Ctrl+C
    try:
        from pynput.keyboard import Key, Controller
        kb = Controller()
        with kb.pressed(Key.ctrl):
            kb.press('c')
            kb.release('c')
        time.sleep(0.1)
        text = run_cmd(["xclip", "-o", "-selection", "clipboard"])
        if text and text.strip():
            return text.strip()
    except Exception:
        pass

    # 3. Fallback to copyq clipboard
    text = run_cmd(["copyq", "clipboard"])
    if text and text.strip():
        return text.strip()

    return ""

def correct_word(w):
    clean = re.sub(r"[^\w']", "", w.lower())
    if not clean:
        return w
    if clean in COMMON_TYPOS:
        rep = COMMON_TYPOS[clean]
        if w.isupper(): return rep.upper()
        if w[0].isupper(): return rep.capitalize()
        return rep
    if clean in WORDS:
        return w
    matches = difflib.get_close_matches(clean, WORDS, n=1, cutoff=0.75)
    if matches:
        rep = matches[0]
        if w.isupper(): return rep.upper()
        if w[0].isupper(): return rep.capitalize()
        return rep
    return w

def fix_with_dictionary(text):
    words = text.split()
    return " ".join(correct_word(w) for w in words)

def fix_with_languagetool(text, lang="auto"):
    data = urllib.parse.urlencode({"text": text, "language": lang}).encode("utf-8")
    req = urllib.request.Request("https://api.languagetool.org/v2/check", data=data, headers={"User-Agent": "TypoFixer/1.0"})
    with urllib.request.urlopen(req, timeout=4) as res:
        result = json.loads(res.read().decode("utf-8"))
        chars = list(text)
        for match in sorted(result.get("matches", []), key=lambda m: m["offset"], reverse=True):
            offset = match["offset"]
            length = match["length"]
            replacements = match.get("replacements", [])
            if replacements:
                repl = replacements[0]["value"]
                chars[offset:offset+length] = list(repl)
        return "".join(chars)

def format_punctuation_and_caps(text):
    if not text: return ""
    text = text.strip()
    if text and text[0].isascii() and text[0].isalpha():
        text = text[0].upper() + text[1:]
    
    question_words = ["what", "who", "where", "when", "why", "how", "is", "are", "can", "could", "would", "do", "does", "did"]
    first_word = text.split()[0].lower().strip(".,!?;:") if text.split() else ""
    if first_word in question_words and not text.endswith(("?", ".", "!")):
        text += "?"
    return text

def fix_text(text):
    if not text: return ""
    # 1. Accidental layout
    text, detected_lang, swapped_layout = detect_accidental_layout(text)

    # 2. If layout was swapped, preserve proper nouns and apply typo map safely
    if swapped_layout:
        words = text.split()
        fixed_words = []
        for w in words:
            clean = re.sub(r"[^\w']", "", w.lower())
            if clean in COMMON_TYPOS:
                rep = COMMON_TYPOS[clean]
                if w.isupper(): rep = rep.upper()
                elif w[0].isupper(): rep = rep.capitalize()
                fixed_words.append(w.replace(clean, rep))
            else:
                fixed_words.append(w)
        text = " ".join(fixed_words)
    else:
        # 3. Standard typo check
        if detected_lang in ["en", "auto"]:
            text = fix_with_dictionary(text)
        try:
            lt_fixed = fix_with_languagetool(text, lang=detected_lang)
            if lt_fixed and lt_fixed.strip():
                text = lt_fixed
        except Exception:
            pass

    # 4. Capitalization & Punctuation
    text = format_punctuation_and_caps(text)
    return text

def main():
    text = ""
    if len(sys.argv) > 1:
        text = " ".join(sys.argv[1:]).strip()
    
    if not text:
        text = get_text()

    if not text:
        try:
            p = subprocess.run([
                "zenity", "--entry", 
                "--title=Typo Fixer", 
                "--text=اكتب أو الصق النص الخاطئ هنا لتصحيحه تلقائياً:"
            ], capture_output=True, text=True, timeout=30)
            if p.returncode == 0:
                text = p.stdout.strip()
        except Exception:
            pass

    if not text:
        run_cmd(["notify-send", "-u", "low", "Typo Fixer", "⚠️ حدد النص أو انسخه أولاً"])
        return

    fixed = fix_text(text)
    if not fixed:
        fixed = text

    print(fixed)

    # Copy to clipboard
    try:
        p = subprocess.Popen(["xclip", "-selection", "clipboard"], stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)
        p.communicate(input=fixed.encode("utf-8"))
    except Exception:
        pass
    try:
        p = subprocess.Popen(["xclip", "-selection", "primary"], stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)
        p.communicate(input=fixed.encode("utf-8"))
    except Exception:
        pass

    run_cmd(["copyq", "copy", fixed])

    # Wait for modifier key release then Auto-Paste
    time.sleep(0.15)
    pasted = False
    try:
        from pynput.keyboard import Key, Controller
        kb = Controller()
        with kb.pressed(Key.ctrl):
            kb.press('v')
            kb.release('v')
        pasted = True
    except Exception:
        pass

    if not pasted:
        run_cmd(["copyq", "paste"])

    # Notify
    msg = f"قبل: {text}\nبعد: {fixed}"
    run_cmd(["notify-send", "-u", "normal", "✨ تم تصحيح ولصق النص!", msg])
    run_cmd(["copyq", "popup", "✨ تم تصحيح النص", f"{fixed}\n(تم استبداله ولصقه تلقائياً)"])

if __name__ == "__main__":
    main()
