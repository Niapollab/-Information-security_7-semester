from typing import Any, Callable
from models import ChmodCommand, ExitCommand, Object, Rights, User


def read_valid(input_message: str, error_message: str, converter: Callable[[str], Any], validator: Callable[[Any], bool]) -> Any:
    while True:
        value = converter(input(input_message))

        if validator(value):
            return value

        print(error_message)


def auth_user(available_users: set[User]) -> User:
    return read_valid('Input user ID: ', 'Failed to login.', User, lambda user: user in available_users)


def read_command(available_objects: set[Object], available_users: set[User]) -> ExitCommand | ChmodCommand:
    def parse(value: str) -> ExitCommand | ChmodCommand | None:
        value = value.strip()

        if value == 'exit':
            return ExitCommand()

        args = value.split()

        if len(args) < 4 \
            or args[0] != 'chmod' \
            or Object(args[1]) not in available_objects \
            or User(args[2]) not in available_users \
            or not (args[3].startswith('-') \
            or args[3].startswith('+')):
            return None

        is_grant = args[3].startswith('+')

        return ChmodCommand(Object(args[1]), User(args[2]), is_grant if 'r' in args[3] else None, is_grant if 'w' in args[3] else None, is_grant if 'p' in args[3] else None)

    return read_valid('Input chmod <object> <user> +|-(r|w|p) or exit: ', 'Failed to recognize input.', parse, lambda value: isinstance(value, ExitCommand) | isinstance(value, ChmodCommand))
