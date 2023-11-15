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

