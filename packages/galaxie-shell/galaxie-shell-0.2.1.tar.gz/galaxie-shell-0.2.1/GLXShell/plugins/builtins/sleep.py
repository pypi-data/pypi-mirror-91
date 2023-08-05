import os
import argparse
import cmd2
import time

from GLXShell.plugins.builtins import PLUGIN_DESCRIPTION
from GLXShell.plugins.builtins import PLUGIN_WARRANTY
from GLXShell.plugins.builtins import PLUGIN_VERSION

sleep_parser = argparse.ArgumentParser(
    description="Pause for NUMBER seconds.  SUFFIX may be 's' for seconds (the default), 'm' for minutes, "
                "'h' for hours or 'd' for days.  Unlike most implementations that require NUMBER be an integer, "
                "here NUMBER may be an arbitrary floating point number.  Given two or more arguments, pause for the "
                "amount of time specified by the sum of their values.")
#      --help               display this help and exit
#      --version            output version information and exit
sleep_parser.add_argument(
    "--version", action="store_true", help="output version information and exit"
)
sleep_parser.add_argument(
    "NUMBER",
    nargs=argparse.ZERO_OR_MORE,
    help="[SUFFIX] delay for a specified amount of time",
)


class GLXSleep(cmd2.CommandSet):
    def __init__(self):
        super().__init__()
        # Internal Variables
        self.__work_with = None

        # First Init
        self.work_with = None
        self.seconds_per_minute = 60
        self.seconds_per_hour = 3600
        self.seconds_per_day = 86400

    @property
    def work_with(self):
        return self.__work_with

    @work_with.setter
    def work_with(self, value=None):
        if value is None:
            value = "seconds"

        if type(value) != str:
            raise TypeError("'work_with' property value must be a str type or None")

        if str(value).lower() not in ['seconds', 'minutes', 'hours', 'days']:
            raise ValueError("'work_with' property value allowed value: 'seconds', 'minutes', 'hours', 'days'")

        if self.work_with != value:
            self.__work_with = value

    @property
    def result(self):
        return f"{os.uname().machine}"

    @staticmethod
    def sleep_print_version():
        cmd2.Cmd().poutput(
            "sleep ({name}) v{version}\n{licence}".format(
                name=PLUGIN_DESCRIPTION,
                version=PLUGIN_VERSION,
                licence=PLUGIN_WARRANTY,
            )
        )

    def sleep(self, values=None):
        time.sleep(self.values_to_seconds(values=values))
        return True

    @cmd2.with_argparser(sleep_parser)
    @cmd2.with_category("Builtins")
    def do_sleep(self, args):
        # print(args.NUMBER)
        if args.version:  # pragma: no cover
            self.sleep_print_version()

        if len(args.NUMBER) > 0:  # pragma: no cover
            self.sleep(values=args.NUMBER)
        else:
            sleep_parser.print_usage()  # pragma: no cover

    def values_to_seconds(self, values=None):
        if values is None:
            values = ["0"]

        if type(values) != list:
            raise TypeError("'values' arguments must be a list or None")

        seconds = 0.0
        for value in values:
            if value[-1:].lower() == "d":
                print(str(value)[:-1])
                seconds += self.days_to_seconds(days=str(value)[:-1])
            elif value[-1:].lower() == "m":
                seconds += self.minutes_to_seconds(minutes=str(value)[:-1])
            elif value[-1:].lower() == "h":
                seconds += self.hours_to_seconds(hours=str(value)[:-1])
            elif value[-1:].lower() == "s":
                seconds += self.seconds_to_seconds(seconds=str(value)[:-1])
            else:
                seconds += self.seconds_to_seconds(seconds=value)

        return seconds

    @staticmethod
    def days_to_seconds(days=None):
        if days is None:
            days = 0
        try:
            float(days)
        except ValueError:
            raise TypeError("'days' arguments must be a int , float type or None")
        return float(86400.0 * float(days))

    @staticmethod
    def hours_to_seconds(hours=None):
        if hours is None:
            hours = 0
        try:
            float(hours)
        except ValueError:
            raise TypeError("'hours' arguments must be a int , float type or None")
        return float(3600.0 * float(hours))

    @staticmethod
    def minutes_to_seconds(minutes=None):
        if minutes is None:
            minutes = 0
        try:
            float(minutes)
        except ValueError:
            raise TypeError("'minutes' arguments must be a int , float type or None")
        return float(60.0 * float(minutes))

    @staticmethod
    def seconds_to_seconds(seconds=None):
        if seconds is None:
            seconds = 0
        try:
            return float(seconds)
        except ValueError:
            raise TypeError("'seconds' arguments must be a int , float type or None")
