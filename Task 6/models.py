
from collections import defaultdict
from dataclasses import dataclass
from enum import Flag, auto
from typing import Dict, Optional
import pandas as pd


class Rights(Flag):
    READ = auto()
    WRITE = auto()
    PROVIDE = auto()
    FULL = READ | WRITE | PROVIDE
    NO_ACCESS = 0

    @property
    def read(self) -> bool:
        return Rights.READ in self

    @property
    def write(self) -> bool:
        return Rights.WRITE in self

    @property
    def provide(self) -> bool:
        return Rights.PROVIDE in self

    @staticmethod
    def patch_rights(rights: 'Rights', read: Optional[bool], write: Optional[bool], provide: Optional[bool]) -> 'Rights':
        if read is not None:
            if read:
                rights |= Rights.READ
            else:
                rights &= ~Rights.READ

        if write is not None:
            if write:
                rights |= Rights.WRITE
            else:
                rights &= ~Rights.WRITE

        if provide is not None:
            if provide:
                rights |= Rights.PROVIDE
            else:
                rights &= ~Rights.PROVIDE

        return rights


@dataclass(frozen=True, eq=True)
class User:
    id: str

    def __str__(self) -> str:
        return self.id


@dataclass(frozen=True, eq=True)
class Object:
    path: str

    def __str__(self) -> str:
        return self.path


class System:
    _root_users: set[User]
    _rights_matrix: Dict[Object, Dict[User, Rights]]

    def __init__(self, root_users: set[User], rights_matrix: Dict[Object, Dict[User, Rights]]) -> None:
        self._root_users = root_users
        self._rights_matrix = rights_matrix

    def get_rights(self, user: User, obj: Object) -> Rights:
        if user in self._root_users:
            return Rights.FULL

        rights = self._rights_matrix[obj]
        if user not in rights:
            return Rights.NO_ACCESS

        return rights[user]

    def set_rights(self, invoker: User, target: User, obj: Object, read: Optional[bool], write: Optional[bool], provide: Optional[bool]) -> None:
        if invoker == target:
            raise ValueError('Invoker can\'t change self rights.')

        if target in self._root_users:
            raise ValueError('Unable to set rights to super user.')

        if invoker in self._root_users:
            self._rights_matrix[obj][target] = Rights.patch_rights(self._rights_matrix[obj][target], read, write, provide)
            return

        if provide == False or read == False or write == False:
            raise ValueError('Only super users can revoke rules.')

        invoker_rights = self.get_rights(invoker, obj)

        if not invoker_rights.provide:
            raise ValueError('Invoker can\'t provide access.')

        if read == True and not invoker_rights.read:
            raise ValueError('Invoker has\'t read access.')

        if write == True and not invoker_rights.write:
            raise ValueError('Invoker has\'t write access.')

        self._rights_matrix[obj][target] = Rights.patch_rights(self._rights_matrix[obj][target], read, write, provide)

    def to_df(self) -> pd.DataFrame:
        CONVERTERS = {
            'R': lambda value: value.read,
            'W': lambda value: value.write,
            'P': lambda value: value.provide
        }

        users = self._get_all_users()

        columns = defaultdict(list)
        for obj in self._rights_matrix.keys():
            for user in users:
                current_rights = self.get_rights(user, obj)
                z = ''.join(right for right in CONVERTERS.keys() if CONVERTERS[right](current_rights))
                columns[user].append(z)

        return pd.DataFrame(columns, index=list(self._rights_matrix.keys()))

    def _get_all_users(self) -> set[User]:
        users = set(self._root_users)

        for user_rights in self._rights_matrix.values():
            for user in user_rights.keys():
                users.add(user)

        return users


class ExitCommand:
    pass


@dataclass(frozen=True, eq=True)
class ChmodCommand:
    obj: Object
    user: User
    read: Optional[bool]
    write: Optional[bool]
    provide: Optional[bool]
