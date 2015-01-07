##
# Makefile to build standalone `packager` Unix-like executable program.
##

FREEZE = cxfreeze
SOURCE = packager.py
TARGET = packager
PACKAGE = io.stpettersens.example.helloworld
MAINCLASS = HelloWorld
ROOTDIR = examples

make:
	$(FREEZE) $(SOURCE) --target-dir dist
test:
	sudo mv dist/${TARGET} /usr/bin 
	$(TARGET) -p $(PACKAGE) -m $(MAINCLASS) -cp . -r $(ROOTDIR) -v
	java -jar $(MAINCLASS).jar

clean:
	rm -r -f dist
	rm -f $(MAINCLASS).jar
