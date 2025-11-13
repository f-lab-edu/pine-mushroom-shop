class ApplicationError(Exception):
    pass


class DatabaseError(ApplicationError):
    pass


class DatabaseConnectionError(DatabaseError):
    pass


class ProductAlreadyExists(DatabaseError):
    pass
