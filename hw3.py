import os
import urllib2
import collections
import random


def IsAllowedSymbol(symbol):
    symbols = list(".,?! ")
    return symbol.isalpha() or symbol.isdigit() or (symbol in symbols)


def DistinguishEndings(text):
    symbols = list(".?!,")
    for symbol in symbols:
        text = text.replace(symbol, " " + symbol + " ")
    return text


def CleanLine(text):
    text = text.lower()
    text = DistinguishEndings(text)
    new_text = ""
    for index, symbol in enumerate(text):
        if not (IsAllowedSymbol(symbol)):
            new_text += " "
        else:
            new_text += symbol
    return new_text


def AddSpaces(words):
    for index, word in enumerate(words):
        words[index] = word + " "
    return words


def GetData(folder):
    text = ""
    for author in os.listdir("./" + folder):
        if author[0] != ".":
            for book in os.listdir("./{}/{}".format(folder, author)):
                with open("./{}/{}/{}".format(folder, author, book), "r") as f:
                    line = f.read()
                    text += CleanLine(line)
    return AddSpaces(text.split())


def FindPairs(words):
    indexes = {}
    for index in xrange(len(words) - 2):
        pair = words[index] + words[index + 1]
        indexes.setdefault(pair, [])
        indexes[pair].append(index + 1)
    return indexes


def FindDotsPositions(words):
    ending_symbols = list("?!.")
    for index, symbol in enumerate(ending_symbols):
        ending_symbols[index] = ending_symbols[index] + " "
    indexes = []
    for index, word in enumerate(words):
        if index == len(words) - 1:
            return indexes
        if (word in ending_symbols) and (words[index + 1] not in
                                         ending_symbols):
            indexes.append(index)


def GenerateSentence(pairs, words, first_word, words_count):
    ending_symbols = list("?!.")
    too_short_words = "t ve re m ll s d".split()
    for index, symbol in enumerate(ending_symbols):
        ending_symbols[index] = symbol + " "
    for index, symbol in enumerate(too_short_words):
        too_short_words[index] = symbol + " "
    text = first_word.title()
    previous_word = first_word
    pair = ". " + first_word
    for i in range(30):
        new_word = ". "
        if pair in pairs:
            max_index = len(pairs[pair]) - 1
            new_word = words[1 + pairs[pair][random.randint(0, max_index)]]
        words_count += 1
        if new_word in too_short_words:
            text = text[:-1] + "'" + new_word
            pair = previous_word + new_word
            previous_word = new_word
            continue
        if new_word == ", ":
            text = text[:-1] + new_word
            pair = previous_word + new_word
            previous_word = new_word
            continue
        if new_word in ending_symbols:
            text = text[:-1] + new_word
            return text, words_count
        if new_word == "i ":
            new_word = "I "
        pair = previous_word + new_word
        previous_word = new_word
        text += new_word
    text = text[:-1] + ". "
    return text, words_count


def GenerateText(pairs, words, dots_positions):
    words_count = 0
    max_index = len(dots_positions) - 1
    text = "\t"
    while words_count < 10000:
        first_word = words[1 + dots_positions[random.randint(0, max_index)]]
        new_sentence, words_count = GenerateSentence(pairs, words, first_word,
                                                     words_count)
        text += new_sentence
        if random.randint(0, 5) == 5:
            text += "\n\t"
    return text

if __name__ == "__main__":
    words = GetData("folder")
    pairs = FindPairs(words)
    dots_positions = FindDotsPositions(words)
    text = GenerateText(pairs, words, dots_positions)
    with open("generated_text.txt", "w") as f:
        f.write(text)
