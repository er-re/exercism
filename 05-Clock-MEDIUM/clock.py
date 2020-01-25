from typing import Tuple


class Clock:
    def __init__(self, hour: int, minute: int) -> None:
        owed_hour, self.minute = self.minute_parser(minute)
        self.hour = self.hour_parser(hour, owed_hour)

    def __repr__(self) -> str:
        hour = str(self.hour) if self.hour > 9 else '0' + str(self.hour)
        minute = str(self.minute) if self.minute > 9 else '0' + str(self.minute)
        return hour + ':' + minute

    def __eq__(self, other) -> bool:
        return True if other.hour == self.hour and other.minute == self.minute else False

    def __add__(self, minute: int) -> 'Clock':
        clock = Clock(0, minute)
        total_minute = self.minute + clock.minute
        total_hour = self.hour + clock.hour
        return self.__class__(total_hour, total_minute)

    def __sub__(self, minute: int) -> 'Clock':
        return self.__add__(-minute)

    @staticmethod
    def minute_parser(minute: int) -> Tuple[int, int]:
        """
        :param minute: Number of minutes
        :return: a tuple, a part of the minute that can be converted into hours and the residual minutes which can not
        be an hour (less than 60 minutes)
        """
        real_minute = minute % 60
        owed_hour = minute // 60
        return owed_hour, real_minute

    @staticmethod
    def hour_parser(*hours: int) -> int:
        """
        :param hours: *args of hours, for example 27, 49
        :return: residual to 24
        """
        hour = sum(hours)
        hour = hour % 24 if hour > 0 else (24 - (abs(hour) % 24)) % 24
        return hour

