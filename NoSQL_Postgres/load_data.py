import psycopg2
import csv

def load_data(file_path):

    conn = psycopg2.connect(dbname="triple_store", user="postgres", password="your_password", host="localhost", port="5432")
    cur = conn.cursor()

    #opening file for reading data
    with open(file_path, 'r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)

        #iterating over each row in the dataset fil
        for subject, predicate, object in reader:

            # SQL command to insert data into the triples table
            cur.execute("""
                INSERT INTO triples (subject, predicate, object)
                VALUES (%s, %s, %s)
                ON CONFLICT (subject, predicate) DO UPDATE
                SET object = EXCLUDED.object;
            """, (subject.strip(), predicate.strip(), object.strip()))
             # Strip whitespace from the beginning and end of each field
        conn.commit()
    cur.close()
    conn.close()

# This condition checks if the script is running as the main program and not being imported as a module
if __name__ == "__main__":
    # Call the load_data function with the path to the data file
    load_data('/Users/varshithvattikuti/Desktop/NoSQL_Postgres/triples.txt')
