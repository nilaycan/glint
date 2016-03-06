import argparse
import os
import sys
from configuration import configurelogging
configurelogging.configureLogging('') #todo should seperate each module to a different folder to have different "namespaces"?
import logging
from numpy import genfromtxt ,loadtxt
from utils import GlintArgumentParser
from parsers import ModuleParser, RefactorParser, EWASParser, MethylationDataParser  #dont remove this is imported in,,,


class GlintParser(ModuleParser):
    def __init__(self, parser):
        optional = parser.add_argument_group('3.Optional arguments')
        optional.add_argument('-h', '--help', action='help', help = "print this help") # add help here so it will be under same group with all other optional argument
        optional.add_argument('--out', type = str,  default = "",   help = "changes the prefix of the output file ")

        modules = parser.add_argument_group('4.Glint modules')
        modules.add_argument('--refactor', action='store_true', help = "<todo add help here>")
        modules.add_argument('--ewas',     action='store_true', help = "<todo add help here>" )

        super(GlintParser, self).__init__(optional, modules)
    

class ModulesArgumentParsers(object):
    MODULES_PARSERS = [ 
                        'MethylationDataParser',
                        'GlintParser'
                        'RefactorParser',
                        'EWASParser'
                      ]
        
    def __init__(self, user_args_selection):
        self.selected_args = user_args_selection
        self.parser = GlintArgumentParser(prog=os.path.basename(sys.argv[0]),
                             description = "<<todo add help before >>",
                             epilog = "<< todo add help after >>",
                             add_help=False) # don't add help because it is added in 'optional group'

        self.glint = None
        self.methylation = None
        self.refactor = None
        self.ewas = None
        self.args = None

    def add_arguments(self):
        # Notice to add arguments by the order you want them to be printed in --help

        #main
        self.methylation = MethylationDataParser(self.parser)
        self.glint = GlintParser(self.parser)

        #modules
        self.refactor = RefactorParser(self.parser)
        self.ewas = EWASParser(self.parser)

    def parse_args(self):
        logging.info("Validating arguments...")
        self.args = self.parser.parse_args()

        optional_args = []

        self.methylation.validate_args(self.args)
        optional_args.extend(self.methylation.all_args)

        self.glint.validate_args(self.args)
        optional_args.extend(self.glint.all_args)
        
        if self.args.refactor:
            self.refactor.validate_args(self.args)
            optional_args.extend(self.refactor.all_args)
        if self.args.ewas:
            self.ewas.validate_args(self.args)
            optional_args.extend(self.ewas.all_args)

        self.check_selected_args(optional_args)
        return self.args


    def check_selected_args(self, optional_args):
        # validate that the user didnt select an argument that is not an option
        differ = set(self.selected_args).difference(set(optional_args))
        if differ:
            logging.error("selected redundent argument" + str(differ))


    def run(self):
        meth_data = self.methylation.init_data(self.args)
        output_file_prefix = self.args.out

        if self.args.refactor:
            refactor_meth_data = meth_data.copy()
            estimates = self.refactor.run(self.args, refactor_meth_data, output_file_prefix)

        if self.args.ewas:
            self.ewas.run(estimates)

if __name__ == '__main__':
    selected_args = [arg for arg in sys.argv if arg.startswith("-")] #TODO startwith "--"? (there are no arguments that starts with -)
    
    parser = ModulesArgumentParsers(selected_args)

    parser.add_arguments()
    parser.parse_args()
    logging.info("Starting glint...")
    parser.run()




