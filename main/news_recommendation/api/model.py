from fastapi import FastAPI, HTTPException
from typing import List
import pandas as pd
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import uvicorn

app = FastAPI()

@app.get("/")
def index():
    return "Welcome to BIHAR"

# Load and preprocess news data
def load_news_data():
    try:
        response = requests.get('https://newsapi.org/v2/everything?sources=the-times-of-india&apiKey=f920a5d9981e42de91c052c8471db7a2')
        if response.status_code == 200:
            news_data = response.json()['articles']
            df = pd.DataFrame(news_data)[['title', 'description', 'url', 'publishedAt','urlToImage']]
            df['tags'] = df['title'] + df['description']
            df['tags'] = df['tags'].apply(lambda x: x.lower())
            return df
        else:
            raise HTTPException(status_code=response.status_code, detail=response.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Function to recommend articles
def recommend_articles(user_activities: List[str], num_recommendations: int = 10):
    df = load_news_data()

    # Initialize TF-IDF vectorizer
    tfidf_vectorizer = TfidfVectorizer(max_features=1689, stop_words='english')
    tfidf_matrix = tfidf_vectorizer.fit_transform(df['tags'])

    try:
        # Combine the user's activities into a single string
        user_activity_text = ' '.join(user_activities)

        # Transform the user's activity using the same TF-IDF vectorizer
        user_profile = tfidf_vectorizer.transform([user_activity_text])

        # Calculate similarity between user profile and all articles
        cosine_scores = cosine_similarity(user_profile, tfidf_matrix)

        # Get indices of articles sorted by similarity score
        article_indices = cosine_scores.argsort()[0][::-1]

        # Recommend top num_recommendations articles
        recommended_articles = df.iloc[article_indices[:num_recommendations]]

        # Create a DataFrame with titles and links
        recommended_df = recommended_articles[['title', 'url', 'description', 'publishedAt','urlToImage']]
        return recommended_df.to_dict(orient='records')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/recommend")
async def get_recommendations(user_activities: List[str]):
    try:
        if not user_activities:
            raise HTTPException(status_code=400, detail="User activities are required.")
        recommendations = recommend_articles(user_activities)
        return recommendations
    except HTTPException as e:
        raise e
    

if __name__ == '__main__':
    uvicorn.run("model:app",host = "localhost", port = 1113,reload = True)