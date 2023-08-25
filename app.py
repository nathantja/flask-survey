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

    return render_template("survey_start.html", survey=survey)


@app.post("/begin")
def begin_survey():
    """Begin survey"""

    session["responses"] = []

    return redirect("/question/0")


@app.get("/question/<int:id>")
def display_question(id):
    """Display question"""

    responses = session.get("responses")
    is_completed = len(responses) == len(survey.questions)

    if responses == None:
        return redirect("/")

    if is_completed:
        flash("You've already completed this survey")
        return redirect("/thank-you")

    if id > len(responses):
        id = len(responses)
        flash("Can't access invalid question")
        return redirect(f"/question/{id}")

    survey_question = survey.questions[id]

    return render_template("question.html", question=survey_question)


@app.post("/answer")
def handle_answer():
    """Submit answer and show next question or thank you page"""
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
    """Render survey results"""
    responses = session.get("responses")

    if responses == None:
        return redirect("/")

    is_completed = len(responses) == len(survey.questions)

    if not is_completed:
        return redirect(f"/question/{len(session['responses'])}")

    return render_template("completion.html",
                           questions=survey.questions,
                           answers=session['responses'])
