import sqlite3

class UserDatabase:
    def __init__(self, db_file='users.db'):
        self.conn = sqlite3.connect(db_file)
        self.tables = ['users', 'locations'] # Foreign key order
        self.create_table()
        self.tables_and_columns = self._tables_and_columns()

    def create_table(self):
        """Creates the user table if it does not already exist."""
        self.conn.execute(
            '''CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            first_name TEXT,
            last_name TEXT,
            gender TEXT,
            email TEXT,
            phone TEXT,
            cell TEXT,
            date_of_birth DATE,
            age TEXT
            )''')
        self.conn.execute(
            '''CREATE TABLE IF NOT EXISTS locations (
            location_id INTEGER PRIMARY KEY,
            user_id INTEGER,
            street_name TEXT,
            street_number TEXT,
            city TEXT,
            state TEXT,
            country TEXT,
            postcode TEXT,
            latitude REAL,
            longitude REAL,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
            )''')
        self.conn.execute(
            '''CREATE TABLE IF NOT EXISTS logins (
            login_id INTEGER PRIMARY KEY,
            user_id INTEGER,
            uuid TEXT,
            username TEXT,
            password TEXT,
            salt TEXT,
            md5 TEXT,
            sha1 TEXT,
            sha256 TEXT,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
            )''')
        self.conn.execute(
            '''CREATE TABLE IF NOT EXISTS pictures (
            picture_d INTEGER PRIMARY KEY,
            user_id INTEGER,
            large TEXT,
            medium TEXT,
            thumbnail TEXT,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
            )''')
        self.conn.commit()

    def _tables_and_columns(self):
        cursor = self.conn.cursor()
        tables_and_columns = []
        for table_name in self.tables:
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = cursor.fetchall()
            column_names = [column[1] for column in columns]
            tables_and_columns.append((table_name,column_names))
        return tables_and_columns

    def insert_users(self, users):
        """Inserts users into the database."""
        cursor = self.conn.cursor()
        for user in users:
            cursor.execute(
                '''INSERT INTO users 
                (first_name, last_name, gender, email, phone, cell, date_of_birth, age)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                (
                    user['first_name'], 
                    user['last_name'], 
                    user['gender'], 
                    user['email'], 
                    user['phone'], 
                    user['cell'],
                    user['date_of_birth'],
                    user['age']
                )
            )
            user_id = cursor.lastrowid
            print(user_id)
            cursor.execute(
                '''INSERT INTO locations 
                (user_id, street_name, street_number, city, state, country, postcode, latitude, longitude) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                (
                    user_id,
                    user['street_name'], 
                    user['street_number'], 
                    user['city'],
                    user['state'],
                    user['country'],
                    user['postcode'],
                    user['latitude'],
                    user['longitude']
                )
                )
            cursor.execute(
                '''INSERT INTO logins 
                (user_id, uuid, username, password, salt, md5, sha1, sha256) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                (
                    user_id,
                    user['uuid'], 
                    user['username'], 
                    user['password'],
                    user['salt'],
                    user['md5'],
                    user['sha1'],
                    user['sha256']
                )
                )
            cursor.execute(
                '''INSERT INTO pictures
                (user_id, large, medium, thumbnail) 
                VALUES (?, ?, ?, ?)''',
                (
                    user_id,
                    user['large'],
                    user['medium'],
                    user['thumbnail']
                )
                )
        self.conn.commit()

    def get_all_users(self):
        """Fetches all users from the database."""
        cursor = self.conn.execute('''
                                   SELECT * FROM users u
                                    INNER JOIN locations loc ON u.user_id=loc.user_id
                                    INNER JOIN logins log ON u.user_id = log.user_id
                                    INNER JOIN pictures p ON u.user_id = p.user_id
                                   ''')
        return self._construct_dict(cursor)

    def get_filtered_users(self, first_name=None, last_name=None):
        """Fetches filtered users based on first and last name."""
        query = '''
        SELECT * FROM users u
        INNER JOIN locations loc ON u.user_id=loc.user_id
        INNER JOIN logins log ON u.user_id = log.user_id
        INNER JOIN pictures p ON u.user_id = p.user_id
        WHERE 1=1
        '''
        params = []
        if first_name:
            query += " AND first_name LIKE ?"
            params.append(f'%{first_name}%')
        if last_name:
            query += " AND last_name LIKE ?"
            params.append(f'%{last_name}%')
        cursor = self.conn.execute(query, params)

        #return [dict(zip([column[0] for column in cursor.description], row)) for row in cursor.fetchall()]
        return self._construct_dict(cursor)

    def get_users_pictures(self):
        """Fetches all users profile images from the database."""
        cursor = self.conn.execute("SELECT * FROM pictures")
        return self._construct_dict(cursor)

    def _construct_dict(self, cursor):
        column_names = [column[0] for column in cursor.description]
        rows = cursor.fetchall()
        data = []
        for row in rows:
            row_dict = dict(zip(column_names, row))
            data.append(row_dict)
        return data