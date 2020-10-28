import pathlib
import attr


def _to_path(item):
    return pathlib.Path(item)


def _is_existing_file(instance, attrib, value: pathlib.Path):
    return value.is_file()


@attr.s
class InputData:

    filled_report = attr.ib(type=pathlib.Path, converter=_to_path, validator=_is_existing_file)
    history = attr.ib(type=pathlib.Path, converter=_to_path, validator=_is_existing_file)
    last_run = attr.ib(type=pathlib.Path, converter=_to_path, validator=_is_existing_file)
    period = attr.ib(type=pathlib.Path, converter=_to_path, validator=_is_existing_file)

