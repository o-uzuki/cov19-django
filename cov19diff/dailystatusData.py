from .models import DailyCsv
from cov19diff.jhudata import readDaily
from cov19diff.restype import DaylyStatus

from datetime import date, datetime, timedelta

class DailyStatusData:

    def __init__(self):
        self.start = datetime.today()
        self.end = self.start - timedelta(days=30)
        self.now = self.start
        
    def reset(self):
        self.now = self.start

    def getData(self):
        lines = []
        while self.end <= self.now:
            datas = readDaily(self.now.strftime('%m-%d-%Y'))
            self.now = self.now - timedelta(days=1)
            if len(datas) > 0:
                lines.append('name\tconfirmed\tdeaths\tdeathRatio\trecover\trecoverRatio\tactive\tactiveRatio')
                for name, data in datas.items():
                    ds = DaylyStatus(name,data['Confirmed'],data['Deaths'],data['Recovered'])
                    lines.append('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s' % (
                                            ds.cname,
                                            ds.confirmed,
                                            ds.deaths,
                                            ds.deathRatio(),
                                            ds.recover,
                                            ds.recoverRatio(),
                                            ds.active(),
                                            ds.activeRatio()
                                        ))
                break
        return '\n'.join(lines)
