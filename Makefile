all: fetch-all build

limit = 3
context = project/context

fetch = scrapy runspider -a limit=$(2) -a category=$(1) \
	--nolog -o - -t json audiobookbay.py > $(context)/$(3)

fetch-clean:
	rm -rf $(context)
	mkdir -p $(context)

fetch-all: fetch-clean
	$(call fetch,fantasy,$(limit),fantasy.json)
	$(call fetch,sci-fi,$(limit),sci_fi.json)

clean:
	rm -rf www

build: clean
	complexity --noserver project
