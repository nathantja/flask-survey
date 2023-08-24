from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


@app.get("/")
def survey_start():
    """Render survey start"""

    session["responses"] = []

    return render_template("survey_start.html", survey=survey)


@app.post("/begin")
def begin_survey():
    """Begin survey"""
    return redirect("/question/0")


# make sure to start the survey before showing questions

@app.get("/question/<int:id>")
def display_question(id):
    """Display question"""

    if (session["responses"] != [] ):
        return redirect("/")

    else:
        survey_question = survey.questions[id]

        return render_template("question.html",
                            question=survey_question)

#response length could be different, can skip questions
#have logic to fill survey in order

@app.post("/answer")
def handle_answer():
    """Appends answer value to reponses and redirects to next question or thank you"""
    answer = request.form['answer']

    responses = session["responses"]
    responses.append(answer)
    session["responses"] = responses

    if len(session["responses"]) == len(survey.questions):
        return redirect("/thank-you")
    else:
        return redirect(f"/question/{len(session['responses'])}")


@app.get("/thank-you")
def thank_user():
    """Grabs questions and reponses and renders survey completion page"""
    results = zip(survey.questions, session["responses"])

    return render_template("completion.html", results=results)
