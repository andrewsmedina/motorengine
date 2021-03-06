#!/usr/bin/env python
# -*- coding: utf-8 -*-

from motorengine.fields.base_field import BaseField


class ListField(BaseField):
    '''
    Field responsible for storing :py:class:`list`.

    Usage:

    .. testcode:: modeling_fields

        posts = ListField(StringField())

    Available arguments (apart from those in `BaseField`):

    * `base_field` - ListField must be another field that describe the items in this list

    '''

    def __init__(self, base_field=None, *args, **kw):
        super(ListField, self).__init__(*args, **kw)

        if not isinstance(base_field, BaseField):
            raise ValueError("The list field 'field' argument must be an instance of BaseField, not '%s'." % str(base_field))

        if not self.default:
            self.default = lambda: []

        self._base_field = base_field

    def validate(self, value):
        for item in value:
            if not self._base_field.validate(item):
                return False

        return True

    def is_empty(self, value):
        return value is None or value == []

    # TODO: use multiprocessing map if available
    def to_son(self, value):
        return list(map(self._base_field.to_son, value))

    def from_son(self, value):
        return list(map(self._base_field.from_son, value))
