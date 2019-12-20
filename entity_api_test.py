
import en_core_web_sm
from spacy import displacy
from flask import Flask, jsonify, request
import uuid


app = Flask(__name__)
reference = 0

references = {}


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


def get_lable(ent):
    return ent.lable_


# print the entities an its position in the document
# @param the document
def entities(doc):
    mapping = map_position_start(doc)
    dic = []

    for ent in doc.ents:  # type of ent is span, extract entities from this document
        ent_dic = {}
        startIndex = ent.start_char
        position = findPosition(startIndex, mapping)
        lable = ent.label_

        ent_dic["entity"] = ent.text
        ent_dic["position"] = position
        ent_dic["label"] = lable

        dic.append(ent_dic)

    return dic


@app.route('/list', methods=['POST'])
def test():
    nlp = en_core_web_sm.load()
    article = request.data.decode()  # return a string
    doc = nlp(article)
    entities_dic = entities(doc)

    return jsonify(entities_dic)


@app.route('/post', methods=['POST'])
def visualization():

    global reference
    global references

    reference = str(uuid.uuid4())
    nlp = en_core_web_sm.load()
    article = request.data.decode()
    doc = nlp(article)
    html = displacy.render(doc, style="ent")
    references[reference] = html
    return jsonify({
        'your reference':
        "http://{}/get?reference={}".format(request.host, reference)
    })


@app.route('/get', methods=['GET'])
def get():
    global references
    if 'reference' in request.args:
        reference = request.args['reference']
        if reference in references:
            html = references[reference]
            return html
        else:
            return "Please enter valid reference."
    else:
        return "Please enter your reference."


if __name__ == '__main__':
    app.run(debug=True)
