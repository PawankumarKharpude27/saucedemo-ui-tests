# Image tag must match the playwright pin in requirements.txt: it ships the browsers
# and OS dependencies, so no `playwright install` is needed.
FROM mcr.microsoft.com/playwright/python:v1.63.0-noble

ENV PIP_BREAK_SYSTEM_PACKAGES=1 PIP_NO_CACHE_DIR=1 BROWSER=chromium
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["bash", "run_tests.sh"]
