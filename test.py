article = '''Asian shares skidded on Tuesday after a rout in tech stocks put Wall Street to the sword, 
while a sharp drop in oil prices and political risks in Europe pushed the dollar to 16-month highs as investors dumped 
riskier assets. MSCI’s broadest index of Asia-Pacific shares outside Japan dropped 1.7 percent to a 1-1/2 
week trough, with Australian shares sinking 1.6 percent. Japan’s Nikkei dived 3.1 percent led by losses in 
electric machinery makers and suppliers of Apple’s iphone parts. Sterling fell to $1.286 after three straight 
sessions of losses took it to the lowest since Nov.1 as there were still considerable unresolved issues with the
European Union over Brexit, British Prime Minister Theresa May said on Monday.'''

import en_core_web_sm

# map the position of the token to the index of the start character of the token in the document(text)
# @param doc the document
# @return a dictionary mapping the position of the token in the document to the index of the start char of this token in the document
def map_position_start(doc):
    mapping = {}
    i = 1  # the first element's position is 1 when we print it out
    for token in doc:

        if token.is_punct or token.is_space:
            i = i  # doing nothing here
        else:
            startIndex = token.idx
            mapping[startIndex] = i
            i += 1
    return mapping


# find the position of the token in the original document using the startIndex of this token
# @param startIndex of the token in the document
# @return the position of this token in the document
def findPosition(startIndex, mapping):
    position = mapping[startIndex]
    return position


# print the entities an its position in the document
# @param the document
def entities(doc):
    mapping = map_position_start(doc)
    for ent in doc.ents:  # type of ent is span
        startIndex = ent.start_char
        position = findPosition(startIndex, mapping)
        print("entity: " + str(ent.text) + ", " + "position in the document: " + str(position))


def main():
    nlp = en_core_web_sm.load()
    doc = nlp(article)
    print('hi')
    entities(doc)
main()