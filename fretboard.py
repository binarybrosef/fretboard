from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsSimpleTextItem, QPushButton
from PyQt5.QtGui import QBrush, QPen
from PyQt5.QtCore import Qt
from scales import *


# Display settings
windowWidth = 909                                   # main window width
windowHeight = 352                                  # main window height
comboX = 4                                          # combobox x-coord
comboY = 16                                         # combobox y-coord
comboWidth = 430                                    # combobox width
comboHeight = 41                                    # combobox height                
bridgeX = -462                                      # x-coord of bridge 
fret12X = 402                                       # x-coord of fret 12
string1Y = -241                                     # y-coord of string 1 (i.e., high-E string in standard tuning)
string6Y = -71                                      # y-coord of string 6 (i.e., low-E string in standard tuning)
fretNum = 12                                        # number of frets
fretSize = (abs(bridgeX) + fret12X) / fretNum       # size of each fret. Frets are of same size in current implementation.
stringNum = 6
stringSize = (abs(abs(string1Y) -                   # spacing between adjacent strings
              abs(string6Y))) / (stringNum - 1)             
noteSize = 20                                       # height/width of notes to be rendered in fretboard


# Fretboard data structures

# Dictionary listing, for every position on the fretboard (every string/fret combo),
# the corresponding note. This dictionary omits open strings (1,0), (2,0), etc.
fretboard = {(1,1): 6, (1,2): 7, (1,3): 8, (1,4): 9, (1,5): 10, (1,6): 11,\
     (1,7): 12, (1,8): 1, (1,9): 2, (1,10): 3, (1,11): 4, (1,12): 5,\
     (2,1): 1, (2,2): 2, (2,3): 3, (2,4): 4, (2,5): 5, (2,6): 6,\
     (2,7): 7, (2,8): 8, (2,9): 9, (2,10): 10, (2,11): 11, (2,12): 12,\
     (3,1): 9, (3,2): 10, (3,3): 11, (3,4): 12, (3,5): 1, (3,6): 2,\
     (3,7): 3, (3,8): 4, (3,9): 5, (3,10): 6, (3,11): 7, (3,12): 8,\
     (4,1): 4, (4,2): 5, (4,3): 6, (4,4): 7, (4,5): 8, (4,6): 9,\
     (4,7): 10, (4,8): 11, (4,9): 12, (4,10): 1, (4,11): 2, (4,12): 3,\
     (5,1): 11, (5,2): 12, (5,3): 1, (5,4): 2, (5,5): 3, (5,6): 4,\
     (5,7): 5, (5,8): 6, (5,9): 7, (5,10): 8, (5,11): 9, (5,12): 10,\
     (6,1): 6, (6,2): 7, (6,3): 8, (6,4): 9, (6,5): 10, (6,6): 11,\
     (6,7): 12, (6,8): 1, (6,9): 2, (6,10): 3, (6,11): 4, (6,12): 5}

# We import scales.py, which includes scaleDict, which is a dict containing all scale families, 
# their modes, and their intervals represented in terms of half steps.

#scaleDict[key][0] = scale family intervals (tuple)
#scaleDict[key][1] = scale family name (list containing one string)
#scaleDict[key][2] = list of scale family modes (list of strings)

# Dictionary mapping letter notes to number representations.
noteToNumber = {'C': 1, 'Db': 2, 'D': 3, 'Eb': 4, 'E': 5,'F': 6, 'Gb': 7\
        ,'G': 8, 'Ab': 9, 'A': 10, 'Bb': 11, 'B': 12}

# Dictionary mapping number representations notes to intervals.
numberToInterval = {1: 'R', 2: 'b2', 3: '2', 4: 'm3', 5: 'M3', 6: '4', 7: 'b5/#11'\
        ,8: '5', 9: 'm6', 10: 'M6', 11: 'm7', 12: 'M7'}

# Dictionary mapping number representations of notes to letters.
numberToNote = {1:'C', 2:'Db', 3:'D', 4:'Eb', 5:'E', 6:'F', 7:'Gb'\
        ,8:'G', 9:'Ab', 10:'A', 11:'Bb', 12:'B'}


# Define main window class
class Ui_MainWindow(object):
     
    # Qt main window setup
    def setupUi(self, MainWindow):
        MainWindow.setObjectName('MainWindow')
        MainWindow.resize(windowWidth, windowHeight)

        self.renderUI()                                 # render UI elements (e.g., comboboxes, note buttons, interval labels)
        self.retranslateUi()                            # set UI element items/label text
        self.UiInteraction()                            # handle user interactions with UI
        self.renderGraphicsScene()                      # render QGraphicsScene
        self.renderFretboard()                          # render fretboard
        self.coordDict = self.getNoteCoords(fretNum,    # get dictionary of all coordinates where notes can be rendered
            stringNum, bridgeX, fretSize, noteSize, string1Y, stringSize)

        
    # Render UI elements (buttons, comboboxes, labels) not including QGraphicsView
    def renderUI(self):
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        MainWindow.setCentralWidget(self.centralwidget)
        
        # Establish horizontal layout for key, family, mode comboboxes
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(comboX,comboY,comboWidth,comboHeight))

        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)

        # Add key, family, mode comboboxes
        self.comboKey = QtWidgets.QComboBox(self.horizontalLayoutWidget)
        self.comboFamily = QtWidgets.QComboBox(self.horizontalLayoutWidget)
        self.comboMode = QtWidgets.QComboBox(self.horizontalLayoutWidget)

        self.horizontalLayout.addWidget(self.comboKey)
        self.horizontalLayout.addWidget(self.comboFamily)
        self.horizontalLayout.addWidget(self.comboMode)

        # Add key, family, mode combobox labels
        self.labelKey = QtWidgets.QLabel(self.centralwidget)
        self.labelKey.setGeometry(QtCore.QRect(4, 0, 47, 31))

        self.labelFamily = QtWidgets.QLabel(self.centralwidget)
        self.labelFamily.setGeometry(QtCore.QRect(128, 0, 47, 31))        

        self.labelMode = QtWidgets.QLabel(self.centralwidget)
        self.labelMode.setGeometry(QtCore.QRect(316, 0, 47, 31))

        # Add individual note buttons
        self.buttonC = QtWidgets.QPushButton(self.centralwidget)
        self.buttonDb = QtWidgets.QPushButton(self.centralwidget)
        self.buttonD = QtWidgets.QPushButton(self.centralwidget)
        self.buttonEb = QtWidgets.QPushButton(self.centralwidget)
        self.buttonE = QtWidgets.QPushButton(self.centralwidget)
        self.buttonF = QtWidgets.QPushButton(self.centralwidget)
        self.buttonGb = QtWidgets.QPushButton(self.centralwidget)
        self.buttonG = QtWidgets.QPushButton(self.centralwidget)
        self.buttonAb = QtWidgets.QPushButton(self.centralwidget)
        self.buttonA = QtWidgets.QPushButton(self.centralwidget)
        self.buttonBb = QtWidgets.QPushButton(self.centralwidget)
        self.buttonB = QtWidgets.QPushButton(self.centralwidget)

        self.scaleButtons = {'C': self.buttonC, 'Db': self.buttonDb, 'D': self.buttonD, 
                        'Eb': self.buttonEb, 'E': self.buttonE, 'F': self.buttonF,
                        'Gb': self.buttonGb, 'G': self.buttonG, 'Ab': self.buttonAb,
                        'A': self.buttonA, 'Bb': self.buttonBb, 'B': self.buttonB}
        
        # Distribute note buttons horizontally
        i = 0
        for key, button in self.scaleButtons.items():
            button.setText(key)
            button.move(4 + i * 75, 300)
            i += 1

        # Init note button labels - labels are filled upon user interaction with
        # key or mode comboboxes in renderNotes().
        self.labelC = QtWidgets.QLabel(self.centralwidget)
        self.labelDb = QtWidgets.QLabel(self.centralwidget)
        self.labelD = QtWidgets.QLabel(self.centralwidget)
        self.labelEb = QtWidgets.QLabel(self.centralwidget)
        self.labelE = QtWidgets.QLabel(self.centralwidget)
        self.labelF = QtWidgets.QLabel(self.centralwidget)
        self.labelGb = QtWidgets.QLabel(self.centralwidget)
        self.labelG = QtWidgets.QLabel(self.centralwidget)
        self.labelAb = QtWidgets.QLabel(self.centralwidget)
        self.labelA = QtWidgets.QLabel(self.centralwidget)
        self.labelBb = QtWidgets.QLabel(self.centralwidget)
        self.labelB = QtWidgets.QLabel(self.centralwidget)

        self.scaleLabels = {'C': self.labelC, 'Db': self.labelDb, 'D': self.labelD, 
                        'Eb': self.labelEb, 'E': self.labelE, 'F': self.labelF,
                        'Gb': self.labelGb, 'G': self.labelG, 'Ab': self.labelAb,
                        'A': self.labelA, 'Bb': self.labelBb, 'B': self.labelB}
        

    # Render QGraphicsView. renderFretboard() renders the actual graphical content
    # (frets, strings, notes) displayed in the QGraphicsView.
    def renderGraphicsScene(self):
        self.scene = QGraphicsScene()
        self.graphicsView = QGraphicsView(self.scene, MainWindow)
        self.graphicsView.setGeometry(QtCore.QRect(4,75,901,214))


    # Set GUI element (buttons, comboboxes) labels/item labels
    def retranslateUi(self):

        _translate = QtCore.QCoreApplication.translate

        # Set window title
        MainWindow.setWindowTitle(_translate("MainWindow", "Fretboard"))

        # Set key, family, mode labels
        self.labelKey.setText(_translate("MainWindow", "Key"))
        self.labelFamily.setText(_translate("MainWindow", "Family"))
        self.labelMode.setText(_translate("MainWindow", "Mode"))
        
        # Add blank entries to key combobox
        for i in range(0, len(noteToNumber.keys())+1):
            self.comboKey.addItem('')

        # Add blank entries to family combobox
        i = 1
        for i in range(0, len(scaleDict.keys())+1):
            self.comboFamily.addItem('')

        # Set key combobox item labels with the keys of noteToNumber dict
        i = 1
        for key in noteToNumber.keys():
            self.comboKey.setItemText(i, _translate('MainWindow', key))
            i += 1

        # Set family combobox items with the keys of scaleDict dict
        i = 1
        for family in scaleDict.keys():
            self.comboFamily.setItemText(i, _translate('MainWindow', scaleDict[family][1][0]))
            i += 1

        # The addition of blank entries and setting of item labels for mode combobox is 
        # handled below in populateModes(), which is called in UiInteraction().


    # When a selection in family combobox is made, map the item label to a corresponding
    # key in scaleDict so that the scaleDict key can be accessed for values therein.
    def getFamily(self):
        family = self.comboFamily.currentText()

        for fam in scaleDict.keys():
            familyName = scaleDict[fam][1][0]
            comparison = family == familyName

            if comparison == True:
                family = fam

        return family


    # Set mode combobox item labels upon user selection of family in family combobox.
    def populateModes(self):

        # Clear modes combobox. Otherwise every family selection will add to the 
        # already existing entries in mode combobox.
        self.comboMode.clear()

        # Only populate modes combobox if index of selected item in family combobox 
        # >= 1. Otherwise, the modes combobox cannot be populated if the family is 
        # not yet selected.
        if self.comboFamily.currentIndex() >= 1:
            family = self.getFamily()            

            # For each mode in the selected family, add blank entries to mode combobox, 
            # and then fill the blank entries with all the modes for the selected family.
            _translate = QtCore.QCoreApplication.translate

            for i in range(0, len(scaleDict[family][2])+1):
                self.comboMode.addItem('')

            for i in range(0, len(scaleDict[family][2])):
                self.comboMode.setItemText(i+1, _translate('MainWindow', scaleDict[family][2][i]))


    # Do UI updates upon user interaction. 
    # populateModes() fills mode combobox entries upon index of family combobox being >= 1.
    # renderNotes() draws fretboard and corresponding notes upon user selection of a mode in mode combobox.
    def UiInteraction(self):
        
        #Get family upon family combobox selection.
        self.comboFamily.activated.connect(self.populateModes)

        #Render notes in selected scale upon user interaction with key or mode combobox.
        self.comboMode.activated.connect(self.renderNotes)
        self.comboKey.activated.connect(self.renderNotes)

    
    # Render fretboard including strings and frets. renderNotes() handles
    # note rendering once a scale is determined.
    def renderFretboard(self):

        pen = QPen(Qt.black, 2)
                
        # Render bridge
        self.scene.addLine(bridgeX, string1Y, bridgeX, string6Y, pen)

        # Render frets 1-11
        # fretXcoords[0] = X-coord of fret 1
        fretXcoords = []

        for i in range(1, fretNum):
            fretX = bridgeX + (i * fretSize)
            fretXcoords.append(fretX)
            self.scene.addLine(fretX, string1Y, fretX, string6Y)

        # Render fret 12 separately with a thicker line (using pen)
        fret12 = self.scene.addLine(fret12X, string1Y, fret12X, string6Y, pen)

        # Render strings 1-6
        stringYcoords = []
        for i in range(0, stringNum):
            stringY = string1Y + (i * stringSize)
            stringYcoords.append(stringY)
            self.scene.addLine(bridgeX, stringY, fret12X, stringY, pen)

        # Render fret numbers (3,5,7,9)
        fretNums = (3,5,7,9)
        frets = []

        # stringYcoords[-1] gives the y-coord of the low-E string
        i = 0
        for num in fretNums:
            frets.append(QtWidgets.QGraphicsSimpleTextItem(str(num)))
            # frets[i].setPos(fretXcoords[num-1]-2, stringYcoords[-1]+2)
            frets[i].setPos(fretXcoords[num-1]-(fretSize/2)-2, stringYcoords[-1]+12)
            self.scene.addItem(frets[i])
            i += 1

        # Render fret number 12 separately by referencing the x-coord of fret 12
        num12 = QtWidgets.QGraphicsSimpleTextItem('12')
        num12.setPos(fret12X-2, stringYcoords[-1]+12)
        self.scene.addItem(num12)


    # Get interval representation of a number scale
    def getIntervals(self, numberScale):

        # The numberToInterval dict expects a number scale starting at 1, so we need to offset number scales
        # that don't start at 1.
        if numberScale[0] != 1:

            # Compute offset and apply to every number, then rebound that resulting number
            offset = numberScale[0] - 1

            for i in range(len(numberScale)):
                offsetNum = numberScale[i] - offset
                numberScale[i] = self.reboundNote(offsetNum)

        # Build list of intervals via lookups to numberToInterval dict
        intervals = []
        for num in numberScale:
            intervals.append(numberToInterval[num])

        return intervals


    # Render notes in selected scale over fretboard
    def renderNotes(self):
        
        # Delete all existing ellipses so that once a subsequent is selected only the new scale is drawn.
        self.deleteNotes()

        # Only render fretboard if index of selected item in mode combobox, 
        # and index of selected item in key combobox, are >= 1. Supplying mode=0 or 
        # an invalid key string (e.g., '') to getScale() does not work.
        if (self.comboMode.currentIndex() >= 1) and (self.comboKey.currentIndex() >= 1):

            # Get selected key and mode from their combobox indices. 
            # call getFamily() to obtain selected family.
            key = self.comboKey.currentText()
            family = self.getFamily()
            mode = self.comboMode.currentIndex()

            # getScale() returns a tuple of ([numberScale], [letterScale]).
            scale = self.getScale(key, family, mode)
            numberScale = scale[0]
            letterScale = scale[1]

            # Render notes in scale across fretboard
            for key, value in fretboard.items():
                if value in numberScale:
                    xCoord, yCoord = self.coordDict[key]

                    if value == scale[0][0]:
                        brush = QBrush(Qt.red)
                        pen = QPen(Qt.red, 2)
                    else:
                        brush = QBrush(Qt.white)
                        pen = QPen(Qt.black, 1)

                    self.scene.addEllipse(xCoord, yCoord, noteSize, noteSize, pen, brush)

            _translate = QtCore.QCoreApplication.translate

            # Get dictionary mapping each scale letter to corresponding interval
            intervals = self.getIntervals(numberScale)
            intervalDict = dict(zip(letterScale, intervals))

            # Clear existing interval labels
            for label in self.scaleLabels.values():
                label.clear()       

            # Render note buttons
            for note, button in self.scaleButtons.items():
                button.setDown(False)
                button.setCheckable(False)

                if note in letterScale:
                    
                    # Depress each button whose note is in selected scale
                    button.setDown(True)

                    # Color button corresponding to root/selected key
                    if note == self.comboKey.currentText():
                        button.setStyleSheet('QPushButton {background-color: #cc0000; color: black;}')
                    else:
                        button.setStyleSheet('QPushButton {background-color: #aaaeb2; color: black;}')

                    # For each note in selected scale, render button label indicating interval of that note
                    # by looking up interval corresponding to button's note from intervalDict
                    xCoord = button.geometry().getRect()[0]
                    label = self.scaleLabels[note]
                    label.setGeometry(QtCore.QRect(xCoord + 34, 320, 35, 30))
                    buttonInterval = intervalDict[note]
                    label.setText(_translate("MainWindow", buttonInterval))

                # If button's note isn't in selected scale, render as not depressed
                else:
                    button.setFlat(True)

            
    # Clear QGraphicsScene so that, once a subsequent scale is selected, only 
    # the new scale is drawn. clear() clears all graphical content, so 
    # call renderFretboard() to redisplay fretboard.
    def deleteNotes(self):
        self.scene.clear()
        self.renderFretboard()


    # Generate dictionary of coordinates for every position in the fretboard
    # where a note can be rendered. Call getNoteCoords() in setupUI() and return
    # as class instance variable (self.coordDict) so that it can be accessed by other
    # class methods and so that coordDict is only generated once per user session.
    def getNoteCoords(self, fretNum, stringNum, bridgeX, fretSize, noteSize, string1Y, stringSize):
        self.coordDict = {}

        for fret in range(1, fretNum+1):
            for string in range(0,stringNum):
                noteX = ((bridgeX + (fret * fretSize)) - (fretSize/2)) - (noteSize/2)
                noteY = ((string1Y + (string * stringSize)) - (noteSize/2))

                self.coordDict[(string+1, fret)] = (noteX, noteY)

        return self.coordDict


    # Maintain numerical note values within [0-12]. numberToNote and noteToNumber
    # dicts expect numerical note values within [0-12].
    def reboundNote(self, note):
        if note > 12:
            note -= 12
        elif note < 1:
            note += 12

        return note

    
    # Obtain number/letter representation of scale according to selected key, family, and mode.
    # Key/family/mode are selected by the user via respective comboboxes. 
    def getScale(self, key, family, mode):

        # Get tuple of intervals for selected family.
        intervals = scaleDict[family][0] 

        # Compute root - the note corresponding to the first mode of the selected family
        # to which the selected mode belongs.
        root = self.reboundNote(noteToNumber[key] - intervals[mode-1])
       
        # Build a number representation of the selected family. Take the root - the 
        # note corresponing to the first mode of the selected family - and add
        # each element in intervals to the root. This yields all notes in the 
        # scale. This list will later be reordered according to the selected mode.
        numberScale = []

        for interval in intervals:
            num = self.reboundNote(root + interval)
            numberScale.append(num)

        # If the first mode is selected, no reordering is needed. Simply build
        # a letter representation of the first mode. 
        if mode == 1:
        
            letterScale = []

            for num in numberScale:
                letterScale.append(numberToNote[num])

            return (numberScale, letterScale)
            
        # For all modes other than the first, reorder notes in numberScale
        # based on the mode to obtain a reorderedScale where the first note is
        # the first note of the selected mode. E.g., to obtain the notes for
        # D dorian (the second mode of C major), we first obtain the notes of C major
        # (C,D,E,F,G,A,B) and then reorder those notes to obtain (D,E,F,G,A,B,C).
        if mode != 1:

            # This defines the max index to go up to in the first step of reordering.
            # Subsequent indices need to "loop back" to the start of numberScale to
            # perform the final step of reordering.
            upperLimit = len(numberScale) - mode

            # Define a new list for the reordered scale. Otherwise, reordering numberScale 
            # itself may result in retrieving a value that was already reordered,
            # which can lead to duplicate notes. 
            reorderedScale = [0] * len(numberScale)
            
            # First reordering step.
            for i in range(0, upperLimit+1):
                reorderedScale[i] = numberScale[i + (mode-1)]

            # Second reordering step.
            for i in range(upperLimit+1, len(numberScale)):
                reorderedScale[i] = numberScale[i - (upperLimit+1)]
            
            letterScale = []

            for num in reorderedScale:
                letterScale.append(numberToNote[num])

            return (reorderedScale, letterScale)


# Qt application logic
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())




