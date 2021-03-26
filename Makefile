#!/bin/bash
all: idk install_dependencies

idk:
	sudo chmod +x setup.py

install_dependencies:
	sudo ./setup.py install

