# numeric_sets

Allows you to perform all operations on sets of numeric intervals.

## Usage example

Import classes from the main module of the package into your Python script.

```python3
from numeric_sets.main import Interval, NumericSet

main.main()
```

Feel free to perform any operation!

```python3
myset_1 = NumericSet()

myset_1.add(Interval(2, 4, True, True))  # [2, 4]
myset_1.add(Interval(5, 7))  # (5, 7)
myset_1.add(Interval(8, 10, is_end_inclusive=True))  # (8, 10]

myset_2 = NumericSet()

myset_2.add(Interval(2, 5))  # (2, 5)
myset_2.add(Interval(6, 9))  # (6, 9)

union = myset_1.union(
    myset_2)  # [2, 5) + (5, 10]
```

## Methods description

### Interval class

#### get_formatted

Returns formatted interval as a string.

```python3
my_interval = Interval(2, 5, is_start_inclusive=True)

my_interval.get_formatted()
```

##### Return

Interval as a formatted string.

#### is_overlapping

Determines whether the interval overlaps with the given interval.

```python3
my_interval_1 = Interval(2, 5)
my_interval_2 = Interval(4, 8)

my_interval_1.is_overlapping(my_interval_2)
```

##### Arguments

- **interval** a numeric interval

##### Return

True if intervals overlap, False otherweise.

#### is_almost_overlapping

```python3
my_interval_1 = Interval(2, 5)
my_interval_2 = Interval(4, 8)

my_interval_1.is_almost_overlapping(my_interval_2)
```

Determines whether the interval almost overlaps with the given interval.

##### Arguments

- **interval** a numeric interval

##### Return

True if intervals almost overlap, False otherweise.

#### includes

Determines whether the interval includes the given point.

```python3
my_interval_1 = Interval(2, 5)
my_interval_2 = Interval(4, 8)

my_interval_1.includes(my_interval_2)
```

##### Arguments

- **point** a numeric point

##### Return

True if the interval includes the given point, False otherweise.

#### copy

Copies the interval.

```python3
my_interval_1 = Interval(2, 5)
my_interval_2 = my_interval_1.copy()
```

##### Return

A copy of the interval.

#### difference `[static]`

Returns the difference between two given intervals.

```python3
my_interval_1 = Interval(2, 5)
my_interval_2 = Interval(4, 8)

diff = Interval.difference(my_interval_1, my_interval_2)
```

##### Arguments

- **interval_1** a numeric interval
- **interval_2** a numeric interval

##### Return

Difference between two given intervals.

#### intersection `[static]`

Returns the intersection of two given intervals.

```python3
my_interval_1 = Interval(2, 5)
my_interval_2 = Interval(4, 8)

intersection = Interval.intersection(my_interval_1, my_interval_2)
```

##### Arguments

- **interval_1** a numeric interval
- **interval_2** a numeric interval

##### Return

Intersection of two given intervals.

#### union `[static]`

Returns the union of two given intervals.

```python3
my_interval_1 = Interval(2, 5)
my_interval_2 = Interval(4, 8)

union = Interval.union(my_interval_1, my_interval_2)
```

##### Arguments

- **interval_1** a numeric interval
- **interval_2** a numeric interval

##### Return

Union of two given intervals.

### NumericSet methods

#### get_left_intervals

Constructs a list of intervals to the left from the interval.

```python3
myset = NumericSet([Interval(3, 5), Interval(10, 12)])


left = myset.get_left_intervals((6, 8))
```

##### Arguments

- **interval** a numeric interval

##### Return

A list of intervals to the left from the interval.

#### get_right_intervals

Constructs a list of intervals to the right from the interval.

```python3
myset = NumericSet([Interval(3, 5), Interval(10, 12)])


right = myset.get_right_intervals((6, 8))
```

##### Arguments

- **interval** a numeric interval

##### Return

A list of intervals to the right from the interval.

#### add

Adds a numeric interval to the set.

```python3
myset = NumericSet()

myset.add(Interval(3, 5))
myset.add(Interval(10, 12))
```

##### Arguments

- **interval** a numeric interval

#### clear

Clears the set from all numeric intervals.

```python3
myset = NumericSet()

myset.add(Interval(3, 5))
myset.add(Interval(10, 12))

myset.clear()
```

#### copy

Copies the numeric set.

```python3
myset = NumericSet()

myset.add(Interval(3, 5))
myset.add(Interval(10, 12))

copy = myset.copy()
```

##### Return

A copy of the numric set.

#### difference

Constructs a set representing the difference between the set and the given set.

```python3
myset_1 = NumericSet([Interval(3, 5), Interval(10, 12)])
myset_2 = NumericSet([Interval(2, 4), Interval(11, 15)])

diff = myset_1.difference(myset_2)
```

##### Arguments

- **numeric_set** a numeric set

##### Return

The difference between the set and the given set.

#### difference_update

Constructs a set representing the difference between the set and the given set and updates the set.

```python3
myset_1 = NumericSet([Interval(3, 5), Interval(10, 12)])
myset_2 = NumericSet([Interval(2, 4), Interval(11, 15)])

myset_1.difference_update(myset_2)
```

##### Arguments

- **numeric_set** a numeric set

#### intersection

Constructs a set representing the intersection of the set and the given set.

```python3
myset_1 = NumericSet([Interval(3, 5), Interval(10, 12)])
myset_2 = NumericSet([Interval(2, 4), Interval(11, 15)])

intersection = myset_1.intersection(myset_2)
```

##### Arguments

- **numeric_set** a numeric set

##### Return

The intersection of the set and the given set.

#### intersection_update

Constructs a set representing the intersection of the set and the given set and updates the set.

```python3
myset_1 = NumericSet([Interval(3, 5), Interval(10, 12)])
myset_2 = NumericSet([Interval(2, 4), Interval(11, 15)])

myset_1.intersection_update(myset_2)
```

##### Arguments

- **numeric_set** a numeric set

#### issubset

Determines whether the set is a subset of the given set.

```python3
myset_1 = NumericSet([Interval(3, 5), Interval(10, 12)])
myset_2 = NumericSet([Interval(2, 4)])

is_subset = myset_2.is_subset(myset_1)
```

##### Arguments

- **numeric_set** a numeric set

##### Return

True if the interval is a subset of the given interval, False otherweise.

#### issuperset

Determines whether the set is a superset of the given set.

```python3
myset_1 = NumericSet([Interval(3, 5), Interval(10, 12)])
myset_2 = NumericSet([Interval(2, 4)])

is_superset = myset_1.is_superset(myset_2)
```

##### Arguments

- **numeric_set** a numeric set

##### Return

True if the interval is a superset of the given interval, False otherweise.

#### pop

Removes the rightmost interval if such exists.

```python3
myset = NumericSet([Interval(3, 5), Interval(10, 12)])

last_interval = myset.pop()
```

##### Return

The rightmost interval if such exists, None otherwise.

#### remove

Removes a numeric interval from the numeric set.

```python3
myset = NumericSet([Interval(3, 5), Interval(10, 12)])

myset.remove(Interval(2, 4))
```

##### Arguments

- **interval** a numeric interval

#### symmetric_difference

Constructs a set representing the symmetric difference of two sets.

```python3
myset_1 = NumericSet([Interval(3, 5), Interval(10, 12)])
myset_2 = NumericSet([Interval(2, 4), Interval(11, 15)])

symmetric_diff = myset_1.symmetric_difference(myset_2)
```

##### Arguments

- **numeric_set** a numeric set

##### Return

The symmetric difference of the set and the given set.

#### symmetric_difference_update

Constructs a set representing the symmetric difference of the set and the given set and updates the set.

```python3
myset_1 = NumericSet([Interval(3, 5), Interval(10, 12)])
myset_2 = NumericSet([Interval(2, 4), Interval(11, 15)])

myset_1.symmetric_difference_update(myset_2)
```

##### Arguments

- **numeric_set** a numeric set

#### union

Constructs a set representing the union of two sets.

```python3
myset_1 = NumericSet([Interval(3, 5), Interval(10, 12)])
myset_2 = NumericSet([Interval(2, 4), Interval(11, 15)])

union = myset_1.union(myset_2)
```

##### Arguments

- **numeric_set** a numeric set

##### Return

The union of the set and the given set.

#### update

Constructs a set representing the union of the set and the given set and updates the set.

```python3
myset_1 = NumericSet([Interval(3, 5), Interval(10, 12)])
myset_2 = NumericSet([Interval(2, 4), Interval(11, 15)])

myset_1.update(myset_2)
```

##### Arguments

- **numeric_set** a numeric set

#### is_empty

Determines whether a set of intervals is empty.

```python3
myset = NumericSet([Interval(3, 5))])

is_empty = myset_1.is_empty()
```

##### Return

True if the set is empty, False otherweise.

#### save

Saves a set of numeric intervals in the given file.

```python3
myset = NumericSet([Interval(3, 5))])

myset_1.save('myset_1.txt')
```

##### Arguments

- **filename** the name of the file

#### read `[static]`

Reads a set of numerical intervals from the given file.

```python3
myset = NumericSet.read('myset_1.txt')
```

##### Arguments

- **filename** the name of the file

## Meta

Dmytro Yaroshevych – dyaroshevych@gmail.com

Distributed under the MIT license. See `LICENSE` for more information.

[https://github.com/dyaroshevych/numeric_sets](https://github.com/dyaroshevych/numeric_sets)

## Contributing

1. Fork it (<https://github.com/dyaroshevych/numeric_sets/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request
