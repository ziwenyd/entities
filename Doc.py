from typing import Dict

import en_core_web_sm
from spacy.lang.en import English
from spacy.tokens.doc import Doc
from spacy.tokens.token import Token


class Doc(object):
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
