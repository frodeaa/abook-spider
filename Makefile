all: fetch-all build

limit = 3
context = project/context

fetch = scrapy runspider -a limit=$(2) -a category=$(1) \
	--nolog -o - -t json audiobookbay.py > $(context)/$(1).json

fetch-clean:
	rm -rf $(context)
	mkdir -p $(context)

fetch-all: fetch-clean
	$(call fetch,fantasy,$(limit))
	$(call fetch,sci-fi,$(limit))

clean:
	rm -rf www

build: clean
	complexity --noserver project
