MIRROR=http://www.gutenberg.org/files
v := 20
volume := $(v)-1A
id1 := 11833
id2 := 11834


parsed: $(volume).tsv
unnested: $(volume)-unnested.tsv

$(volume).tsv: $(volume)-unnested.tsv
	../../scripts/parse.py -f $<  > $@

$(volume)-unnested.tsv: $(volume)-1-unnested.tsv $(volume)-2-unnested.tsv
	cat $^ > $@

$(volume)-1-unnested.tsv: $(id1)-8.txt
	../../scripts/unnest -f $< -s 52 -v $(v) -p 1A -n 1 -e iso-8859-15 > $@

$(volume)-2-unnested.tsv: $(id2)-8.txt
	../../scripts/unnest -f $< -s 52 -v $(v) -p 1A -n 2 -e iso-8859-15 > $@

$(id1)-8.txt:
	wget -q -N $(MIRROR)/$(id1)/$@

$(id2)-8.txt:
	wget -q -N $(MIRROR)/$(id2)/$@


clean:
	rm *.txt && rm *.tsv
