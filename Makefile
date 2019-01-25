all: bin move clean-intermediate

bin:
	pyinstaller --clean --onefile --name asap --log-level INFO main.py

move:
	mv dist/asap ./


clean-intermediate:
	rm -rf build dist asap.spec

clean-all:
	rm -rf build asap.spec dist asap
