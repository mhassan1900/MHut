# Author: Mahmud Hassan
# Date:   Oct 23, 2014
# Description:
# 	Standard makefile for all python projects
# 	This should serve as a template. Copy this and modify as per project

project=MHut
save_lint=n

all:
	@echo 'Please enter a command for make:'
	@echo '	  test|install|uninstall|cover|distro|clean'

test: clean
	python3 regress.py | tee 2>&1 regress.log

cover:
	coverage run regress.py
	coverage report --omit='/System/*','*/Library*','*testdir*'
	coverage html --omit='/System/*','*/Library*','*testdir*'

lint:
	pylint --rcfile .pylintrc mhut -f colorized  --files-output=$(save_lint) 

install:
	python3 setup.py install --user

uninstall:
	pip uninstall $(project)

distro:
	@echo 'Preparing to upload to PyPi'
	# python setup.py register
	python3 setup.py sdist
	twine upload dist/*

clean:
	/bin/rm -rf build dist *egg-info */*egg-info *.log
	/bin/rm -rf htmlcov .coverage
	find . -name '*.pyc' -exec rm -rf {} \;
