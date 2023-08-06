from importlib import resources

import toml

from philter_lite import filters


def load_regex_db():
    return toml.loads(resources.read_text(filters, "regex.toml"))


def load_regex_context_db():
    return toml.loads(resources.read_text(filters, "regex_context.toml"))


def load_set_db():
    return toml.loads(resources.read_text(filters, "set.toml"))


regex_db = load_regex_db()
regex_context_db = load_regex_context_db()
set_db = load_set_db()
