import datetime
from typing import List, Optional


class DatesFilter:
    @classmethod
    def filter_existing_keys_by_dates_range(cls, existing_keys: List[str], start_date: datetime.date,
                                            end_date: datetime.date, weekday: Optional[int] = None) -> set:
        """Filters a list of existing keys by a given dates range.

        Args:
            existing_keys (List[str]): A list of string keys to filter.
            start_date (datetime.date): The start date of the range to filter by.
            end_date (datetime.date): The end date of the range to filter by.
            weekday Optional(int): weekday value, will be 0 for only-monday filter

        Returns:
            set: A set of keys that fall within the specified date range.
        """
        DATE_START_INDEX = 26
        DATE_END_INDEX = 36

        valid_keys = set()
        # Loop through each key
        for key in existing_keys:
            # Extract the date string from the key
            key_date_str = key[DATE_START_INDEX:DATE_END_INDEX]

            # Convert the date string to a date object
            key_date = datetime.datetime.strptime(key_date_str, '%Y-%m-%d').date()

            # Check if the date falls within the specified range
            if start_date <= key_date <= end_date and ((weekday is None) or (key_date.weekday() == weekday)):
                valid_keys.add(key)

        # Return the set of valid keys
        return valid_keys
