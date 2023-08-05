def POIRankings(informationCPS):

    averageRanking = {}
    ### add every ranking average of every POI into the list averageRanking!
    for POIs in informationCPS:
        averageRanking[POIs] = ((informationCPS[POIs]["comfort"] + \
                                informationCPS[POIs]["centrality"] + \
                                informationCPS[POIs]["distance"] + \
                                informationCPS[POIs]["rebooking"] + \
                                informationCPS[POIs]["supply"]) / 5)
    return averageRanking

