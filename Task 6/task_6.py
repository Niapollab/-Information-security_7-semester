#!/usr/bin/env python
from tabulate import tabulate
from random import choice, sample
from collections import defaultdict
from cli import auth_user, read_command
from models import ChmodCommand, ExitCommand, Object, Rights, System, User


def build_users(count: int) -> set[User]:
    NICKNAMES = [
        "Bestie",
        "BFF",
        "Queen",
        "Senorita",
        "Girly",
        "Gal",
        "Friend4Life",
        "ForeverFriend",
        "SoulSister",
        "Sis",
        "Chica",
        "Missy",
        "RideOrDie",
        "Homegirl",
        "Buddy",
        "King",
        "Champ",
        "Bro",
        "Amigo",
        "Bubba",
        "Tank",
        "Tiny",
        "Sport",
        "Slim",
        "Chief",
        "Buck",
        "Coach",
        "Junior",
        "Senior",
        "Doc",
        "Dude",
        "Pal",
        "Buster",
        "Bud",
        "Boo",
        "Mouse",
        "Munchkin",
        "Bee",
        "Dolly",
        "Precious",
        "Bug",
        "Chipmunk",
        "Dottie",
        "CutiePie",
        "BonnyLass",
        "Sweetums",
        "Toots",
        "Buttercup",
        "Lovey",
        "Nugget",
        "Teacup",
        "Oldie",
        "Shortie",
        "Kiddo",
        "Smarty",
        "Boomer",
        "Scout",
        "Ace",
        "Goon",
        "Punk",
        "Rambo",
        "Gump",
        "Bond",
        "Giggles",
        "Speedy",
        "Squirt",
        "Smiley",
        "Rapunzel",
        "MsCongeniality",
        "Teeny"
    ]

    return set(User(nick) for nick in sample(NICKNAMES, count))


def build_files(count: int) -> set[Object]:
    return set(Object(f'File_{index}') for index in range(1, count + 1))


def generate_random_rights() -> Rights:
    BOOL_LIST = [True, False]

    read_right = choice(BOOL_LIST)
    write_right = choice(BOOL_LIST)
    provide_right = (read_right or write_right) and choice(BOOL_LIST)

    return Rights.patch_rights(Rights.NO_ACCESS, read_right, write_right, provide_right)


def build_random_system(users: set[User], root_users: set[User], objects: set[Object]) -> System:
    not_root_users = users - root_users

    rights_matrix = defaultdict(dict)
    for user in not_root_users:
        for obj in objects:
            rights_matrix[obj][user] = generate_random_rights()

    return System(root_users, rights_matrix)


def print_rights_table(system: System) -> None:
    print(tabulate(system.to_df(), headers='keys', tablefmt='grid')) # type: ignore


def main() -> None:
    USERS_COUNT = 4
    FILES_COUNT = 4

    users = build_users(USERS_COUNT)
    admin = choice([*users])
    objects = build_files(FILES_COUNT)

    system = build_random_system(users, {admin}, objects)
    while True:
        print_rights_table(system)

        current_user = auth_user(users)
        print(f'Hello, {current_user}')

        while True:
            command = read_command(objects, users)

            if not isinstance(command, ChmodCommand):
                break

            try:
                system.set_rights(current_user, command.user, command.obj, command.read, command.write, command.provide)
            except Exception as ex:
                print(f'Error: {ex}')

            print_rights_table(system)


if __name__ == "__main__":
    main()
