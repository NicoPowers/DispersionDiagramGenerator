import sys, xlrd, csv
import matplotlib.pyplot as plt
from PyQt4 import QtGui, QtCore
from matplotlib import rc


timesGenerated = 0

class Window(QtGui.QMainWindow):

    def __init__(self):

        super(Window, self).__init__()

        self.setGeometry(300, 300, 700, 500)
        self.setWindowTitle("Dispersion Diagram Generator V8")
        self.setWindowIcon(QtGui.QIcon('logo.png'))


        # Gamma to X button
        gammaToXbtn = QtGui.QPushButton("Gamma To X", self)
        gammaToXbtn.clicked.connect(self.file_open_gammaToX)
        gammaToXbtn.resize(gammaToXbtn.minimumSizeHint())
        gammaToXbtn.move(50,50)
        self.gammaToXData = None
        
        
        
        # X to M button
        xToMbtn = QtGui.QPushButton("X to M", self)
        xToMbtn.clicked.connect(self.file_open_xToM)
        xToMbtn.resize(xToMbtn.minimumSizeHint())
        xToMbtn.move(50,100)
        self.xToMData = None
        
        
        
        # M to Gamma button
        mToGammabtn = QtGui.QPushButton("M to Gamma", self)
        mToGammabtn.clicked.connect(self.file_open_mToGamma)
        mToGammabtn.resize(mToGammabtn.minimumSizeHint())
        mToGammabtn.move(50,150)
        self.mToGammaData = None
        

        # Generate Dispersion Diagram button
        generateBtn = QtGui.QPushButton("Generate Dispersion Diagram", self)
        generateBtn.clicked.connect(self.generate_dispersion_diagram)
        generateBtn.resize(200, 100)
        generateBtn.move(150,100)

        self.show()




    # store .csv data for gamma to x, x to m, m to gamma functions
    def file_open_gammaToX(self, btn):
        
        
        filePath = QtGui.QFileDialog.getOpenFileName(self, 'Open File', '*.csv')

        
        with open(filePath) as csvFile:
            dataArray = []
            data = csv.reader(csvFile)
            counter = 0
            for line in data:
                counter += 1
                dataArray.append(line)
        
        self.gammaToXData = dataArray
        
        

    def file_open_xToM(self, btn):

        
        filePath = QtGui.QFileDialog.getOpenFileName(self, 'Open File', '*.csv')

        
        with open(filePath) as csvFile:
            dataArray = []
            data = csv.reader(csvFile)
            for line in data:
                dataArray.append(line)
        self.xToMData = dataArray
        


    def file_open_mToGamma(self, btn):

        
        filePath = QtGui.QFileDialog.getOpenFileName(self, 'Open File', '*.csv')

 
        with open(filePath) as csvFile:
            dataArray = []
            data = csv.reader(csvFile)
            for line in data:
                dataArray.append(line)
        self.mToGammaData = dataArray
        



    # make sure dispersion diagram can be generated (checks to see if all 3 files have been uploaded
    def validate(self):

        passed = True

        if self.gammaToXData == None:
            QtGui.QMessageBox.critical(self, 'Error',"You must upload a file for Gamma to X.")
            passed = False

        if self.xToMData == None:
            QtGui.QMessageBox.critical(self, 'Error',"You must upload a file for X to M.")
            passed = False

        if self.mToGammaData == None:
            QtGui.QMessageBox.critical(self, 'Error',"You must upload a file for M to Gamma.")
            passed = False

        return passed
        
    def generate_dispersion_diagram(self):
        if self.validate() == True:
            self.numOfModes = len(self.gammaToXData[0]) - 1 # 'degree' cell unit will take up 1 spot for first file
            self.y = {}
            self.x = (len(self.gammaToXData)-1) + (len(self.xToMData)-1) + (len(self.mToGammaData)-1)
            self.XMark = (len(self.gammaToXData)-1)
            self.MMark = self.XMark + (len(self.xToMData)-1)

            for mode in range(1, self.numOfModes+1):
                series = "Mode {}".format(mode)
                self.y.update({series: []})
                
            self.extract_gammaToX()
            self.extract_xToM()
            self.extract_mToGamma()

            global timesGenerated
            timesGenerated += 1
            plt.figure(num="Dispersion Diagram {}".format(str(timesGenerated))) 
                
            for mode in range(1, self.numOfModes+1):
                series = "Mode {}".format(mode)
                plt.plot(list(range(self.x)), self.y[series], label=series)

            plt.axis([0, self.x-1, 0, None])

            xTicks = [0, self.XMark, self.MMark, self.x-1]
            xSymbolTicks = [r'$\Gamma$', 'X', 'M', r'$\Gamma$']
            plt.xticks(xTicks, xSymbolTicks)
            
            plt.ylabel('Frequency (GHz)')
            
            plt.axvline(x=self.XMark, linestyle='--', color= 'black')
            plt.axvline(x=self.MMark, linestyle='--', color='black')
            plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,ncol=3, mode="expand", borderaxespad=0.)

            plt.show()
            
    def extract_gammaToX(self):
        
            for mode in range(1, self.numOfModes+1):
                series = "Mode {}".format(mode)
                for row in range(1, len(self.gammaToXData)):
                    self.y[series].append(float(self.gammaToXData[row][mode])/1e9)
                  

    def extract_xToM(self):
    
            for mode in range(1, self.numOfModes+1):
                series = "Mode {}".format(mode)
                for row in range(1, len(self.xToMData)):
                    self.y[series].append(float(self.xToMData[row][(len(self.xToMData)-1)*mode])/1e9)
                    

    def extract_mToGamma(self):
            for mode in range(1, self.numOfModes+1):
                series = "Mode {}".format(mode)
                counter = 0
                for row in range(len(self.mToGammaData)-1, 0, -1):
                    self.y[series].append(float(self.mToGammaData[row][((len(self.mToGammaData)-1)*mode)-counter])/1e9)
                    counter += 1


def main():
    app = QtGui.QApplication(sys.argv)
    GUI = Window()
    sys.exit(app.exec_())


main()     
