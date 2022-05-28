import mysql.connector as mysql

class dbservice:
    def __init__(self):
        self.connector = None
        self.dbcursor = None
        self.connect_mysql_db()
        self.create_table()
    

    def connect_mysql_db(self):
        '''Connects to MySQL Database'''

        self.connector = mysql.connect(host='127.0.0.1', user='root', password='<mysqlpassword>')
        self.dbcursor = self.connector.cursor()
        self.dbcursor.execute('USE JORDEN')


    def create_table(self):
        '''Creats tables for USER, their Address and Company,
        Posts and Comments'''

        self.dbcursor.execute('''CREATE TABLE IF NOT EXISTS ADDRESS(
            ID INT NOT NULL AUTO_INCREMENT,
            STREET VARCHAR(100),
            SUITE VARCHAR(100),
            CITY VARCHAR(50),
            ZIPCODE VARCHAR(50),
            LAT VARCHAR(20),
            LNG VARCHAR(20),
            PRIMARY KEY (ID)
        );''')
        
        self.dbcursor.execute('''CREATE TABLE IF NOT EXISTS COMPANY(
            ID INT NOT NULL AUTO_INCREMENT,
            NAME VARCHAR(100),
            CATCHPHRASE VARCHAR(200),
            BS VARCHAR(200),
            PRIMARY KEY (ID)
        );''')

        self.dbcursor.execute('''CREATE TABLE IF NOT EXISTS USER(
            ID INT NOT NULL AUTO_INCREMENT,
            NAME VARCHAR(100),
            USERNAME VARCHAR(50),
            EMAIL VARCHAR(50),
            PHONE VARCHAR(30),
            WEBSITE VARCHAR(50),
            PRIMARY KEY (ID)
        );''')

        self.dbcursor.execute('''CREATE TABLE IF NOT EXISTS POST(
            USERID INT NOT NULL,
            ID INT NOT NULL AUTO_INCREMENT,
            TITLE VARCHAR(200),
            BODY VARCHAR(300),
            PRIMARY KEY (ID),
            FOREIGN KEY (USERID) REFERENCES USER(ID) ON UPDATE CASCADE ON DELETE CASCADE
        );''')

        self.dbcursor.execute('''CREATE TABLE IF NOT EXISTS COMMENT(
            POSTID INT NOT NULL,
            ID INT NOT NULL AUTO_INCREMENT,
            NAME VARCHAR(200),
            EMAIL VARCHAR(50),
            BODY VARCHAR(500),
            PRIMARY KEY (ID),
            FOREIGN KEY (POSTID) REFERENCES POST(ID) ON UPDATE CASCADE ON DELETE CASCADE
        );''')

        self.connector.commit()

    
    def add_user(self, table_values):
        '''Adds user to the Database alongwith 
        their address and company'''

        address = table_values["address"]
        company = table_values["company"]
        user_values = ""

        for i, k in enumerate(table_values):
            if k == "id" or k == "address" or k == "company":
                continue
            if i == len(table_values) - 2:
                user_values += f"'{table_values[k]}'"
                break
            user_values += f"'{table_values[k]}', "

        add_address_query = (f'''INSERT INTO ADDRESS 
        (STREET, SUITE, CITY, ZIPCODE, LAT, LNG)
        VALUES {address["street"], address["suite"], 
        address["city"], address["zipcode"], 
        address["geo"]["lat"], address["geo"]["lng"]}''')

        add_company_query = (f'''INSERT INTO COMPANY 
        (NAME, CATCHPHRASE, BS) 
        VALUES {company["name"], 
        company["catchPhrase"], company["bs"]}''')

        add_user_query = (f'''INSERT INTO USER
        (NAME, USERNAME, EMAIL, PHONE, WEBSITE)
        VALUES ({user_values})''')

        try:
            self.dbcursor.execute(add_address_query)
            self.dbcursor.execute(add_company_query)
            self.dbcursor.execute(add_user_query)
            self.connector.commit()
        except Exception as e:
            print(e)

        
    def add_post(self, table_values):
        '''Adds post in the Database'''
        
        add_post_query = (f'''INSERT INTO POST VALUES
            {table_values["userId"], table_values["id"], 
            table_values["title"], table_values["body"]}''')

        try:
            self.dbcursor.execute(add_post_query)
            self.connector.commit()
        except Exception as e:
            print(e)
    

    def add_comment(self, table_values):
        '''Adds comment in the Database'''
        
        add_comment_query = (f'''INSERT INTO COMMENT VALUES 
        {table_values["postId"], table_values["id"], table_values["name"],
        table_values["email"], table_values["body"]}''')

        try:
            self.dbcursor.execute(add_comment_query)
            self.connector.commit()
        except Exception as e:
            print(e)

    
    def read_users(self):
        '''Fetches user records from USER table'''

        select_query = (f'''SELECT user.*, STREET, SUITE, CITY, ZIPCODE, LAT, LNG, 
        company.NAME, CATCHPHRASE, BS FROM user, address, company 
        WHERE user.ID = address.ID AND user.ID = company.ID;''')

        try:
            self.dbcursor.execute(select_query)
            records = self.dbcursor.fetchall()
        except Exception as e:
            print(e)
            records = e
        return records

    
    def read_posts(self):
        '''Fetches post records from POST table'''

        select_query = (f"SELECT USERID, ID, TITLE, BODY FROM POST")

        try:
            self.dbcursor.execute(select_query)
            records = self.dbcursor.fetchall()
        except Exception as e:
            print(e)
            records = e
        return records
    

    def read_comments(self):
        '''Fetches comments from COMMENT table'''

        select_query = (f"SELECT POSTID, ID, NAME, EMAIL, BODY FROM COMMENT")

        try:
            self.dbcursor.execute(select_query)
            records = self.dbcursor.fetchall()
        except Exception as e:
            print(e)
            records = e
        return records


    def update_record(self, table_name, Id, updated_data):
        pass


    def delete_record(self, table_name, Id):
        '''Deletes record from the Database'''

        delete_query = (f"DELETE FROM {table_name} WHERE ID = {Id}")

        try:
            self.dbcursor.execute(delete_query)
            if table_name == 'USER':
                # deleting entries from address and company alongwith the user
                self.dbcursor.execute(f"DELETE FROM ADDRESS WHERE ID = {Id}")
                self.dbcursor.execute(f"DELETE FROM COMPANY WHERE ID = {Id}")
            self.connector.commit()
        except Exception as e:
            print(e)
        
    
