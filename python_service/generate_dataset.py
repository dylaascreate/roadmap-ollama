import json
import csv
import random

# ==========================================
# 1. CONFIGURATION
# ==========================================
INPUT_JSON = 'courses_db.json'
OUTPUT_CSV = 'dataset.csv'
TARGET_ROWS = 50000  # <--- UPGRADED TO 50K

# Synonyms to create variety
VERBS = ["learn", "study", "understand", "master", "practice", "get better at", "explore", "review"]
NOUNS = ["course", "class", "module", "subject", "lesson", "tutorial", "guide"]
ADJECTIVES = ["basic", "advanced", "quick", "detailed", "comprehensive", "simple", "professional", "industry-standard", "complete"]
PREFIXES = ["I want to", "I need to", "Can you help me", "How do I", "Where to", "Best way to", "Looking for", "Recommend a"]

# ==========================================
# 2. LOAD DATA
# ==========================================
print(f"📖 Reading skills from {INPUT_JSON}...")
try:
    with open(INPUT_JSON, 'r', encoding='utf-8') as f:
        courses = json.load(f)
except FileNotFoundError:
    print(f"❌ Error: {INPUT_JSON} not found.")
    exit()

# ==========================================
# 3. GENERATE MASSIVE DATA
# ==========================================
dataset = []
print(f"⚙️ Generating {TARGET_ROWS} rows of synthetic data...")

# We loop until we hit the target
while len(dataset) < TARGET_ROWS:
    
    # Pick a random course
    course = random.choice(courses)
    code = course['course_code']
    name = course['course_name']
    
    # Pick a random skill from that course (or use the course name)
    possible_keywords = course['associated_skills'] + [name] + name.split()
    keyword = random.choice(possible_keywords)
    
    # Clean the keyword (remove brackets)
    clean_keyword = keyword.split('(')[0].strip()
    if len(clean_keyword) < 2: continue

    # --- GENERATION STRATEGIES ---
    
    # Strategy 1: The "Robot" Sentence (Standard)
    # "I want to learn Java"
    sentence = f"{random.choice(PREFIXES)} {random.choice(VERBS)} {clean_keyword}"
    dataset.append([sentence, code])

    # Strategy 2: The "Lazy Student" (Just the keyword + question mark)
    # "java?"
    if random.random() > 0.5:
        dataset.append([f"{clean_keyword}?", code])

    # Strategy 3: The "Specific" Request (Adjectives)
    # "advanced Java tutorials"
    sentence = f"{random.choice(ADJECTIVES)} {clean_keyword} {random.choice(NOUNS)}"
    dataset.append([sentence, code])
    
    # Strategy 4: The "Natural" Question
    # "is java hard to learn?"
    sentence = f"is {clean_keyword} hard to {random.choice(VERBS)}?"
    dataset.append([sentence, code])
    
    # Strategy 5: Random Case (Noise)
    # "JAVA programming"
    if random.random() > 0.7:
        dataset.append([clean_keyword.upper(), code])
    else:
        dataset.append([clean_keyword.lower(), code])

# ==========================================
# 4. FINALIZE
# ==========================================
# Shuffle so the AI doesn't learn patterns based on order
random.shuffle(dataset)

# Cut exactly to target (in case we went over)
final_data = dataset[:TARGET_ROWS]

print(f"💾 Saving {len(final_data)} rows to {OUTPUT_CSV}...")

with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['query', 'course_code']) # Header
    writer.writerows(final_data)

print("✅ Done! You now have a 50,000 row dataset.")