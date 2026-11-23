from functools import wraps


def error_handler(func):
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except PhoneInputError as e:
            raise PhoneInputError(str(e))
        except NoContactError as e:
            raise NoContactError(str(e))
        except DateInputError as e:
            raise DateInputError(str(e))
        except Exception as e:
            print(f"An error occurred: {e}")

    return inner


class NoContactError(Exception):
    pass


class NameInputError(Exception):
    pass


class PhoneInputError(Exception):
    pass


class DateInputError(Exception):
    pass
