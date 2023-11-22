SPHINXOPTS ?=
SPHINXBUILD ?= sphinx-build
SOURCEDIR = .
BUILDDIR  = _build

# Put it first so that `make` without an argument is like `make help`.
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
