
import configparser, time, os, sys, getopt
from EnceladusParser import FileParser
from EnceladusConfig import Config

class Enceladus:

    def __init__(self):
        self.config = Config()

    def runEnceladus(self):
        print(self.config.configFile)
        print(self.config.working_dir)
        parser = FileParser(self.config)
        parser.parseFileStack()


    def main(self, *argv):
        try:
            opts, args = getopt.getopt(argv, "h:c:w:")
        except getopt.GetoptError as e:
            print('>>>> ERROR: %s' % str(e))
            sys.exit(2)
        for opt, arg in opts:
            if opt == '-h':
                print('Enceladus.py -h \nHelp Message')
                print('Enceladus.py -p <date>')
                print('Enceladus.py -c{config.file}')
                print('Enceladus.py -p date')
                print('Enceladus.py -w{working.dir}')
                sys.exit()
            elif opt in "-c":
                self.config.configFile = arg
            elif opt in "-w":
                self.config.working_dir = arg

        self.runEnceladus()


if __name__ == "__main__":
    enceladus = Enceladus()
    enceladus.main(*sys.argv[1:])
