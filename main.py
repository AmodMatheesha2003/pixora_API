from fastapi import FastAPI

app = FastAPI(title="pixora API",
              description="Blockchain-based Photos/Digital Art publishing, buying & selling platform")

@app.get("/")
def read_root():
    return {"Pixora FastAPI"}