"""Interval and NumericSet classes with methods to work with numeric intervals.

    Interval methods
    ----------------
        get_formatted - return formatted interval as a string
        is_overlapping - determine whether intervals overlap
        is_almost_overlapping - determine whether intervals almost overlap
        includes - determine whether the interval includes the given point
        copy - return a copy of the interval
        difference - return the difference between two given intervals
        intersection - return the intersection of two given intervals
        union - return the union of two given intervals

    NumericSet methods
    ----------------
        get_left_intervals - construct a list of intervals to the left from the interval
        get_right_intervals - construct a list of intervals to the right from the interval
        add - add a numeric interval to the set
        clear - clear the set from all numeric intervals
        copy - return a copy of the numric set
        difference - return the difference between the set and the given set
        difference_update - assign set to difference between it and the given set
        intersection - return an intersection of the set and the given set
        intersection_update - assign set to an intersection of it and the given set
        issubset - determine whether the set is a subset of the given set
        issuperset - determine whether the set is a superset of the given set
        pop - remove the rightmost interval if such exists
        remove - remove a numeric interval from the set
        symmetric_difference - return the symmetric difference of two sets
        symmetric_difference_update - assign set to the symmetric difference of two sets
        union - return a union of the set and the given set
        update - assign set to the union of it and the given set
        is_empty - determine whether a set of intervals is empty
        save - save a set of numeric intervals in the given file
        read - read a set of numerical intervals from the given file
"""

from typing import List
from numbers import Number


class Interval:
    """Class for performing operations on numeric intervals."""

    def __init__(self, start: int, end: int,
                 is_start_inclusive: bool = False, is_end_inclusive: int = False):
        """
        Initialize a numeric interval with certain range.
        """
        self.start = start
        self.end = end
        self.is_start_inclusive = is_start_inclusive or start == end
        self.is_end_inclusive = is_end_inclusive or start == end

    def get_formatted(self) -> str:
        """
        Return formatted interval as a string.
        """
        # Corner case - single point
        if self.start == self.end:
            return f'{{{self.start}}}'

        opening_bracket = '[' if self.is_start_inclusive else '('
        closing_bracket = ']' if self.is_end_inclusive else ')'

        return f'{opening_bracket}{self.start}, {self.end}{closing_bracket}'

    def is_overlapping(self, interval) -> bool:
        """
        Determine whether the interval overlaps with the given interval.
        """
        # Check if start of the first interval is to
        # the right from the start of the second interval
        if self.is_start_inclusive and interval.is_start_inclusive:
            start_check_1 = self.start >= interval.start
        else:
            start_check_1 = self.start > interval.start

        # Check if start of the first interval is to
        # the left from the end of the second interval
        if self.is_start_inclusive and interval.is_end_inclusive:
            end_check_1 = self.start <= interval.end
        else:
            end_check_1 = self.start < interval.end

        # Check if start of the second interval is to
        # the right from the start of the first interval
        if interval.is_start_inclusive and self.is_start_inclusive:
            start_check_2 = interval.start >= self.start
        else:
            start_check_2 = interval.start > self.start

        # Check if start of the second interval is to
        # the left from the end of the first interval
        if interval.is_start_inclusive and self.is_end_inclusive:
            end_check_2 = interval.start <= self.end
        else:
            end_check_2 = interval.start < self.end

        return (start_check_1 and end_check_1) or (start_check_2 and end_check_2)

    def is_almost_overlapping(self, interval) -> bool:
        """
        Determine whether the interval almost overlaps with the other interval.
        Two intervals almost overlap if their union forms one interval.
        """
        # If intervals overlap, they are not almost overlapping
        if self.is_overlapping(interval):
            return False

        is_start_junction = self.start == interval.end and (
            self.is_start_inclusive or interval.is_end_inclusive)
        is_end_junction = self.end == interval.start and (
            self.is_end_inclusive or interval.is_start_inclusive)

        return is_start_junction or is_end_junction

    def includes(self, point: Number) -> bool:
        """
        Determine whether the interval includes the given point.
        """
        is_inside = self.start < point < self.end
        is_start = self.is_start_inclusive and self.start == point
        is_end = self.is_end_inclusive and self.end == point

        return is_inside or is_start or is_end

    def copy(self):
        """
        Return a copy of the interval.
        """
        start, end = self.start, self.end
        is_start_inclusive, is_end_inclusive = self.is_start_inclusive, self.is_end_inclusive

        return Interval(start, end, is_start_inclusive, is_end_inclusive)

    @staticmethod
    def difference(interval_1, interval_2):
        """
        Return a set that consists of difference between two given intervals.
        """
        intersection = Interval.intersection(interval_1, interval_2)

        if intersection is None:
            return interval_1.copy()

        # Take the left part - between ends of intervals
        start = interval_1.start
        end = intersection.start

        is_start_inclusive = interval_1.is_start_inclusive
        is_end_inclusive = not intersection.is_start_inclusive

        if start == end:
            is_start_inclusive = is_end_inclusive = is_start_inclusive and is_end_inclusive

        if start > end or (start == end and not is_start_inclusive):
            left = None
        else:
            left = Interval(start, end, is_start_inclusive, is_end_inclusive)

        # Take the right part - between ends of intervals
        start = intersection.end
        end = interval_1.end

        is_start_inclusive = not intersection.is_end_inclusive
        is_end_inclusive = interval_1.is_end_inclusive

        if start == end:
            is_start_inclusive = is_end_inclusive = is_start_inclusive and is_end_inclusive

        if start > end or (start == end and not is_end_inclusive):
            right = None
        else:
            right = Interval(start, end, is_start_inclusive, is_end_inclusive)

        # Add constructed intervals to the set.
        numeric_set = NumericSet()

        if left is not None:
            numeric_set.add(left)

        if right is not None:
            numeric_set.add(right)

        return numeric_set

    @staticmethod
    def intersection(interval_1, interval_2):
        """
        Return an interval that consists of intersection of two given intervals.
        Return None if the result interval is empty.
        """
        start = max(interval_1.start, interval_2.start)
        end = min(interval_1.end, interval_2.end)

        is_start_inclusive = interval_1.includes(
            start) and interval_2.includes(start)
        is_end_inclusive = interval_1.includes(
            end) and interval_2.includes(end)

        if start > end or (start == end and not is_start_inclusive):
            return None

        return Interval(start, end, is_start_inclusive, is_end_inclusive)

    @staticmethod
    def union(interval_1, interval_2):
        """
        Return a set of intervals that consists of union of two given intervals.
        """
        # Check if the result should consist of two separate intervals.
        if not (interval_1.is_overlapping(interval_2) or
                interval_1.is_almost_overlapping(interval_2)):
            return NumericSet([interval_1, interval_2])

        start = min(interval_1.start, interval_2.start)
        end = max(interval_1.end, interval_2.end)

        is_start_inclusive = interval_1.includes(
            start) or interval_2.includes(start)
        is_end_inclusive = interval_1.includes(
            end) or interval_2.includes(end)

        result = Interval(start, end, is_start_inclusive, is_end_inclusive)

        return NumericSet([result])


class NumericSet:
    """Class for performing operations on sets of numeric intervals."""

    def __init__(self, intervals=None):
        if intervals is None:
            intervals = []

        self.intervals = sorted(intervals, key=lambda interval: interval.start)

    def get_left_intervals(self, interval: Interval) -> List[Interval]:
        """
        Construct a list of intervals that are to the left from the given interval.
        """
        left = []

        for intr in self.intervals:
            if intr.end <= interval.start and not intr.is_almost_overlapping(interval):
                left.append(intr)

        return left

    def get_right_intervals(self, interval: Interval) -> List[Interval]:
        """
        Construct a list of intervals that are to the right from the given interval.
        """
        right = []

        for intr in self.intervals:
            if intr.start >= interval.end and not intr.is_almost_overlapping(interval):
                right.append(intr)

        return right

    def add(self, new_interval: Interval) -> None:
        """
        Add a numeric interval to the set.
        """
        # If there are no other intervals, simply add the interval
        if self.is_empty():
            self.intervals.append(new_interval)
            return

        # If interval should be the leftmost one and does not
        # overlap with the first one, insert it at the start
        if (new_interval.end <= self.intervals[0].start and
                not new_interval.is_overlapping(self.intervals[0]) and
                not new_interval.is_almost_overlapping(self.intervals[0])):
            self.intervals.insert(0, new_interval)
            return

        # If interval should be the right one and does not
        # overlap with the last one, insert it at the start
        if (new_interval.start >= self.intervals[-1].end and
                not new_interval.is_overlapping(self.intervals[-1]) and
                not new_interval.is_almost_overlapping(self.intervals[-1])):
            self.intervals.append(new_interval)
            return

        new_start, new_end = new_interval.start, new_interval.end

        # All intervals located to the left from the new interval
        left = self.get_left_intervals(new_interval)

        # All intervals located to the right from the new interval
        right = self.get_right_intervals(new_interval)

        if left + right != self.intervals:
            new_start = min(new_start, self.intervals[len(left)].start)
            new_end = max(new_end, self.intervals[~len(right)].end)

        is_start_inclusive = ((new_interval.start == new_start and
                               new_interval.is_start_inclusive) or (
            self.intervals[len(left)].start == new_start and
            self.intervals[len(left)].is_start_inclusive))
        is_end_inclusive = ((new_interval.end == new_end and
                             new_interval.is_end_inclusive) or (
            self.intervals[~len(right)].end == new_end and
            self.intervals[~len(right)].is_end_inclusive))

        updated_interval = Interval(
            new_start, new_end, is_start_inclusive, is_end_inclusive)

        self.intervals = left + [updated_interval] + right

    def clear(self) -> None:
        """
        Clear the set from all numeric intervals.
        """
        self.intervals = []

    def copy(self):
        """
        Return a copy of the numric set.
        """
        return NumericSet([interval.copy() for interval in self.intervals])

    def difference(self, numeric_set) -> None:
        """
        Return a set representing a difference
        between the set and the given set.
        """
        updated_set = self.copy()
        updated_set.difference_update(numeric_set)

        return updated_set

    def difference_update(self, numeric_set) -> None:
        """
        Calculate difference between the set and the
        given set and update the set in-place.
        """
        for interval in numeric_set.intervals:
            self.remove(interval)

    def intersection(self, numeric_set):
        """
        Return an intersection of the set and the given set.
        """
        updated_set = self.copy()
        updated_set.intersection_update(numeric_set)

        return updated_set

    def intersection_update(self, numeric_set) -> None:
        """
        Calculate intersection of the set and the
        given set and update the set in-place.
        """
        updated_intervals = []

        for interval in numeric_set.intervals:
            for intr in self.intervals:
                intersection = Interval.intersection(interval, intr)

                if intersection is not None:
                    updated_intervals.append(intersection)

        self.intervals = updated_intervals

    def issubset(self, numeric_set) -> bool:
        """
        Determine whether the set is a subset of the given set.
        """
        return self.difference(numeric_set).is_empty()

    def issuperset(self, numeric_set) -> bool:
        """
        Determine whether the set is a superset of the given set.
        """
        return numeric_set.issubset(self)

    def pop(self) -> Interval:
        """
        Remove the rightmost interval if such exists.
        Otherwise, return None.
        """
        if self.is_empty():
            return None

        return self.intervals.pop()

    def remove(self, interval: Interval) -> None:
        """
        Remove a numeric interval from the set.
        """
        # All intervals located to the left from the new interval
        left = self.get_left_intervals(interval)

        # All intervals located to the right from the new interval
        right = self.get_right_intervals(interval)

        middle = []

        if len(right) == 0:
            middle_intervals = self.intervals[len(left):]
        else:
            middle_intervals = self.intervals[len(left):~len(right) + 1]

        for intr in middle_intervals:
            diff = Interval.difference(intr, interval)

            middle += diff.intervals

        self.intervals = left + middle + right

    def symmetric_difference(self, numeric_set):
        """
        Return a set with the symmetric difference of two sets.
        """
        return self.difference(numeric_set).union(numeric_set.difference(self))

    def symmetric_difference_update(self, numeric_set):
        """
        Find a set with the symmetric difference of two sets
        and update the set to be equal to it.
        """
        self.intervals = self.difference(numeric_set).union(
            numeric_set.difference(self)).intervals

    def union(self, numeric_set) -> None:
        """
        Return a union of the set and the given set of numeric intervals.
        """
        updated_set = self.copy()
        updated_set.update(numeric_set)

        return updated_set

    def update(self, numeric_set) -> None:
        """
        Find a union of the set and the given set of numeric intervals
        and update the set to be equal to it.
        """
        for interval in numeric_set.intervals:
            self.add(interval)

    def is_empty(self) -> bool:
        """
        Determine whether a set of intervals is empty.
        """
        return len(self.intervals) == 0

    def save(self, filename: str = 'result.txt') -> None:
        """
        Save a set of numeric intervals in the given file.
        The default filename is 'results.txt'.
        """
        with open(filename, 'w') as output_file:
            for interval in self.intervals:
                output_file.write(interval.get_formatted() + '\n')

    @ staticmethod
    def read(filename: str):
        """
        Read a set of numerical intervals from the given file and return a numeric set.
        """
        numeric_set = NumericSet()

        with open(filename, 'r') as input_file:
            for raw_interval in input_file.readlines():
                # remove '\n' at the end of the line, remove parentheses, split into parts
                raw_interval = raw_interval.rstrip()[1:-1].split(', ')

                if not raw_interval:
                    continue

                if len(raw_interval) == 1:
                    start = end = float(raw_interval[0])
                else:
                    start, end = map(float, raw_interval)

                is_start_inclusive = raw_interval[0] == '['
                is_end_inclusive = raw_interval[-1] == ']'

                numeric_set.add(
                    Interval(start, end, is_start_inclusive, is_end_inclusive))

        return numeric_set
