import bcrypt as bc


def encrypt(password):
    password = password.encode()
    return bc.hashpw(password, bc.gensalt())


def verify(password, hashed):
    password = password.encode()
    hashed = hashed.encode()
    return bc.checkpw(password, hashed)