from ex48 import ex48_convert

directions = ['north', 'south', 'east', 'west']
verbs = ["go", "stop", "kill", "eat"]
stops = ["the", "in", "of", "from", "at", "it"]
nouns = ["door", "bear", "princess", "cabinet"]

def scan(sentence):
    result = []
    words = sentence.split()
    
    for word in words:
        word_lower = word.lower()
        number = ex48_convert.convert_number(word)
        
        if word_lower in directions:
            result.append(tuple(['direction', word]))
        elif word_lower in verbs:
            result.append(tuple(['verb', word]))
        elif word_lower in stops:
            result.append(tuple(['stop', word]))
        elif word_lower in nouns:
            result.append(tuple(['noun', word]))
        elif number != None:
            result.append(tuple(['number', number]))
        else:
            result.append(tuple(['error', word]))
            
    return result