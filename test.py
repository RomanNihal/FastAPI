from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def hello():
    return {'message': 'Hello World'}

@app.get("/about")
def about():
    return {'about': 'i am a student learning FastAPI'}

# visit url/docs for the auto generated documentation