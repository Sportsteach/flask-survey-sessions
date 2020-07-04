from flask import Flask, request, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "Oregon-trail-rules"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

ANSWERS = "answers"


@app.route("/start")
def start_survey():
    """Start of the survey"""
    session[ANSWERS] = []
    return render_template("/start.html", survey=survey)


@app.route("/questions/<int:id>")
def start_questions(id):
    """First question and moves to the next"""
    responses = session.get(ANSWERS)
    question = survey.questions[id]

    if (len(responses) == len(survey.questions)):
        return redirect("/complete")

    if (len(responses) != id):
        flash(f"Invalid question id: {id}.")
        return redirect(f"/questions/{len(responses)}")

    return render_template("/questions.html", question=question)


@ app.route("/answers", methods=["POST"])
def answer_survey():
    """Grabs the answers from the survey"""
    choice = request.form['answer']

    responses = session[ANSWERS]
    responses.append(choice)
    session[ANSWERS] = responses

    if (len(responses) == len(survey.questions)):
        return redirect("/complete")

    return redirect(f"/questions/{len(responses)}")


@ app.route("/complete")
def complete():
    responses = session.get(ANSWERS)
    """After survey is complete page to thank"""
    return render_template("complete.html", responses=responses)
