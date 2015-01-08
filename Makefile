all: fetch-all build

limit = 3
abooks = project/context/abooks

fetch = scrapy runspider -a limit=$(2) -a category=$(1) \
	--nolog -o - -t json audiobookbay.py > $(abooks)/$(1).json

fetch-clean:
	rm -rf $(abooks)
	mkdir -p $(abooks)

fetch-all: fetch-clean
	$(call fetch,fantasy,$(limit))
	$(call fetch,sci-fi,$(limit))

clean:
	rm -rf www

build: clean
	complexity --noserver project
