#http://127.0.0.1:5000/movie?pelicula=terminator
from dotenv import load_dotenv
import os

import sys
from flask import Flask, jsonify, request
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain.schema.runnable import RunnableSequence
from flask import Flask, request, render_template, jsonify

# This is a sample Python script.

# Press Mayús+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from dotenv import load_dotenv
load_dotenv()
openai_api_key = os.environ.get("OPENAI_API_KEY")
#openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

def obtener_genero(pelicula_name):
    prompt = ChatPromptTemplate.from_template("Indica en una palabra de qué género es la película: {pelicula}")
    #llm = ChatOpenAI()
    llm = ChatOpenAI(openai_api_key=openai_api_key)
    parser = StrOutputParser()
    pipeline = RunnableSequence(prompt | llm | parser)
    return pipeline.invoke({"pelicula": pelicula_name})

@app.route('/', methods=['GET', 'POST'])
def main():
    resultado =""
    if request.method == 'POST':
        pelicula_name = request.form.get('pelicula')
        resultado = obtener_genero(pelicula_name)
    return render_template('index.html', resultado=resultado)


@app.route('/movie', methods=['GET'])
def get_movie():
    pelicula_name = request.args.get('pelicula')
    if not pelicula_name:
        return jsonify({"error": "Debe enviar el parámetro 'pelicula'"}), 400
    resultado = obtener_genero(pelicula_name)
    return jsonify({"genero": resultado})



#necesario si se ejecuta de manera local
#if __name__ == "__main__":
#    app.run(debug=True)
