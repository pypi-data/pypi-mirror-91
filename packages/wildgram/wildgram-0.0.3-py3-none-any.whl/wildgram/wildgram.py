import regex as re
import string
import os


TOPICWORDS = [
"no",
"due to",
"secondary to",
"s/p",
"ruled out",
"w/o",
"c/b",
"complicated by",
"experience",
"become",
"becomes",
"if",
"denies",
"denied",
"suggests",
"suggest",
"suggested"
]

STOPWORDS = [
"with",
"and",
"or",
"on",
"as well as",
"was",
"from",
"when",
"for",
"vs",
"without",
"in",
"came back",
"who",
"had",
"at",
"but",
"though",
"verses",
"to",
"the",
"could",
"including",
"indicate",
"since",
"towards",
"toward",
"out",
"you",
"your",
"by",
"developed",
"develop",
"described",
"describe",
"is",
"status",
"are",
"represented",
"represent",
"that",
"in the",
"been",
"be",
"a"
]

def wildgram(text):
    # corner case for inappropriate input
    if not isinstance(text, str):
        raise Exception("What you just gave wildgram isn't a string, mate.")
    # if its just whitespace
    if text.isspace():
        return [], []

    punc = [x for x in string.punctuation]
    topics = "|".join(["(\s|^)"+stop+"(\s|$)" for stop in TOPICWORDS])
    regex = '('+"|".join(["(\s|^)"+stop+"(\s|$)" for stop in STOPWORDS])+"|"+topics+'|\n|[\s' + "|\\".join(punc)+ ']{'+ str(2)+',})'
    prog = re.compile(regex)

    prev = 0
    count = 0
    ranges = []
    for match in prog.finditer(text.lower(),overlapped=True):
        if match.start() > prev:
            ranges.append((prev, match.start()))
        prev = match.end()

        # all of this nonsense deals with topic changing words
        if re.match("("+topics+")", match.group(0)):
            start = match.start()
            end = match.end()
            if text[match.start()].isspace():
                start = start + 1
            if text[match.end()-1].isspace():
                end = end -1
            ranges.append((start, end))

    if len(text) > prev:
        ranges.append((prev, len(text)))

    tokens = []
    for snippet in ranges:
        tokens.append(text[snippet[0]:snippet[1]])

    return tokens, ranges
