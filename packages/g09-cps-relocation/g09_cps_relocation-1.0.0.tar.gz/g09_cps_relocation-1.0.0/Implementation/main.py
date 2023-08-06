from Implementation.Relocation.InformationPOIs import *
from Implementation.Relocation.StartingPOI import *
from Implementation.Relocation.POIRankings import *

### define CPS-Names

CPS1 = "CPS1"
CPS2 = "CPS2"

### define CPS-Ontologies
ontoCPS1 = "http://wwwlab.cs.univie.ac.at/~lukasl93/CPS1init.owl"
ontoCPS2 = "http://wwwlab.cs.univie.ac.at/~lukasl93/CPS2init.owl"

### get city/POIs/coordinates from Ontology
informationCPS1 = getInformationPOIs(ontoCPS1)
informationCPS2 = getInformationPOIs(ontoCPS2)
initial_locationCPS1, initial_locationCPS2 = startingLocation(informationCPS1)

###Calculate average ranking:
'''
We have listed following rankings: comfort, centrality, distance, rebooking, supply. 
All of them have a range between 1-10. The CPS will choose the POI with the highest average ranking!
'''
CPS1_average = POIRankings(informationCPS1)
CPS2_average = POIRankings(informationCPS2)

print("CPS1-POIs have following average: ", CPS1_average)
print("CPS2-POIS have following average: ", CPS2_average)

### get Pre-Decision of CPS!
CPS1_relocation = max(CPS1_average, key=CPS1_average.get)
CPS2_relocation = max(CPS2_average, key=CPS2_average.get)

### if both CPS will decide on the same relocation, then the CPS with the lower ranking chooses the POI with the 2nd highest ranking.
if CPS1_relocation == CPS2_relocation:
    if CPS1_average[CPS1_relocation] >= CPS2_average[CPS2_relocation]:
        ##for getting the 2nd highest POI we need to sort the CPSAverage. The order will be descending
        CPS2_average_sorted = list(sorted(CPS2_average.items(), key=lambda item: item[1], reverse=True))
        ##The new CPS relocation will be the 2nd highest ranking.
        CPS2_relocation = CPS2_average_sorted[1][0]
    elif CPS2_average[CPS1_relocation] < CPS2_average[CPS2_relocation]:
        CPS1_average_sorted = list(sorted(CPS1_average.items(), key=lambda item: item[1], reverse=True))
        CPS1_relocation = CPS1_average_sorted[1][0]

##get coordinates of relocation from ontology
CPS1_relocation_coordinates = getInformationPOIs(ontoCPS1)[CPS1_relocation]["coordinates"]
CPS2_relocation_coordinates = getInformationPOIs(ontoCPS2)[CPS2_relocation]["coordinates"]

print("CPS1 relocation --> ", CPS1_relocation, " @coordinates ", CPS1_relocation_coordinates)
print("CPS2 relocation --> ", CPS2_relocation, " @coordinates ", CPS2_relocation_coordinates)

