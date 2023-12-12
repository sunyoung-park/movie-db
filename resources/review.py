from flask import request
from flask_jwt_extended import create_access_token, get_jwt, get_jwt_identity, jwt_required
from flask_restful import Resource
from mysql_connection import get_connection
from mysql.connector import Error


class ReviewResource(Resource) :

    @jwt_required()
    def post(self) :
        
        data = request.get_json()
        user_id = get_jwt_identity()


        try :
            connection = get_connection()

            query = '''insert into review
                        (movieId, userId, rating, content)
                        values
                        (%s,%s,%s,%s);'''
            
            record =(data['movieId'],
                     user_id,
                     data['rating'],
                     data['content'])
            
            cursor = connection.cursor()
            cursor.execute(query,record)
            connection.commit()

            cursor.close()
            connection.close()
        except Error as e :
            print(e)
            cursor.close()
            connection.close()
            return{'error': str(e)}, 500
        return {'result':'success'}, 200

    @jwt_required(optional=True) #이 API 헤더 있어도 되고 없어도 되는 파라미터 설정
    def get(self):

        movieId = request.args.get('movieId')
        
        offset = request.args.get('offset')
        limit = request.args.get('limit')

        try :
            connection = get_connection()
            query = '''select r.id, u.nickname, r.content, r.rating
                    from review r
                    join user u
                    on r.userId = u.id
                    where r.movieId=%s
                    order by r.createdAt desc
                    limit '''+ str(offset) +''','''+ str(limit)+''';'''
            
            record = (movieId, )

            cursor = connection.cursor(dictionary=True)
            cursor.execute(query,record)
            
            result_list = cursor.fetchall()

            cursor.close()
            connection.close()

        except Error as e :
            print(e)
            cursor.close()
            connection.close()
            return{'error': str(e)}, 500
        return {'result':'success',
                'items':result_list,
                'count': len(result_list)}, 200