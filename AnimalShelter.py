from pymongo import MongoClient
from bson.objectid import ObjectId


class AnimalShelter(object):
    """ CRUD operations for Animal collection in MongoDB """

    def __init__(self, username, password):
        # Initializing the MongoClient. This helps to
        # access the MongoDB databases and collections.
        # This is hard-wired to use the aac database, the
        # animals collection, and the aac user.
        # Definitions of the connection string variables are
        # unique to the individual Apporto environment.
        #
        # Connection Variables
        #
        USER = 'aacuser'
        PASS = 'SNHU1234'
        HOST = 'nv-desktop-services.apporto.com'
        PORT = 33384  # My port 33384? Given port: 31580
        DB = 'AAC'
        COL = 'animals'
        #
        # Initialize Connection
        #
        self.client = MongoClient('mongodb://%s:%s@%s:%d' % (USER, PASS, HOST, PORT))
        self.database = self.client['%s' % DB]
        self.collection = self.database['%s' % COL]

# Complete this create method to implement the C in CRUD.
    def create(self, data):
        if data:  # originally had...  is not None:
            try:
                #  originally had ...self.database.animals.insert_one(data)  # data should be dictionary
                self.collection.insert_one(data)
                return True
            except Exception as e:
                print(f"Insert failed: {e}")
                return False
        else:
            raise Exception("Nothing to save, because data parameter is empty")

# Create method to implement the R in CRUD.
    def read(self, query):
        """
        - This read method queries for specific document from MongoDB database and collection.
        - It uses key-value pairs into MongoDB driver insert API call.
        - Returns result in list if successful, else empty list
        - Uses find() instead of find_one()
        """
        results_list = []
        try:
            cursor = self.collection.find(query)
            for document in cursor:
                results_list.append(document)
            return results_list
        except Exception as e:
            print(f"Read failed: {e}")
            return []

# Create method to implement the U in CRUD
    def update(self, query, values, multiple=False):
        """
        - Updates queries for and changes document(s) from a specified MongoDB database and specified collection.
        - Input -> arguments to function should be the key/value lookup pair to use with the MongoDB driver Find API call.
        - The last argument to function will be a set of key/value pairs in the data type acceptable to the MongoDB driver update_one() or update_many() API call.
        - Return -> The number of objects modified in the collection.
        """
        if not query or not values:
            raise Exception("Both parameters must be provided.")

        try:
            if multiple:
                result = self.collection.update_many(query, {"$set": values})
            else:
                result = self.collection.update_one(query, {"$set": values})
            return result.modified_count
        except Exception as e:
            print(f"Update failed: {e}")
            return 0

# Create method to implement the D in CRUD
    def delete(self, query, multiple=False):
        """
        - A Delete method that queries for and removes document(s) from a specified MongoDB database and specified collection
        - Input -> arguments to function should be the key/value lookup pair to use with the MongoDB driver find API call.
        - Return -> The number of objects removed from the collection.
        """
        if not query:
            raise Exception("Parameter must be provided to run delete()")

        try:
            if multiple:
                result = self.collection.delete_many(query)
            else:
                result = self.collection.delete_one(query)
            return result.deleted_count
        except Exception as e:
            print(f"Delete failed: {e}")
            return 0


