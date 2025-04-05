from fastapi import FastAPI

app = FastAPI()

messages = {"greeting": "Hello, World!", "farewell": "Goodbye, World!"}


# dummy commits to bump
@app.get("/message/{key}")
async def get_message(key: str):
    return {"message": messages.get(key, "Message not found")}
