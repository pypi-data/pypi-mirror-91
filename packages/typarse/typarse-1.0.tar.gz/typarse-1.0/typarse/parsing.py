from typing import List, Optional, Union, get_type_hints, get_args, get_origin

from argparse import ArgumentParser


class BaseParser:

    _help = {

    }

    _default = {

    }

    _abbrev = {

    }

    def __init__(self):
        args_types = get_type_hints(self)
        parser = ArgumentParser()

        required = {}

        for name, type_ in args_types.items():
            # Handle optional arguments
            if get_origin(type_) == Union:
                assert type(None) in get_args(type_), "Generic Unions not supported - only Optionals"
                required[name] = False
                type_ = get_args(type_)[0]
            else:
                required[name] = name not in self._default

            flags = [f"--{name}"]
            if abbrev := self._abbrev.get(name, None):
                flags.append(f"-{abbrev}")
            help_ = self._help.get(name, None)

            if get_origin(type_) == list:
                type_ = get_args(type_)[0]

                parser.add_argument(*flags, nargs='+', help=help_, required=required[name], type=type_)
            elif type_ == bool:
                parser.add_argument(*flags, action="store_true", help=help_)
            else:
                parser.add_argument(*flags, action="store", type=type_, default=self._default.get(name, None),
                                    help=help_, required=required[name])

        args = parser.parse_args()

        for name in args_types:
            try:
                value = getattr(args, name)
            except AttributeError:
                value = self._default.get(name, None)
                if value is None and required[name]:
                    raise AttributeError(f"Required argument {name} not entered and not given a default value.")

            setattr(self, name, value)

