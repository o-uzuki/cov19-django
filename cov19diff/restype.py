from cov19diff.populations import populations
import json
from json import JSONEncoder

class ResultType:
    def __init__(self,cname,oldcount,newcount):
        self.cname = cname
        self.oldcount = int(oldcount)
        self.newcount = int(newcount)
        self.diff = self.newcount-self.oldcount
        self.fpcent = self.diff/self.oldcount*100
        self.pcent = '%(pc)3.1f' % {'pc': self.diff/self.oldcount*100}
        if self.cname in populations:
            self.population = '%(pd)5.1f' % {'pd': populations[self.cname]/self.newcount}


class ResultTypeEncoder(JSONEncoder):
    def default(self,o):
        if isinstance(o,ResultType):
            return o.__dict__
        return json.JSONEncoder.default(self, o)

class DaylyStatus:
    def __init__(self,cname,confirmed,deaths,recover):
        self.cname = cname
        self.confirmed = confirmed
        self.deaths = deaths
        self.recover = recover
        self.day = ''
        self.nActive = self.active()
        self.dRatio = self.deathRatio()
        self.rRatio = self.recoverRatio()
        self.aRatio = self.activeRatio()

    def active(self):
        return self.confirmed - self.deaths - self.recover

    def deathRatio(self):
        return '%2.1f' % ((self.deaths/self.confirmed) * 100)

    def recoverRatio(self):
        return '%2.1f' % ((self.recover/self.confirmed) * 100)

    def activeRatio(self):
        return '%2.1f' % ((self.active()/self.confirmed) * 100)

    def setdiff(self, old):
        self.dConfirmed = self.confirmed - old.confirmed
        self.dDeaths = self.deaths - old.deaths
        self.dRecover = self.recover - old.recover
        self.dActive = self.active() - old.active()
        return self

class DaylyStatusEncoder(JSONEncoder):
    def default(self,o):
        if isinstance(o,DaylyStatus):
            return o.__dict__
        return json.JSONEncoder.default(self, o)
