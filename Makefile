#
# Makefile to build standalone `packager` Unix-like executable program.
#

FREEZE = cxfreeze
SOURCE = packager.py
TARGET = packager
PACKAGE = io.stpettersens.example.helloworld
MAINCLASS = HelloWorld
ROOTDIR = examples

make:
	$(FREEZE) $(SOURCE) --target-dir dist
	
dependencies:
	pip -q install cx_Freeze
	yes | sudo add-apt-repository ppa:s.stpettersen/txtrevise-util
	sudo apt-get update > /dev/null
	sudo apt-get install txtrevise
	
test:
	sudo mv dist/${TARGET} /usr/bin 
	$(TARGET) -p $(PACKAGE) -m $(MAINCLASS) -cp . -r $(ROOTDIR) -v
	java -jar $(MAINCLASS).jar

clean:
	rm -r -f dist
	rm -f $(MAINCLASS).jar
