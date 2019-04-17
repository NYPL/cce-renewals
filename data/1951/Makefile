v := 5
volume := $(v)-1A
id1 := 11803
id2 := 11804
s1 := 51
s2 := 51

parsed: $(volume).tsv
unnested: $(volume)-unnested.tsv

$(volume).tsv: $(volume)-unnested.tsv
	../../scripts/parse.py -f $<  > $@

$(volume)-unnested.tsv: $(volume)-1-unnested.tsv $(volume)-2-unnested.tsv
	cat $^ > $@

$(volume)-1-unnested.tsv: $(id1)-8.txt
	../../scripts/unnest -f $< -s $(s1) -v $(v) -p 1A -n 1 -e iso-8859-15 > $@

$(volume)-2-unnested.tsv: $(id2)-8.txt
	../../scripts/unnest -f $< -s $(s2) -v $(v) -p 1A -n 2 -e iso-8859-15 > $@

$(id1)-8.txt:
	wget -q -N $(MIRROR)/$(id1)/$@

$(id2)-8.txt:
	wget -q -N $(MIRROR)/$(id2)/$@


clean:
	rm *.txt && rm *.tsv

