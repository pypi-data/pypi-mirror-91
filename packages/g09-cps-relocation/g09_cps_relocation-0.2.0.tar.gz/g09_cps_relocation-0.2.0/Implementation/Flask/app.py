import json
import encodings

from markupsafe import escape
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flaskwebgui import FlaskUI
import ast

import livereload

from werkzeug.wrappers import ETagRequestMixin, BaseRequest
from owlready2 import *

import paramiko
from owlready2 import *

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


@app.route('/', methods=['GET', 'POST'], strict_slashes=False)
def welcome():
    error = None
    if request.method == 'POST':
        try:
            select_cps = request.form["select_cps"]
        except:
            return "No input."
        # TODO: GET SELECT_CPS
        return redirect(url_for('reconstructChoice', select_cps=select_cps))
    return render_template('welcome_new.html', error=error)


@app.route('/reconstruct/<select_cps>', methods=['GET', 'POST'], strict_slashes=False)
def reconstructChoice(select_cps):
    error = None
    # i want to choose the individual CPS and display its individual features
    if request.method == 'GET':
        try:
            select_cps = {"select_cps": select_cps}
        except:
            return "Not working."
        return redirect(url_for("getPOIData", select_cps=select_cps))
    return render_template("reconstruct.html", select_cps=select_cps, error=error)


@app.route('/choosePOI/<select_cps>/', methods=['GET', 'POST'])
def getPOIData(select_cps):
    error = None
    # i want to choose the individual CPS and display its individual features
    if request.method == 'POST':
        try:
            select_poi = request.form["select_poi"]
        except:
            "No input"
        # TODO: GET SELECT_POI
        return redirect(url_for('reconstructChoicePOI', select_cps=select_cps, select_poi=select_poi))
    return render_template('choosePOI.html', error=error)


@app.route('/choosePOI/<select_cps>/<select_poi>/', methods=['GET', 'POST'])
def reconstructChoicePOI(select_cps, select_poi):
    error = None
    # i want to choose the individual CPS and display its individual features
    if request.method == 'GET':
        try:
            select_poi = {"select_poi": select_poi}
        except:
            return "Not working."
        return redirect(url_for('getSurveyResults', select_cps=select_cps, select_poi=select_poi))
    return render_template("reconstructPOI.html", select_cps=select_cps, select_poi=select_poi, error=error)


@app.route('/survey/<select_cps>/<select_poi>/', methods=['GET', 'POST'])
def getSurveyResults(select_cps, select_poi):
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
            url_for('visualizeUserInput', select_cps=select_cps, select_poi=select_poi, comfort_rating=comfort_rating,
                    distance_rating=distance_rating,
                    centrality_rating=centrality_rating, supply_rating=supply_rating,
                    rebooking_rating=rebooking_rating))
    return render_template('survey.html', select_cps=select_cps, select_po=select_poi, error=error)


@app.route("/userInput/<select_cps>/<select_poi>/<comfort_rating>/<distance_rating>/<centrality_rating>/"
           "/<supply_rating>/<rebooking_rating>/", methods=["GET", "POST"])
def visualizeUserInput(select_cps, select_poi, comfort_rating, distance_rating, centrality_rating, supply_rating,
                       rebooking_rating):
    error = None
    if request.method == "GET":
        try:
            user_input = {"select_cps": select_cps, "select_poi": select_poi, "comfort_rating": comfort_rating,
                          "distance_rating": distance_rating, "centrality_rating": centrality_rating,
                          "supply_rating": supply_rating,
                          "rebooking_rating": rebooking_rating}
        except:
            return "Not working."
        return redirect(url_for('updateCharacterOnto', select_cps=select_cps, select_poi=select_poi,
                                comfort_rating=comfort_rating, distance_rating=distance_rating,
                                centrality_rating=centrality_rating, supply_rating=supply_rating,
                                rebooking_rating=rebooking_rating))

    # TODO: NOT REACHING THIS POINT
    return render_template("userInput.html", comfort_rating=comfort_rating, distance_rating=distance_rating,
                           centrality_rating=centrality_rating, supply_rating=supply_rating,
                           rebooking_rating=rebooking_rating, error=error)


###
# we want to integrate the functionality of using the flask-user-input and store it
###

@app.route(
    '/process/userInput/<select_cps>/<select_poi>/<comfort_rating>/<distance_rating>/<centrality_rating>/<supply_rating>/<rebooking_rating>/',
    methods=["GET", "POST"])
def updateCharacterOnto(select_cps, select_poi, comfort_rating, distance_rating, centrality_rating, supply_rating,
                        rebooking_rating):
    error = None
    # if request.method == "POST":

    user_input = {"comfort_rating": comfort_rating, "distance_rating": distance_rating,
                  "centrality_rating": centrality_rating, "supply_rating": supply_rating,
                  "rebooking_rating": rebooking_rating}
    print()
    print("User_input received SUCCESS:", user_input)
    # TODO: INSERT ONTO FUNCTIONALITY

    ########### UPDATE ONTOLOGY ############

    # This ontology is empty
    # ontology = "http://wwwlab.cs.univie.ac.at/~lukasl93/CPS1_init.owl"
    # onto = get_ontology(ontology).load()

    print("Ontology loaded")
    print("Following input will be used to create SPARQL:")

    # prepare select_cps variable
    select_cps = ast.literal_eval(select_cps)
    print("CPS selected: ", select_cps)

    # prepare select_poi variable
    select_poi = ast.literal_eval(select_poi)
    print("POI selected: ", select_poi)

    # visualize user_input
    print("User_Input selected: ", user_input)

    # choose the CPS where the character needs to be updated
    if select_cps['select_cps'] == 'CPS1':

        print("CPS1 selected and ready to update!")
        ontology = "http://wwwlab.cs.univie.ac.at/~lukasl93/CPS1init.owl"
        onto = get_ontology(ontology).load()

        with onto:
            for i in range(1, 11):
                sparql_delete = ' PREFIX uni: <http://wwwlab.cs.univie.ac.at/~lukasl93/CPS1init.owl#> DELETE DATA  ' \
                                '{ uni:' + str(select_poi['select_poi']) + \
                                ' uni:hasComfortRating ' + str(i) + \
                                '; uni:hasDistanceRating ' + str(i) + \
                                '; uni:hasCentralityRating ' + str(i) + \
                                '; uni:hasSupplyRating ' + str(i) + \
                                '; uni:hasRebookingRating ' + str(i) + ' . }'

                graph = owlready2.default_world.as_rdflib_graph()
                print("Now delete with:", sparql_delete)
                update_onto = graph.update(sparql_delete)

            sparql_insert = ' PREFIX uni: <http://wwwlab.cs.univie.ac.at/~lukasl93/CPS1init.owl#> INSERT DATA { uni:' \
                            + str(select_poi['select_poi']) + \
                            '  uni:hasComfortRating ' + str(comfort_rating) + \
                            '; uni:hasDistanceRating ' + str(distance_rating) + \
                            '; uni:hasCentralityRating ' + str(centrality_rating) + \
                            '; uni:hasSupplyRating ' + str(supply_rating) + \
                            '; uni:hasRebookingRating ' + str(rebooking_rating) + ' . }'
            print("The SPARQL INSERT STATEMENT is ready:")
            print(sparql_insert)

            graph = owlready2.default_world.as_rdflib_graph()
            update_onto = graph.update(sparql_insert)

        onto.save("CPS1init.owl", format="rdfxml")
        print("Updated ontology successfully!")

        ########### CONNECT TO SERVER ############

        # connect to the server and upload the updated ontology
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect('almighty.cs.univie.ac.at', port=22, username='lukasl93', password='Luki190193')
        sftp = ssh.open_sftp()
        print('The connection to server was successful.')

        # sftp put local and remote path and push to server
        print('The paths getting sorted.')
        localPath = 'CPS1init.owl'
        remotePath = '/home/lukasl93/public_html/CPS1init.owl'
        sftp.put(localPath, remotePath)
        print('Files are uploaded - SUCCESS!')

        # close connection to server
        sftp.close()
        ssh.close()
        print('The connection to server got closed.')

    if select_cps['select_cps'] == 'CPS2':

        print("CPS2 selected and ready to update!")
        ontology = "http://wwwlab.cs.univie.ac.at/~lukasl93/CPS2init.owl"
        onto = get_ontology(ontology).load()

        with onto:
            for i in range(1, 11):
                sparql_delete = ' PREFIX uni: <http://wwwlab.cs.univie.ac.at/~lukasl93/CPS2init.owl#> DELETE DATA  ' \
                                '{ uni:' + str(select_poi['select_poi']) + \
                                ' uni:hasComfortRating ' + str(i) + \
                                '; uni:hasDistanceRating ' + str(i) + \
                                '; uni:hasCentralityRating ' + str(i) + \
                                '; uni:hasSupplyRating ' + str(i) + \
                                '; uni:hasRebookingRating ' + str(i) + ' . }'

                graph = owlready2.default_world.as_rdflib_graph()
                print("Now delete with:", sparql_delete)
                update_onto = graph.update(sparql_delete)

            sparql_insert = ' PREFIX uni: <http://wwwlab.cs.univie.ac.at/~lukasl93/CPS2init.owl#> INSERT DATA { uni:' \
                            + str(select_poi['select_poi']) + \
                            '  uni:hasComfortRating ' + str(comfort_rating) + \
                            '; uni:hasDistanceRating ' + str(distance_rating) + \
                            '; uni:hasCentralityRating ' + str(centrality_rating) + \
                            '; uni:hasSupplyRating ' + str(supply_rating) + \
                            '; uni:hasRebookingRating ' + str(rebooking_rating) + ' . }'
            print("The SPARQL INSERT STATEMENT is ready:")
            print(sparql_insert)

            graph = owlready2.default_world.as_rdflib_graph()
            update_onto = graph.update(sparql_insert)

        onto.save("CPS2init.owl", format="rdfxml")
        print("Updated ontology successfully!")

        ########### CONNECT TO SERVER ############

        # connect to the server and upload the updated ontology
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect('almighty.cs.univie.ac.at', port=22, username='lukasl93', password='Luki190193')
        sftp = ssh.open_sftp()
        print('The connection to server was successful.')

        # sftp put local and remote path and push to server
        print('The paths getting sorted.')
        localPath = 'CPS2init.owl'
        remotePath = '/home/lukasl93/public_html/CPS2init.owl'
        sftp.put(localPath, remotePath)
        print('Files are uploaded - SUCCESS!')

        # close connection to server
        sftp.close()
        ssh.close()
        print('The connection to server got closed.')

    # except:
    # return "Not working."

    return render_template('review.html', comfort_rating=comfort_rating, distance_rating=distance_rating,
                           centrality_rating=centrality_rating, supply_rating=supply_rating,
                           rebooking_rating=rebooking_rating, error=error)


@app.route('/reset/')
def initReset():
    # TODO: RESTART THE APP
    # cache = Cache(config={'CACHE_TYPE': 'simple'})
    # cache.init_app(app, config={'CACHE_TYPE': 'simple'})

    # with app.app_context():
    # cache.clear()

    return render_template('reset.html')


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
