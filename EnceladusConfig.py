from dataclasses import dataclass
import os, configparser, time

@dataclass
class Config:
    userDefinedKey: bool = False
    configFile: str = 'db.ini'
    working_dir: str = '/opt/apps/denials'
    cdir: str = os.path.dirname(os.path.abspath(__file__))
