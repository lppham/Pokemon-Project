import pandas as pd
import sys, urllib2
import requests
from PyQt4 import QtGui, QtCore

specs = ['Name', 'Type', 'HP', 'Attack', 'Sp. Atk', 'Defense', 'Sp. Def', 'Speed', 'Total']

txt = ''
for spec in specs:
	txt += '\n' + spec + ':\n'

class PokeDex(QtGui.QWidget):

	def __init__(self):
		super(PokeDex, self).__init__()

		self.initUI()

	def initUI(self):
		#Grid
		self.grid = QtGui.QGridLayout()
		self.setLayout(self.grid)

		#Parse
		self.df = pd.read_json('PokeData.json')
		print self.df.keys()
		self.df = self.df.set_index(['#'])
		
		#Make a Dropdown menu
		self.dropdown = QtGui.QComboBox(self)
		self.names = sorted(self.df['Name'].values)
		self.dropdown.addItems(self.names)
		self.grid.addWidget(self.dropdown, 0,0,1,1)
		
		#Search button
		self.btn = QtGui.QPushButton('Search', self)
		self.btn.clicked.connect(self.Search_Button)
		self.grid.addWidget(self.btn, 0,1,1,1)

		#Picture
		self.img = QtGui.QLabel(self)
		self.grid.addWidget(self.img, 1,1,1,1)

		#Data
		self.label = QtGui.QLabel(self)
		self.label.setAlignment(QtCore.Qt.AlignCenter)
		self.label.setText(txt)
		self.label.setAlignment(QtCore.Qt.AlignLeft)
		self.grid.addWidget(self.label, 1,0,1,1)


		self.resize(500, 250)
		self.center()
		self.setWindowTitle('PokeDex')
		self.show()

	def Search_Button(self):

		#Parse
		index = self.dropdown.currentIndex()
		val = self.names[index]
		cond = self.df['Name'] == val
		#Image
		img_url = 'http://img.pokemondb.net/artwork/' + val.lower().split(" ")[0] + '.jpg'
		img_bin = urllib2.urlopen(img_url).read()
		image = QtGui.QImage()
		image.loadFromData(img_bin)
		self.img.setPixmap(QtGui.QPixmap(image))

		#Set values

		PData = 'Name:\t\t\t' + val + '\n\n'
		PData += 'Type:\t\t\t' + ', '.join(self.df[cond]['Type'].values[0]) + '\n\n'
		for spec in specs[2:]:
			PData += spec + ':\t\t\t' + str(self.df[cond][spec].values[0]) + '\n\n'
		self.label.setText(PData)

	def center(self):
		qr = self.frameGeometry()
		cp = QtGui.QDesktopWidget().availableGeometry().center()
		qr.moveCenter(cp)
		self.move(qr.topLeft())

def main():
	app = QtGui.QApplication(sys.argv)
	app.aboutToQuit.connect(app.deleteLater)

	gui = PokeDex()
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()
















