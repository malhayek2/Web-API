from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
from UsersDB import UsersDB
import json, os
from passlib.hash import bcrypt


class MyRequestHandler(BaseHTTPRequestHandler):
    error = "invaild request"
    ##overrides
    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", self.headers["Origin"])
        self.send_header("Access-Control-Allow-Credentials", "true")
        BaseHTTPRequestHandler.end_headers(self)

    #GET ALL and GET ONE?
    def do_GET(self):
        path = self.path.split("/")
        if path[1] == "users" and len(path) == 2: ## /users
                # some repsonse code
                self.send_response(200)
                self.end_headers()
                db = UsersDB()
                users = db.get_all_users()
                jsonstring = json.dumps(users)
                self.wfile.write(bytes(jsonstring, "utf-8"))
        elif path[1] == "users" and len(path) == 3: ## /users/[user_id]
                  print(path[2])
                  self.send_response(200)
                  # self.send_header("Content-type", "application/json")
                  # self.send_header("Access-Control-Allow-Origin", self.headers["Origin"])
                  self.end_headers()
                  db = UsersDB()
                  users = db.get_by_id(path[2])
                  jsonstring = json.dumps(users)
                  self.wfile.write(bytes(jsonstring, "utf-8"))
        else:
            self.send_error(404, "Not Found")

    def do_OPTIONS(self):
        # self.load_session()
        self.send_response(200)
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, DELETE, PUT, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type,application/x-www-form-urlencoded')
        self.end_headers()


    def do_POST(self):
        #AUTH the user
        #self.load_session()
        if self.path == "/login":
            length = self.headers["Content-length"]
            length = int(length)
            print("content length is:", length)
            body = self.rfile.read(length).decode("utf-8")
            #print("body is:", body)
            parsed_body = parse_qs(body)
            print("parsed body is:", parsed_body)
            user_name = parsed_body['user_name'][0]
            user_password = parsed_body['user_password'][0]
            
        
            hashed_password = bcrypt.hash(user_password)
            db = UsersDB()
            #print(hashed_password)
            user = db.get_by_name(user_name)
            # print(user)
            # print("pulled password ", user['user_password'])
            # print("given password ", user_password)
            if (user == None):
                self.send_error(422, "Faliure, user does not exist ")
                return
            if bcrypt.verify(user_password, user['user_password']):
                    #sets session to the sote with existing session for user
                    user_id = user['user_id']
                    print("user_id:" , user_id)
                    print("Log in successful")
                    self.send_response(200)
                    self.end_headers()
                    return
            else:
                self.send_response(404)
                print("invaild email or password")
                self.end_headers()

        if self.path == "/users":

                    length = self.headers["Content-length"]
                    length = int(length)
                    print("content length is:", length)
                    body = self.rfile.read(length).decode("utf-8")
                    print("body is:", body)
                    parsed_body = parse_qs(body)
                    print("parsed body is:", parsed_body)

                    user_name = parsed_body['user_name'][0]
                    
                    user_password = parsed_body['user_password'][0]
                    
                    user_wifi = parsed_body['user_wifi'][0]
                    user_wifi_password = parsed_body['user_wifi_password'][0]
                    user_wifi_coords = parsed_body['user_wifi_coords'][0]
                    user_reserved_int = parsed_body['user_reserved_int'][0]
                    user_reserved_str = parsed_body['user_reserved_str'][0]
                    user_type = parsed_body['user_type'][0]
                    #hash password
                    hashed_password = bcrypt.hash(user_password)
                    db = UsersDB()
                    

                    db.createUser(user_name, hashed_password, user_wifi, user_wifi_password, user_wifi_coords, user_reserved_int, user_reserved_str, user_type)


                    self.send_response(201)
                    self.send_header("Access-Control-Allow-Origin", self.headers["Origin"])
                    self.send_header("Access-Control-Allow-Origin", "true")
                    self.end_headers()
                    return
        else:
                  self.send_error(404, "Not Found")
                  return
    #UPDATE OR REPLACE
    def do_PUT(self):

        if self.path == "/users":
                length = self.headers["Content-length"]
                length = int(length)
                print("content length is:", length)
                body = self.rfile.read(length).decode("utf-8")
                print("body is:", body)
                parsed_body = parse_qs(body)
                print("parsed body is:", parsed_body)

                user_id = parsed_body['user_id'][0]
                
                #user_id, user_name, user_password, user_wifi, user_wifi_password, user_wifi_coords, reserved_int, reserved_str, user_type
                user_name = parsed_body['user_name'][0]
                
                user_password = parsed_body['user_password'][0]
                
                user_wifi = parsed_body['user_wifi'][0]
                user_wifi_password = parsed_body['user_wifi_password'][0]
                user_wifi_coords = parsed_body['user_wifi_coords'][0]
                user_reserved_int = parsed_body['user_reserved_int'][0]
                user_reserved_str = parsed_body['user_reserved_str'][0]
                user_type = parsed_body['user_type'][0]
                #password hashed
                hashed_password = bcrypt.hash(user_password)
                

                db = UsersDB()

                db.update_by_id(user_id, user_name, hashed_password, user_wifi, user_wifi_password, user_wifi_coords, user_reserved_int, user_reserved_str, user_type)

                self.send_response(200)
                self.end_headers()
        else:
                self.send_error(404, "Not Found")
                return

    #DELETE A RECOED
    def do_DELETE(self):

        if self.path == "/users":
                length = self.headers["Content-length"]
                length = int(length)
                print("content length is:", length)
                body = self.rfile.read(length).decode("utf-8")
                print("body is:", body)
                parsed_body = parse_qs(body)
                print("parsed body is:", parsed_body)

                user_id = parsed_body['user_id'][0]
                
                db = UsersDB()
                db.delete_User(user_id)

                self.send_response(200)
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()

        else:
                self.send_error(404, "Not Found")
                return
    def do_COPY(self):
            self.send_error(404)
            return
    def do_HEAD(self):
            self.send_error(404)
            return
    def do_LINK(self):
            self.send_error(404)
            return
    def do_PATCH(self):
            self.send_error(404)
            return
    def do_UNLINK(self):
            self.send_error(404)
            return
    def do_PURGE(self):
            self.send_error(404)
            return
    def do_LOCK(self):
            self.send_error(404)
            return
    def do_UNLOCK(self):
            self.send_error(404)
            return
    def do_PROPFIND(self):
            self.send_error(404)
            return
    def do_VIEW(self):
            self.send_error(404)
            return

def main():
    #listen = ("127.0.0.1", 8080)
    listen = ("0.0.0.0", 8080)
    print(listen)
    server = HTTPServer(listen, MyRequestHandler)
    print("Listening...")
    server.serve_forever()


main()






# pass= input("password:")
# hashed = bcrypt.hash(pass)
#
#
# if bcrypt.verify(givenpassword, hashed):
# 	print("work")
# else:
# 	print("fail")
