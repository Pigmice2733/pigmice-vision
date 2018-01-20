init:
	pipenv 

test:
	py.test tests

.PHONY: init test

