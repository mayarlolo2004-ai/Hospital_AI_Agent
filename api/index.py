from fastapi import FastAPI`n`napp = FastAPI(title="Hospital AI Agent")`n`n@app.get("/")`ndef root():`n    return {"status": "online", "message": "Hospital AI Agent API is running"}
