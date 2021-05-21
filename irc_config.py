def loadconfig(path):
    dictionary = {}
    with open(path) as f:
        for line in f:
            line = line.strip()
            (key, val) = line.split("=", 1)
            dictionary[key] = val

    return dictionary

