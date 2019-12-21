import en_core_web_sm
from spacy import displacy
from flask import Flask, jsonify, request
import uuid

app = Flask(__name__)
reference = 0  # 2 different variables with similar name

references = {}


class Find_entity(object):
    def __init__(self, article):
        self.nlp = en_core_web_sm.load()
        self.doc = self.nlp(article)

    # @return a document
    def get_doc(self):
        return self.doc

    # map the position of the token to the index of the start character of the token in the document(text)
    # @param doc the document
    # @return a dictionary mapping the position of the token in the document to the index of the start char of this token in the document
    def map_position_startIndex(self):
        mapping = {}
        i = 1  # the first element's position is 1 when we print it out
        for token in self.doc:

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
    def get_position(self, startIndex, mapping):
        position = mapping[startIndex]
        return position

    # @return the lable of the entity
    # @param the entity to get lable
    def get_label(self, ent):
        return ent.label_

    # @param the entity to get text
    # @return the text of the entity
    def get_text(self, ent):
        return ent.text



# generate a response to the /list POST request
# the user should post an article (raw text format) to this api
# response: list the details of the entites in the article, in the json format
@app.route('/list', methods=['POST'])
def test():
    article = request.data.decode()
    my_doc = Find_entity(article)
    dic = []
    mapping = my_doc.map_position_startIndex()

    for ent in my_doc.get_doc().ents:
        ent_dic = {}
        startIndex = ent.start_char
        position = my_doc.get_position(startIndex, mapping)
        label = my_doc.get_label(ent)

        ent_dic["entity"] = ent.text
        ent_dic["position"] = position
        ent_dic["label"] = label

        dic.append(ent_dic)
    return jsonify(dic)


# Post request
# response: return a URL containing the reference number of this POST
# user can use the URL in the browser to see the visualized entity extract result
@app.route('/post', methods=['POST'])
def visualization():
    global reference
    global references

    article = request.data.decode()
    my_doc = Find_entity(article)

    reference = str(uuid.uuid4())

    html = displacy.render(my_doc.get_doc(), style="ent")
    references[reference] = html

    return jsonify({
        'your reference':
            "http://{}/get?reference={}".format(request.host, reference)
    })


# GET request
# before using this, the user must have used a POST request
# the user using the reference he got from the POST reqeust response to get the GET response
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
