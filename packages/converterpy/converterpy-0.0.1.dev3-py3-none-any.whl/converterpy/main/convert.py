import logging
import pathlib
import json
import sys

from converterpy.adapter import ConverterTextAdapter
from converterpy.converter import Converter
from converterpy.cli import Cli

from converterpy.exception import SuitableConverterNotFoundException, MultipleSuitableConverterException
from converterpy.provider.builtin import BuiltinConverterProvider
from converterpy.util.assertion import assert_list_is_instance
from converterpy.util.logger import LogManager, LEVEL_OUT
from converterpy.util.import__ import import_class


class Config(object):

    @staticmethod
    def from_file(path='/etc/converterpy.json'):
        logger = LogManager.get_logger()

        configs = None
        if pathlib.Path(path).exists():
            logger.debug("reading config file [%s]" % path)
            with open(path) as fd:
                content = fd.read()
                configs = json.loads(content)
        else:
            logger.warning("Config file not found [%s], using defaults" % path)

        return Config(configs)

    # ------

    def __init__(self, configs=None, use_built_in_provider=True):
        if configs is None:
            configs = list()

        assert isinstance(configs, list)
        assert_list_is_instance(configs, dict)

        self.provider_configs = configs
        self.use_built_in_provider = use_built_in_provider


class ConvertMain(object):

    def __init__(self, logger, config):
        self.config = config
        self.logger = logger

        self.converters = []
        self.init_providers(config.provider_configs)

        if config.use_built_in_provider:
            self.provide_converters(BuiltinConverterProvider())

    def init_providers(self, provider_configs):
        self.logger.debug("Found [%s] provider configs" % len(provider_configs))
        for cfg in provider_configs:
            clazz = import_class(**cfg)

            provider = clazz()
            self.provide_converters(provider)

    def provide_converters(self, provider):
        converters = provider.provide()

        assert_list_is_instance(converters, Converter)

        self.logger.debug("adding [%s] new converters [%s]" % (len(converters), converters))
        return self.add_converters(converters)

    def add_converters(self, converters):
        self.converters.extend([ConverterTextAdapter(converter) for converter in converters])

    def find_suitable_converters_to_convert(self, source_selector, target_selector):
        assert isinstance(source_selector, str)
        assert isinstance(target_selector, str)

        return [c for c in self.converters if c.is_convertible(source_selector, target_selector)]

    def find_converter(self, source_selector, target_selector):
        suitable_converters = self.find_suitable_converters_to_convert(source_selector, target_selector)

        if len(suitable_converters) == 0:
            raise SuitableConverterNotFoundException("Suitable converter not found for for source [%s] and target [%s] "
                                                     "selectors" % (source_selector, target_selector))
        elif len(suitable_converters) > 1:
            raise MultipleSuitableConverterException("More than one converter found found for source [%s] and target "
                                                     "[%s] selectors, found: [%s]" % (source_selector, target_selector,
                                                                                      suitable_converters))

        return suitable_converters[0]

    def convert(self, source_selector, source_value, target_selector):
        converter = self.find_converter(source_selector, target_selector)

        self.logger.debug('Converter [%s] is selected for conversion [%s] to [%s]' %
                          (converter.name, source_selector, target_selector))

        return converter.convert(source_selector, source_value, target_selector)


def main():
    args = sys.argv

    # be initializer of logger to set log_format
    logger_name = LogManager.DEFAULT_LOGGER_NAME
    logger = LogManager.create_logger(name=logger_name, level=LEVEL_OUT, log_format='%(message)s')

    cli = Cli(logger)
    args = cli.parse(args[1:])

    # ------

    if args.get('help', False):
        logger.out(cli.usage())
        exit(0)

    if args.get('verbose', False):
        LogManager.override_format(logger_name, LogManager.DEFAULT_LOG_FORMAT)
        LogManager.override_log_level(logger_name, logging.DEBUG)

    # ------

    source_value = args['value']
    source_selector = args['source']
    target_selector = args['target']

    # ------
    cfg = Config.from_file()
    result_value = ConvertMain(logger, cfg).convert(source_selector, source_value, target_selector)
    logger.out(result_value)


if __name__ == "__main__":
    main()
