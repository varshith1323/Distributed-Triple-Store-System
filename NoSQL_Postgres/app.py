# For managing data in a PostgreSQL database by handling basic CRUD (Create, Read, Update, Delete) operations
# Also includes functionality to export data to a JSON file and reload data from a JSON file (specifically merged data)

import psycopg2
import csv
import os

# Function to establish a connection to the PostgreSQL database
def connect_db():
    return psycopg2.connect(
        dbname="triple_store", user="varshithvattikuti", password="12345", host="localhost", port="5432"
    )

# Function to perform a query operation in the database
def query(subject):
    conn = connect_db() # Establish a connection to the database
    cur = conn.cursor() # Create a cursor object to execute SQL commands
    cur.execute("SELECT * FROM triples WHERE subject = %s;", [subject])
    results = cur.fetchall() # Fetch all rows of the query result
    cur.close()
    conn.close()
    return results

#ON CONFLICT: if there's an attempt to insert a subject and predicate combination that already exists in the table.

def update(subject, predicate, object):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO triples (subject, predicate, object)
        VALUES (%s, %s, %s)
        ON CONFLICT (subject, predicate) DO UPDATE SET object = EXCLUDED.object;
    """, (subject, predicate, object))
    conn.commit()
    cur.close()
    conn.close()

def delete(subject, predicate, object):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        DELETE FROM triples
        WHERE subject = %s AND predicate = %s AND object = %s;
        """, (subject, predicate, object))
    conn.commit()
    if cur.rowcount == 0:
        print("No matching triple found.")
    else:
        print(f"Deleted triple: {subject} {predicate} {object}")
    cur.close()
    conn.close()

def load_data(file_path):
    conn = connect_db()
    cur = conn.cursor()
    with open(file_path, 'r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            cur.execute("""
                INSERT INTO triples (subject, predicate, object)
                VALUES (%s, %s, %s)
                ON CONFLICT (subject, predicate) DO UPDATE SET object = EXCLUDED.object; 
            """, (row[0].strip(), row[1].strip(), row[2].strip()))
        conn.commit()
    cur.close()
    conn.close()

import json

# Function to export data from PostgreSQL to a JSON file
def export_postgres_data_to_json():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT subject, predicate, object FROM triples;")
    data = cur.fetchall()
    cur.close()
    conn.close()
    with open('postgres_data.json', 'w') as f: # Open a file to write
        json.dump([{'subject': sub, 'predicate': pred, 'object': obj} for sub, pred, obj in data], f) # Write data to file in JSON format

# Function to load merged data from a JSON file into the database
def load_merged_data():
    with open('/Users/varshithvattikuti/Desktop/NoSQL_MongoDB/merged_data.json', 'r') as f:
        data = json.load(f) # Load data from JSON file
    conn = connect_db()
    cur = conn.cursor()
    for item in data:
        # SQL command to insert merged data or update on conflict
        cur.execute("""
            INSERT INTO triples (subject, predicate, object)
            VALUES (%s, %s, %s)
            ON CONFLICT (subject, predicate) DO UPDATE SET object = EXCLUDED.object;
        """, (item['subject'], item['predicate'], item['object']))
    conn.commit()
    cur.close()
    conn.close()


def main():
    while True:
        print("\nAvailable commands: [query, update, delete, load, exit]")
        command = input("Enter command: ").strip().lower()
        if command == "exit":
            break
        elif command == "query":
            subject = input("Enter subject to query: ").strip()
            results = query(subject)
            print(results)
        elif command == "update":
            subject = input("Enter subject: ").strip()
            predicate = input("Enter predicate: ").strip()
            object = input("Enter object: ").strip()
            update(subject, predicate, object)
            print(f"Updated: {subject} {predicate} {object}")
        elif command == "delete":
            subject = input("Enter subject to delete: ").strip()
            predicate = input("Enter predicate to delete: ").strip()
            object = input("Enter object to delete: ").strip()
            delete(subject, predicate, object)
        elif command == "load":
            print("Loading data from file...")
            load_data('/Users/varshithvattikuti/Desktop/NoSQL_Postgres/triples.txt')
            print("Data loaded successfully.")
        else:
            print("Unknown command")

if __name__ == "__main__":
    load_merged_data()
    main()
