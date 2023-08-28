# Team Member: Manpreet Dhindsa
# Team Member: Eric Lorback
# Team Member: Brian Kelly

import mysql.connector

# Note: SQL already handles duplicate username and email with the way table is created, it throws an error.

# Global Variables
host = 'localhost'
user = 'root' # Change this line locally, DO NOT PUSH THIS CHANGE TO MASTER
password = 'THESEbiscuts78!' # Change this line locally, DO NOT PUSH THIS CHANGE TO MASTER
database_name = 'comp440'

logged_in_username = None

# Creates a new database named comp440 if it does not exist, does nothing otherwise.
def create_database_if_not_exists():
    global host, user, password, database_name

    try:
        # Connect to MySQL server
        connection = mysql.connector.connect(host=host, user=user, password=password)
        cursor = connection.cursor()

        # Check if the database already exists
        cursor.execute("SHOW DATABASES LIKE %s", (database_name,))
        result = cursor.fetchone()

        if result:
            print(f"The database '{database_name}' already exists.")
        else:
            # Create the database if it doesn't exist
            cursor.execute(f"CREATE DATABASE {database_name}")
            print(f"The database '{database_name}' has been created.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Creates the user table if does not exist, does nothing if it already exists.
def create_user_table_if_not_exists():
    global host, user, password, database_name

    # SQL query to create a new table
    create_table_query = """
    CREATE TABLE IF NOT EXISTS user (
        username VARCHAR(50) PRIMARY KEY,
        password VARCHAR(100) NOT NULL,
        firstName VARCHAR(50) NOT NULL,
        lastName VARCHAR(50) NOT NULL,
        email VARCHAR(100) UNIQUE
    )
    """

    try:
        # Connect to MySQL server
        connection = mysql.connector.connect(host=host, user=user, password=password, database=database_name)
        cursor = connection.cursor()

        # Execute the SQL query
        cursor.execute(create_table_query)
        connection.commit()

        print("Table 'user' is ready to use!")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Returns true if user credentials in the table, false otherwise.
def check_user_credentials(username, user_password):
    global host, user, password, database_name
    global logged_in_username

    # SQL query to check if the username and password match exist in the table
    check_credentials_query = """
    SELECT * FROM user
    WHERE username = %s AND password = %s
    """

    try:
        # Connect to MySQL server
        connection = mysql.connector.connect(host=host, user=user, password=password, database=database_name)
        cursor = connection.cursor()

        # Execute the SQL query with the provided username and password as parameters
        cursor.execute(check_credentials_query, (username, user_password))
        result = cursor.fetchone()

        if result:
            print("Username and password match exist in the table.")
            print(result)
            logged_in_username = username
            print(logged_in_username)
            return username
        else:
            print("Username and password match do not exist in the table.")
            return None

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Adds new user to user table if username and email are unique. Returns True if user in user table, else False. 
def add_new_user(username, user_password, firstName, lastName, email):
    global host, user, password, database_name

    # SQL query to check if the username and password match exist in the table
    add_user_query = """
    INSERT INTO user (username, password, firstName, lastName, email) VALUES
    (%s, %s, %s, %s, %s);
    """

    try:
        # Connect to MySQL server
        connection = mysql.connector.connect(host=host, user=user, password=password, database=database_name)
        cursor = connection.cursor()

        # Execute the SQL query with the provided username and password as parameters
        cursor.execute(add_user_query, (username, user_password, firstName, lastName, email))
        result = cursor.fetchone()
        connection.commit()

        print("User has been added")
        return True

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return False

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Function to fetch all data from the "user" table
def get_all_users():
    global host, user, password, database_name

    # SQL query to grab user table
    fetch_user_query = """
    SELECT * from user;
    """

    try:
        # Connect to MySQL server
        connection = mysql.connector.connect(host=host, user=user, password=password, database=database_name)
        cursor = connection.cursor()

        # Execute the SQL query
        cursor.execute(fetch_user_query)
        users = cursor.fetchall()
        return users

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def initalizeDatabase():
    print("In sql.py Initialize Database method")
    global host, user, password, database_name

    create_users = """
        CREATE TABLE IF NOT EXISTS user (
            username VARCHAR(50) PRIMARY KEY,
            password VARCHAR(100) NOT NULL,
            firstName VARCHAR(50) NOT NULL,
            lastName VARCHAR(50) NOT NULL,
            email VARCHAR(100) UNIQUE
        );
    """

    create_items = """
        CREATE TABLE IF NOT EXISTS items (
            item_id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) NOT NULL,
            title VARCHAR(255) NOT NULL,
            description VARCHAR(255) NOT NULL,
            date_posted TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            price DECIMAL(10, 2),
            FOREIGN KEY (username) REFERENCES user(username)
        );
    """

    create_categories = """
        CREATE TABLE IF NOT EXISTS categories (
            category_id INT AUTO_INCREMENT PRIMARY KEY,
            category_name VARCHAR(50) NOT NULL,
            item_id INT,
            FOREIGN KEY (item_id) REFERENCES Items(item_id)
        );
    """

    create_reviews = """
        CREATE TABLE IF NOT EXISTS Reviews (
            review_id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) NOT NULL,
            item_id INT NOT NULL,
            score VARCHAR(20) NOT NULL,
            remark TEXT NOT NULL,
            review_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (username) REFERENCES user(username),
            FOREIGN KEY (item_id) REFERENCES Items(item_id),
            CONSTRAINT no_update_reviews CHECK (1 = 1),
            CONSTRAINT unique_user_item_review UNIQUE (username, item_id)
        );
    """

    create_useracts = """
        CREATE TABLE IF NOT EXISTS UserActivity (
            username VARCHAR(50),
            activity_date DATE,
            items_posted INT DEFAULT 0,
            reviews_posted INT DEFAULT 0,
            PRIMARY KEY (username, activity_date),
            FOREIGN KEY (username) REFERENCES user(username)
        );
    """

    drop_trigger = "DROP TRIGGER IF EXISTS set_default_activity_date;"

    create_trigger = """
        CREATE TRIGGER set_default_activity_date
        BEFORE INSERT ON UserActivity
        FOR EACH ROW
        BEGIN
            IF NEW.activity_date IS NULL THEN
                SET NEW.activity_date = CURRENT_DATE();
            END IF;
        END;
    """

    insert_users = """
        INSERT INTO user (username, password, firstName, lastName, email)
        VALUES
        ('john_doe', 'hashed_password_here', 'John', 'Doe', 'john.doe@example.com'),
        ('mary_smith', 'hashed_password_here', 'Mary', 'Smith', 'mary.smith@example.com'),
        ('jane_doe', 'hashed_password_here', 'Jane', 'Doe', 'jane.doe@example.com'),
        ('alex_johnson', 'hashed_password_here', 'Alex', 'Johnson', 'alex.johnson@example.com'),
        ('sam_wilson', 'hashed_password_here', 'Sam', 'Wilson', 'sam.wilson@example.com');
    """

    insert_items = """
        INSERT INTO items (item_id, username, title, description, date_posted, price)
        VALUES
        (1, 'john_doe', 'Smartphone', 'Brand new smartphone with advanced features.', '2023-07-26 10:15:00', 599.99),
        (2, 'john_doe', 'Laptop', 'Powerful laptop for gaming and productivity.', '2023-07-26 15:30:00', 1299.00),
        (3, 'john_doe', 'Headphones', 'Wireless headphones with noise-canceling.', '2023-07-26 08:45:00', 149.99),
        (4, 'jane_doe', 'Smart Watch', 'Fitness tracking smartwatch.', '2023-07-26 11:20:00', 79.99),
        (5, 'jane_doe', 'Camera', 'Mirrorless camera with interchangeable lenses.', '2023-07-26 14:10:00', 899.00);
    """

    insert_categories = """
        INSERT INTO categories (category_id, category_name, item_id)
        VALUES
        (1, 'Electronics', 1),
        (2, 'Electronics', 2),
        (3, 'Electronics', 3),
        (4, 'Fitness', 4),
        (5, 'Photography', 5);
    """

    insert_reviews = """
        INSERT INTO Reviews (review_id, username, item_id, score, remark)
        VALUES
        (1, 'john_doe', 5, 'Excellent', 'Excellent Camera, highly recommended.'),
        (2, 'mary_smith', 2, 'Excellent', 'Great laptop, but battery life could be better.'),
        (3, 'jane_doe', 3, 'Excellent', 'Fantastic headphones, love the sound quality.'),
        (4, 'alex_johnson', 4, 'Excellent', 'Decent smartwatch, wish it had more apps.'),
        (5, 'sam_wilson', 5, 'Excellent', 'Impressive camera, perfect for photography enthusiasts.');
    """

    insert_useracts = """
        INSERT INTO UserActivity (username, activity_date, items_posted, reviews_posted)
        VALUES
        ('john_doe', '2023-07-26', 3, 1),
        ('mary_smith', '2023-07-26', 0, 1),
        ('jane_doe', '2023-07-26', 2, 1),
        ('alex_johnson', '2023-07-26', 0, 1),
        ('sam_wilson', '2023-07-26', 0, 1);
    """

    try:
        # Connect to MySQL server
        connection = mysql.connector.connect(host=host, user=user, password=password, database=database_name)
        cursor = connection.cursor()

        # Execute the SQL query
        cursor.execute(create_users)
        connection.commit()

        # Execute the SQL query
        cursor.execute(create_items)
        connection.commit()

        # Execute the SQL query
        cursor.execute(create_categories)
        connection.commit()

        # Execute the SQL query
        cursor.execute(create_reviews)
        connection.commit()

        # Execute the SQL query
        cursor.execute(create_useracts)
        connection.commit()

        # Execute the SQL query
        cursor.execute(drop_trigger)
        connection.commit()

        # Execute the SQL query
        cursor.execute(create_trigger)
        connection.commit()

        cursor.execute(insert_users)
        connection.commit()

        cursor.execute(insert_items)
        connection.commit()
        
        cursor.execute(insert_categories)
        connection.commit()
        
        cursor.execute(insert_reviews)
        connection.commit()

        cursor.execute(insert_useracts)
        connection.commit()

        print("Tables ready to use!")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def create_schema_if_not_exists():
    print("Create Schema if not exists sql method. Initalize database button will also use this.")

    global host, user, password, database_name

    create_users = """
        CREATE TABLE IF NOT EXISTS user (
            username VARCHAR(50) PRIMARY KEY,
            password VARCHAR(100) NOT NULL,
            firstName VARCHAR(50) NOT NULL,
            lastName VARCHAR(50) NOT NULL,
            email VARCHAR(100) UNIQUE
        );
    """

    create_items = """
        CREATE TABLE IF NOT EXISTS items (
            item_id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) NOT NULL,
            title VARCHAR(255) NOT NULL,
            description VARCHAR(255) NOT NULL,
            date_posted TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            price DECIMAL(10, 2),
            FOREIGN KEY (username) REFERENCES user(username)
        );
    """

    create_categories = """
        CREATE TABLE IF NOT EXISTS categories (
            category_id INT AUTO_INCREMENT PRIMARY KEY,
            category_name VARCHAR(50) NOT NULL,
            item_id INT,
            FOREIGN KEY (item_id) REFERENCES Items(item_id)
        );
    """

    create_reviews = """
        CREATE TABLE IF NOT EXISTS Reviews (
            review_id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) NOT NULL,
            item_id INT NOT NULL,
            score VARCHAR(20) NOT NULL,
            remark TEXT NOT NULL,
            review_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (username) REFERENCES user(username),
            FOREIGN KEY (item_id) REFERENCES Items(item_id),
            CONSTRAINT no_update_reviews CHECK (1 = 1),
            CONSTRAINT unique_user_item_review UNIQUE (username, item_id)
        );
    """

    create_useracts = """
        CREATE TABLE IF NOT EXISTS UserActivity (
            username VARCHAR(50),
            activity_date DATE,
            items_posted INT DEFAULT 0,
            reviews_posted INT DEFAULT 0,
            PRIMARY KEY (username, activity_date),
            FOREIGN KEY (username) REFERENCES user(username)
        );
    """

    drop_trigger = "DROP TRIGGER IF EXISTS set_default_activity_date;"

    create_trigger = """
        CREATE TRIGGER set_default_activity_date
        BEFORE INSERT ON UserActivity
        FOR EACH ROW
        BEGIN
            IF NEW.activity_date IS NULL THEN
                SET NEW.activity_date = CURRENT_DATE();
            END IF;
        END;
    """

    try:
        # Connect to MySQL server
        connection = mysql.connector.connect(host=host, user=user, password=password, database=database_name)
        cursor = connection.cursor()

        # Execute the SQL query
        cursor.execute(create_users)
        connection.commit()

        # Execute the SQL query
        cursor.execute(create_items)
        connection.commit()

        # Execute the SQL query
        cursor.execute(create_categories)
        connection.commit()

        # Execute the SQL query
        cursor.execute(create_reviews)
        connection.commit()

        # Execute the SQL query
        cursor.execute(create_useracts)
        connection.commit()

        # Execute the SQL query
        cursor.execute(drop_trigger)
        connection.commit()

        # Execute the SQL query
        cursor.execute(create_trigger)
        connection.commit()

        print("Tables ready to use!")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def insertItem(title, description, categories, price):
    print("In insert item sql button ") 

    global host, user, password, database_name

    get_items_posted_by_user_count = """
    select items_posted from useractivity ua
    where ua.username = %s and ua.activity_date = DATE_FORMAT(CURDATE(), '%Y-%m-%d')
    """

    insert_item = """
    insert into items (username, title, description, price) values
    (%s, %s, %s, %s)
    """

    last_insert_id_sql = """SELECT LAST_INSERT_ID();"""

    update_items_posted_sql = """
    INSERT INTO useractivity (username, items_posted)
    VALUES (%s, 1)
    ON DUPLICATE KEY UPDATE items_posted = items_posted + 1;
    """

    insert_category_sql = """
    insert into categories (category_name, item_id) values (%s, %s)
    """

    try:
        # Connect to MySQL server
        connection = mysql.connector.connect(host=host, user=user, password=password, database=database_name)
        cursor = connection.cursor()

        # Execute the SQL query
        cursor.execute(get_items_posted_by_user_count, (logged_in_username,))
        items_posted = cursor.fetchone()
        print("Number of items posted")

        if items_posted == None or items_posted[0] < 3:
            # Execute the SQL query
            cursor.execute(insert_item, (logged_in_username, title, description, price))
            connection.commit()

            # Execute the SQL query
            cursor.execute(last_insert_id_sql)
            item_id = cursor.fetchone()

            for category in categories:
                # Add to category table
                # Execute the SQL query
                cursor.execute(insert_category_sql, (category, item_id[0]))
                connection.commit()

            # Update user's items posted count
            cursor.execute(update_items_posted_sql, (logged_in_username,))
            connection.commit()

            return True
        else:
            return False

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def insertReview(reviewer_username, itemID, selectedRankValue, reviewDescription):
    print("In insert review sql method ") 

    global host, user, password, database_name

    get_reviews_posted_by_user_count = """
    select reviews_posted from useractivity ua
    where ua.username = %s and ua.activity_date = DATE_FORMAT(CURDATE(), '%Y-%m-%d')
    """

    insert_review = """
    insert into reviews (username, item_id, score, remark) values
    (%s, %s, %s, %s)
    """

    update_reviews_posted_sql = """
    INSERT INTO useractivity (username, reviews_posted)
    VALUES (%s, 1)
    ON DUPLICATE KEY UPDATE reviews_posted = reviews_posted + 1;
    """

    try:
        # Connect to MySQL server
        connection = mysql.connector.connect(host=host, user=user, password=password, database=database_name)
        cursor = connection.cursor()

        # Execute the SQL query
        cursor.execute(get_reviews_posted_by_user_count, (logged_in_username,))
        reviews_posted = cursor.fetchone()

        if reviews_posted == None or reviews_posted[0] < 3:
            # Execute the SQL query
            cursor.execute(insert_review, (logged_in_username, itemID, selectedRankValue, reviewDescription))
            connection.commit()

            # Update user's reviews posted count
            cursor.execute(update_reviews_posted_sql, (logged_in_username,))
            connection.commit()

            return True
        else:
            return False

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def dropTables():
    global host, user, password, database_name

    drop_tables_sql_script = """
        DROP TABLE IF EXISTS Reviews;
        DROP TABLE IF EXISTS UserActivity;
        DROP TABLE IF EXISTS categories;
        DROP TABLE IF EXISTS items;
        DROP TABLE IF EXISTS user;  
    """

    try:
        # Connect to MySQL server
        connection = mysql.connector.connect(host=host, user=user, password=password, database=database_name)
        cursor = connection.cursor()

        # Execute the SQL query
        cursor.execute(drop_tables_sql_script)
        connection.commit()

        print("Table 'user' is ready to use!")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def get_category_items(category):
    global host, user, password, database_name

    # SQL query to grab user table
    category_items_query = """
    select i.* 
    from items i join categories c
    on i.item_id = c.item_id where c.category_name like %s
    """

    try:
        # Connect to MySQL server
        connection = mysql.connector.connect(host=host, user=user, password=password, database=database_name)
        cursor = connection.cursor()

        # Execute the SQL query
        cursor.execute(category_items_query, (category,))
        items = cursor.fetchall()
        print(items)
        return items

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def get_phase3_1():
    global host, user, password, database_name

    # SQL query to grab user table
    category_items_query = """
    select cname, i.item_id, i.price, i.username 
    from items i join categories c on i.item_id = c.item_id
    join (select max(i.price) as max_price, c.category_name as cname
        from categories c join items i on c.item_id = i.item_id
        group by c.category_name) maxprices on maxprices.max_price = i.price and c.category_name = cname
    """

    try:
        # Connect to MySQL server
        connection = mysql.connector.connect(host=host, user=user, password=password, database=database_name)
        cursor = connection.cursor()

        # Execute the SQL query
        cursor.execute(category_items_query)
        items = cursor.fetchall()
        print(items)
        return items

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def get_phase3_2(c1, c2):
    global host, user, password, database_name

    # SQL query to grab user table
    category_items_query = """
    SELECT DISTINCT u1.username, DATE(u1.date_posted)
    FROM items u1
    JOIN items u2 ON u1.username = u2.username AND DATE(u1.date_posted) = DATE(u2.date_posted)
    JOIN categories c1 on c1.item_id = u1.item_id
    JOIN categories c2 on c2.item_id = u2.item_id
    WHERE c1.category_name = %s 
        AND c2.category_name = %s
        AND c1.category_name <> c2.category_name;
    """

    try:
        # Connect to MySQL server
        connection = mysql.connector.connect(host=host, user=user, password=password, database=database_name)
        cursor = connection.cursor()

        # Execute the SQL query
        cursor.execute(category_items_query, (c1, c2))
        items = cursor.fetchall()
        print(items)
        return items

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def get_phase3_3(username):
    global host, user, password, database_name

    # SQL query to grab user table
    category_items_query = """
    SELECT I.*
    FROM items I
    JOIN Reviews R ON I.item_id = R.item_id
    WHERE I.username = %s
    GROUP BY I.item_id
    HAVING COUNT(R.item_id) = COUNT(CASE WHEN R.score IN ('Excellent', 'Good') THEN 1 END);
    """

    try:
        # Connect to MySQL server
        connection = mysql.connector.connect(host=host, user=user, password=password, database=database_name)
        cursor = connection.cursor()

        # Execute the SQL query
        cursor.execute(category_items_query, (username,))
        items = cursor.fetchall()
        print(items)
        return items

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def get_phase3_4():
    global host, user, password, database_name

    # SQL query to grab user table
    category_items_query = """
    SELECT UA.USERNAME, UA.ACTIVITY_DATE
    FROM USERACTIVITY UA
    WHERE DATE(UA.ACTIVITY_DATE) = '2023-07-26'
    AND UA.ITEMS_POSTED = (
        SELECT MAX(UA1.ITEMS_POSTED)
        FROM USERACTIVITY UA1
        WHERE DATE(UA1.ACTIVITY_DATE) = '2023-07-26'
    )
    """

    try:
        # Connect to MySQL server
        connection = mysql.connector.connect(host=host, user=user, password=password, database=database_name)
        cursor = connection.cursor()

        # Execute the SQL query
        cursor.execute(category_items_query)
        items = cursor.fetchall()
        print(items)
        return items

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def get_phase3_5():
    global host, user, password, database_name

    # SQL query to grab user table
    category_items_query = """
    SELECT R.USERNAME
    FROM REVIEWS R
    GROUP BY R.USERNAME
    HAVING COUNT(R.USERNAME) = COUNT(CASE WHEN R.score = 'Poor' THEN 1 END);
    """

    try:
        # Connect to MySQL server
        connection = mysql.connector.connect(host=host, user=user, password=password, database=database_name)
        cursor = connection.cursor()

        # Execute the SQL query
        cursor.execute(category_items_query)
        items = cursor.fetchall()
        print(items)
        return items

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def get_phase3_6():
    global host, user, password, database_name

    # SQL query to grab user table
    category_items_query = """
    SELECT i.username
    FROM items i left JOIN Reviews R2
    ON I.item_id = R2.item_id
    group by i.username
    having COUNT(R2.item_id) = COUNT(CASE WHEN R2.score Not IN ('Poor') OR R2.item_id not in (select item_id from reviews) THEN 1 END);
    """

    try:
        # Connect to MySQL server
        connection = mysql.connector.connect(host=host, user=user, password=password, database=database_name)
        cursor = connection.cursor()

        # Execute the SQL query
        cursor.execute(category_items_query)
        items = cursor.fetchall()
        print(items)
        return items

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


if __name__ == "__main__":
    create_database_if_not_exists()
    create_user_table_if_not_exists()
    check_user_credentials('mdhindsa', 'Preet1997!')
    add_new_user('mdhindsa1', 'Preet1997!', 'Manpreet', 'Dhindsa', 'manpreet.dhindsa.747@gmail.com')
    add_new_user('mdhindsa2', 'Preet1997!', 'Manpreet', 'Dhindsa', 'mdhindsa1997@gmail.com')
    