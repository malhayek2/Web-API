import json, sqlite3
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d
class UsersDB:
    def __init__(self):
        print("connecting...")
        self.connection = sqlite3.connect("users.db")
        self.connection.row_factory = dict_factory
        self.cursor = self.connection.cursor()

    def __del__(self):
        self.connection.close()
        print("disconnected")

    def createUser(self, user_name, user_password, user_wifi, user_wifi_password, user_wifi_coords, reserved_int, reserved_str, user_type):
        self.cursor.execute('INSERT INTO Users (user_name,user_password,user_wifi,user_wifi_password, user_wifi_coords, reserved_int, reserved_str, user_type) VALUES (?,?,?,?,?,?,?,?)', (user_name, user_password, user_wifi, user_wifi_password, user_wifi_coords, reserved_int, reserved_str, user_type))
        self.connection.commit()

#create new user :)

    def get_by_id_name(self,user_id, user_name):
        self.cursor.execute('SELECT * FROM Users WHERE user_id=? and user_name=?', (user_name,user_name))
        return self.cursor.fetchone()

    def get_by_id(self,user_id):
        self.cursor.execute('SELECT * FROM Users WHERE user_id=?', (user_id,))
        return self.cursor.fetchone()

    def get_by_name(self, user_name):
        self.cursor.execute('SELECT * FROM Users WHERE user_name=?', (user_name,))
        return self.cursor.fetchone()

    def get_by_wifi(self, user_wifi):
        self.cursor.execute('SELECT * FROM Users WHERE user_wifi=?', (user_wifi,))
        return self.cursor.fetchone()

    def get_all_users(self):
        self.cursor.execute("SELECT * FROM Users")
        return self.cursor.fetchall()

    def update_by_id(self,user_id, user_name, user_password, user_wifi, user_wifi_password, user_wifi_coords, reserved_int, reserved_str, user_type):
        print("replacing...")
        self.cursor.execute('UPDATE Users SET user_name=?, user_password=?, user_wifi=?, user_wifi_password=?, user_wifi_coords=?, reserved_int=?, reserved_str=?, user_type=? WHERE user_id=?', (user_name, user_password,user_wifi,user_wifi_password, user_wifi_coords, reserved_int,reserved_str,user_type ,user_id))
        #print("Done?")
        self.connection.commit()


    def delete_User(self, user_id):
        print("deleting")
        self.cursor.execute('DELETE FROM Users WHERE user_id=?', (user_id,))
        #print("Done?")
        self.connection.commit()

db = UsersDB()

