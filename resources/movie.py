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
    

class MovieResource(Resource) :
    
    @jwt_required(optional=True)
    def get(self, movie_id) :

        user_id = get_jwt_identity()


        try :
            connection = get_connection()

            query = '''select m.*, avg(r.rating) rating_avg, count(r.rating) review_cnt
                        from movie m
                        left join review r
                        on m.id = r.movieId
                        where m.id = %s;'''
            
            
            record = (movie_id,)

            cursor = connection.cursor(dictionary=True)

            cursor.execute(query, record)

            result_list = cursor.fetchall() # 가져온 것을 끄집어 내는 것

            i = 0
            for row in result_list :
                result_list[i]['year']= row['year'].isoformat()
                result_list[i]['createdAt']= row['createdAt'].isoformat() # TypeError: Object of type datetime is not JSON serializable
                result_list[i]['rating_avg']= float(row['rating_avg']) # TypeError: Object of type Decimal is not JSON serializable
                i = i + 1

            cursor.close()
            connection.close()


        except Error as e:
            print(e)
            cursor.close()
            connection.close()
            return{"result":"fail", "error":str(e)}, 500
        
        # if len(result_list) == 0 :
        #     return{"result":"fail","message":"해당 없는 영화"}, 400
        # else :
        #     return{'result':'success','item': str(result_list[0])}

        print(result_list[0])
    

        return{'result':'success','movieInfo': result_list[0]}
    

class MovieListResource(Resource) :

    @jwt_required()
    def get(self) :

        order = request.args.get('order')
        offset = request.args.get('offset')
        limit = request.args.get('limit')

        user_id = get_jwt_identity()

        try :
            connection = get_connection()
            query = '''select m.id, m.title , count(r.id) reviewCnt, avg(r.rating) avgRating, if(f.id is null, 0,1) isFavorite
                    from movie m
                    left join review r
                    on m.id = r.movieId
                    left join favorite f
                    on m.id = f.movieId and f.userId = %s
                    group by m.id
                    order by '''+ order +''' desc
                    limit '''+ offset +''','''+ limit +''';'''

                    # order 리뷰수별, 별점 평균별 선택할 수 있도록 파라미터 키 입력

            record = (user_id,)

            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, record)

            result_list = cursor.fetchall()

            cursor.close()
            connection.close()


        except Error as e :
            print(e)
            cursor.close()
            connection.close()
            return{'error':str(e)}, 500
        
        print(result_list)

        i = 0
        for row in result_list :
            result_list[i]['avgRating']=float(row['avgRating'])
            i = i + 1
        
        return{'result':'success',
               'items':result_list,
               'count':len(result_list)}
    

class MovieSearchResource(Resource) :

    @jwt_required()
    def get(self):    

        keyword = request.args.get('keyword')
        offset = request.args.get('offset')
        limit = request.args.get('limit')

        try :
            connection = get_connection()
            query = '''select m.id, m.title, m.summary, count(r.id) reviewCnt, ifnull(avg(r.rating),0) avgRating
                    from movie m
                    left join review r
                    on m.id = r.movieId
                    where title like '%'''+ keyword +'''%'or summary like '%'''+ keyword +'''%'
                    group by m.id
                    limit '''+ offset +''','''+ limit +''';'''
            
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query)

            result_list = cursor.fetchall()

            cursor.close()
            connection.close()


        except Error as e :
            print(e)
            cursor.close()
            connection.close()
            return{'error' :str(e)}, 500        

        i = 0
        for row in result_list :
            result_list[i]['avgRating']=float(row['avgRating'])
            i = i + 1
        
        return{'result':'success',
               'items':result_list,
               'count':len(result_list)}
    

