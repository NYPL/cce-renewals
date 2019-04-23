export MIRROR := https://www.gutenberg.org/dirs/1/1/8/0
export s1 := 52
export s2 := 52
PRE1977 = 1950 1951 1952 1953 1954 1955 1956 1957 1958 1959 1960 1961 1962 \
	1963 1964 1965 1966 1967 1968 1969 1970 1971 1972 1973 1974 1975 1976 \
	1977
POST77 := 1978 1979 1980 1981 1982 1983 1984 1985 1986 1987 1988 1989 1990 \
	1991 1992 1993 1995 1996 2001
PG := 11801 11802 11803 11804 11805 11806 11807 11808 11809 11810	\
11811 11812 11813 11814 11815 11816 11817 11818 11819 11820 11821	\
11822 11823 11824 11825 11826 11827 11828 11829 11830 11831 11832	\
11833 11834 11835 11836 11837 11838 11839 11840 11841 11842 11843	\
11844 11845 11846 11847 11848 11849 11850 11851 11852 11853 11854	\
11855 11856

.PHONY: post-1977 $(POST77) $(YEARFILE) pre-1977 $(PRE1977)
.PHONY: $(PG) all clean

all: pre-1977 post-1977

pre-1977: $(PRE1977)

post-1977: $(POST77)

$(POST77): temp/google-renewals-all-20080624.xml
	../scripts/expl-googl-cce -f $< -y $@ > $@-from-db.tsv

temp/google-renewals-all-20080624.xml: |temp/google-renewals-20080516.zip
	cd temp && unzip -o -j google-renewals-20080516.zip google-renewals-20080624/google-renewals-all-20080624.xml

temp/google-renewals-20080516.zip:
	cd temp && wget -q -N http://dl.google.com/rights/books/renewals/$(@F)

%-14A.tsv: temp/%-all.tsv 
	../scripts/parse.py -f $< > $@

%-1A.tsv: temp/%-all.tsv 
	../scripts/parse.py -f $< > $@

%-1.tsv: temp/%-all.tsv 
	../scripts/parse.py -f $< > $@

temp/%-all.tsv: temp/%-1.tsv temp/%-2.tsv
	cat $^ > $@

$(PG):
	cd temp && wget -q -N https://www.gutenberg.org/files/$@/$@-8.txt


1950: 1950-14A.tsv
temp/1950-1.tsv: temp/11801-8.txt
	../scripts/unnest -f $^ -v 4 -p 14A -n 1 -e iso-8859-15 > $@
temp/1950-2.tsv: temp/11802-8.txt
	../scripts/unnest -f $^ -v 4 -p 14A -n 2 -e iso-8859-15 > $@
temp/11801-8.txt: 11801
temp/11802-8.txt: 11802

1951: 1951-1A.tsv
temp/1951-1.tsv: temp/11803-8.txt
	../scripts/unnest -f $^ -v 5 -p 1A -n 1 -e iso-8859-15 > $@
temp/1951-2.tsv: temp/11804-8.txt
	../scripts/unnest -f $^ -v 5 -p 1A -n 2 -e iso-8859-15 > $@
temp/11803-8.txt: 11803
temp/11804-8.txt: 11804

1952: 1952-1A.tsv
temp/1952-1.tsv: temp/11805-8.txt
	../scripts/unnest -f $^ -v 6 -p 1A -n 1 -e iso-8859-15 > $@
temp/1952-2.tsv: temp/11806-8.txt
	../scripts/unnest -f $^ -v 6 -p 1A -n 2 -e iso-8859-15 > $@
temp/11805-8.txt: 11805
temp/11806-8.txt: 11806

1953: 1953-1A.tsv
temp/1953-1.tsv: temp/11807-8.txt
	../scripts/unnest -f $^ -v 7 -p 1A -n 1 -e iso-8859-15 > $@
temp/1953-2.tsv: temp/11808-8.txt
	../scripts/unnest -f $^ -v 7 -p 1 -n 2 -e iso-8859-15 > $@
temp/11807-8.txt: 11807
temp/11808-8.txt: 11808

1954: 1954-1.tsv
temp/1954-1.tsv: temp/11809-8.txt
	../scripts/unnest -f $^ -v 8 -p 1 -n 1 -e iso-8859-15 > $@
temp/1954-2.tsv: temp/11810-8.txt
	../scripts/unnest -f $^ -v 8 -p 1 -n 2 -e iso-8859-15 > $@
temp/11809-8.txt: 11809
temp/11810-8.txt: 11810

1955: 1955-1.tsv
temp/1955-1.tsv: temp/11811-8.txt
	../scripts/unnest -f $^ -v 9 -p 1 -n 1 -e iso-8859-15 > $@
temp/1955-2.tsv: temp/11812-8.txt
	../scripts/unnest -f $^ -v 9 -p 1 -n 2 -e iso-8859-15 > $@
temp/11811-8.txt: 11811
temp/11812-8.txt: 11812

1956: 1956-1.tsv
temp/1956-1.tsv: temp/11813-8.txt
	../scripts/unnest -f $^ -v 10 -p 1A -n 1 -e iso-8859-15 > $@
temp/1956-2.tsv: temp/11814-8.txt
	../scripts/unnest -f $^ -v 10 -p 1A -n 2 -e iso-8859-15 > $@
temp/11813-8.txt: 11813
temp/11814-8.txt: 11814

1957: 1957-1A.tsv
temp/1957-1.tsv: temp/11815-8.txt
	../scripts/unnest -f $^ -v 11 -p 1 -n 1 -e iso-8859-15 > $@
temp/1957-2.tsv: temp/11816-8.txt
	../scripts/unnest -f $^ -v 11 -p 1 -n 2 -e iso-8859-15 > $@
temp/11815-8.txt: 11815
temp/11816-8.txt: 11816

1958: 1958-1.tsv
temp/1958-1.tsv: temp/11817-8.txt
	../scripts/unnest -f $^ -v 12 -p 1 -n 1 -e iso-8859-15 > $@
temp/1958-2.tsv: temp/11818-8.txt
	../scripts/unnest -f $^ -v 12 -p 1 -n 2 -e iso-8859-15 > $@
temp/11817-8.txt: 11817
temp/11818-8.txt: 11818

1959: 1959-1.tsv
temp/1959-1.tsv: temp/11819-8.txt
	../scripts/unnest -f $^ -v 13 -p 1 -n 1 -e iso-8859-15 > $@
temp/1959-2.tsv: temp/11820-8.txt
	../scripts/unnest -f $^ -v 13 -p 1 -n 2 -e iso-8859-15 > $@
temp/11819-8.txt: 11819
temp/11820-8.txt: 11820


1960: 1960-1.tsv
temp/1960-1.tsv: temp/11821-8.txt
	../scripts/unnest -f $^ -v 14 -p 1 -n 1 -e iso-8859-15 > $@
temp/1960-2.tsv: temp/11822-8.txt
	../scripts/unnest -f $^ -v 14 -p 1 -n 2 -e iso-8859-15 > $@
temp/11821-8.txt: 11821
temp/11822-8.txt: 11822

1961: 1961-1.tsv
temp/1961-1.tsv: temp/11823-8.txt
	../scripts/unnest -f $^ -v 15 -p 1 -n 1 -e iso-8859-15 > $@
temp/1961-2.tsv: temp/11824-8.txt
	../scripts/unnest -f $^ -v 15 -p 1 -n 2 -e iso-8859-15 > $@
temp/11823-8.txt: 11823
temp/11824-8.txt: 11824

1962: 1962-1.tsv
temp/1962-1.tsv: temp/11825-8.txt
	../scripts/unnest -f $^ -v 16 -p 1 -n 1 -e iso-8859-15 > $@
temp/1962-2.tsv: temp/11826-8.txt
	../scripts/unnest -f $^ -v 16 -p 1 -n 2 -e iso-8859-15 > $@
temp/11825-8.txt: 11825
temp/11826-8.txt: 11826

1963: 1963-1.tsv
temp/1963-1.tsv: temp/11827-8.txt
	../scripts/unnest -f $^ -v 17 -p 1 -n 1 -e iso-8859-15 > $@
temp/1963-2.tsv: temp/11828-8.txt
	../scripts/unnest -f $^ -v 17 -p 1 -n 2 -e iso-8859-15 > $@
temp/11827-8.txt: 11827
temp/11828-8.txt: 11828

1964: 1964-1.tsv
temp/1964-1.tsv: temp/11829-8.txt
	../scripts/unnest -f $^ -v 18 -p 1 -n 1 -e iso-8859-15 > $@
temp/1964-2.tsv: temp/11810-8.txt
	../scripts/unnest -f $^ -v 18 -p 1 -n 2 -e iso-8859-15 > $@
temp/11829-8.txt: 11829
temp/11830-8.txt: 11830

1965: 1965-1.tsv
temp/1965-1.tsv: temp/11831-8.txt
	../scripts/unnest -f $^ -v 19 -p 1 -n 1 -e iso-8859-15 > $@
temp/1965-2.tsv: temp/11832-8.txt
	../scripts/unnest -f $^ -v 19 -p 1 -n 2 -e iso-8859-15 > $@
temp/11831-8.txt: 11831
temp/11832-8.txt: 11832

1966: 1966-1.tsv
temp/1966-1.tsv: temp/11833-8.txt
	../scripts/unnest -f $^ -v 20 -p 1 -n 1 -e iso-8859-15 > $@
temp/1966-2.tsv: temp/11834-8.txt
	../scripts/unnest -f $^ -v 20 -p 1 -n 2 -e iso-8859-15 > $@
temp/11833-8.txt: 11833
temp/11834-8.txt: 11834

1967: 1967-1.tsv
temp/1967-1.tsv: temp/11835-8.txt
	../scripts/unnest -f $^ -v 21 -p 1 -n 1 -e iso-8859-15 > $@
temp/1967-2.tsv: temp/11836-8.txt
	../scripts/unnest -f $^ -v 21 -p 1 -n 2 -e iso-8859-15 > $@
temp/11835-8.txt: 11835
temp/11836-8.txt: 11836

1968: 1968-1.tsv
temp/1968-1.tsv: temp/11837-8.txt
	../scripts/unnest -f $^ -v 22 -p 1 -n 1 -e iso-8859-15 > $@
temp/1968-2.tsv: temp/11838-8.txt
	../scripts/unnest -f $^ -v 22 -p 1 -n 2 -e iso-8859-15 > $@
temp/11837-8.txt: 11837
temp/11838-8.txt: 11838

1969: 1969-1.tsv
temp/1969-1.tsv: temp/11839-8.txt
	../scripts/unnest -f $^ -v 23 -p 1 -n 1 -e iso-8859-15 > $@
temp/1969-2.tsv: temp/11820-8.txt
	../scripts/unnest -f $^ -v 23 -p 1 -n 2 -e iso-8859-15 > $@
temp/11839-8.txt: 11839
temp/11820-8.txt: 11840

1970: 1970-1.tsv
temp/1970-1.tsv: temp/11841-8.txt
	../scripts/unnest -f $^ -v 24 -p 1 -n 1 -e iso-8859-15 > $@
temp/1970-2.tsv: temp/11842-8.txt
	../scripts/unnest -f $^ -v 24 -p 1 -n 2 -e iso-8859-15 > $@
temp/11841-8.txt: 11841
temp/11842-8.txt: 11842

1971: 1971-1.tsv
temp/1971-1.tsv: temp/11843-8.txt
	../scripts/unnest -f $^ -v 25 -p 1 -n 1 -e iso-8859-15 > $@
temp/1971-2.tsv: temp/11844-8.txt
	../scripts/unnest -f $^ -v 25 -p 1 -n 2 -e iso-8859-15 > $@
temp/11843-8.txt: 11843
temp/11844-8.txt: 11844

1972: 1972-1A.tsv
temp/1972-1.tsv: temp/11845-8.txt
	../scripts/unnest -f $^ -v 26 -p 1 -n 1 -e iso-8859-15 > $@
temp/1972-2.tsv: temp/11846-8.txt
	../scripts/unnest -f $^ -v 26 -p 1 -n 2 -e iso-8859-15 > $@
temp/11845-8.txt: 11845
temp/11846-8.txt: 11846

1973: 1973-1.tsv
temp/1973-1.tsv: temp/11847-8.txt
	../scripts/unnest -f $^ -v 27 -p 1 -n 1 -e iso-8859-15 > $@
temp/1973-2.tsv: temp/11848-8.txt
	../scripts/unnest -f $^ -v 27 -p 1 -n 2 -e iso-8859-15 -7 > $@
temp/11847-8.txt: 11847
temp/11848-8.txt: 11848

1974: 1974-1.tsv
temp/1974-1.tsv: temp/11849-8.txt
	../scripts/unnest -f $^ -v 28 -p 1 -n 1 -e iso-8859-15 -7 > $@
temp/1974-2.tsv: temp/11850-8.txt
	../scripts/unnest -f $^ -v 28 -p 1 -n 2 -e iso-8859-15 -7 > $@
temp/11849-8.txt: 11849
temp/11850-8.txt: 11850

1975: 1975-1.tsv
temp/1975-1.tsv: temp/11851-8.txt
	../scripts/unnest -f $^ -v 29 -p 1 -n 1 -e iso-8859-15 -7 > $@
temp/1975-2.tsv: temp/11852-8.txt
	../scripts/unnest -f $^ -v 29 -p 1 -n 2 -e iso-8859-15 -7 > $@
temp/11851-8.txt: 11851
temp/11852-8.txt: 11852

1976: 1976-1.tsv
temp/1976-1.tsv: temp/11853-8.txt
	../scripts/unnest -f $^ -v 30 -p 1 -n 1 -e iso-8859-15 -7 > $@
temp/1976-2.tsv: temp/11854-8.txt
	../scripts/unnest -f $^ -v 30 -p 1 -n 2 -e iso-8859-15 -7 > $@
temp/11853-8.txt: 11853
temp/11854-8.txt: 11854

1977: 1977-1.tsv
temp/1977-1.tsv: temp/11855-8.txt
	../scripts/unnest -f $^ -v 31 -p 1 -n 1 -e iso-8859-15 -7 > $@
temp/1977-2.tsv: temp/11856-8.txt
	../scripts/unnest -f $^ -v 31 -p 1 -n 2 -e iso-8859-15 -7 > $@
temp/11855-8.txt: 11855
temp/11856-8.txt: 11856

clean:
	cd temp && rm *
