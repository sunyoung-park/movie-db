from flask import request
from flask_jwt_extended import create_access_token, get_jwt, get_jwt_identity, jwt_required
from flask_restful import Resource
from mysql_connection import get_connection
from mysql.connector import Error

from email_validator import validate_email, EmailNotValidError
from utils import check_password, hash_password



class MovieListReviewResource(Resource) :

    def get(self) :
        
        offset = request.args.get('offset')
        limit = request.args.get('limit')

        try :
            
            connection = get_connection()

            query = '''select m.id, m.title, count(r.content) review_cnt, ifnull(avg(r.rating),0) rating_avg
                        from movie m
                        left join review r
                        on m.id =r.movieId
                        group by m.id
                        order by review_cnt desc
                        limit '''+ str(offset) +''', '''+ str(limit) +''';'''
            

            cursor = connection.cursor(dictionary=True)

            cursor.execute(query)

            result_list = cursor.fetchall()

            cursor.close()
            connection.close()

        except Error as e :
            print(e)
            cursor.close()
            connection.close()
            return{'result':'fail','error':str(e)}, 500

        return {'result' : 'success',
                'items':str(result_list),
                'count': len(result_list)}, 200
    

class MovieListRatingResource(Resource) :

    def get(self) :
        
        offset = request.args.get('offset')
        limit = request.args.get('limit')

        try :
            
            connection = get_connection()

            query = '''select m.id, m.title, count(r.content) review_cnt, ifnull(avg(r.rating),0) rating_avg
                        from movie m
                        left join review r
                        on m.id =r.movieId
                        group by m.id
                        order by rating_avg desc    
                        limit '''+ str(offset) +''', '''+ str(limit) +''';'''
            

            cursor = connection.cursor(dictionary=True)

            cursor.execute(query)

            result_list = cursor.fetchall()

            cursor.close()
            connection.close()

        except Error as e :
            print(e)
            cursor.close()
            connection.close()
            return{'result':'fail','error':str(e)}, 500

        return {'result' : 'success',
                'items':str(result_list),
                'count': len(result_list)}, 200
    

class MovieDetailResource(Resource) :

    def get(self, movie_id) :

        print(movie_id)

        try :
            connection = get_connection()

            query = '''select m.title, m.imageUrl, m.summary, m.genre, m.year, m.attendance, avg(r.rating) rating_avg, count(r.rating) review_cnt
                        from movie m
                        left join review r
                        on m.id = r.movieId
                        where m.id = %s;'''
            
            
            record = (movie_id,)

            cursor = connection.cursor(dictionary=True)

            cursor.execute(query, record)

            result_list = cursor.fetchall()

            print(result_list)

            i = 0
            for row in result_list :
                result_list[i]['year']= row['year'].isoformat()
                i = i + 1

            cursor.close()
            connection.close()


        except Error as e:
            print(e)
            cursor.close()
            connection.close()
            return{"result":"fail", "error":str(e)}, 500
        
        if len(result_list) == 0 :
            return{"result":"fail","message":"해당 없는 영화"}, 400
        else :
            return{'result':'success','item': str(result_list[0])}