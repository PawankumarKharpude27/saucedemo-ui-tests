.PHONY: install test smoke regression sample-reports docker clean

install:
	python -m pip install -r requirements.txt
	playwright install --with-deps chromium

test:
	./run_tests.sh

smoke:
	MARKER=smoke ./run_tests.sh

regression:
	MARKER=regression ./run_tests.sh

# Run once locally, then commit sample-reports/ (deliverable).
sample-reports: test
	cp reports/junit-chromium.xml reports/report-chromium.html sample-reports/

docker:
	docker build -t saucedemo-ui-tests .
	docker run --rm --ipc=host -v "$(CURDIR)/reports:/app/reports" -v "$(CURDIR)/test-results:/app/test-results" saucedemo-ui-tests

clean:
	rm -rf reports test-results .pytest_cache
