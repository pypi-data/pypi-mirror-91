class Cli(object):

    def __init__(self, logger):
        self.logger = logger

    def usage(self):
        return """
usage: convert <value> <source> to <target> [optional arguments]

    optional arguments:
    -h, --help          show help message
    -v                  verbose mode
        """

    # convert 10 seconds to minutes
    def parse(self, params):
        orig_params = params
        params = list(params)
        self.logger.debug("args: [%s]" % params)

        args = dict()

        # parse options
        for param in orig_params:
            if param in ['-h', '--help']:
                args['help'] = True
                params.remove(param)
            elif param in ['-v', '--verbose']:
                args['verbose'] = True
                params.remove(param)
            elif param.startswith('-'):
                raise SyntaxError("Unexpected optional argument [%s]" % param)

        if len(params) == 0:
            args['help'] = True
        elif len(params) < 4:
            raise SyntaxError("Missing expression, see usage..")
        else:
            args['value'] = params[0]
            args['source'] = params[1]

            if params[2] != 'to':
                raise SyntaxError("Token error! Expected value: [to], found: [%s]" % params[2])

            args['target'] = params[3]

            self.logger.debug("CLI source_selector:%s source_value:%s target_value:%s"
                              % (args['source'], args['value'], args['target']))

        # ------

        self.validate(args)

        # ------

        return args

    def validate(self, parsed_args):
        if 'help' in parsed_args:
            return

        def _val(n):
            if n not in parsed_args:
                raise SyntaxError("Argument [%s] is missing" % n)

        _val('value')
        _val('source')
        _val('target')
