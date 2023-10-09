extract-translations:
	@echo "Extracting translations..."
	@find -type f -iname "*.py" | xargs xgettext -o data.pot
	@find locale -maxdepth 1 -mindepth 1 -type d | \
	xargs -I {} msgmerge --no-fuzzy-matching --backup=none --update {}/LC_MESSAGES/data.po data.pot
	@rm data.pot

compile-translations:
	@echo "Compiling translations..."
	@find locale -maxdepth 1 -mindepth 1 -type d | \
	xargs -I {} msgfmt -o {}/LC_MESSAGES/data.mo {}/LC_MESSAGES/data.po


.PHONY: extract-translations compile-translations
