PROJECT = ProvisionLWConfig
DIR_NAME = provisionLWConfig
FUNCTION = $(PROJECT)
DIST_DIR ?= "$(BASE)"/functions/packages/$(DIR_NAME)
HONEY_DATASET = $(DATASET)

all: build

.PHONY: clean build

clean:
	rm -rf build
	rm $(DIST_DIR)/$(FUNCTION).zip || true

build: clean
	mkdir -p build
	cp ../common/* build
	buildid=$$(git describe --all --long | cut -d "/" -f 2); \
	sed -e "s|\$$BUILD|$$buildid|g" -e "s|\$$DATASET|$(HONEY_DATASET)|g" -e "s|\$$HONEY_KEY|$(HONEY_KEY)|g" provisionLWConfig.py > build/provisionLWConfig.py
	pip install -r requirements.txt -t build
	cd build; zip -r $(DIST_DIR)/$(FUNCTION).zip . -x "*.DS_Store*" "*.git*" "build*" "Makefile"
	rm -rf build


