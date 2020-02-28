import bcrypt as bc


def encrypt(password):
    passwd = password.encode()
    return bc.hashpw(passwd, bc.gensalt())


def verify(password, hashed):
    passwd = password.encode()
    return bc.checkpw(passwd, hashed)