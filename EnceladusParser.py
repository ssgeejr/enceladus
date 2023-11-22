import csv, time, sys, getopt, glob, os, datetime
import mysql.connector, configparser, hashlib
from mysql.connector import connect, Error
from pathlib import Path
from EnceladusConfig import Config


class FileParser:

    def __init__(self, config: Config):
        self.config = configparser.ConfigParser()
        #Shared Configuration Settings
        self.userDefinedKey = config.userDefinedKey
        self.configFile = config.configFile
        self.cdir = config.cdir
        self.working_dir = config.working_dir

    def parseFileStack(self):
        st = time.time()
        print(f'Switching to working directory: {self.working_dir}')
        os.chdir(self.working_dir)
        loadfile_list = []
        for file in glob.glob("*.835"):
            print('***** LOADING DATA FILE ', file, ' *****')
            old_file = os.path.join(self.working_dir, file)
            new_file = os.path.join(self.working_dir, file + '.loaded')
            with open(file, mode='r') as rofile:
                count = 0

                try:
                    claimID = None
                    adjustments = {}
                    grandtotal = 0.0
                    header = None
                    """
                    GS Functional Group Header
                    GS01 Functional Identifier Code ‘HP’ Health Care Claim
                    Payment/Advice (835)
                    """
                    for line in rofile:
                        if line.startswith('GS*HP*'):
                            gshp = line[6:].split('*',2)
                            print(f'Group: {gshp[1]}')
                            group = None
                        elif line.startswith('CLP*'):
                            if claimID and len(adjustments) > 0:
                                print('Claim ID: ', claimID)
                                total = 0.0

                                for key, value in adjustments.items():
                                    fadj = float(value)
                                    print(f"   Key: {key} Adjustment:  ${fadj:,.2f}")
                                    total += fadj

                                print(f"   Total Adjustment: ${total:,.2f}")
                                claimID = None
                                adjustments = {}
                                grandtotal += total
                                total = 0.0
                                header = None


                            tokens = line.split('*',2)
                            claimID = tokens[1]
                            #print(claimID)
#                            for key in tokens:
#                                print (key)
                        elif line.startswith('SVC*NU>0271') and claimID:
                            adj = line[12:].split('*')
                            adjustments['271'] = adj[0]

                        elif line.startswith('SVC*NU>0272') and claimID:
                            adj = line[12:].split('*')
                            adjustments['272'] = adj[0]

                        elif line.startswith('SVC*NU>0278') and claimID:
                            adj = line[12:].split('*')
                            adjustments['278'] = adj[0]

                    print(f"Grand Total Adjustment: ${grandtotal:,.2f}")
                    print('______________________________________________________________')
                    grandtotal = 0.0
                except Error as e:
                    print('Error at line: ', count)
                    print(e)

        et = time.time()
        elapsed_time = et - st
        print('Execution time:', elapsed_time, 'seconds')