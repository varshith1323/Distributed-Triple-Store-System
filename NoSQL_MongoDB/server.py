from pymongo import MongoClient
import json

class TripleStore:
    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client['triple_store']
        self.collection = self.db['triples']

    def load_dataset_from_txt(self, file_path):
        with open(file_path, 'r') as file:
            for line in file:
                subject, predicate, obj = line.strip().split(',')
                triple = {'subject': subject, 'predicate': predicate, 'object': obj}
                self.collection.insert_one(triple)

    def query(self, subject):
        triples = self.collection.find({'subject': subject})
        return list(triples)

    def update(self, subject, predicate, obj):
        self.collection.update_one(
            {'subject': subject, 'predicate': predicate},
            {'$set': {'object': obj}},
            upsert=True
        )

    def load_merged_data_to_mongo(self):
        with open('/Users/varshithvattikuti/Desktop/NoSQL_MongoDB/merged_data.json', 'r') as f:
            data = json.load(f)
        for item in data:
            self.collection.update_one(
                {'subject': item['subject'], 'predicate': item['predicate']},
                {'$set': {'object': item['object']}},
                upsert=True
            )

    def export_data_to_json(self, file_path):
        data = list(self.collection.find({}, {'_id': 0}))  # Exclude MongoDB's _id from export
        with open(file_path, 'w') as file:
            json.dump(data, file)


# Create an instance of TripleStore
triple_store = TripleStore()

# Load dataset from .txt file
triple_store.load_dataset_from_txt('/Users/varshithvattikuti/Desktop/NoSQL_MongoDB/triples_mongo.txt')

# Prompt user to select action
action = input("Enter 'query' to perform a query or 'update' to perform an update: ")

if action == 'query':
    # Perform query
    subject = input("Enter the subject for the query: ")
    result = triple_store.query(subject)
    print("Query result:")
    for triple in result:
        print(triple)
elif action == 'update':
    # Perform update
    subject = input("Enter the subject to update: ")
    predicate = input("Enter the predicate to update: ")
    new_object = input("Enter the new object value: ")
    triple_store.update(subject, predicate, new_object)
    print("Update successful!")
else:
    print("Invalid action. Please enter either 'query' or 'update'.")

if __name__ == "__main__":
    # Create an instance of TripleStore
    triple_store = TripleStore()

    # Load dataset from the text file into MongoDB
    triple_store.load_dataset_from_txt('/Users/varshithvattikuti/Desktop/NoSQL_MongoDB/triples_mongo.txt')
    print("Data loaded from text file into MongoDB.")

    # Load merged data into MongoDB from the merged JSON file
    triple_store.load_merged_data_to_mongo()
    print("Merged data has been loaded into MongoDB.")

    # Continue with interactive commands
    action = input("Enter 'query' to perform a query, 'update' to perform an update, or 'exit' to finish: ")
    while action != 'exit':
        if action == 'query':
            # Perform query
            subject = input("Enter the subject for the query: ")
            result = triple_store.query(subject)
            print("Query result:")
            for triple in result:
                print(triple)
        elif action == 'update':
            # Perform update
            subject = input("Enter the subject to update: ")
            predicate = input("Enter the predicate to update: ")
            new_object = input("Enter the new object value: ")
            triple_store.update(subject, predicate, new_object)
            print("Update successful!")
        
        action = input("Enter 'query' to perform a query, 'update' to perform an update, or 'exit' to finish: ")

    # Optionally, export the current MongoDB data to a JSON file
    triple_store.export_data_to_json('/Users/varshithvattikuti/Desktop/NoSQL_MongoDB/mongo_data.json')
    print("Current MongoDB data exported to JSON.")





