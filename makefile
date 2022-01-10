

PYTHON=python

run :
	$(PYTHON) titlepdf.py

install :
	-mkdir c:/tmp 
	-cp  titlepdf.py  c:/tmp
	-pyinstaller c:/tmp/titlepdf.py

