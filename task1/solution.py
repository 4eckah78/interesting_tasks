from functools import wraps


def strict(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        types = func.__annotations__

        for arg_name, arg_value in zip(types.keys(), args):
            expected_type = types[arg_name]
            if not type(arg_value) is expected_type:
                raise TypeError(
                    f"Type of argument '{arg_name}' must be '{expected_type.__name__}', "
                    f"not '{type(arg_value).__name__}'"
                )
        for arg_name, arg_value in kwargs.items():
            if arg_name in types:
                expected_type = types[arg_name]
                if not type(arg_value) is expected_type:
                    raise TypeError(
                        f"Type of argument '{arg_name}' must be '{expected_type.__name__}', "
                        f"not '{type(arg_value).__name__}'"
                    )

        result = func(*args, **kwargs)
        return result

    return wrapper


@strict
def sum_two(a: float, b: int) -> int:
    return a + b
