characterFrequency = {
    'a' : 8.12,
    'b' : 1.49,
    'c' : 2.71,
    'd' : 4.32,
    'e' : 12.02,
    'f' : 2.30,
    'g' : 2.03,
    'h' : 5.92,
    'i' : 7.31,
    'j' : 0.10,
    'k' : 0.69,
    'l' : 3.98,
    'm' : 2.61,
    'n' : 6.95,
    'o' : 7.68,
    'p' : 1.82,
    'q' : 0.11,
    'r' : 6.02,
    's' : 6.28,
    't' : 9.10,
    'u' : 2.88,
    'v' : 1.11,
    'w' : 2.09,
    'x' : 0.17,
    'y' : 2.11,
    'z' : 0.07,
}


def readLines(filename):
	f = open(filename)
	lines = f.read()
	lines = lines.split()
	return lines

def parseSwearWords():
	return readLines('data/swearWords.txt')

def parseTriggeredResponses():
	return readLines('data/triggeredResponses.txt')

def parseUrduResponses():
	return readLines('data/urduResponses.txt')

def characterFrequencyCalculator(string):
    freq = {}
    nonAlphaCharacters = 0;
    for i in characterFrequency.keys():
        freq[i] = 0;
    for i in string:
        if i in freq:
            freq[i] = freq[i] + 1;
        else:
            nonAlphaCharacters += 1;

    allOnes = True
    for i in freq.keys():
        if freq[i] != 0:
            allOnes = False;
        freq[i] = freq[i] * 100.0 / len(string)
    if allOnes:
        return nonAlphaCharacters, {}
    return nonAlphaCharacters, freq

def stringScoring(string):
    nonAlphaCharacters, freq = characterFrequencyCalculator(string)
    score = 0;
    if nonAlphaCharacters == len(string):
        return float('+inf');
    else:
        score += 100.0 * nonAlphaCharacters / len(string)
        for i in freq.keys():
            score += abs(freq[i] - characterFrequency[i])
    return score;
