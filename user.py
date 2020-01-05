USERS = {}


def get_user_by_email(email):
    """
    Returns user object for the provided email address
    :param email: String
    :return: Object (User)
    """
    return USERS.get(email)


class User(object):
    def __init__(self, first_name, last_name, email, password):
        """
        :param first_name: String
        :param last_name: String
        :param email: String
        :param password: String
        """
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password

    def get_password(self):
        return self.password

    def get_name(self):
        return self.first_name + " " +self.last_name

    def create_new_user(self):
        USERS[self.email] = User(self.first_name, self.last_name, self.email, self.password)
        print(USERS)