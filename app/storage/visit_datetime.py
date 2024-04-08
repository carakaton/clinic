from datetime import datetime
from dataclasses import dataclass


@dataclass
class VisitDate:

    timestamp: datetime

    def __str__(self):
        return self.timestamp.strftime('%d.%m')


@dataclass
class VisitTime:

    timestamp: datetime

    def __str__(self):
        return self.timestamp.strftime('%H:%M')
