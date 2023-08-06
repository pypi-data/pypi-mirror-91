import datetime

from converterpy.converter import Converter
from converterpy.exception import ConversionNotSupportedException
from converterpy.unit import Unit

UNIT_TIMESTAMP = Unit('ts', 'timestamp')
UNIT_DATE = Unit('dt', 'date')


class TimestampToDateConverter(Converter):

    DATE_FORMAT = f"%Y-%m-%d %H:%M:%S"

    def __init__(self, timezone=None):
        super(TimestampToDateConverter, self).__init__('Timestamp to Date converter')

        self.timezone = timezone

    def supported_conversions(self):
        return {
            UNIT_TIMESTAMP: [UNIT_DATE]
        }

    def is_convertible(self, source_unit, target_unit):
        isinstance(source_unit, Unit)
        isinstance(target_unit, Unit)

        return source_unit == UNIT_TIMESTAMP and target_unit == UNIT_DATE

    def map_source_value(self, source_value):
        if isinstance(source_value, str):
            return int(source_value)

        return source_value

    def convert(self, source_unit, source_value, target_unit):
        assert isinstance(source_unit, Unit)
        assert isinstance(target_unit, Unit)

        if not self.is_convertible(source_unit, target_unit):
            raise ConversionNotSupportedException(self, source_unit, target_unit)

        # -----

        timestamp = self.map_source_value(source_value)
        date = datetime.datetime.fromtimestamp(timestamp, tz=self.timezone)
        return date.strftime(TimestampToDateConverter.DATE_FORMAT)
