#!/usr/bin/env python
"""
Packager
Utility to morph a non-structured project into a proper Java package.

Copyright 2014-2015 Sam Saint-Pettersen.
Licensed under the MIT/X11 License.

Depends on txtrevise utility, Java compiler (javac) and Java archiver (jar).
"""
import sys
import re
import os
import subprocess
import platform
import argparse
import shutil
import glob

signature = "Packager 1.0 (https://github.com/stpettersens/Packager)"

def displayVersion():
	print('\n' + signature)

def displayInfo():
	print(__doc__)

def pkg(package, mainClass, classPath, rootFolder, verbose, version, info):

	if package == None and mainClass == None and classPath == None and rootFolder == None:
		if verbose == False and version == True and info == False:
			displayVersion()

		elif verbose == False and version == False and info == True:
			displayInfo()

		sys.exit(0)

	javac_version = subprocess.check_output(['javac', '-version'], stderr=subprocess.STDOUT)

	jars = path = startPath = ''
	jarsArray = []

	# Create packager root
	if not os.path.exists('packager'):
		os.mkdir('packager')
		startPath = os.path.abspath('packager')

	if classPath != '.':
		if verbose: print('Finding required JAR libraries:')
		if rootFolder != '.': os.chdir('{0}/{1}'.format(rootFolder, classPath))
		for jar in glob.glob('*.jar'):
			if verbose: print(jar)
			jars += '{0}/{1} '.format(classPath, jar)
			jarsArray.append('../{0}/{1}/{2};'.format(rootFolder, classPath, jar))

		os.chdir('..')

	if classPath == '.': os.chdir(rootFolder)

	if verbose: print('Copying Java source files:')
	for java in glob.glob('*.java'):
		if verbose: print(java)
		shutil.copy(java, '../packager')

	if rootFolder != '.': os.chdir('../packager')

	if verbose: print('Writing manifest for {0}.{1}'.format(package, mainClass))
	f = open('Manifest.mf'.format(rootFolder), 'w')
	f.write('Packager-Version: {0}\n'.format(signature))
	f.write('Created-By: {0}\n'.format(javac_version.rstrip()))
	f.write('Main-Class: {0}.{1}\n'.format(package, mainClass))
	if classPath != '.': f.write('Class-Path: {0}\n'.format(jars))
	f.close()

	if verbose: print('Prepending package declaration to sources:')
	for java in glob.glob('*.java'):
		if verbose: print(java)
		os.system('txtrevise -q -f {0} -l 1 -m "//package" -r "{1}"'.format(java, 'package {0};'.format(package)))

	if verbose: print('Creating folder structure from package declaration:')
	structure = 'package {0}'.format(package)
	folders = re.split('\.|\s', structure)
	folders.pop(0)
	for folder in folders:
		path += "{0}/".format(folder)
	rootPackage = folders.pop(0)

	if verbose: print(path)
	os.makedirs(path)

	if verbose: print('Copy source files to package structure:')
	for java in glob.glob('*.java'):
		if verbose: print('Copy {0}'.format(java))
		shutil.copy(java, path)

	if verbose: print('Compiling classes:')
	cp = ".;"
	if platform.system() != 'Windows': cp = '.:'

	if classPath != '.':
		for jar in jarsArray:
			cp += jar

	for java in glob.glob('*.java'):
		if verbose: print('Compiling {0}'.format(java))
		os.system('javac -cp {0} {1}/{2}'.format(cp[:-1], path, java))

	os.chdir(path)
	for java in glob.glob('*.java'):
		if verbose: print('Removing duplicate {0}'.format(java))
		os.remove(java)

	os.chdir(startPath)
	if verbose: print('Creating final JAR...')
	args = 'cfm'
	if verbose: args = 'cfvm'
	os.system('jar {0} {1}.jar Manifest.mf {2}'.format(args, mainClass, rootPackage))
	shutil.move('{0}.jar'.format(mainClass), '..')

# Handle any command line arguments.
parser = argparse.ArgumentParser(description='Utility to morph a BlueJ project into a proper Java package.')
parser.add_argument('-p', '--package', action='store', dest='package', metavar="PACKAGE")
parser.add_argument('-m', '--mainClass', action='store', dest='mainClass', metavar="MAINCLASS")
parser.add_argument('-cp', '--classPath', action='store', dest='classPath', metavar="FOLDER")
parser.add_argument('-r', '--root', action='store', dest='rootFolder', metavar="ROOTFOLDER")
parser.add_argument('-l', '--verbose', action='store_true', dest='verbose')
parser.add_argument('-v', '--version', action='store_true', dest='version')
parser.add_argument('-i', '--info', action='store_true', dest='info')
argv = parser.parse_args()

pkg(argv.package, argv.mainClass, argv.classPath, argv.rootFolder, argv.verbose, argv.version, argv.info)
