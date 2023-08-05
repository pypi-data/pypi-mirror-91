# DON'T FORGET: TABS AND NOT SPACES!
# Kudos to https://krzysztofzuraw.com/blog/2016/makefiles-in-python-projects.html
# Kudos to https://gist.github.com/lumengxi/0ae4645124cd4066f676
.PHONY: clean-pyc clean-build docs clean
define BROWSER_PYSCRIPT
import os, webbrowser, sys
try:
	from urllib import pathname2url
except:
	from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT
BROWSER := python -c "$$BROWSER_PYSCRIPT"

help:
	@echo "clean - remove all build, test, coverage and Python artifacts"
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "clean-test - remove test and coverage artifacts"
	@echo "lint - check style with flake8"
	@echo "test - run tests quickly with the default Python"
	@echo "test-all - run tests on every Python version with tox"
	@echo "coverage - check code coverage quickly with the default Python"
	@echo "docs - generate Sphinx HTML documentation, including API docs"
	@echo "release - package and upload a release"
	@echo "dist - package"
	@echo "install - install the package to the active Python's site-packages"

clean: clean-build clean-pyc clean-test

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -rf {} +

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test:
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/

lint:
	autoflake -i -r dmake
	sh -c "isort --skip-glob=.tox --combine-star --force-single-line-imports --recursive dmake tests "
	flake8 --max-line-length=180 dmake tests
	black dmake

test:
	tox -- --flake8
#	python setup.py test

# test-all:
# 	tox

coverage:
	coverage run --source dmake setup.py test
	coverage report -m
	coverage html
	$(BROWSER) htmlcov/index.html

# docs:
# 	rm -f docs/leviathan_serving.rst
# 	rm -f docs/modules.rst
# 	sphinx-apidoc -o docs/ leviathan_serving
# 	$(MAKE) -C docs clean
# 	$(MAKE) -C docs html
# 	$(BROWSER) docs/_build/html/index.html

# servedocs: docs
# 	watchmedo shell-command -p '*.rst' -c '$(MAKE) -C docs html' -R -D .

release: clean
	#python setup.py sdist upload
	python setup.py bdist_wheel

dist: clean
	python setup.py sdist
	python setup.py bdist_wheel
	twine upload dist/*

install: clean
	pip install .
	#python ./setup.py install

#
# lint:
# 	flake8 --exclude=.tox
#
# test: clean-pyc
# 	py.test --verbose --color=yes $(TEST_PATH)
#
# run:
# 	python manage.py runserver
#
# docker-run:
# 	docker build \
# 	  --file=./Dockerfile \
# 	  --tag=my_project ./
# 	docker run \
# 	  --detach=false \
# 	  --name=my_project \
# 	  --publish=$(HOST):8080 \
# 	  my_project
#
# .PHONY: clean-pyc clean-build
