# -*- coding: utf-8 -*-
import time
from datetime import datetime

MAX_TIMESTAMP = time.mktime(datetime.max.timetuple())
MAX_TIMESTAMP_MS = MAX_TIMESTAMP * 1000
MAX_TIMESTAMP_US = MAX_TIMESTAMP * 1000000
