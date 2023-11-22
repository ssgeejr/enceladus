import csv, time, sys, getopt, glob, os, datetime
import mysql.connector, configparser, hashlib
from mysql.connector import connect, Error
from pathlib import Path
from EnceladusConfig import Config
from DenialRecord import Record


class FileParser:
    claimID = None
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
        batchTotal = 0.0
        fileCount = 0
        filedate = None
        adjustments = {}
        grandtotal = 0.0
        total = 0.0
        casco = False
        lqhe = False

        groupname = None
        for file in glob.glob("*.835"):
            fileCount += 1

            old_file = os.path.join(self.working_dir, file)
            new_file = os.path.join(self.working_dir, file + '.loaded')
            with open(file, mode='r') as rofile:
                record = None
                count = 0



                try:
                    for line in rofile:
                        if line.startswith('GS*HP*'):
                            gshp = line[6:].split('*',3)
                            groupname = gshp[0]
                            filedate = gshp[2]
                            #print(f'File {file}')
                            #print(f'Group: {groupname}')
                            #print(f'Date: {filedate}')
                            record = Record(file,filedate,groupname)

                        elif line.startswith('CLP*'):
                            if self.claimID \
                                    and len(adjustments) > 0 \
                                    and casco\
                                    and lqhe:
                                #print('Claim ID: ', self.claimID)

                                for key, value in adjustments.items():
                                    fadj = float(value)
                                    #print(f"   Key: {key} Adjustment:  ${fadj:,.2f}")
                                    total += fadj

                                #print(f"   Total Adjustment: ${total:,.2f}")
                            self.claimID = None
                            adjustments = {}
                            grandtotal += total
                            record.setGrandTotal(grandtotal)
                            total = 0.0
                            casco = False
                            lqhe = False

                            tokens = line.split('*',2)
                            self.claimID = tokens[1]
                            #print(claimID)
#                            for key in tokens:
#                                print (key)
                        elif line.startswith("SVC*NU>0271") and self.claimID:
                            adj = line[12:].split('*')
                            #print(line)
                            #print(f'271 {adj[0]}')
                            adjustments['271'] = adj[0]
                            record.addAdjustment(f'271*{self.claimID}', adj[0])
                        elif line.startswith("SVC*NU>0272") and self.claimID:
                            adj = line[12:].split('*')
                            #print(line)
                            #print(f'272 {adj[0]}')
                            adjustments['272'] = adj[0]
                            record.addAdjustment(f'272*{self.claimID}', adj[0])
                        elif line.startswith("SVC*NU>0278") and self.claimID:
                            adj = line[12:].split('*')
                            #print(line)
                            #print(f'278 {adj[0]}')
                            adjustments['278'] = adj[0]
                            record.addAdjustment(f'278*{self.claimID}',adj[0])
                        elif line.startswith('CAS*CO*16') and self.claimID:
                            casco = True
                        elif line.startswith('LQ*HE*M51') and self.claimID:
                            lqhe = True

                    groupname = None
                    filedate = None

                    if self.claimID \
                            and len(adjustments) > 0 \
                            and casco \
                            and lqhe:
                        # print('Claim ID: ', self.claimID)

                        for key, value in adjustments.items():
                            fadj = float(value)
                            # print(f"   Key: {key} Adjustment:  ${fadj:,.2f}")
                            total += fadj

                        # print(f"   Total Adjustment: ${total:,.2f}")
                    self.claimID = None
                    adjustments = {}
                    grandtotal += total
                    record.setGrandTotal(grandtotal)
                    total = 0.0
                    casco = False
                    lqhe = False

                        # print(f"   Total Adjustment: ${total:,.2f}")
                    self.claimID = None
                    adjustments = {}
                    grandtotal += total
                    record.setGrandTotal(grandtotal)

                    if grandtotal > 0:
                        print(f">>> Grand Total Adjustment: ${grandtotal:,.2f}")
                        record.setGrandTotal(grandtotal)
                        print('______________________________________________________________')
                        batchTotal += grandtotal

                        print('>>>>>>>>>>>>>>>>>', record.filename)
                        print('>>>>>>>>>>>>>>>>>', record.filedate)
                        print('>>>>>>>>>>>>>>>>>', record.groupname)
                        print('>>>>>>>>>>>>>>>>>', record.grandtotal)
                        print('>>>>>>>>>>>>>>>>>', record.adjustments)

                    grandtotal = 0.0


                except Error as e:
                    print('Error at line: ', count)
                    print(e)
        et = time.time()
        elapsed_time = et - st
        print(f"####  BATCH TOTAL: ${batchTotal:,.2f} ####")
        print(f'Parsed [{fileCount}] in [{elapsed_time}] seconds')

#INSERT INTO custorder
# VALUES ('Kevin', 'yes' , STR_TO_DATE('1-01-2012', '%d-%m-%Y') ) ;