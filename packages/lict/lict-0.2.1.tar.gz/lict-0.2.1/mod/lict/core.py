# Copyright 2017 Chi-kwan Chan
# Copyright 2017 Harvard-Smithsonian Center for Astrophysics
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

class Lict(list):
    """Lict

    `Lict` is a hybrid list-dict container.  It supports
    metadata-based object management by allowing its keys/names to be
    transformed seamlessly among hierarchical, flat, and mixed
    structures.  Its simple, flexible, and transformable design is
    ideal for building interpolatable python classes.

    """
    __slots__ = ()

    #==========================================================================
    # Nested "private" class to hold metakey-metadata pair

    class _Pair(tuple):
        """_Pair

        Because lict's metakey-metadata pairs (MKDPs) are never needed
        outside lict's own algorithm, we introduce this nested `_Pair`
        class inside the `Lict` class to track all the MKDPs.  We can
        perform the isinstance() check against `Lict` and `_Pair` to
        distinguish the nature of the items in `Lict`.

        """
        __slots__ = ()

        def __new__(cls, item):
            hash(item[0]) # raise a TypeError if unhashable
            return super().__new__(cls, item)

        def __repr__(self):
            return ':'.join(map(repr, self))

    #--------------------------------------------------------------------------
    # Logical `_Pair` getters that do not assume `item` is `_Pair`

    @classmethod
    def _isPair(cls, item):
        return isinstance(item, cls._Pair)

    @classmethod
    def _getkey(cls, item):
        return item[0] if cls._isPair(item) else None

    @classmethod
    def _getvalue(cls, item):
        return item[1] if cls._isPair(item) else item

    @classmethod
    def _getitem(cls, item):
        return item if cls._isPair(item) else cls._Pair((None, item))

    @classmethod
    def _matchkey(cls, item, key, cmp=None):
        if not cmp:
            cmp = lambda a, b: a == b
        return cmp(key, cls._getkey(item))

    #==========================================================================
    # Input and initialization

    def __init__(self, *args, **kwargs):
        for arg in args:
            self.append(arg)
        for k, v in kwargs.items():
            self.append(k, v)

    def append(self, *args, **kwargs):
        lens = len(args), len(kwargs)

        # Handle unkeyed value
        if   lens == (1, 0):
            item = args[0]
        elif lens == (2, 0) and args[0] is None:
            item = args[1]

        # Handle keyed value
        elif lens == (2, 0):
            item = self._Pair(args)
        elif lens == (0, 1):
            item = self._Pair(*kwargs.items())

        # Invalid input
        else:
            raise ValueError("append() takes exactly one metakey:metadata pair")

        # Really extend or append
        if isinstance(item, Lict) and item.allunkeyed(): # unkeyed value; unbox
            super().extend(item)
        else:
            super().append(item)

    def setdefault(self, key, value, cmp=None):
        return self.filterdefault(key, value, cmp=cmp).values()

    #--------------------------------------------------------------------------
    # Characteristics reporting

    def isempty(self):
        return len(self) == 0

    def istrivial(self):
        return len(self) == 1 and not isinstance(self[0], self._Pair)

    def somekeyed(self):
        for item in self:
            if isinstance(item, self._Pair):
                return True
        return False

    def someunkeyed(self):
        for item in self:
            if not isinstance(item, self._Pair):
                return True
        return False

    def allkeyed(self):
        return not self.someunkeyed()

    def allunkeyed(self):
        return not self.somekeyed()

    #--------------------------------------------------------------------------
    # Output
    #
    # Python has multiple ways to access elements from dictionary.
    # The `[]` operator is equivalent to calling `__getitem__()`.
    # However, python dictionary also provides the `get()` method.
    #
    # In CPython, `dict.__getitem__()` and `dict.get()` are
    # implemented as `dict_subscript()` and `dict_get_impl()` in C,
    # respectively.  The two functions are very similar except the
    # former uses the `__missing__()` method to handle missing keys,
    # while the later simply take optional default value argument.
    #
    # We do not override `__getitem__()` so we may still access the
    # raw items by indices.

    def get(self, *args, cmp=None):
        l = len(args)
        if l > 2:
            raise TypeError('Lict.get() takes at most 2 arguments')
        k = None if len(args) == 0 else args[0]
        f = self.filter(k, cmp=cmp)
        if len(f) == 0 and l == 2:
            return type(self)(args[1])
        else:
            return f.values()

    def keys(self): # TODO: turn results into views
        return type(self)(*dict.fromkeys(self._getkey(item) for item in self))

    def values(self): # TODO: turn results into views
        return type(self)(*(self._getvalue(item) for item in self))

    def items(self): # TODO: turn results into views
        return type(self)(*(self._getitem(item) for item in self))

    def filter(self, key=None, cmp=None): # TODO: turn results into views
        return type(self)(*(item for item in self if self._matchkey(item, key, cmp=cmp)))

    def filterdefault(self, key, value, cmp=None):
        f = self.filter(key, cmp=cmp)
        if f:
            return f
        else:
            self.append(key, value)
            return type(self)(self[-1])

    def __repr__(self):
        if '__name__' in self.keys():
            return '_'.join(self.filter('__name__').values())
        else:
            return '['+', '.join(map(repr, self))+']'

    #--------------------------------------------------------------------------
    # Transformations

    def group(self, key):
        l = type(self)()
        for item in self:
            if isinstance(item, self._Pair):
                raise ValueError('group() works only for unkeyed lict')
            if isinstance(item, Lict):
                s = item.filter(key)
                if s:
                    for k in s.values():
                        l.append(k, item)
                else:
                    l.append(item) # key not found
            else:
                l.append(item) # not a lict
        return l

    def ungroup(self, key):
        l = type(self)()
        for item in self:
            if isinstance(item, self._Pair):
                k, item = item
                if not isinstance(item, Lict):
                    item = type(self)(item)
                if k not in item.filter(key).values():
                    item.append(key, k)
            l.append(item)
        return l

    def tree(self, *keys):
        if len(keys) == 0:
            return self
        else:
            g = self.values().group(keys[0])
            l = type(self)()
            for k in g.keys():
                f = g.filter(k).values() # must be non-empty
                t = f.tree(*keys[1:])
                l.append(k, t[0] if t.istrivial() else t)
            return l
