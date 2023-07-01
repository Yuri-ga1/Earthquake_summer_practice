help:
	@echo "Make project with following instructions"
	@cat Makefile

dev:
	pip install -e .

test: dev
	python app/test_earthquake.py

build: clean
	pip install wheel
	python setup.py bdist_wheel

clean:
	@if exist .pytest_cache (rmdir /s /q .pytest_cache)
	@if exist .mypy_cache (rmdir /s /q .mypy_cache)
	@if exist junit (rmdir /s /q junit)
	@if exist build (rmdir /s /q build)
	@if exist dist (rmdir /s /q dist)
	@if exist app/pycache (rmdir /s /q app/pycache)
	@if exist app.egg-info (rmdir /s /q app.egg-info)
	@for /r %%i in (pycache) do @if exist "%%i" del /s /q "%%i"
	@for /r %%i in (__pycache__) do @if exist "%%i" rmdir /s /q "%%i"