#!/usr/bin/env python3
#
# Copyright (C) 2020 Guillaume Bernard <contact@guillaume-bernard.fr>
#
# This is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

__version_info__ = {
    "number": {
        "major": "0",
        "minor": "1",
        "revision": "0",
    },
}
__version__ = ".".join(__version_info__.get("number").values()) + __version_info__.get("tag", "")

import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(funcName)s in %(module)s − %(message)s")

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
logger.setLevel(logging.DEBUG)

newseye_languages = {"fr", "de", "fi"}


def date_range(start_date: datetime, time_window_days: int = 365, bucket_length: int = 365):
    """
    Split the period of time between start date and start date + time window delays into buckets of specified size.

    :param start_date: the start date of the date range
    :param time_window_days: the number of days after the start days that will generate the end date
    :param bucket_length: the length, in days of each time bucket
    """
    bucket_nb = int(int((start_date + timedelta(days=time_window_days) - start_date).days) / bucket_length)
    for bucket_count in range(bucket_nb):
        yield start_date + timedelta(days=bucket_length * (bucket_count + 1))
