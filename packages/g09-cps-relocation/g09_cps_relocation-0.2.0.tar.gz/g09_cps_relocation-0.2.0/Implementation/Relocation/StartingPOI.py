def startingLocation(information):
    numberOfPOIs = len(information)
    namesOfPOIs = []
    for entries in information:
        namesOfPOIs.append(entries)

    print("You are located in the city of Vienna and", numberOfPOIs,
          "POIs are available.\nPlease define the starting location of CPS1 & CPS2! You have following POIs available for selection: ",
          namesOfPOIs)

    ##Exception handling if POI does not exist.
    while True:
        initial_locationCPS1 = input("Please enter CPS1 starting location here: ")
        if initial_locationCPS1 not in namesOfPOIs:
            print("Sorry, this POI does not exist. Try it again: ")
            continue
        else:
            break
    while True:
        initial_locationCPS2 = input("Please enter CPS2 starting location here: ")
        if initial_locationCPS2 not in namesOfPOIs:
            print("Sorry, this POI does not exist. Try it again: ")
            continue
        else:
            break

    print("Starting location of CPS1 --> ", initial_locationCPS1, " @coordinates ", information[initial_locationCPS1]['coordinates'])
    print("Starting location of CPS2 --> ", initial_locationCPS2, " @coordinates ", information[initial_locationCPS2]['coordinates'])

    return initial_locationCPS1, initial_locationCPS2


