from owlready2 import *


def getInformationPOIs(ontoCPS):
    POIs = {}

    if (ontoCPS == "http://wwwlab.cs.univie.ac.at/~lukasl93/CPS1init.owl"):
        onto = get_ontology(ontoCPS).load()
        graph = default_world.as_rdflib_graph()
        ratings = list(graph.query(
            '''
            PREFIX uni: <http://wwwlab.cs.univie.ac.at/~lukasl93/CPS1init.owl#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            SELECT ?inst (str(?hasComfortRating) AS ?comfort) (str(?hasName) AS ?name) (str(?hasCentralityRating) AS ?centrality) 
                         (str(?hasDistanceRating) AS ?distance) (str(?hasRebookingRating) AS ?rebooking)
                         (str(?hasSupplyRating) AS ?supply) (str(?Xcoordinate) AS ?xcoordinate) (str(?Ycoordinate) AS ?ycoordinate)
                 WHERE {{
                 ?inst rdf:type owl:NamedIndividual;
                 uni:hasComfortRating ?hasComfortRating;
                 uni:hasCentralityRating ?hasCentralityRating;
                 uni:hasDistanceRating ?hasDistanceRating;
                 uni:hasRebookingRating ?hasRebookingRating;
                 uni:hasSupplyRating ?hasSupplyRating;
                 uni:Xcoordinate ?Xcoordinate;
                 uni:Ycoordinate ?Ycoordinate;
                 uni:hasName ?hasName.

          }} '''))

        for row in ratings:
            name = str(row.asdict()['name'].toPython())
            xcoordinate = int(row.asdict()['xcoordinate'].toPython())
            ycoordinate = int(row.asdict()['ycoordinate'].toPython())
            coordinate = (xcoordinate, ycoordinate)
            comfort = int(row.asdict()['comfort'].toPython())
            centrality = int(row.asdict()['centrality'].toPython())
            distance = int(row.asdict()['distance'].toPython())
            rebooking = int(row.asdict()['rebooking'].toPython())
            supply = int(row.asdict()['supply'].toPython())

            POIs[name] = {"coordinates": coordinate, "comfort": comfort, "centrality": centrality,
                          "distance": distance, "rebooking": rebooking, "supply": supply}

    elif (ontoCPS == "http://wwwlab.cs.univie.ac.at/~lukasl93/CPS2init.owl"):
        onto = get_ontology(ontoCPS).load()
        graph = default_world.as_rdflib_graph()
        ratings = list(graph.query(
            '''
            PREFIX uni: <http://wwwlab.cs.univie.ac.at/~lukasl93/CPS2init.owl#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            SELECT ?inst (str(?hasComfortRating) AS ?comfort) (str(?hasName) AS ?name) (str(?hasCentralityRating) AS ?centrality) 
                         (str(?hasDistanceRating) AS ?distance) (str(?hasRebookingRating) AS ?rebooking)
                         (str(?hasSupplyRating) AS ?supply) (str(?Xcoordinate) AS ?xcoordinate) (str(?Ycoordinate) AS ?ycoordinate)
                 WHERE {{
                 ?inst rdf:type owl:NamedIndividual;
                 uni:hasComfortRating ?hasComfortRating;
                 uni:hasCentralityRating ?hasCentralityRating;
                 uni:hasDistanceRating ?hasDistanceRating;
                 uni:hasRebookingRating ?hasRebookingRating;
                 uni:hasSupplyRating ?hasSupplyRating;
                 uni:Xcoordinate ?Xcoordinate;
                 uni:Ycoordinate ?Ycoordinate;
                 uni:hasName ?hasName.

          }} '''))

        for row in ratings:
            name = str(row.asdict()['name'].toPython())
            xcoordinate = int(row.asdict()['xcoordinate'].toPython())
            ycoordinate = int(row.asdict()['ycoordinate'].toPython())
            coordinate = (xcoordinate, ycoordinate)
            comfort = int(row.asdict()['comfort'].toPython())
            centrality = int(row.asdict()['centrality'].toPython())
            distance = int(row.asdict()['distance'].toPython())
            rebooking = int(row.asdict()['rebooking'].toPython())
            supply = int(row.asdict()['supply'].toPython())

            POIs[name] = {"coordinates": coordinate, "comfort": comfort, "centrality": centrality,
                          "distance": distance, "rebooking": rebooking, "supply": supply}

    return POIs
