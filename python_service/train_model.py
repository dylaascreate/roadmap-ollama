import pandas as pd
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# 1. Load the new dataset
print("📂 Loading dataset...")
try:
    df = pd.read_csv('dataset.csv')
    
    # Check if we need to rename columns to match legacy code or use new names
    # The new generator uses 'text' and 'label'
    if 'text' in df.columns and 'label' in df.columns:
        df = df.dropna(subset=['text', 'label'])
        X = df['text']
        y = df['label']
    # Fallback for old CSV format
    elif 'query' in df.columns and 'course_code' in df.columns:
        df = df.dropna(subset=['query', 'course_code'])
        X = df['query']
        y = df['course_code']
    else:
        raise ValueError("CSV columns must be ['text', 'label'] or ['query', 'course_code']")

    print(f"✅ Loaded {len(df)} rows of training data.")

    # 2. Split Data (Optional, but good for verifying accuracy)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 3. Build the Pipeline
    # CountVectorizer: Converts text to matrix of token counts
    # MultinomialNB: The classifier
    model = make_pipeline(CountVectorizer(), MultinomialNB())

    # 4. Train
    print("🧠 Training the model (this might take a moment)...")
    model.fit(X_train, y_train)

    # 5. Evaluate
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    print(f"🎯 Model Accuracy: {accuracy * 100:.2f}%")

    # 6. Save the Model
    with open('devnexus_recommender.pkl', 'wb') as f:
        pickle.dump(model, f)
    
    print("💾 Model saved as 'devnexus_recommender.pkl'")

except Exception as e:
    print(f"❌ Error: {e}")