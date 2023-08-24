from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

responses = []

@app.get("/")
def survey_start():
    """Page where user can start the survey"""
    return render_template("survey_start.html",
                           title = survey.title,
                           instructions = survey.instructions)

@app.post("/begin")
def begin_survey():
    """Begin survey"""
    return redirect("/question/0")

@app.get("/question/<int:id>")
def display_question(id):
    """Display question"""
    survey_question = survey.questions[id]

    return render_template("question.html",
                           question = survey_question)




# @app.post("/answer")