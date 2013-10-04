SHELL:=/bin/bash -e
export SHELLOPTS=pipefail

.PHONY = all clean

all: bin/cairo_visualization_wheel

bin/%: src/%.py
	mkdir -p $(dir $@)
	cp $< $@.tmp
	chmod 755 $@.tmp
	mv $@.tmp $@

clean:
	rm -rf bin/
