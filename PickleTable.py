import pickle

def formatError():
    raise Exception("Invalid Format (Probably due to incorrect type)")

def indexError():
    raise Exception("Invalid Index (right type, but too big or too small)")

def getVersion():
    return {"Python":"3.6.1","PickleTable":"0.3"}

def rawSave(filename,data):
    outfile=open(filename,"w")
    outfile.close()
    outfile=open(filename,"rb+")
    outfile.truncate(0)
    outfile.seek(0,0)
    pickle.dump(data,outfile,4)
    outfile.close()

def rawLoad(filename):
    infile=open(filename,"rb+")
    data=pickle.load(infile)
    infile.close()
    return data

def goodType(obj):
    t=type(obj)
    if t==float:
        return True
    if t==int:
        return True
    if t==str:
        return True
    if t==bool:
        return True
    return False

def checkFilename(fn):
    if type(fn)!=str:
        formatError()
    x=fn.split(".")
    if x[-1]!="pickletable":
        raise Exception("This module can only handle files whose extension is .pickletable")

class table:
    def __init__(self):
        self.name=""
        self.readme=""
        self.width=int(-1)
        self.data=[]
    def setWidth(self,w):
        if len(self.data)!=0:
            raise Exception("You can't reset the width of a table that has data in it. Try clearing all the data first.")
        if type(w)!=int:
            formatError()
        self.width=w
    def addRow(self,row):
        if self.width<0:
            raise Exception("You tried writing to a table before specifying its width")
        if type(row)!=list:
            formatError()
        if len(row)!=self.width:
            raise Exception("You tried writing a row with a size that is diffeent from the table that you are writing to")
        r=[]
        for x in row:
            if goodType(x):
                r.append(x)
            else:
                formatError()
        self.data.append(r)
    def clearData(self):
        self.data=[]
    def writeOut(self):
        if type(self.name)!=str:
            formatError()
        if type(self.readme)!=str:
            formatError()
        if type(self.width)!=int:
            formatError()
        if type(self.data)!=list:
            formatError()
        ou=[self.name,self.readme,self.width,self.data]
        return ou
    def readIn(self,inp):
        if type(inp)!=list:
            formatError()
        if len(inp)!=4:
            formatError()
        if type(inp[0])!=str:
            formatError()
        if type(inp[1])!=str:
            formatError()
        if type(inp[2])!=int:
            formatError()
        if type(inp[3])!=list:
            formatError()
        self.name=inp[0]
        self.readme=inp[1]
        self.width=inp[2]
        self.data=inp[3]
    def __getitem__(self,item):
        return self.data[item]

class PickleTable:
    def __init__(self):
        self.name=""
        self.readme=""
        self.tabs=[]
    #internal
    def writeOut(self):
        if type(self.name)!=str:
            formatError()
        if type(self.readme)!=str:
            formatError()
        if type(self.tabs)!=list:
            formatError()
        h=[]
        for x in self.tabs:
            h.append(x.writeOut())
        ou=[self.name,self.readme,h]
        return ou
    def readIn(self,inp):
        if type(inp)!=list:
            formatError()
        if len(inp)!=3:
            formatError()
        if type(inp[0])!=str:
            formatError()
        if type(inp[1])!=str:
            formatError()
        if type(inp[2])!=list:
            formatError()
        self.name=inp[0]
        self.readme=inp[1]
        self.tabs=[]
        for x in inp[2]:
            b=table()
            b.readIn(x)
            self.tabs.append(b)
    #API
    #files
    def toFile(self,filename):
        checkFilename(filename)
        s=self.writeOut()
        rawSave(filename,s)
    def fromFile(self,filename):
        checkFilename(filename)
        s=rawLoad(filename)
        self.readIn(s)
    #general
    def clear(self):
        self.name=""
        self.readme=""
        self.tabs=[]
    def setName(self,name):
        if type(name)!=str:
            formatError()
        self.name=name
    def setReadme(self,readme):
        if type(readme)!=str:
            formatError()
        self.readme=readme
    def getName(self):
        return self.name
    def getReadme(self):
        return self.readme
    def getTableCount(self):
        return len(self.tabs)
    #table stuff
    def addTable(self):
        self.tabs.append(table())
    def setTableName(self,name):
        if type(name)!=str:
            formatError()
        if len(self.tabs)==0:
            self.addTable()
        self.tabs[-1].name=name
    def setTableReadme(self,readme):
        if type(readme)!=str:
            formatError()
        if len(self.tabs)==0:
            self.addTable()
        self.tabs[-1].readme=readme
    def setTableWidth(self,width):
        if len(self.tabs)==0:
            self.addTable()
        self.tabs[-1].setWidth(width)
    def getTableName(self,index):
        if type(index)!=int:
            formatError()
        if index<0:
            indexError()
        if index>=self.getTableCount():
            indexError()
        return self.tabs[index].name
    def getTableReadme(self,index):
        if type(index)!=int:
            formatError()
        if index<0:
            indexError()
        if index>=self.getTableCount():
            indexError()
        return self.tabs[index].readme
    def getTableWidth(self,index):
        if type(index)!=int:
            formatError()
        if index<0:
            indexError()
        if index>=self.getTableCount():
            indexError()
        return self.tabs[index].width
    def getTableRowCount(self,index):
        if type(index)!=int:
            formatError()
        if index<0:
            indexError()
        if index>=self.getTableCount():
            indexError()
        return len(self.tabs[index].data)
    #data stuff
    def add(self,row):
        if len(self.tabs)==0:
            raise Exception("You need to make a table before you can write to one")
        self.tabs[-1].addRow(row)
    def get(self,tindex,rnum):
        if type(tindex)!=int:
            formatError()
        if tindex<0:
            indexError()
        if tindex>=self.getTableCount():
            indexError()
        if type(rnum)!=int:
            formatError()
        if rnum<0:
            indexError()
        if rnum>=self.getTableRowCount(tindex):
            indexError()
        return self.tabs[tindex].data[rnum]
    #overloading
    def __getitem__(self,index):
        return self.tabs[index]
