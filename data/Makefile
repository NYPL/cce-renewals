export MIRROR := https://www.gutenberg.org/dirs/1/1/8/0
export s1 := 52
export s2 := 52
SUBDIRS = 1950 1951 1952 1953 1954 1955 1956 1957 1958 1959 1960 1961 1962 \
	1963 1964 1965 1966 1967 1968 1969 1970 1971 1972 1973 1974 1975 1976 \
	1977
POST77 := 1978 1979 1980 1981 1982 1983 1984 1985 1986 1987 1988 1989 1990 \
	1991 1992 1993 1995 1996 2001

.PHONY: subdirs $(SUBDIRS)
.PHONY: post-1977 $(POST77) $(YEARFILE)

all: $(SUBDIRS)

$(SUBDIRS):
	$(MAKE) -C $@

$(POST77): google-renewals-all-20080624.xml
	../scripts/expl-googl-cce -f $< -y $@ > $@.tsv

google-renewals-all-20080624.xml: |google-renewals-20080516.zip
	unzip -j google-renewals-20080516.zip google-renewals-20080624/google-renewals-all-20080624.xml

google-renewals-20080516.zip:
	wget -q -N http://dl.google.com/rights/books/renewals/$@




