from pickle import dump, load


def save(name: str, object_to_save) -> None:
    with open(name, 'wb') as f:
        dump(object_to_save, f)


def read(name: str) -> object:
    with open(name, 'rb') as f:
        return load(f)
