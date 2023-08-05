# Operations on Sets of Numeric Intervals

This package allows you to perform all operations on sets of numeric intervals. NumericSet class has all methods of Python set data structure as well as many additional ones. Intervals class has all basic methods to work with numeric intervals.

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
