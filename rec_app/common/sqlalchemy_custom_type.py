from sqlalchemy.types import TypeDecorator
import datetime


class DoubleTimestamp(TypeDecorator):
    impl = DOUBLE

    def __init__(self):
        TypeDecorator.__init__(self, as_decimal=False)

    def process_bind_param(self, value, dialect):
        return value.replace(tzinfo=datetime.timezone.utc).timestamp() * 1000

    def process_result_value(self, value, dialect):
        return datetime.datetime.utcfromtimestamp(value / 1000)