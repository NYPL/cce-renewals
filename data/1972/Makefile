MIRROR=http://www.gutenberg.org/files
v := 26
volume := $(v)-1A
id1 := 11845
id2 := 11846


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

# MIRROR=https://www.gutenberg.org/dirs/1/1/8/4

# unnested: 26-1-unnested.tsv

# 26-1-unnested.tsv: 26-1-1-unnested.tsv 26-1-2-unnested.tsv
# 	cat $^ > $@

# 26-1-1-unnested.tsv: 11845-8.txt
# 	../../scripts/unnest -f $< -s 52 -v 26 -p 1 -n 1 -e iso-8859-15 > $@

# 26-1-2-unnested.tsv: 11846-8.txt
# 	../../scripts/unnest -f $< -s 52 -v 26 -p 1 -n 2 -e iso-8859-15 > $@

# 11845-8.txt:
# 	wget -q -N $(MIRROR)/11845/$@

# 11846-8.txt:
# 	wget -q -N $(MIRROR)/11846/$@


clean:
	rm *.txt && rm *.tsv


