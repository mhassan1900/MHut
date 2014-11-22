# Author: Mahmud Hassan
# Date:   Oct 23, 2014
# Description: 
# 	Standard makefile for all python projects
# 	This should serve as a template. Copy this and modify as per project

project=MHutils

all: 
	@echo 'Please enter a command for make:' 
	@echo '	  install|uninstall|distro|clean'

test: clean 
	python regress.py | tee 2>&1 regress.log

cover:
	coverage run regress.py 
	coverage report --omit='/System/*','*/Library*','*testdir*'
	coverage html --omit='/System/*','*/Library*','*testdir*'

install:
	python setup.py install --user 

uninstall:
	pip uninstall $(project)

distro:
	@echo 'This is an option for the future. Not yet implemented' 

clean:
	/bin/rm -rf build dist *egg-info */*egg-info *.log
	/bin/rm -rf htmlcov .coverage
	find . -name '*.pyc' -exec rm -rf {} \;
    
