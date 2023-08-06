# `Lict`

`Lict` is a hybrid list-dict container.
It supports metadata-based object management by allowing its
keys/names to be transformed seamlessly among hierarchical, flat, and
mixed structures.
Its simple, flexible, and transformable design is ideal for building
interpolatable python classes.


## Basic Licts and Interface/Behaviors

A trivial lict does not have any metadata.
Logically, it is simply a boxed python data object:

    trivial = [data]                                                        (1)

A simple (non-trivial) lict contains multiple data objects and
metakey-metadata pairs (MKDPs):

    simple = [                                                              (2)
        data1,
        data2,
        ...,
        mkey1:meta1,
        mkey2:meta2,
        ...,
    ]

Any hashable python object `mkey1`, ..., which may be a string like
`'meta'`, can be used as lict's metakey; any python object `meta1`,
..., including another lict, can be used as lict's metadata.

We compare the lict's interface with list, tuple, and dict in the
following table:

Usage            | Lict                       | Tuple           | List             | Dict
---              | ---                        | ---             | ---              | ---
Class            | `Lict`                     | `tuple`         | `list`           | `dict`
Print            | `[d1, k2:d2, ...]`         | `(d1, d2, ...)` | `[d1, d2, ...]`  | `{k1:d1, k2:d2, ...}`
Construct        | `l = Lict(d1, k2=d2, ...)` | `t = (d1, ...)` | `l = [d1, ...]`  | `d = {k1:d1, ...}`
Append           | `l.append(k, v)`           | N/A             | `l.append(v)`    | `d[k] = v`
Insert           | N/A                        | N/A             | `l.insert(i, v)` | `d[k] = v`
Set              | N/A                        | N/A             | `l[i] = x`       | `d[k] = v`
Set if not exist | `l.setdefault(k, v)`       | N/A             | N/A              | `d.setdefault(k, v)`
Get              | `v = l.get(k)`             | `v = t[i]`      | `v = l[i]`       | `v = l[k]` or `v = d.get(k, default)`
Delete           | N/A                        | N/A             | `del l[i]`       | `del d[k]`
Keys             | `l.keys()`                 | `range(len(t))` | `range(len(l))`  | `d` or `d.keys()`
Values           | `l.values()`               | `t`             | `l`              | `d.values()`
Pair             | `l.items()`                | `enumerate(t)`  | `enumerate(l)`   | `d.items()`
Raw item         | `l`                        | `t`             | `l`              | N/A


## Hierarchical Licts

`Lict` is designed for hierarchical origination of data and metadata.
Its power comes from nesting different levels of licts together.

In the above example, the metakeys themselves can be seen as metadata
of the metadata.
By giving them a new name, e.g., "kind key" `kkey1`, we can "deepen"
the hierarchy as:

    simple -> [                                                             (3)
        data1,
        data2,
        ...,
        [meta1, kkey1:mkey1],
        [meta2, kkey1:mkey2],
        ...,
    ]

The metadata `meta1` and `meta2` now are simply data nested in deeper
lict hierarchy.

Alternatively, We are also free to use licts for data and metadata:

    hierarchical = [                                                        (4)
        data1,
        [data2, kkey2:keyd1],
        ...,
        mkey1:meta1,
        mkey2:[meta2, kkey2:keyd2, ...],
        ...,
    ]


## Flattening and Grouping

If we turn `hierarchical`'s MKDPs into licts, we obtain

    hierarchical -> [                                                       (5)
        data1,
        [data2, kkey2:keyd1],
        ...,
        [meta1, kkey1:mkey1],
        [[meta2, kkey2:keyd2, ...], kkey1:mkey2],
        ...,
    ]

We can then "flatten" the hierarchical as `kkey1:mkey2`,
`kkey2:keyd2`, ..., are all MKDPs associated with `meta2`:

    hierarchical -> [                                                       (6)
        data1,
        [data2, kkey2:keyd1],
        ...,
        [meta1, kkey1:mkey1],
        [meta2, kkey1:mkey2, kkey2:keyd2, ...],
        ...,
    ]

Conversely, we may "group" this lict according to `kkey2`, which
results:

    hierarchical -> [                                                       (7)
        data1,
        keyd1:data2,
        ...,
        [meta1, kkey1:mkey1],
        keyd2:[meta2, kkey1:mkey2, ...],
        ...,
    ]

This lict is very similar to the original definition of
`hierarchical`.
If we reorder the content in the above form and compare it
side-by-side with the original definition, they become

    hierarchical = [                     ~~> [                              (8)
        data1,                               data1,
        [data2, kkey2:keyd1],                [meta1, kkey1:mkey1],
        ...,                                 ...,
        mkey1:meta1,                         keyd1:data2,
        mkey2:[meta2, kkey2:keyd2, ...],     keyd2:[meta2, kkey1:mkey2, ...],
        ...,                                 ...,
    ]                                    ]


## Default Grouping/Mount

Form (8) demonstrates that the default values of `hierarchical`
depends on how its metadata are grouped.
In general, even the number of default data objects can depends on the
grouping.

Licts has three features to address this.

1. It is possible to set the default grouping/mount.
   This allows users to adjust the view of a lict according to its
   application.

2. There are use cases that we need multiple views of the same lict.
   It is possible to create additional views based on a different
   default grouping/mount.

3. Because the default values and/or a key may return multiple data
   objects, lict data access always return a new lict that contains
   the proper data objects.

A lict propagates its method calls to its data but not its metadata.
Hence,

    simple.method() -> simple.data1.method(); simple.data2.method()

This is similar to applying a function to a numpy array---the function
is applied on the array itself but but not metadata.
It is also possible to use descriptors as metakeys, so the metadata
can be derived dynamically from the data.


## Implementation

There are multiple ways to implement lict.
In fact, form (6) suggests that it is possible to track all the
metakeys and metadata in a numpy record array or a pandas dataframe.
Nevertheless, to maximize portability, we provide a simple
implementation that only uses python's built-in data structures.
Although some of the operations may scales as O(N^2), we do not expect
lict to be a performance bottleneck because the number of fields in a
python object should be relatively small.

The hierarchical examples above demonstrate that licts are lists of
three things: data objects, MKDPs, and another licts.
This leads to two natural ways to implement licts:

1. We may simply define a `Lict` as a list of two-tuple, and introduce
   a special key, e.g., `Default`, to track the unkeyed data object.
   I.e.,

        normalized = [
            (Default, unkeyed_object),
            ...
            (key,     keyed_object),
            ...
        ]

2. Alternatively, since MKDPs is never needed outside lict's own
   algorithm, we may introduce a nested `_Pair` class insider the
   `Lict` class to track all the MKDPs.
   We can perform the `isinstance()` check against `Lict` and `_Pair`
   to distinguish the multiple cases.

The first approach uniformizes the different cases, and require an
special hashable object `Default` as the special key.
The second approach uses the class information to distinguish the
different situations, and require an extra `Lict._Pair` nested class.

The first approach is more uniform, easier to implement, and has
better "coding taste".
However, it makes returning a grouping result more tricky.
Should we return a normal python list?
Or should we return a `Lict` and pay the price that the returned list
contains pairs instead of the objects themselves.

Therefore, the default implementation of lict uses the second case.
We will make the code easier to read by hiding the class testing in a
single `Lict._getkey()` class method.
