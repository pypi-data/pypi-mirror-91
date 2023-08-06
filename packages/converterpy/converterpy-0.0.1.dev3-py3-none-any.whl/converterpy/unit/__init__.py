class Unit(object):

    def __init__(self, shortname, fullname):
        self._shortname = shortname
        self._fullname = fullname

    def shortname(self):
        return self._shortname

    def fullname(self):
        return self._fullname

    def __repr__(self):
        return 'Unit(%s, %s)' % (self.shortname(), self.fullname())