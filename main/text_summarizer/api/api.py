from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import uvicorn

# Initialize a session using Amazon S3
app = FastAPI()

class TextSummarization(BaseModel):
    text: str

@app.get("/")
def index():
    return {"message" : "Welcome to the Text Summarization API"}

@app.post("/summarize")
async def summarize(textData: TextSummarization):
    try:
        with open("text_summarizer/models/text.pkl","rb") as f:
            model = pickle.load(f)
        # textData.text = re.sub(r"[\\'\"]",repl="",string=textData.text)
        return  model(textData.text, min_length=10)

    except Exception as e:
        return {"error": str(e)}
    
if __name__ == "__main__":
    uvicorn.run("api:app", host="localhost", port=1112, reload=True)
