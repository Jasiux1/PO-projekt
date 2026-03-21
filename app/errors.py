class ValidationError(Exception):
    pass


class NotFoundError(Exception):
    pass


__all__ = ("ValidationError", "NotFoundError")
