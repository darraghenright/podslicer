.PHONY: run test watch

TEST_DIR = ./tests

run:
	python -m podslicer

test:
	pytest $(TEST_DIR)

watch:
	ptw -- -vv $(TEST_DIR)
