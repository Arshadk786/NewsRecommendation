from fastapi import FastAPI
from pydantic import BaseModel
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
import uvicorn
import warnings
from sklearn.exceptions import InconsistentVersionWarning
warnings.filterwarnings("ignore", category=InconsistentVersionWarning)

class FakeNews(BaseModel):
    text: str

app = FastAPI()

with open("fake_news/models/fake_news.pkl", "rb") as f:
    model_data = pickle.load(f)

tfidf_vectorizer = model_data['vectorizer']
model = model_data['model']

#Endpoints
@app.get('/')
def index():
    return {"message": "Welcome to Fake News API"}

@app.post("/check")
def check(fake_news: FakeNews):
    # Transform input text into TF-IDF features
    tfidf_features = tfidf_vectorizer.transform([fake_news.text])

    # Make prediction using the pre-trained model
    prediction = model.predict(tfidf_features)

    return {"prediction": prediction.tolist()}

if __name__ == "__main__":
    uvicorn.run("api:app", host="localhost", port=1111, reload=True)



