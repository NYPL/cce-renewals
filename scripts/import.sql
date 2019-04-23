begin;

drop table if exists renewals_temp;
create table renewals_temp (
       entry_id uuid,
       volume int,
       part text,
       number int,
       page int,
       author text,
       title text,
       oreg text,
       odat date,
       id text,
       rdat date,
       claimants text,
       previous text,
       new_matter text,
       see_also_ren text,
       see_also_reg text,
       notes text,
       full_text text
);

\copy renewals_temp from 1950-14A.tsv csv delimiter E'\t' header
\copy renewals_temp from 1951-1A.tsv csv delimiter E'\t' header
\copy renewals_temp from 1952-1A.tsv csv delimiter E'\t' header
\copy renewals_temp from 1953-1A.tsv csv delimiter E'\t' header
\copy renewals_temp from 1954-1.tsv csv delimiter E'\t' header
\copy renewals_temp from 1955-1.tsv csv delimiter E'\t' header
\copy renewals_temp from 1956-1.tsv csv delimiter E'\t' header
\copy renewals_temp from 1957-1.tsv csv delimiter E'\t' header
\copy renewals_temp from 1958-1.tsv csv delimiter E'\t' header
\copy renewals_temp from 1959-1.tsv csv delimiter E'\t' header
\copy renewals_temp from 1960-1.tsv csv delimiter E'\t' header
\copy renewals_temp from 1961-1.tsv csv delimiter E'\t' header
\copy renewals_temp from 1962-1.tsv csv delimiter E'\t' header
\copy renewals_temp from 1963-1.tsv csv delimiter E'\t' header
\copy renewals_temp from 1964-1.tsv csv delimiter E'\t' header
\copy renewals_temp from 1965-1.tsv csv delimiter E'\t' header
\copy renewals_temp from 1966-1.tsv csv delimiter E'\t' header
\copy renewals_temp from 1967-1.tsv csv delimiter E'\t' header
\copy renewals_temp from 1968-1.tsv csv delimiter E'\t' header
\copy renewals_temp from 1969-1.tsv csv delimiter E'\t' header
\copy renewals_temp from 1970-1.tsv csv delimiter E'\t' header
\copy renewals_temp from 1971-1.tsv csv delimiter E'\t' header
\copy renewals_temp from 1972-1.tsv csv delimiter E'\t' header
\copy renewals_temp from 1973-1.tsv csv delimiter E'\t' header
\copy renewals_temp from 1974-1.tsv csv delimiter E'\t' header
\copy renewals_temp from 1975-1.tsv csv delimiter E'\t' header
\copy renewals_temp from 1976-1.tsv csv delimiter E'\t' header
\copy renewals_temp from 1977-1.tsv csv delimiter E'\t' header
\copy renewals_temp from 1978-from-db.tsv csv delimiter E'\t' header
\copy renewals_temp from 1979-from-db.tsv csv delimiter E'\t' header
\copy renewals_temp from 1980-from-db.tsv csv delimiter E'\t' header
\copy renewals_temp from 1981-from-db.tsv csv delimiter E'\t' header
\copy renewals_temp from 1982-from-db.tsv csv delimiter E'\t' header
\copy renewals_temp from 1983-from-db.tsv csv delimiter E'\t' header
\copy renewals_temp from 1984-from-db.tsv csv delimiter E'\t' header
\copy renewals_temp from 1985-from-db.tsv csv delimiter E'\t' header
\copy renewals_temp from 1986-from-db.tsv csv delimiter E'\t' header
\copy renewals_temp from 1987-from-db.tsv csv delimiter E'\t' header
\copy renewals_temp from 1988-from-db.tsv csv delimiter E'\t' header
\copy renewals_temp from 1989-from-db.tsv csv delimiter E'\t' header
\copy renewals_temp from 1990-from-db.tsv csv delimiter E'\t' header
\copy renewals_temp from 1991-from-db.tsv csv delimiter E'\t' header
\copy renewals_temp from 1992-from-db.tsv csv delimiter E'\t' header
\copy renewals_temp from 1993-from-db.tsv csv delimiter E'\t' header
\copy renewals_temp from 1995-from-db.tsv csv delimiter E'\t' header
\copy renewals_temp from 1996-from-db.tsv csv delimiter E'\t' header
\copy renewals_temp from 2001-from-db.tsv csv delimiter E'\t' header

create index on renewals_temp(oreg);
create index on renewals_temp(odat);

commit;
