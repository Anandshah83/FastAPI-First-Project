from fastapi import FastAPI
app=FastAPI()

@app.get('/')
def home():
    return{
        "message":"Hello ji fist I would like to say thanks using fatsapi"
    }