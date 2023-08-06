from converterpy.util.logger import LogManager


class Converter(object):

    def __init__(self, name):
        self.name = name
        self.logger = LogManager.get_logger()

    def supported_conversions(self):
        raise NotImplementedError()

    def is_convertible(self, source_unit, target_unit):
        raise NotImplementedError()

    def convert(self, source_unit, source_value, target_unit):
        raise NotImplementedError()

    # ----

    def __repr__(self):
        return 'Converter{%s}' % self.name
