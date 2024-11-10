import requests
import mysql.connector
from mysql.connector import Error


# Function to create a database connection
def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='pokemon_db',
            user='root',
            password='Tess Dog0804'
        )
        if connection.is_connected():
            print("Successfully connected to the database")
            return connection
    except Error as e:
        print(f"Error: '{e}'")
        return None


# Function to create the tables if they don't exist
def create_tables(connection):
    create_users_table_query = """
    CREATE TABLE IF NOT EXISTS users (
        user_id VARCHAR(255) PRIMARY KEY,
        user_name VARCHAR(255) NOT NULL
    );
    """

    create_favorite_pokemon_table_query = """
    CREATE TABLE IF NOT EXISTS favorite_pokemon (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id VARCHAR(255) NOT NULL,
        pokemon_id INT NOT NULL,
        pokemon_name VARCHAR(255) NOT NULL,
        height INT NOT NULL,
        weight INT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    );
    """
    try:
        cursor = connection.cursor()
        cursor.execute(create_users_table_query)
        cursor.execute(create_favorite_pokemon_table_query)
        connection.commit()
        print("Tables are ready")
    except Error as e:
        print(f"Error: '{e}'")
        connection.rollback()


# Function to insert user data into the database
def insert_user(connection, user_id, user_name):
    try:
        cursor = connection.cursor()
        insert_query = """
        INSERT INTO users (user_id, user_name)
        VALUES (%s, %s)
        ON DUPLICATE KEY UPDATE user_name = VALUES(user_name);
        """
        cursor.execute(insert_query, (user_id, user_name))
        connection.commit()
        print(f"User {user_name} inserted/updated successfully")
    except Error as e:
        print(f"Error: '{e}'")
        connection.rollback()


# Function to insert favorite Pokémon data into the database
def insert_favorite_pokemon(connection, user_id, pokemon_id, name, height, weight):
    try:
        cursor = connection.cursor()
        insert_query = """
        INSERT INTO favorite_pokemon (user_id, pokemon_id, pokemon_name, height, weight)
        VALUES (%s, %s, %s, %s, %s);
        """
        cursor.execute(insert_query, (user_id, pokemon_id, name, height, weight))
        connection.commit()
        print(f"Pokémon {name} inserted successfully")
    except Error as e:
        print(f"Error: '{e}'")
        connection.rollback()


# Function to export favorite Pokémon data of a specific user to a text file
def export_favorite_pokemon(connection, user_id):
    select_query = """
    SELECT u.user_name, fp.pokemon_id, fp.pokemon_name, fp.height, fp.weight
    FROM favorite_pokemon fp
    JOIN users u ON fp.user_id = u.user_id
    WHERE fp.user_id = %s
    """
    try:
        cursor = connection.cursor()
        cursor.execute(select_query, (user_id,))
        rows = cursor.fetchall()
        if rows:
            with open('user_favorite_pokemon.txt', 'w') as file:
                user_name = rows[0][0]
                file.write(f"User ID: {user_id}\nUser Name: {user_name}\n\n")
                for row in rows:
                    pokemon_id, name, height, weight = row[1:]
                    file.write(f"Pokémon ID: {pokemon_id}\n"
                               f"Name: {name}\n"
                               f"Height: {height}\n"
                               f"Weight: {weight}\n\n")
            print(f"\nThe favorite Pokémon of user ID {user_id} have been saved to 'user_favorite_pokemon.txt'.")
        else:
            print(f"No favorite Pokémon found for user ID {user_id}.")
    except Error as e:
        print(f"Error: '{e}'")


def main():
    connection = create_connection()
    if connection is not None:
        create_tables(connection)

        # Prompt user to either input Pokémon or export favorites
        choice = input("Enter '1' to input Pokémon or '2' to export favorite Pokémon: ")

        if choice == '1':
            # User ID and name input
            user_id = input("Enter your user ID: ")
            user_name = input("Enter your user name: ")

            # Insert or update user in the database
            insert_user(connection, user_id, user_name)

            # Variable containing an empty list (will later be filled with user input PokeIDs)
            pokemon_ids = []

            # For loop with 6 iterations, asks the user to input a PokeID 6 times
            for i in range(6):
                pokemon_id = input(f"Enter Pokémon ID #{i + 1}: ")
                # User input is appended to the pokemon_ids list
                pokemon_ids.append(pokemon_id)

            # Using the open() function to write 'pokemon.txt' as a txt file
            with open('pokemon.txt', 'w') as file:
                # For loop to iterate through list of Pokémon IDs
                for pokemon_id in pokemon_ids:
                    # Variable for accessing the Pokémon ID using the PokeAPI
                    response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{pokemon_id}')
                    # If statement to make sure response is '200', i.e., good, from API
                    if response.status_code == 200:
                        # Variables accessing the dictionaries/lists in the PokeAPI
                        pokemon_data = response.json()
                        name = pokemon_data['name']
                        height = pokemon_data['height']
                        weight = pokemon_data['weight']
                        # Writing required Pokémon info to a file using f-string to format
                        file.write(f"Name: {name}\nHeight: {height}\nWeight: {weight}\n\n")
                        # Inserting data into the database
                        insert_favorite_pokemon(connection, user_id, pokemon_id, name, height, weight)
                    else:
                        # There are 1010 Pokémon. So, in case a user enters 0 or 1011+, I've added an error message.
                        file.write(f"This Pokémon ID doesn't exist: {pokemon_id}\n\n")

            # This message lets the user know that their file has been created
            print("\nThe details of the 6 Pokémon you selected have now been saved to the file 'pokemon.txt'.")

        elif choice == '2':
            # User ID input for export
            user_id = input("Enter the user ID to export favorite Pokémon: ")
            export_favorite_pokemon(connection, user_id)

        else:
            print("Invalid choice. Please enter '1' or '2'.")

        # Close the database connection
        connection.close()

if __name__ == "__main__":
    main()

def abcd():
    x = 4
    y = 2178
    z = 18369
    return x, y, z
