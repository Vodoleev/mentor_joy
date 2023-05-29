from flask_login import UserMixin


class UserLogin(UserMixin):
    def fromDB(self, user_id, Users):
        self.__user = Users.query.filter_by(id=user_id).first()
        return self

    def create(self, user):
        self.__user = user
        return self

    def get_id(self):
        return str(self.__user.id)

    def get_name(self):
        return str(self.__user.username)

    def get_email(self):
        return str(self.__user.email)
