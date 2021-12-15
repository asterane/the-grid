# Makefile for asterane.github.io

.PHONY: deploy serve publish

deploy:
	@./deploy.sh

serve:
	@echo "Serving..."
	hugo server -D --bind 0.0.0.0

publish:
	@echo "Publishing..."
	hugo

clean:
	@echo "Cleaning generated files..."
	@rm -rvf ../docs/*
	@rm -rvf content/*
