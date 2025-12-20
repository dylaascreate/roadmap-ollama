import pandas as pd
import pickle
import os
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

# CONFIGURATION
POSSIBLE_DATASETS = ['final_dataset.csv']
MODEL_FILE = 'devnexus.pkl'

def load_data():
    """Tries to find the best available dataset file."""
    for filename in POSSIBLE_DATASETS:
        if os.path.exists(filename):
            print(f"📂 Found dataset: '{filename}'")
            return pd.read_csv(filename)
    return None

def train_devnexus_model():
    print("🚀 Starting Training Process...")
    
    df = load_data()
    
    if df is None:
        print(f"❌ Error: No dataset found. Please run 'generate_dataset.py' first.")
        print(f"   Looking for: {POSSIBLE_DATASETS}")
        return

    try:
        # Standardize column names
        if 'text' in df.columns and 'label' in df.columns:
            df = df.dropna(subset=['text', 'label'])
            X, y = df['text'], df['label']
        elif 'query' in df.columns and 'course_code' in df.columns:
            df = df.dropna(subset=['query', 'course_code'])
            X, y = df['query'], df['course_code']
        else:
            raise ValueError("CSV columns must be ['text', 'label'] or ['query', 'course_code']")

        print(f"✅ Loaded {len(df)} rows. Unique Courses: {y.nunique()}")

        # 1. Split Data (80% Train, 20% Test)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # 2. Build Pipeline
        # TfidfVectorizer: Converts text to numbers, ignoring noise words ('the', 'a')
        # MultinomialNB: fast and effective for text classification
        model = make_pipeline(
            TfidfVectorizer(stop_words='english', ngram_range=(1, 2), min_df=2), 
            MultinomialNB()
        )

        # 3. Train
        print("🧠 Training the model...")
        model.fit(X_train, y_train)

        # 4. Detailed Evaluation
        predictions = model.predict(X_test)
        acc = accuracy_score(y_test, predictions)
        print(f"\n🎯 Model Accuracy: {acc * 100:.2f}%")
        
        # Shows Precision/Recall for every single course
        print("\n📊 detailed Classification Report:")
        print(classification_report(y_test, predictions))

        # 5. Save Model
        with open(MODEL_FILE, 'wb') as f:
            pickle.dump(model, f)
        print(f"💾 Brain saved to '{MODEL_FILE}'")

        # 6. 🧪 SMART TEST MODE (With Confidence Scores)
        print("\n🧪 --- Verification Tests ---")
        
        # Specific queries to test your "Design" fix
        test_queries = [
            "I want to learn design",          # Should be DES3043
            "software architecture patterns",  # Should be DES3043
            "manage a software project",       # Should be DES3073 (Project)
            "how to build mobile apps",        # Should be DES3113
            "learn laravel framework"          # Should be DES3073
        ]
        
        print(f"Testing {len(test_queries)} specific scenarios...\n")
        
        for q in test_queries:
            # Predict just the label
            prediction = model.predict([q])[0]
            
            # Get probability (confidence)
            probs = model.predict_proba([q])[0]
            best_prob = np.max(probs) * 100
            
            # Print result with confidence
            # If confidence is low (< 60%), it means the model is confused
            confidence_marker = "✅" if best_prob > 80 else "⚠️"
            
            print(f"   Query: '{q}'")
            print(f"   👉 Prediction: {prediction} ({best_prob:.1f}% confident) {confidence_marker}")
            print("-" * 40)

    except Exception as e:
        print(f"\n❌ Critical Error during training: {e}")

if __name__ == "__main__":
    train_devnexus_model()