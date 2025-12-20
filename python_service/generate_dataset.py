import json
import pandas as pd
import random
import re
import itertools

# ==========================================
# 1. SETUP & CONFIGURATION
# ==========================================
DATA_FILE = 'courses_db.json'
OUTPUT_FILE = 'dataset.csv'
TOTAL_TARGET = 20000

# 🛑 GLOBAL STOP WORDS
GLOBAL_STOP_WORDS = {
    "introduction", "overview", "basics", "fundamental", "advanced", 
    "week", "application", "concept", "principles", "theory", "summary"
}

# 🛑 COURSE-SPECIFIC BLACKLIST (Fixes overlap issues)
KEYWORD_BLACKLIST = {
    "DES3073": ["design", "ui", "ux", "interface", "prototype"],
    "DES3013": ["requirements"], 
}

# ==========================================
# 2. TEMPLATES
# ==========================================
single_templates = [
    "I want to learn {k1}", "How do I use {k1}?", "Teach me about {k1}", "What is {k1}?", 
    "Explain {k1} to me", "I need to understand {k1}", "Best course for {k1}", 
    "Where can I learn {k1}?", "Is {k1} covered in this syllabus?", "I need {k1} for my job",
    "How to apply {k1} in real life?", "I want to be a developer who knows {k1}", 
    "Is {k1} important for my career?", "Does the exam cover {k1}?", 
    "Help me with my {k1} assignment", "What are the basics of {k1}?", 
    "{k1} tutorial", "{k1} help", "Learning {k1}", "Can you define {k1}?", 
    "Guide for {k1}", "Difference between old methods and {k1}", 
    "Why is {k1} used?", "Examples of {k1}", "Mastering {k1}"
]

dual_templates = [
    "Relationship between {k1} and {k2}", "How does {k1} relate to {k2}?", 
    "I need help with {k1} and {k2}", "Does this course cover {k1} or {k2}?", 
    "Using {k1} with {k2}", "Explain the connection between {k1} and {k2}", 
    "I am studying {k1} but stuck on {k2}", "Can I use {k1} for {k2}?", 
    "Tutorial for {k1} and {k2}", "Concepts of {k1} vs {k2}", 
    "Difference between {k1} and {k2}", "{k1} vs {k2}", "Can {k1} work with {k2}?"
]

# ==========================================
# 3. HELPER FUNCTIONS
# ==========================================
def clean_outline_text(text):
    return re.sub(r"Week \d+[-]?\d*: ", "", text).strip()

def extract_keywords_from_string(text):
    text = text.replace("(", "|").replace(")", "|").replace("/", "|").replace(",", "|")
    text = text.replace("&", "|").replace(" or ", "|").replace(" and ", "|")
    return [p.strip() for p in text.split("|") if len(p.strip()) > 2]

def is_valid_keyword(word, course_code):
    word_lower = word.lower()
    if word_lower in GLOBAL_STOP_WORDS: return False
    if course_code in KEYWORD_BLACKLIST:
        for bad_term in KEYWORD_BLACKLIST[course_code]:
            if bad_term in word_lower: return False
    return True

# ==========================================
# 4. GENERATION LOGIC
# ==========================================
def generate():
    print("📂 Loading raw data...")
    try:
        with open(DATA_FILE, 'r') as f:
            raw_data = json.load(f)
    except FileNotFoundError:
        print(f"❌ Error: '{DATA_FILE}' not found.")
        return

    # --- 🆕 DEDUPLICATION LOGIC ---
    unique_courses_map = {}
    for entry in raw_data:
        code = entry['course_code']
        # Only add if we haven't seen this code before
        if code not in unique_courses_map:
            unique_courses_map[code] = entry
            
    clean_courses = list(unique_courses_map.values())
    
    print(f"✅ Loaded {len(raw_data)} raw entries.")
    print(f"🧹 Processing {len(clean_courses)} UNIQUE courses.")
    
    if len(clean_courses) == 0:
        print("❌ Error: No courses found.")
        return

    num_courses = len(clean_courses)
    target_per_course = (TOTAL_TARGET // num_courses) + 1
    print(f"🎯 Target: ~{target_per_course} rows per course.")

    dataset = []

    for course in clean_courses:
        code = course['course_code']
        name = course['course_name']
        
        # Gather Keywords
        raw_keywords = set()
        raw_keywords.add(code)
        raw_keywords.add(name)
        
        for skill in course.get('associated_skills', []):
            raw_keywords.add(skill)
            raw_keywords.update(extract_keywords_from_string(skill))
            
        for topic in course.get('course_content_outline', []):
            clean_topic = clean_outline_text(topic)
            raw_keywords.add(clean_topic)
            raw_keywords.update(extract_keywords_from_string(clean_topic))
            
        # Filter Keywords
        final_keywords = []
        for k in raw_keywords:
            if is_valid_keyword(k, code):
                final_keywords.append(k)
        
        final_keywords = sorted(list(set(final_keywords)))
        
        # Generate Rows
        course_unique_texts = set()
        course_data = []
        
        random.shuffle(final_keywords)
        
        # Single keywords
        for k in final_keywords:
            for t in single_templates:
                text = t.format(k1=k)
                if text not in course_unique_texts:
                    course_unique_texts.add(text)
                    course_data.append({"text": text, "label": code})

        # Dual keywords
        if len(course_data) < target_per_course and len(final_keywords) > 1:
            pairs = list(itertools.permutations(final_keywords, 2))
            random.shuffle(pairs)
            pair_idx = 0
            while len(course_data) < target_per_course and pair_idx < len(pairs):
                k1, k2 = pairs[pair_idx]
                template = random.choice(dual_templates)
                text = template.format(k1=k1, k2=k2)
                if text not in course_unique_texts:
                    course_unique_texts.add(text)
                    course_data.append({"text": text, "label": code})
                pair_idx += 1
                
        # Trim to target
        if len(course_data) > target_per_course:
            course_data = course_data[:target_per_course]
            
        print(f"   🔹 {code}: Generated {len(course_data)} rows")
        dataset.extend(course_data)

    # Save
    df = pd.DataFrame(dataset)
    df = df.sample(frac=1).reset_index(drop=True) 
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"\n✅ SUCCESS: Generated {len(df)} training rows.")
    print(f"💾 Saved to '{OUTPUT_FILE}'")

if __name__ == "__main__":
    generate()