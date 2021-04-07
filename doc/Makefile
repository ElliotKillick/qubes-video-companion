# Copyright (C) 2021 Elliot Killick <elliotkillick@zohomail.eu>
# Licensed under the MIT License. See LICENSE file for details.

DATADIR ?= /usr/share
MANDIR ?= $(DATADIR)/man
MAN1DIR ?= $(MANDIR)/man1

INSTALL_DIR = install -d
INSTALL_DATA = install -Dm 644

MANPAGES=$(patsubst %.rst,%.1.gz,$(wildcard *.rst))

help:
	@echo "make manpages	Generate manpages"
	@echo "make install	Generate manpages and install them to $(MAN1DIR)"

manpages: $(MANPAGES)

%.1: %.rst
	pandoc -s -f rst -t man -o $@ $<

%.1.gz: %.1
	gzip -f $<

install: manpages
	$(INSTALL_DIR) $(DESTDIR)$(MAN1DIR)
	$(INSTALL_DATA) $(MANPAGES) $(DESTDIR)$(MAN1DIR)

clean:
	rm -f $(MANPAGES)
