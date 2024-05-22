from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain_google_genai import GoogleGenerativeAI
from langchain.output_parsers.json import SimpleJsonOutputParser
from fastapi import FastAPI,Form
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated
app=FastAPI()
load_dotenv()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Data(BaseModel):
    tema:Annotated[str, Form()]
    dificuldade:Annotated[str, Form()]
    question_type:Annotated[str, Form()]
    numero_questoes:Annotated[int, Form()]
    lingua:Annotated[str, Form()]
json_parser = SimpleJsonOutputParser()
llm = GoogleGenerativeAI(model="gemini-pro")

@app.post('/chat')
def getQuestions(data:Data):
    try:
        prompt = PromptTemplate.from_template(

        """
        I want you to generate a quiz game following these steps,respond only the questions and must be in json: 
        Title: Quiz Game
        Theme: {tema}
        Difficulty: {dificuldade}
        Number of Questions: {numero_questoes}
        Question Types:{question_type}
        language:{lingua}

        Example Questions:

        Question 1: [Write an example question based on the theme and question type]
        Answer 1: [Write a possible answer]
        Answer 2: [Write a possible answer]
        Answer 3: [Write a possible answer]

        Correct Answer: [Specify the correct answer]
        Question 2: [Write another example question]
        Answer 1: [Write a possible answer]
        Answer 2: [Write a possible answer]
        Answer 3: [Write a possible answer]
        Correct Answer: [Specify the correct answer]

        Additional Information:
        [Include any other information that would be helpful for generating the quiz game]
        Output:

        Example Output:

        "questions": [
            
            "question": "What is the capital of France?",
            "answers": ["Berlin", "Paris", "Madrid","Spain"],
            "correctAnswer": "Paris"
            
        
            "question": "Who painted the Mona Lisa?",
            "answers": ["Michelangelo", "Leonardo da Vinci", "Raphael","Will Smith"],
            "correctAnswer": "Leonardo da Vinci"

            """
        )
        model=prompt|llm|json_parser

        res=model.invoke({'tema':data.tema,'numero_questoes':data.numero_questoes,'dificuldade':data.dificuldade,'question_type':data.question_type,'lingua':data.lingua})
        return res["questions"]
    except:
        return ('ocorreu algum erro tente novamente')


