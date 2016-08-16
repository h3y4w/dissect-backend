import subprocess
import os
from SMByteConvert import ByteConvert

class FileHandler (object):
    FILE = None

    def __init__(self, FILE):
        self.FILE=FILE

    def process(self):

        self.findSplitSize()
        fileName = self.FILE['id']
        if self.FILE['compress']=='SM-7Z':
            fileName = self.FILE['id'] + '.7z'
            compress_7z_command = ['7z', 'a', fileName, self.FILE['id']]
            subprocess.check_call(compress_7z_command)

        splitName= fileName+'.'
        sizeandunit = str(self.FILE['split']['gcd']) + self.FILE['split']['unit']
        split_command = ['split', '--bytes', sizeandunit, '-d', '-a', '3', fileName, splitName]
        subprocess.check_call(split_command)

    def findSplitSize(self):
        self.FILE['size']=os.path.getsize(self.FILE['id'])
            # CLEANS THIS UP
        self.FILE['size']
        p=[]
        accountPercentage = [.30,.50,.20]
        for percent in accountPercentage:
            p.append(int(percent*self.FILE['size']))

        SMBC = ByteConvert(p)
        self.FILE['split']= SMBC.getBestUnit()
        print 'numbers=' + str(self.FILE['split']['numbers'])
        print 'gcd=' + str(self.FILE['split']['gcd'])
        for a in self.FILE['split']['numbers']:
            print str(a) + self.FILE['split']['unit'] +  ' that have ' + str(a/self.FILE['split']['gcd']) + ' files'

    def smartSplit(self):

        # calls a function in FileMovementHandler.py or some shit
        # basiclly calls a function to check the remaining space in each account
        #returns a dict.  The key is the account id, the value is the space following unit
        #FUCK MTY LIFE
        storage={34:'12g', 23:'12m',56:'2g'}

        #it will convert the all numbers into bytes



#test = SMFileHandler()
#FILE = {'compress':'SM-7Z', 'id':'test.mov','ratio':'3', 'unit':'m', 'size':31.9}
#test.setFile(FILE)
#test.File()
