import json
import encodings

from flask import Flask, render_template, request, redirect, url_for, session, flash
from flaskwebgui import FlaskUI
from werkzeug.wrappers import ETagRequestMixin, BaseRequest
from owlready2 import *
import Implementation.Relocation2.POIRankings as relocation

app = Flask(__name__)

# Add variables to app
app.secret_key = "ComfortRating"
app.secret_key = "DistanceRating"
app.secret_key = "CentralityRating"
app.secret_key = "SupplyRating"
app.secret_key = "RebookingRating"

# Run UI app instead of browser
ui = FlaskUI(app)

# App config
width = 500
height = 400
fullscreen = False
maximized = False
app_mode = True
port = 500


class Request(BaseRequest, ETagRequestMixin):
    pass


@app.route('/', methods=['GET', 'POST'])
def welcome():
    error = None
    if request.method == 'POST':
        try:
            select_cps = request.form["select_cps"]
        except:
            return "No input."
        # TODO: GET SELECT_CPS
        return redirect(url_for('reconstructChoice', select_cps=select_cps)), select_cps
    return render_template('welcome_new.html', error=error)


@app.route('/reconstruct/<select_cps>', methods=['GET', 'POST'])
def reconstructChoice(select_cps):
    error = None
    # i want to choose the individual CPS and display its individual features
    if request.method == 'GET':
        select_cps = {"select_cps": select_cps}
        return render_template("reconstruct.html", select_cps=select_cps)
    else:
        return "User input visualization failed. We did not receive your data."



@app.route('/choosePOI/', methods=['GET', 'POST'])
def getPOIData():
    error = None
    # i want to choose the individual CPS and display its individual features
    if request.method == 'POST':
        try:
            select_poi = request.form["select_poi"]
        except:
            "No input"
        # TODO: GET SELECT_POI
        return redirect(url_for('reconstructChoicePOI', select_poi=select_poi)), select_poi
    return render_template('choosePOI.html', error=error)


@app.route('/choosePOI/<select_poi>', methods=['GET', 'POST'])
def reconstructChoicePOI(select_poi):
    error = None
    # i want to choose the individual CPS and display its individual features
    if request.method == 'GET':
        select_poi = {"select_poi": select_poi}
        return render_template("reconstructPOI.html", select_poi=select_poi)
    else:
        return "User input visualization failed. We did not receive your data."


@app.route('/survey/', methods=['GET', 'POST'])
def getSurveyResults():
    error = None
    # Post the rating into owl if input ok
    if request.method == 'POST':
        try:
            comfort_rating = int(request.form["comfort_rating"])
            distance_rating = int(request.form["distance_rating"])
            centrality_rating = int(request.form["centrality_rating"])
            supply_rating = int(request.form["supply_rating"])
            rebooking_rating = int(request.form["rebooking_rating"])
        except:
            return "Not all requested fields are specified. Please review your input."

        # ComfortRating = int(request.form('ComfortRating', type=int)
        if int(request.form["comfort_rating"]) not in range(1, 11) \
                or int(request.form["distance_rating"]) not in range(1, 11) \
                or int(request.form["centrality_rating"]) not in range(1, 11) \
                or int(request.form["supply_rating"]) not in range(1, 11) \
                or int(request.form["rebooking_rating"]) not in range(1, 11):
            error = 'Rating value not in range 1-10, where 10 is optimal'
        else:
            # TODO: integration of additional functionality as for example REASONING
            session['survey_complete'] = True
            flash('Survey submitted. Thank you very much!')
            return redirect(
                url_for('visualizeUserInput', comfort_rating=comfort_rating, distance_rating=distance_rating,
                        centrality_rating=centrality_rating, supply_rating=supply_rating,
                        rebooking_rating=rebooking_rating))
    return render_template('survey.html', error=error)


@app.route("/userInput/<comfort_rating>/<distance_rating>/<centrality_rating>/<supply_rating>/<rebooking_rating>",
           methods=["GET", "POST"])
def visualizeUserInput(comfort_rating, distance_rating, centrality_rating, supply_rating, rebooking_rating):
    if request.method == "GET":
        user_input = {"comfort_rating": comfort_rating, "distance_rating": distance_rating,
                      "centrality_rating": centrality_rating, "supply_rating": supply_rating,
                      "rebooking_rating": rebooking_rating}
        # TODO: GET USER_INPUT
        return render_template("userInput.html", user_input=user_input), user_input
    else:
        return "User input visualization failed. We did not receive your data."


@app.route("/reconstruct/relocation/", methods=["GET", "POST"])
def runRelocation():
    error = None
    if request.method == "POST":
        try:
            point_of_interest = int(request.form["point_of_interest"])

        except:
            return "Not all requested fields are specified. Please review your input."


###
# we want to integrate the functionality of using the flask-user-input and store it
###

@app.route('/process', methods=["GET", "POST"])
def updateCharacterOnto():
    error = None
    if request.method == "POST":
        comfort_rating = int(request.form["comfort_rating"])
        distance_rating = int(request.form["distance_rating"])
        centrality_rating = int(request.form["centrality_rating"])
        supply_rating = int(request.form["supply_rating"])
        rebooking_rating = int(request.form["rebooking_rating"])

        user_input = {"comfort_rating": comfort_rating, "distance_rating": distance_rating,
                      "centrality_rating": centrality_rating, "supply_rating": supply_rating,
                      "rebooking_rating": rebooking_rating}

        ### define CPS-Ontologies
        ontoCPS1 = "http://wwwlab.cs.univie.ac.at/~lukasl93/CPS1.owl"

        # at this point, we want to somehow communicate with another .py or ontology
        # TODO: how to connect to outter source here
        onto = get_ontology(ontoCPS1).load()
        graph = default_world.as_rdflib_graph()

        # here we wanna query the ontology concept or the .py that needs to be updated
        # TODO: how to access the outter sourcest

        flash('arrived here')

        # TODO: how to update based on our rating the outter source
        # now update the needs based on the rating we got
        # onto.update()
        # current_user = onto.query(query.getCurrentUser())[0][0]
        # POIRating = ['Comfort', 'Distance', 'Centrality', 'Supply', 'Rebooking']
        # for rating in ratings:
        # onto.query(query.updatePOIRatings(current_user, rating))

        # return render_template('checkout.html')
        # return render_template('checkout.html')
    # else:
    # return render_template('review.html')

    return render_template('review.html', error=error), user_input


###
# we want to integrate the functionality of using the flask-user-input and store it
###


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    # Method Post needs to request and check the data
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid credentials. Please try again'
        else:
            session['logged_in'] = True
            flash('login successful')
            return redirect(url_for('welcome'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('logout successful. Bye!')
    return redirect(url_for('welcome'))


# Run UI
# ui.run()

# Run browser
if __name__ == '__main__':
    app.run(port=1337, debug=True)
