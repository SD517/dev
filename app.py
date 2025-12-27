from flask import Flask, request, render_template
import pandas as pd
import google.generativeai as genai
from dotenv import load_dotenv
import os

#calling api key / creating an environment
load_dotenv()

app = Flask(__name__)

#configure gemini #env create model version
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model=genai.GenerativeModel("gemini-2.5-flash")

#reading data pandas to read csv or dataframwork
df=pd.read_csv("qa_data (1).csv")

#convert csv for into text content
context_text =""
for _,row in df.iterrows():
    context_text += f"Q: {row['question']}\nA: {row['answer']}\n\n"

def ask_gemini(query):
    prompt =f"""
You are a Q&A assistant.

Answer ONLY using the context below.
If the answer is not resent, say: No relevant Q&A found.

Context:
{context_text}

Question: {query}
"""
    response=model.generate_content(prompt)
    return response.text.strip()

#Route function
@app.route("/", methods=["GET","POST"])
def home():
    answer = "" 
    if request.method=="POST":
        query = request.form["query"]
        answer =ask_gemini(query)
    return render_template("index.html",answer=answer)
#run flask app
if __name__=="__main__":
    app.run()
