from flask import request
from flask_jwt_extended import create_access_token
from flask_restful import Resource
from mysql_connection import get_connection
from mysql.connector import Error

from email_validator import validate_email, EmailNotValidError
from utils import check_password, hash_password


class UserRegisterResource(Resource) :
    
    def post(self) :

        data = request.get_json()

        # Email Validation
        try :
            validate_email(data['email'])
        except EmailNotValidError as e :
            print(e)
            return{'error' : str(e)}, 400
        
        
        # Password Validation
        
        if len(data['password']) < 4 or len(data['password']) > 14 :
            return {'error':'비밀번호 길이가 올바르지 않습니다.'}, 400
        

        # Password Hashing
        password = hash_password(data['password'])

        print(password)


        # User table DB save

        try :
            connection= get_connection()
            
            query = '''insert into user
                        (email, password,nickname,gender)
                        values
                        (%s,%s,%s,%s);'''
            
            record = (data['email'],
                      password,                      
                      data['nickname'],
                      data['gender'])
            
            cursor = connection.cursor()
            cursor.execute(query, record)
            connection.commit()


            # insert ID
            user_id = cursor.lastrowid

            cursor.close()
            connection.close() 

        except Error as e :
            print(e)
            cursor.close()
            connection.close() 
            return{'error':str(e)},500
        
        # user table id make JWT token

        access_token = create_access_token(user_id)

        return {'result':'sucess','access_token':access_token}, 200
    


class UserLoginResource(Resource) :

    def post(self) :

        try :
            pass
        except Error as e :
            pass
        return














