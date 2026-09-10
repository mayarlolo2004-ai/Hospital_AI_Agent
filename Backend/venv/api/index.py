from fastapi import FastAPI

app = FastAPI(title="Hospital AI Agent")

@app.get("/")
def read_root():
    return {"status": "online", "message": "Hospital AI Agent API is running"}