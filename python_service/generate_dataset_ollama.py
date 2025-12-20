import json
import pandas as pd
import ollama
from ollama import Client
import time
from tqdm import tqdm

# ==========================================
# 1. CONFIGURATION
# ==========================================
# Connect to your specific local Ollama instance
OLLAMA_URL = "http://127.0.0.1:11434"
MODEL_NAME = "gpt-oss:120b-cloud"  # Your custom model

DATA_FILE = "courses_db.json"
OUTPUT_FILE = "dataset_ollama.csv"
SAMPLES_PER_COURSE = 10  # Start small to test speed (3 batches * 5 queries = 15 rows per course)

# Initialize the client with your specific URL
client = Client(host=OLLAMA_URL)

# ==========================================
# 2. GENERATION LOGIC
# ==========================================
def generate_queries_with_ollama(course_code, course_name, skills):
    """
    Sends a prompt to your local Ollama instance to generate realistic student queries.
    """
    # Clean skills list for the prompt (limit to top 8 to save context/speed)
    skills_str = ", ".join(skills[:8]) 
    
    prompt = f"""
    Act as a university student. I need you to generate 5 different search queries or questions 
    that a student would type to find a course called "{course_name}" ({course_code}).
    
    The course teaches these skills: {skills_str}.
    
    Rules:
    1. Do not mention the course code "{course_code}" in the queries.
    2. Use natural, casual language (e.g., "how to build apps", "class for python").
    3. Vary the intent: some conceptual ("what is X"), some practical ("learn to X"), some career-focused.
    4. Provide ONLY the 5 queries, one per line. No numbering, no extra text.
    """

    try:
        # Using the specific client configured for your URL
        response = client.chat(model=MODEL_NAME, messages=[
            {'role': 'user', 'content': prompt},
        ])
        
        # Extract content and split by lines
        raw_text = response['message']['content']
        
        # Cleanup: remove empty lines and bullet points/numbers if the model adds them
        queries = []
        for line in raw_text.split('\n'):
            clean_line = line.strip()
            # Remove "1. ", "2. ", "- " etc. if present
            clean_line = clean_line.lstrip("1234567890.- ")
            if clean_line:
                queries.append(clean_line)
                
        return queries
    
    except Exception as e:
        print(f"❌ Error with Ollama ({MODEL_NAME}): {e}")
        return []

# ==========================================
# 3. MAIN EXECUTION
# ==========================================
if __name__ == "__main__":
    print(f"🔌 Connecting to Ollama at {OLLAMA_URL}...")
    
    # 1. Load your course DB
    try:
        with open(DATA_FILE, 'r') as f:
            raw_courses = json.load(f)
    except FileNotFoundError:
        print(f"❌ Error: '{DATA_FILE}' not found.")
        exit()

    # 2. Deduplicate (Smart Logic from before)
    unique_courses_map = {}
    for entry in raw_courses:
        code = entry.get('course_code')
        if not code: continue
        
        current_score = len(entry.get('associated_skills', [])) + len(entry.get('course_content_outline', []))
        
        if code not in unique_courses_map:
            unique_courses_map[code] = entry
        else:
            existing_entry = unique_courses_map[code]
            existing_score = len(existing_entry.get('associated_skills', [])) + len(existing_entry.get('course_content_outline', []))
            if current_score > existing_score:
                unique_courses_map[code] = entry

    unique_courses = list(unique_courses_map.values())
    
    dataset = []
    print(f"🚀 Starting AI Generation using model: {MODEL_NAME}")
    print(f"📝 Processing {len(unique_courses)} courses. Target: {SAMPLES_PER_COURSE * 5} queries per course.")

    # 3. Loop through courses
    for course in tqdm(unique_courses, desc="Generating Rows"):
        code = course['course_code']
        name = course['course_name']
        skills = course.get('associated_skills', [])

        # Generate N batches of queries
        for _ in range(SAMPLES_PER_COURSE):
            ai_queries = generate_queries_with_ollama(code, name, skills)
            
            for q in ai_queries:
                dataset.append({"text": q, "label": code})
                
    # 4. Save
    if dataset:
        df = pd.DataFrame(dataset)
        df.to_csv(OUTPUT_FILE, index=False)
        print(f"\n✅ Success! Generated {len(df)} AI-powered rows.")
        print(f"💾 Saved to '{OUTPUT_FILE}'")
    else:
        print("\n⚠️ No data generated. Check if Ollama is running.")
    
    df_template = pd.read_csv("dataset.csv")
    df_ollama = pd.read_csv("dataset_ollama.csv")
    final_df = pd.concat([df_template, df_ollama])
    final_df.to_csv("final_dataset.csv", index=False)