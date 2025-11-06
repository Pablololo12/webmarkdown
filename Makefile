install:
	@echo "Installing"
	pip install --upgrade pip
	pip install -e .

test:
	pytest

testing:
	webmd && open test_out.html
