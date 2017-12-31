all:
	@rm -f data.txt
	python3 main.py
reset:
	rm -f *.txt
make analyze:
	python3 main_analyze.py

make a:
	python3 main_analyze_bis.py