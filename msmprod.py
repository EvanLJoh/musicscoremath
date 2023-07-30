from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QTextBrowser, QFileDialog, QWidget
from music21 import converter, note, stream

class App(QMainWindow):
    def __init__(self):
        super().__init__()

        # Initialize UI
        self.title = 'Music Score Math'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Button to load the music file
        load_btn = QPushButton('Load Music File', self)
        load_btn.clicked.connect(self.loadMusicFile)
        layout.addWidget(load_btn)

        # Text browser to display the measures
        self.text_browser = QTextBrowser(self)
        layout.addWidget(self.text_browser)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.show()

    def loadMusicFile(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open MusicXML file", "", "MusicXML Files (*.mxl);;All Files (*)")
        if file_path:
            self.text_browser.clear()
            self.parseMusic(file_path)

    def parseMusic(self, file_path):
        score = converter.parse(file_path)
        first_part = score.parts[0]
        measure_count = 1
        for measure in first_part.getElementsByClass(stream.Measure):
            measure_notes = "Measure {}: ".format(measure_count)
            for el in measure.notes:
                if isinstance(el, note.Note):
                    x = el.offset
                    y = el.pitch.ps - 60
                    measure_notes += "({}, {}), ".format(x, y)
            self.text_browser.append(measure_notes[:-2])
            measure_count += 1
        
        # Plot the score in a separate window
        score.plot('horizontalbar')

if __name__ == '__main__':
    app = QApplication([])
    ex = App()
    app.exec()
