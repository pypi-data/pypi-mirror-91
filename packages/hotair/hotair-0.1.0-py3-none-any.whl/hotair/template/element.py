from __future__ import annotations

import typing
from xml.sax.saxutils import escape

from lxml import etree, html

from .handler import Handler
from .node import Node
from .text import Text


def element(**kwargs):
    def wrap(cls):
        name = kwargs.get('name', '')
        newlines = kwargs.get('newlines', True)
        if not name:
            name = cls.__name__.lower()

        cls.name = name
        cls.newlines = newlines
        return cls
    return wrap


class Element(Node):
    name: str
    newlines: bool

    def __init__(self, **kwargs):
        self.handlers = {}
        self.uuid_to_handler = {}
        self.children = []
        self.assign_attrs(**kwargs)

    def __call__(self, **kwargs):
        self.assign_attrs(**kwargs)
        return self

    def assign_attrs(self, **kwargs):
        for k, v in kwargs.items():
            if k.startswith('on_'):
                self.register_handler(k.removeprefix('on_'), v)
            setattr(self, k, v)  # limit

    def add_child(self, child: typing.Any):
        if isinstance(child, str):
            child = Text(child)

        if isinstance(child, Node):
            return self.children.append(child)

        raise TypeError(
            f'Child of {self.name!r} with value {child!r} is not serialisable.')

    def __getitem__(self, key):
        if isinstance(key, tuple):
            for k in key:
                self.add_child(k)
        elif isinstance(key, Node):
            self.add_child(key)
        else:
            self.add_child(str(key))

        return self

    def __class_getitem__(cls, key):
        self = cls()
        return self[key]

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}{self.children!r}"

    def register_handler(self, k: str, v):
        h = Handler(v)
        self.handlers[k] = h
        self.uuid_to_handler[h.uuid] = v

    def register_handlers(self, **kwargs):
        for k, v in kwargs.items():
            self.register_handler(k, v)

    def serialised(self) -> str:
        inner_formatted = " ".join(c.serialised() for c in self.children)

        attrs = {}

        if hasattr(self, 'id'):
            attrs['id'] = self.id  # why

        attrs.update({f"on{k}": v.to_js() for k, v in self.handlers.items()})
        attrs_serialised = " ".join(
            f'{k}="{escape(v)}"' for k, v in attrs.items())

        outer = f"<{self.name}{' ' + attrs_serialised if attrs_serialised else ''}>{inner_formatted}</{self.name}>"

        doc = html.fromstring(outer)
        return etree.tostring(doc, encoding='unicode', pretty_print=True)
