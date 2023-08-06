class ConversionNotSupportedException(Exception):

    def __init__(self, converter, source, target):
        super(ConversionNotSupportedException, self).__init__('Converter [%s] does not support conversion from [%s] to'
                                                              ' [%s]' % (converter.name, source, target))


class UnexpectedResultException(Exception):
    pass


class SuitableConverterNotFoundException(Exception):
    pass


class MultipleSuitableConverterException(Exception):
    pass


class LoggerNotFoundException(Exception):

    def __init__(self, name):
        super(LoggerNotFoundException, self).__init__('Logger [%s] not found or not created with LogManager' % name)


class SuitableDateFormatNotFoundException(Exception):

    def __init__(self, date_str):
        super(SuitableDateFormatNotFoundException, self).__init__('Suitable date format not found for [%s]' % date_str)
