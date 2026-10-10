.PHONY: all install uninstall deps

all:
	@echo "Run 'make install' to install Typo Fixer"

install:
	@bash ./install.sh

uninstall:
	@bash ./uninstall.sh

deps:
	@which python3 copyq xclip zenity notify-send >/dev/null || (echo "Missing some dependencies. Run 'make install' to auto-install." && exit 1)
	@echo "All dependencies satisfied."
