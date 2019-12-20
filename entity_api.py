import spacy
from flask import Flask,jsonify,request


app = Flask(__name__)


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
    dic = []

    for ent in doc.ents:  # type of ent is span, extract entities from this document
        ent_dic = {}
        startIndex = ent.start_char
        position = findPosition(startIndex, mapping)
        ent_dic["entity"] = ent.text
        ent_dic["position"] = position
        dic.append(ent_dic)


    return dic


#def main(article):
 #   nlp = spacy.load('en')
  #  doc = nlp(article)
   # returning = entities(doc)
    #return returning

@app.route('/test', methods = ['POST'])
def test():
    nlp = spacy.load('en')
    article = request.data.decode()  #return a string
    doc = nlp(article)
    entities_dic = entities(doc)
    return jsonify(entities_dic)




if __name__ == '__main__':
    app.run(debug=True)
