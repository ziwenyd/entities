import en_core_web_sm
from spacy import displacy
from flask import Flask, jsonify, request
import uuid

app = Flask(__name__)

# every time you use this, you assign it before, so you don't really need it as
# a global variable
reference_number = 0  # two different variables (int and dict) with really similar names
references = {}  # you want to avoid that


# Find_entity breaks several conventions of naming classes.
# First: the case. In python, classes are named in UpperCaseCamelCase
# Second: It's a class, give it a more descriptive name, it shouldn't look like
# a function
class EntityFinder(object):  # usually you want to inherit from object (convention)
    def __init__(self, article):  # try to use type hints (kind of like in java)
                                  # for clarity
        self.nlp = en_core_web_sm.load()
        self.doc = self.nlp(article)

    # Try to have your comments (and line of codes) wrap to 80 chars long
    # that's easy to configure inside your Pycharm

    # Also, you're describing what your method does. This should go inside a
    # docstring: triple quote string below the method (or function)
    # For this particular line, it looks like you're trying to do a getter.
    # Getter are more of a java thing. In python, we either don't use them, or
    # use @property (tiny complicated, you don't need to know that now)

    # It's not really a problem though so I let it for now
    def get_doc(self):
        """ returns a document """  # not specific. Which document ?
        return self.doc


    # We use google style docstrings
    # https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html
    # To integrate that in Pycharm:
    # https://www.jetbrains.com/help/pycharm/settings-tools-python-integrated-tools.html
    def map_position_startIndex(self):
        """
        map the position of the token to the index of the start character of the
        token in the document(text)

        @param doc the document
        @return a dictionary mapping the position of the token in the document
                to the index of the start char of this token in the document
        """
        mapping = {}
        i = 1  # the first element's position is 1 when we print it out
        for token in self.doc:

            # not necessarily a problem, but 'i = i' does nothing, which means
            # that you can just avoid it. You could reverse your condition :
            if not(token.is_punct or token.is_space):
                startIndex = token.idx
                mapping[startIndex] = i
                i += 1
        return mapping

    def get_position(self, startIndex, mapping):
        """
        find the position of the token in the original document using the
        startIndex of this token

        @param startIndex of the token in the document
        @return the position of this token in the document
        """
        # position = mapping[startIndex]
        # return position

        # Again, not necessarily better, but you can return it instantly.
        # we know by the name of the function that you return a position, so the
        # variable name does not provide additional information. Thus it's a
        # non-necessary line of code
        return mapping[startIndex]

    def get_label(self, ent):
        """
        @return the lable of the entity
        @param the entity to get lable
        """
        return ent.label_

    def get_text(self, ent):
        """
        @param the entity to get text
        @return the text of the entity
        """
        return ent.text



# generate a response to the /list POST request
# the user should post an article (raw text format) to this api
# response: list the details of the entites in the article, in the json format
@app.route('/list', methods=['POST'])
def test():
    article = request.data.decode()
    my_doc = EntityFinder(article)
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


# If you can, avoid globals !!!
# Actually, both of those vars are defined on file level, so they are 'global'
# anyway
@app.route('/post', methods=['POST'])
def visualization():
    """
    Post request
    response: return a URL containing the reference number of this POST
    user can use the URL in the browser to see the visualized entity extract result
    """
    article = request.data.decode()
    my_doc = EntityFinder(article)

    reference_number = str(uuid.uuid4())

    html = displacy.render(my_doc.get_doc(), style="ent")
    references[reference_number] = html

    return jsonify({
        # use the python 3.6+ hendy way of formatting, more readable
        'your reference':
            f"http://{request.host}/get?reference={reference_number}"
    })


# GET request
# before using this, the user must have used a POST request
# the user using the reference he got from the POST reqeust response to get the GET response
@app.route('/get', methods=['GET'])
def get():
    if 'reference' in request.args:
        reference_number = request.args['reference']
        if reference_number in references:
            # here the extra line to assign to html does give valuable
            # information avout what your code does
            html = references[reference_number]
            return html
        # you are certain to quit from the above condition, so you can remove the
        # else
        return "Please enter valid reference."
    # same here
    return "Please enter your reference."


if __name__ == '__main__':
    app.run(debug=True)
