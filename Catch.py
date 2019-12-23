
class Catch(object):
    """
    A dictionary stores references.

    In the "api_extracted_entities.py", this class is used to store the references
    of the UUID (the user gets UUID via each POST request) and
    the associated response(in this case, an html).
    """
    def __init__(self):
        self.references = {}

    def add_reference(self, key, value):
        """
        Add a key and the associated value to the dictionary.
        """
        self.references[key] = value

    def get_value(self, key):
        """
        Get the value of the associated key.
        """
        return self.references[key]

