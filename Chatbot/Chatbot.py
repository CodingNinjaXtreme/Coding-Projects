import wikipedia
import random
import pyttsx3

# --- Text-to-Speech setup ---
engine = pyttsx3.init()
engine.setProperty('rate', 175)  # Speed (default 200)
engine.setProperty('volume', 1)  # Max volume

def speak(text):
    print(f"🗣 {text}")
    try:
        engine.say(text)
        engine.runAndWait()
    except:
        print("⚠️ Speech engine failed.")

# --- Safety filter ---
BAD_WORDS = [
    "sex", "violence", "kill", "drugs", "terror", "nazi", "racist", "suicide",
    "murder", "assault", "genocide", "porn", "abuse", "mhiolest"
]

def is_safe(text):
    text = text.lower()
    return not any(bad in text for bad in BAD_WORDS)

# --- Greetings ---
GREETINGS = ["hi", "hello", "hey", "yo", "sup", "hola", "namaste"]
GREETING_RESPONSES = ["Hello!", "Hi there!", "Hey!", "Howdy!", "Nice to see you!"]

def is_greeting(text):
    return text.lower().strip() in GREETINGS

# --- Clean user question for search ---
def clean_query(raw):
    raw = raw.lower().strip()
    prefixes = [
        "who is", "what is", "what's", "when is", "when was",
        "why is", "why does", "how does", "how is", "how do",
        "tell me about", "give me info on", "define", "explain"
    ]
    for prefix in prefixes:
        if raw.startswith(prefix):
            raw = raw[len(prefix):].strip()
            break
    return raw

# --- Best Summary Fetcher ---
def get_summary(user_input):
    try:
        query = clean_query(user_input)
        search_results = wikipedia.search(query)

        if not search_results:
            return "❓ I couldn't find anything about that."

        keywords = query.lower().split()
        scored_results = []

        for title in search_results:
            score = 0
            title_lower = title.lower()

            # Boost score for exact match
            if title_lower == query:
                score += 100

            # Add score for keyword matches
            score += sum(1 for word in keywords if word in title_lower)

            if "(" not in title:
                score += 2  # Prefer cleaner titles

            scored_results.append((score, title))

        scored_results.sort(reverse=True)

        for score, title in scored_results:
            try:
                summary = wikipedia.summary(title, sentences=2)
                result = f"📘 ({title})\n{summary}"

                if is_safe(result) and any(word in result.lower() for word in keywords):
                    return result

            except (wikipedia.exceptions.DisambiguationError, wikipedia.exceptions.PageError):
                continue
            except:
                try:
                    page = wikipedia.page(title)
                    summary = page.summary[:500]
                    result = f"📘 ({page.title})\n{summary}..."
                    if is_safe(result):
                        return result
                except:
                    continue

        return "⚠️ I found related topics, but couldn’t find a safe or exact summary."

    except Exception:
        return "⚠️ Something went wrong while getting the information."

# --- Chatbot Loop ---
def chatbot():
    print("🤖 SafeSmartBot: Ask me anything about the world, ideas, or history!")
    print("⚠️ I won’t respond to unsafe or inappropriate topics.")
    speak(random.choice(GREETING_RESPONSES))

    while True:
        user_input = input("\nYou: ").strip()

        if user_input.lower() in ["exit", "quit", "bye"]:
            speak("Goodbye! Stay curious and stay safe!")
            break

        if not is_safe(user_input):
            speak("❌ That topic is restricted. Please ask something appropriate.")
            continue

        if is_greeting(user_input):
            speak(random.choice(GREETING_RESPONSES))
            continue

        response = get_summary(user_input)
        speak(response)

# --- Run it ---
chatbot()
