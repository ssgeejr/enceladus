
class Record:


    filename = None
    filedate = None
    groupname = None
    grandtotal = 0.0
    adjustments = {}


    def __init__(self, filename, filedate, groupname):
        self.filename = filename
        self.filedate = filedate
        self.groupname = groupname

    def addAdjustment(self, key, value):
        self.adjustments[key] = value
    def setGrandTotal(self, gt):
        self.grandtotal = gt
