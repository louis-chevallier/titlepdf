

PYTHON=python

run :
	$(PYTHON) titlepdf.py

install :
	-pyinstaller titlepdf.py

