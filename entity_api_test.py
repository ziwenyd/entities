from typing import Dict

import en_core_web_sm
from spacy import displacy
from spacy.lang.en import English
from spacy.tokens.doc import Doc
from flask import Flask, jsonify, request
import uuid

from spacy.tokens.span import Span
from spacy.tokens.token import Token

app = Flask(__name__)


class References(object):
    def __init__(self):
        self.references = {}

    def add_reference(self, key, value):
        self.references[key] = value

    def get_value(self, key):
        return self.references[key]


class EntityFinder(object):
    """Extract entities from a given text(via argument). Useful
    information of the entities can be get via functions.

    Arg:
        article(String): the text sent from the POST request

    Attribute:
        nlp(:obj:'nlp'): using the English model from spacy library.
        doc(:obh:'DOC'): construct the DOC object via the nlp object
    """

    def __init__(self, article: str):
        self.nlp: English = en_core_web_sm.load()
        self.doc: Doc = self.nlp(article)

    def get_doc(self) -> Doc:
        """
        Returns:
            obj:'DOC' : a DOC object of the article
        """
        return self.doc

    def map_position_start_index(self) -> Dict[int, int]:
        """ Generate a Dictionary to hold the references of the position of the token,
        and the index of the start character of the token in the text.

          Note:
              The position of the token in the text only counts the word, ignore
              punctuation and white spaces.
              The position starts from 1.

          Returns:
              Dictionary: a dictionary mapping the position of the token in the
              document, to the index of the start char of this token in the document.
          """
        mapping = {}
        i = 1
        for token in self.doc:
            if not (token.is_punct or token.is_space):
                start_index = token.idx
                mapping[start_index] = i
                i += 1
        return mapping

    @staticmethod
    def get_position(start_index: int, mapping: Dict[int, int]):
        """ Find the position of the token in the original document using the
        startIndex of this token.

        Args:
            start_index(int): the index of the start character of the token in the text.

        Returns:
            Int: the position of this token in the text.
        """
        return mapping[start_index]

    @staticmethod
    def get_label(ent: Token):
        """Classify the entity passed by argument.

        Args:
            ent (Token):the entity to get its label

        Returns:
            ent.label_ (String)
        """
        return ent.label_

    @staticmethod
    def get_text(ent: Token):
        """
        Args:
            ent (Token): the entity to get its text(content).
        Returns:
            ent.text (String): the content of this entity.

        """
        print(type(ent.text))
        return ent.text


references = References()


@app.route('/list', methods=['POST'])
def list_all_entities():
    """POST request, generate a response listing the details of all the entities.

    Args:
        raw text: the user should post an article (raw text format) to this api.

    Returns:
        json: list the details of the entities in the article, in the json format
    """

    article = request.data.decode()
    my_doc = EntityFinder(article)
    dic = []
    mapping = my_doc.map_position_start_index()

    for ent in my_doc.get_doc().ents:
        ent_dic = {}
        start_index = ent.start_char
        position = my_doc.get_position(start_index, mapping)
        label = my_doc.get_label(ent)

        ent_dic["entity"] = ent.text
        ent_dic["position"] = position
        ent_dic["label"] = label

        dic.append(ent_dic)
    return jsonify(dic)


@app.route('/post', methods=['POST'])
def visualization():
    """ Post request.

    Args:
        raw text: the body of the POST request should be raw text.
    Returns:
        String: Return a URL containing the reference number of this POST, the user
        can use the URL in the browser to see the visualized entity extract result
    """
    article = request.data.decode()  # String

    my_doc = EntityFinder(article)
    reference_number = str(uuid.uuid4())

    html = displacy.render(my_doc.get_doc(), style="ent")
    references.add_reference(reference_number, html)

    return jsonify({
        'your reference':
            f"http://{request.host}/get?reference={reference_number}"
    })


@app.route('/get', methods=['GET'])
def get():
    """ GET request, before using this, the user must have used a POST request to
    get the URL in order to create a valid GET request.

    Args:
        String: the special ID created by the corresponding POST request.

    Returns:
        "Please enter valid reference."(String): if the reference number does not exist.
        "Please enter your reference."(String): if the user didn't pass a reference number.
        html(HTML): if the user passes a valid reference number.
    """
    if 'reference' in request.args:
        reference_number = request.args['reference']
        if reference_number in references.references:
            html = references.get_value(reference_number)
            return html
        return "Please enter valid reference."
    return "Please enter your reference."


if __name__ == '__main__':
    app.run(debug=True)
