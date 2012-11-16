# Make Docs
 SHELL := /bin/bash

.PHONY: all

TARGETS = README.html


all: makefile $(TARGETS) 
	cp README.rst ../README.rst

%.html: %.rst
	@echo $@
	rst2html $< $@




