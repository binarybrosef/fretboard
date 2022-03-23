from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsSimpleTextItem
from PyQt5.QtGui import QBrush, QPen
from PyQt5.QtCore import Qt


#Display settings
windowWidth = 909                               #Main window width
windowHeight = 352                              #Main window height
comboX = 4                                      #combobox x-coord
comboY = 16                                     #combobox y-coord
comboWidth = 430                                #combobox width
comboHeight = 41                                #combobox height                
bridgeX = -462                                  #x-coord of bridge 
fret12X = 402                                   #x-coord of fret 12
string1Y = -241                                 #y-coord of string 1 (i.e., high-E string in standard tuning)
string6Y = -71                                  #y-coord of string 6 (i.e., low-E string in standard tuning)
fretNum = 12                                    #number of frets
fretSize = (abs(bridgeX) + fret12X) / fretNum   #size of each fret. Frets are of same size in current implementation.
stringNum = 6
stringSize = (abs(abs(string1Y) -               #spacing between adjacent strings
              abs(string6Y))) / (stringNum - 1)         
noteSize = 20                                   #height/width of notes to be rendered in fretboard


#Fretboard data structures

#Dictionary listing, for every position on the fretboard (every string/fret combo),
#the corresponding note. This dictionary omits open strings (1,0), (2,0), etc.

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

#This dictionary contains all scale families, their modes, and their intervals
#represented in terms of half steps.

#scaleDict[key][0] = scale family intervals (tuple)
#scaleDict[key][1] = scale family name (list containing one string)
#scaleDict[key][2] = list of scale family modes (list of strings)

scaleDict = {'maj_min':    [(0,2,4,5,7,9,11), ['Major/Minor'],
                            ['Major/Ionian', 'Dorian', 'Phrygian', 'Lydian', 
                            'Mixolydian','Minor/Aeolian', 'Locrian']],

              'mel_min':    [(0,2,3,5,7,9,11), ['Melodic Minor'],
                            ['Melodic Minor', 'Dorian b2/Phrygian #6', 'Lydian Augmented',
                             'Lydian Dominant', 'Mixolydian b6', 'Aeolian b5/Locrian #2',
                             'Altered/Super Locrian']],

              'harm_min':   [(0,2,3,5,7,8,11), ['Harmonic Minor'],
                            ['Harmonic Minor/Aeolian #7', 'Locrian #6', 'Ionian #5/Augmented Major',
                             'Ukranian Dorian', 'Phrygian Dominant', 'Lydian #2', 
                             'Superlocrian bb7/Altered Diminished']],

              'harm_maj':   [(0,2,4,5,7,8,11), ['Harmonic Major'],
                            ['Harmonic Major', 'Locrian #2 #6/Dorian b5', 'Altered Dominant #5/Phrygian b4',
                             'Melodic Minor #4/Lydian b3', 'Mixolydian b2', 'Lydian Augmented #2',
                              'Locrian bb7']],      

              'half_whole': [(0,1,3,4,6,7,9,10), ['Half-Whole Diminished/Octatonic'],
                            ['Half-Whole Diminished 1', 'Whole-Half Diminished 1',
                             'Half-Whole Diminished 2', 'Whole-Half Diminished 2',
                             'Half-Whole Diminished 3', 'Whole-Half Diminished 3',
                             'Half-Whole Diminished 4', 'Whole-Half Diminished 4',]],

              'whole_tone': [(0,2,4,6,8,10), ['Whole-tone'], ['Whole-tone 1', 'Whole-tone 2', 'Whole-tone 3',
                             'Whole-tone 4', 'Whole-tone 5', 'Whole-tone 6']],

              'pentatonic': [(0,3,5,7,10), ['Pentatonic'], ['Pentatonic 1', 'Pentatonic 2',
                             'Pentatonic 3', 'Pentatonic 4', 'Pentatonic 5']],

              'chromatic':  [(0,1,2,3,4,5,6,7,8,9,10,11), ['Chromatic'], ['Chromatic 1', 'Chromatic 2',
                             'Chromatic 3', 'Chromatic 4', 'Chromatic 5', 'Chromatic 6', 'Chromatic 7',
                             'Chromatic 8', 'Chromatic 9', 'Chromatic 10', 'Chromatic 11', 'Chromatic 12']]
                            
             }

#Dictionary mapping letter notes to number representations.
noteToNumber = {'C': 1, 'Db': 2, 'D': 3, 'Eb': 4, 'E': 5,'F': 6, 'Gb': 7\
        ,'G': 8, 'Ab': 9, 'A': 10, 'Bb': 11, 'B': 12}

#Dictionary mapping number representations of notes to letters.
numberToNote = {1:'C', 2:'Db', 3:'D', 4:'Eb', 5:'E', 6:'F', 7:'Gb'\
        ,8:'G', 9:'Ab', 10:'A', 11:'Bb', 12:'B'}


#Define main window class
class Ui_MainWindow(object):
    
    ##--Qt main window setup--##
    def setupUi(self, MainWindow):
        MainWindow.setObjectName('MainWindow')
        MainWindow.resize(windowWidth, windowHeight)

        self.renderUI()                                 #render UI elements (e.g., comboboxes)
        self.retranslateUi()                            #set UI element items/label text
        self.UiInteraction()                            #handle user interactions with UI
        self.renderGraphicsScene()                      #render QGraphicsScene
        self.renderFretboard()                          #render fretboard
        self.coordDict = self.getNoteCoords(fretNum,    #get dictionary of all coordinates where notes can be rendered
            stringNum, bridgeX, fretSize, noteSize, string1Y, stringSize)
        
        #Initialize list for storing the pointers for all the ellipses to be drawn.
        #This list can later be accessed for deleting all ellipses from screen
        #before a new scale is drawn, so that notes from both scales are not displayed.
        #Current implementation uses QGraphicsScene.removeItem() to remove ellipses.
        self.ellipses = []

        #Initialize for same deletion purpose for key indicators.
        self.keyIndicator = []
        self.indicators = 0
        

    ##--Render UI elements (buttons, comboboxes) not including QGraphicsView--##
    def renderUI(self):
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        MainWindow.setCentralWidget(self.centralwidget)
        
        #Establish horizontal layout for key, family, mode comboboxes
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(comboX,comboY,comboWidth,comboHeight))

        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)

        #Add key, family, mode comboboxes
        self.comboKey = QtWidgets.QComboBox(self.horizontalLayoutWidget)
        self.comboFamily = QtWidgets.QComboBox(self.horizontalLayoutWidget)
        self.comboMode = QtWidgets.QComboBox(self.horizontalLayoutWidget)

        self.horizontalLayout.addWidget(self.comboKey)
        self.horizontalLayout.addWidget(self.comboFamily)
        self.horizontalLayout.addWidget(self.comboMode)

        #Add key, family, mode combobox labels
        self.labelKey = QtWidgets.QLabel(self.centralwidget)
        self.labelKey.setGeometry(QtCore.QRect(4, 0, 47, 31))

        self.labelFamily = QtWidgets.QLabel(self.centralwidget)
        self.labelFamily.setGeometry(QtCore.QRect(128, 0, 47, 31))        

        self.labelMode = QtWidgets.QLabel(self.centralwidget)
        self.labelMode.setGeometry(QtCore.QRect(316, 0, 47, 31))


    ##--Render QGraphicsView. renderFretboard() renders the actual graphical content
    ##--(frets, strings, notes) displayed in the QGraphicsView.
    def renderGraphicsScene(self):
        self.scene = QGraphicsScene()

        self.graphicsView = QGraphicsView(self.scene, MainWindow)
        self.graphicsView.setGeometry(QtCore.QRect(4,75,901,214))


    ##--Set GUI element (buttons, comboboxes) labels/item labels.
    def retranslateUi(self):

        _translate = QtCore.QCoreApplication.translate

        #Set window title
        MainWindow.setWindowTitle(_translate("MainWindow", "Fretboard"))

        #Set key, family, mode label text
        self.labelKey.setText(_translate("MainWindow", "Key"))
        self.labelFamily.setText(_translate("MainWindow", "Family"))
        self.labelMode.setText(_translate("MainWindow", "Mode"))
        
        #Add blank entries to key combobox.
        for i in range(0, len(noteToNumber.keys())+1):
            self.comboKey.addItem('')

        #Add blank entries to family combobox.
        for key in scaleDict.keys():
            self.comboFamily.addItem('')

        #Set key combobox item labels with the keys of noteToNumber dict.
        i = 1
        for key in noteToNumber.keys():
            self.comboKey.setItemText(i, _translate('MainWindow', key))
            i += 1

        #Set family combobox items with the keys of scaleDict dict.
        i = 1
        for family in scaleDict.keys():
            self.comboFamily.setItemText(i, _translate('MainWindow', scaleDict[family][1][0]))
            i += 1

        #The addition of blank entries and setting of item labels for mode combobox is 
        #handled below in populateModes(), which is called in UiInteraction().


    ##--When a selection in family combobox is made, map the item label to a corresponding
    ##--key in scaleDict so that the scaleDict key can be accessed for values therein.
    def getFamily(self):
        family = self.comboFamily.currentText()

        for fam in scaleDict.keys():
            familyName = scaleDict[fam][1][0]
            comparison = family == familyName

            if comparison == True:
                family = fam

        return family


    ##--Set mode combobox item labels upon user selection of family in family combobox.--##
    def populateModes(self):

        #Clear modes combobox. Otherwise every family selection will add to the 
        #already existing entries in mode combobox.
        self.comboMode.clear()

        #Only populate modes combobox if index of selected item in family combobox 
        # >= 1. Otherwise, the modes combobox cannot be populated if the family is 
        #not yet selected.
        if self.comboFamily.currentIndex() >= 1:
            family = self.getFamily()            

            #For each mode in the selected family, add blank entries to mode combobox, 
            #and then fill the blank entries with all the modes for the selected family.
            _translate = QtCore.QCoreApplication.translate

            for i in range(0, len(scaleDict[family][2])+1):
                self.comboMode.addItem('')

            for i in range(0, len(scaleDict[family][2])):
                self.comboMode.setItemText(i+1, _translate('MainWindow', scaleDict[family][2][i]))


    ##--Do UI updates upon user interaction. 
    ##--populateModes() fills mode combobox entries upon index of family combobox being >= 1.
    ##--renderNotes() draws fretboard and corresponding notes upon user selection of a mode in mode combobox.--##
    def UiInteraction(self):
        
        #Get family upon family combobox selection.
        self.comboFamily.activated.connect(self.populateModes)

        #Render notes in selected scale upon user interaction with mode combobox.
        self.comboMode.activated.connect(self.renderNotes)

        #Render notes in selected scale upon user interaction with key combobox.
        self.comboKey.activated.connect(self.renderNotes)


    ##--Render fretboard including strings and frets. renderNotes() handles
    ##--note rendering once a scale is determined.--##
    def renderFretboard(self):

        pen = QPen(Qt.black, 2)
                
        #Render bridge
        self.scene.addLine(bridgeX, string1Y, bridgeX, string6Y, pen)

        #Render frets 1-11
        #fretXcoords[0] = X-coord of fret 1
        fretXcoords = []

        for i in range(1, fretNum):
            fretX = bridgeX + (i * fretSize)
            fretXcoords.append(fretX)
            self.scene.addLine(fretX, string1Y, fretX, string6Y)

        #Render fret 12 separately with a thicker line (using pen)
        fret12 = self.scene.addLine(fret12X, string1Y, fret12X, string6Y, pen)

        #Render strings 1-6
        stringYcoords = []

        for i in range(0, stringNum):
            stringY = string1Y + (i * stringSize)
            stringYcoords.append(stringY)
            self.scene.addLine(bridgeX, stringY, fret12X, stringY, pen)

        #Render fret numbers (3,5,7,9)
        fretNums = (3,5,7,9)
        frets = []

        #stringYcoords[-1] gives the y-coord of the low-E string
        i = 0
        for num in fretNums:
            frets.append(QtWidgets.QGraphicsSimpleTextItem(str(num)))
            frets[i].setPos(fretXcoords[num-1]-2, stringYcoords[-1]+2)
            self.scene.addItem(frets[i])
            i += 1

        #Render fret number 12 separately by referencing the x-coord of fret 12
            num12 = QtWidgets.QGraphicsSimpleTextItem('12')
            num12.setPos(fret12X-2, stringYcoords[-1]+2)
            self.scene.addItem(num12)


    ##--Render notes in selected scale over fretboard.--##
    def renderNotes(self):
        #Delete all existing ellipses so that once a subsequent is selected only the new scale is drawn.
        self.deleteNotes()

        #Only render the fretboard if the index of the selected item in mode combobox, 
        #and index of selected item in key combobox, are >= 1. Supplying mode=0 or 
        #an invalid key string (e.g., '') to getScale() does not work.
        if (self.comboMode.currentIndex() >= 1) and (self.comboKey.currentIndex() >= 1):

            #Get selected key and mode from their combobox indices. 
            #call getFamily() to obtain selected family.
            key = self.comboKey.currentText()
            family = self.getFamily()
            mode = self.comboMode.currentIndex()

            #Render graphical indicator of fret corresponding to selected key.
            self.renderKeyIndicator(key)

            #getScale() returns a tuple of ([numberScale], [letterScale]).
            #Access numberScale at the 0th index.
            scale = self.getScale(key, family, mode)

            brush = QBrush(Qt.black)
            pen = QPen(Qt.black, 2)

            #Go through every value in fretboard dict. If given value is in
            #selected scale, draw ellipse at coordinates obtained from coordDict,
            #and append pointer to that ellipse to self.ellipses.
            for key, value in fretboard.items():
                if value in scale[0]:
                    xCoord, yCoord = self.coordDict[key]
                    self.ellipses.append(self.scene.addEllipse(xCoord, yCoord, noteSize, noteSize, pen, brush))

    ##--Delete previously-drawn ellipses so that, once a subsequent scale is selected, only 
    ##--the new scale is drawn.
    def deleteNotes(self):
        for ellipse in self.ellipses:
            self.scene.removeItem(ellipse)

    ##--Render graphical indicator indicating fret corresponding to selected key.
    def renderKeyIndicator(self, key):
        #Delete any existing indicators if added
        if len(self.keyIndicator) > 0:
            self.scene.removeItem(self.keyIndicator[self.indicators-1])

        #Look up note number using key as index
        keyNum = noteToNumber[key]

        #Loop through fretboard, only low-E string (keys (6,1) through (6,12)), to find key 
        #having value matching note number.
        for i in range(1, 13):
            comparison = fretboard[(6,i)] == keyNum
            if comparison:
                fret = i

        #Use key where matching value is found to index into coordDict to get x/y coords
        xCoord, yCoord = self.coordDict[(6,fret)]

        brush = QBrush(Qt.blue)
        pen = QPen(Qt.blue, 2)

        #Render indicator at x-coord
        self.keyIndicator.append(self.scene.addRect(xCoord+6, yCoord+28, 8, 8, pen, brush))
        self.indicators += 1


    ##--Generate dictionary of coordinates for every position in the fretboard
    ##--where a note can be rendered. Call getNoteCoords() in setupUI() and return
    ##--as class instance variable (self.coordDict) so that it can be accessed by other
    ##--class methods and so that coordDict is only generated once per user session.
    def getNoteCoords(self, fretNum, stringNum, bridgeX, fretSize, noteSize, string1Y, stringSize):
        self.coordDict = {}

        for fret in range(1, fretNum+1):
            for string in range(0,stringNum):
                noteX = ((bridgeX + (fret * fretSize)) - (fretSize/2)) - (noteSize/2)
                noteY = ((string1Y + (string * stringSize)) - (noteSize/2))

                self.coordDict[(string+1, fret)] = (noteX, noteY)

        return self.coordDict


    ##--Maintain numerical note values within [0-12]. numberToNote and noteToNumber
    ##--dicts expect numerical note values within [0-12].
    def reboundNote(self, note):
        if note > 12:
            note -= 12
        elif note < 1:
            note += 12
        else:
            note = note

        return note

    
    ##--Obtain number/letter representation of scale according to selected key, family, and mode.
    ##--Key/family/mode are selected by the user via respective comboboxes. 
    def getScale(self, key, family, mode):

        #Get tuple of intervals for selected family.
        intervals = scaleDict[family][0] 

        #Compute root - the note corresponding to the first mode of the selected family
        #to which the selected mode belongs.
        root = self.reboundNote(noteToNumber[key] - intervals[mode-1])
       
        #Build a number representation of the selected family. Take the root - the 
        #note corresponing to the first mode of the selected family - and add
        #each element in intervals to the root. This yields all notes in the 
        #scale. This list will later be reordered according to the selected mode.
        numberScale = []

        for interval in intervals:
            num = self.reboundNote(root + interval)
            numberScale.append(num)

        #If the first mode is selected, no reordering is needed. Simply build
        #a letter representation of the first mode. 
        if mode == 1:
        
            letterScale = []

            for num in numberScale:
                letterScale.append(numberToNote[num])

            return (numberScale, letterScale)
            
        #For all modes other than the first, reorder notes in numberScale
        #based on the mode to obtain a reorderedScale where the first note is
        #the first note of the selected mode. E.g., to obtain the notes for
        #D dorian (the second mode of C major), we first obtain the notes of C major
        #(C,D,E,F,G,A,B) and then reorder those notes to obtain (D,E,F,G,A,B,C).

        if mode != 1:

            #This defines the max index to go up to in the first step of reordering.
            #Subsequent indices need to "loop back" to the start of numberScale to
            #perform the final step of reordering.
            upperLimit = len(numberScale) - mode

            #Define a new list for the reordered scale. Otherwise, reordering numberScale 
            #itself may result in retrieving a value that was already reordered,
            #which can lead to duplicate notes. 
            reorderedScale = [0] * len(numberScale)
            
            #First reordering step.
            for i in range(0, upperLimit+1):
                reorderedScale[i] = numberScale[i + (mode-1)]

            #Second reordering step.
            for i in range(upperLimit+1, len(numberScale)):
                reorderedScale[i] = numberScale[i - (upperLimit+1)]
            
            letterScale = []

            for num in reorderedScale:
                letterScale.append(numberToNote[num])

            return (reorderedScale, letterScale)


#Qt application logic

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())




