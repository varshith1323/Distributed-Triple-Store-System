import json

def load_data(filename):
    with open(filename, 'r') as file:
        return json.load(file)

def merge_data(postgres_data, mongo_data):
    # Create a dictionary with a unique key from subject and predicate with PostgreSQL data as baseline
    merged_data = {f"{item['subject']}_{item['predicate']}": item for item in postgres_data}
    
    # Loop through MongoDB data to either update or add new entries
    for item in mongo_data:
        key = f"{item['subject']}_{item['predicate']}"
        if key in merged_data:
            # Check if MongoDB's object is non-null and different, then overwrite
            if item['object'] and merged_data[key]['object'] != item['object']:
                merged_data[key]['object'] = item['object']
        else:
            # If no entry exists in merged_data, add MongoDB's item
            merged_data[key] = item

    return list(merged_data.values())

if __name__ == "__main__":
    postgres_data = load_data('/Users/varshithvattikuti/Desktop/NoSQL_Postgres/postgres_data.json')
    mongo_data = load_data('/Users/varshithvattikuti/Desktop/NoSQL_MongoDB/mongo_data.json')
    merged_data = merge_data(postgres_data, mongo_data)
    with open('/Users/varshithvattikuti/Desktop/NoSQL_MongoDB/merged_data.json', 'w') as f:
        json.dump(merged_data, f)
