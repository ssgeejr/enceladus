import csv, time, sys, getopt, glob, os, datetime
import mysql.connector, configparser, hashlib
from mysql.connector import connect, Error
from pathlib import Path
from EnceladusConfig import Config
from DenialRecord import Record


class FileParser:
    claimID = None

    def __init__(self, global_cfg):
        self.config = global_cfg
        print(self.config.configFile)
        print(self.config.working_dir)
        print(self.config.dryrun)


        print('**********************************************************')
        print('Configuration File: ', self.config.configFile)
        config_source = os.path.join(self.config.cdir, self.config.configFile)
        print('Configuration Source: ', config_source)
        credentials = configparser.ConfigParser()
        credentials.read(config_source)

        print('**********************************************************')

        self.cnx = mysql.connector.connect(user=credentials['enceladus']['user'],
              password=credentials['enceladus']['passwd'],
              host=credentials['enceladus']['host'],
              database=credentials['enceladus']['db'])
        print(f"Connection to database successful [{self.cnx.is_connected()}]")
        self.mycursor = self.cnx.cursor()




    def parseFileStack(self):
        st = time.time()
        print(f'Switching to working directory: {self.config.working_dir}')
        os.chdir(self.config.working_dir)
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

        denailsql = ("insert into denials"
                + " (groupname,filedate,grandtotal,filename)"
                + " values(%s,STR_TO_DATE(%s, '%Y%m%d'),%s,%s)")
        adjustmentsql = ("insert into adjustments"
                + " (denialid,claimid,keytype,amount)"
                + " values(%s,%s,%s,%s)")

        for file in glob.glob("*.835"):
            fileCount += 1

            old_file = os.path.join(self.config.working_dir, file)
            new_file = os.path.join(self.config.working_dir, file + '.loaded')
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
                            if float(adj[0]) > 0:
                                adjustments['271'] = adj[0]
                                record.addAdjustment(f'271*{self.claimID}', adj[0])
#                            else:
#                                print(f'skipping negative/non-positive value: {adj[0]}')
                        elif line.startswith("SVC*NU>0272") and self.claimID:
                            adj = line[12:].split('*')
                            #print(line)
                            #print(f'272 {adj[0]}')
                            if float(adj[0]) > 0:
                                adjustments['272'] = adj[0]
                                record.addAdjustment(f'272*{self.claimID}', adj[0])
 #                           else:
 #                               print(f'skipping negative/non-positive value: {adj[0]}')
                        elif line.startswith("SVC*NU>0278") and self.claimID:
                            adj = line[12:].split('*')
                            #print(line)
                            #print(f'278 {adj[0]}')
                            if float(adj[0]) > 0:
                                adjustments['278'] = adj[0]
                                record.addAdjustment(f'278*{self.claimID}',adj[0])
#                            else:
#                                print(f'skipping negative/non-positive value: {adj[0]}')
                        elif line.startswith('CAS*CO*16') and self.claimID:
                            casco = True
                        elif line.startswith('LQ*HE*M51') and self.claimID:
                            lqhe = True
                        elif line.startswith('CAS*CO*22') and self.claimID:
                            print('****FOUND CAS*CO*22 *****')
                            self.claimID = None
                            adjustments = {}
                            total = 0.0
                            casco = False
                            lqhe = False

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

                        #print('>>>>>>>>>>>>>>>>>', record.filename)
                        #print('>>>>>>>>>>>>>>>>>', record.filedate)
                        #print('>>>>>>>>>>>>>>>>>', record.groupname)
                        #print('>>>>>>>>>>>>>>>>>', record.grandtotal)
                        #print('>>>>>>>>>>>>>>>>>', record.adjustments)

                        if not self.config.dryrun:
                            values = (record.groupname,record.filedate,record.grandtotal,record.filename)
                            self.mycursor.execute(denailsql, values)
                            rowid = self.mycursor.lastrowid
                            #print(rowid)

                            for key, value in record.adjustments.items():
                                items = key.split('*')
                                #print(f'Type: {items[0]} claimID {items[1]} amount {value}')

                                avalues = (rowid,items[1],items[0],value)
                                self.mycursor.execute(adjustmentsql, avalues)
                            self.cnx.commit()
                        else:
                            print('********* DRY RUN ENABLED -- DATA NOT STORED IN DB *********')

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
