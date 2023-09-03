.PHONY: default run test watch

TEST_DIR = ./tests

default:     # Show all available commands.
	@echo "Welcome to podslicer!\n"
	@grep -E '^\w+:' Makefile
	@echo "\n"

run:         # Run podslicer application.
	python -m podslicer

test:        # Run tests.
	pytest $(TEST_DIR)

watch:       # Run and watch tests.
	ptw -- -vv $(TEST_DIR)
