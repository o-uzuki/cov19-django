from cov19diff.populations import populations

class ResultType:
    def __init__(self,cname,oldcount,newcount):
        self.cname = cname
        self.oldcount = int(oldcount)
        self.newcount = int(newcount)
        self.pcent = '%(pc)3.1f' % {'pc': (self.newcount-self.oldcount)/self.oldcount*100}
        if self.cname in populations:
            self.population = '%(pd)5.1f' % {'pd': populations[self.cname]/self.newcount}

class DaylyStatus:
    def __init__(self,cname,confirmed,deaths,recover):
        self.cname = cname
        self.confirmed = confirmed
        self.deaths = deaths
        self.recover = recover

    def active(self):
        return self.confirmed - self.deaths - self.recover

    def deathRatio(self):
        return '%2.1f' % ((self.deaths/self.confirmed) * 100)

    def recoverRatio(self):
        return '%2.1f' % ((self.recover/self.confirmed) * 100)

    def activeRatio(self):
        return '%2.1f' % ((self.active()/self.confirmed) * 100)
