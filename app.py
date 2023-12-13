from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api
from config import Config
from resources.movie import MovieListRatingResource, MovieListResource, MovieListReviewResource, MovieResource, MovieSearchResource
from resources.recommend import MovieRecommendResource
from resources.review import ReviewResource

from resources.user import UserLoginResource, UserLogoutResource, UserRegisterResource
from resources.user import jwt_blocklist

app = Flask(__name__)

app.config.from_object(Config)

jwt = JWTManager(app)

@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload) :
    jti = jwt_payload['jti']
    return jti in jwt_blocklist


api = Api(app)

api.add_resource(UserRegisterResource,'/user/register')
api.add_resource(UserLoginResource,'/user/login')
api.add_resource(UserLogoutResource,'/user/logout')
api.add_resource(MovieListReviewResource,'/movies/review')
api.add_resource(MovieListRatingResource,'/movies/rating')
api.add_resource(MovieResource,'/movie/<int:movie_id>')
api.add_resource(ReviewResource,'/review')
api.add_resource(MovieListResource,'/movie')
api.add_resource(MovieSearchResource,'/movie/search')
api.add_resource(MovieRecommendResource,'/movie/recommend')


if __name__ == '__main__' :
    app.run()