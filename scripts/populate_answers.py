import json
import sqlite3

def main():
    """Execute SQL queries from a JSON file and update it with the results."""
    db_path = 'movies.db'
    json_path = 'data/queries_and_answer.json'

    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Read the JSON file
    with open(json_path, 'r') as f:
        data = json.load(f)

    # Execute each query and store the results
    for item in data:
        try:
            cursor.execute(item['sql'])
            rows = cursor.fetchall()
            # Convert rows to a list of dictionaries
            result = [dict(row) for row in rows]
            item['answer'] = result
        except sqlite3.Error as e:
            print(f"An error occurred with query for question '{item['question']}': {e}")
            item['answer'] = {'error': str(e)}

    # Close the database connection
    conn.close()

    # Write the updated data back to the JSON file
    with open(json_path, 'w') as f:
        json.dump(data, f, indent=4)

    print(f"Successfully updated {json_path} with query results.")

if __name__ == '__main__':
    main()
