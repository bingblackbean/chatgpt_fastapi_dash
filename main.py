from typing import Optional
import openai
from fastapi import FastAPI
import uvicorn
from fastapi.responses import Response,RedirectResponse


app = FastAPI()


@app.get("/", include_in_schema=False)
async def docs_redirect():
    return RedirectResponse(url='/docs')


@app.put("/chat")
async def ask_data_amber(text):
    openai.api_key = 'sk-your key'
    response = openai.Completion.create(engine = 'text-davinci-003',
                                        prompt = text,temperature = 0.6,
                                        max_tokens = 1000)
    
    return Response( response.choices[0].text)

if __name__ == '__main__':
    uvicorn.run(app)