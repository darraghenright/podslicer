.PHONY: test watch

TEST_DIR = ./tests

test:
	pytest $(TEST_DIR)

watch:
	ptw -- -vv $(TEST_DIR)
