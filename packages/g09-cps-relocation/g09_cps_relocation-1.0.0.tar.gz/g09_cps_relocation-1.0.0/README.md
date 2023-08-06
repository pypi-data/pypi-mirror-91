# CPS relocation

We are Group9 and in the following we'll give you an instruction of how to use our CPS relocation implementation. 

## Setup
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the necessary modules.

First, clone the repository to your local system. On [PyPi](https://pypi.org/project/g09-cps-relocation/) you can find the pip statement to install all necessary modules within your project automatically.

```bash
pip install g09-cps-relocation==1.0.0
```

Alternatively, you can install the modules one by one.

```bash
pip install paramiko
```

```bash
pip install Owlready2
```
```bash
pip install Flask
```
```bash
pip install flaskwebgui
```
```bash
pip install Werkzeug
```
```bash
pip install rdflib
```
For some cases we figured out that a html-library is necessary for running the code. However, this might be optional for you:
```bash
pip install requests
```

## Relocation

In general, you have to think yourself into two views:
1. CPS point of view
2. Passenger point of view (the guy who enters the CPS on a certain location)

By running the "main.py" in the folder "Implementation" you'll get an overview of the available points of interest. It is now up to you to give the CPS1 and CPS2 a starting position (= input in terminal). This human input is necessary to 
a.) get the relocation process running and b.) continue the process when a CPS has dropped of a passenger. Afterwards, each CPS decides individually based on its character where the relocation should be.

### Ontology
Every decision of the CPS is based on their individual ontology.
You can find the written .owl files in the folder "Ontologies". For just in time access, the ontologies are positioned on the Apache2 server under following links:

- [CPS1-Ontology](http://wwwlab.cs.univie.ac.at/~lukasl93/CPS1init.owl)
- [CPS2-Ontology](http://wwwlab.cs.univie.ac.at/~lukasl93/CPS2init.owl)

### Using Flask
By running the the "app.py" a link in output console will appear. The URL will probably look like the following: "http://127.0.0.1:1337/". When you open this link your web browser will open and you are confronted with our GUI. From here on you act as from the passengers point of view. Just imagine to order a CPS, go to the CPS and let the CPS drive you to your destination. While you are driving to your destination you have enough time to fill out the survey about rating the pickup location which you started previously by running "app.py". Depending on how good or bad your ranking will be, the CPS will choose your pickup location next time again for his relocation. 

TechTalk: by entering the survey data about a pickup location, the ontologies that form the CPS characters will update. This enables us to give the CPS an intelligent character trait.