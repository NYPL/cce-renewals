# Catalog of Copyright Entries Renewals

## Tab-delimited Copyright Renewals, 1950–1991

These files contain, in tab-delimited format, copyright renewals from the US Copyright Office's _Catalog of Copyright Entries_ for the years 1950–1977 (based on [Project Gutenberg transcriptions](https://www.gutenberg.org/ebooks/search/?query=11800) and data from the [Copyright Office's database](https://cocatalog.loc.gov/cgi-bin/Pwebrecon.cgi?DB=local&PAGE=First) for 1978–1991, with a sprinkling of later years (based on [data made available by Google](https://booksearch.blogspot.com/2008/06/us-copyright-renewal-records-available.html)). Renewals from 1950 are not strictly relevant since all books renewed that year are now public domain, but they are included here for completeness.

## Differences from Stanford Copyright Renewals

In 2007 Stanford University Libraries and Academic Information Resources launched a [copyright renewals database](https://exhibits.stanford.edu/copyrightrenewals) covering the same material. You can download a comma-delimited copy of their underlying data ([latest version](http://web.stanford.edu/dept/SUL/collections/copyrightrenewals/files/20170427-copyright-renewals-records.csv.zip)) which contaiins 246,448 renewal records. The Stanford database is intended to make it simple to a book by published before 1964 author or title and see whether or not its copyright haf been renewed. While [transcribing and parsing the original book registration entries](https://github.com/NYPL/catalog_of_copyright_entries_project) (CCE Project) at NYPL we have worked extensively with this data, but our task is a little different since we would like to accurately match every registered entry with a renewal _or not_. The data in this repository is organized to make it easier to match a registration ID and date with a renewal if it exists, so it differs from the Stanford data in a few areas.

### Unrolling of batch renewals

Many renewal entries actually contain multiple renewals or registrations. These might be multiples of both registrations and renewals, or they might be multiple registrations renewed under a single renewal ID (the reverse is also possible). Special effort has been made to "unroll" these entries so that every row contains a unique combination of registration id, registration date and renewal id, and so that every id is accounted for. For example, this entry ([1958, vol. 12.1.1 p. 764](https://archive.org/stream/catalogofcopyrig3121lib#page/764/mode/1up))

    RULING CASE LAW. 1930 supplement,
      continuing Permanent supplement
      ed. Vol. 1-28. © 24May30; A23877-23904.
      Lawyers Co-operative Pub.
      Co. & Bancroft-Whitney Co. (PCW);
      28Apr58; R213954-213981.

Is converted into 28 rows, each with the proper registration and renewal id so that they acan all be matched to our registration data entries. In the Stanford data, each renewal id is separate, but they are all assigned to the same registration id, `A23877`.

_Conversely_ many records in this dataset do not have authors or titles parsed into the proper fields, so it is less useful for that kind of searching.

### Non-book entries

Stanford's data includes only "Book" or "Class A" registrations. In our CCE project we are transcribing the Book volumes (Part 1, Group 1, 1923–1946; Part 1A, 1947–1953; Part 1, 1953–1964) which include some non-book registrations (about 2% of registration entries). If any of these have renewals, they would be excluded from the Stanford data, but possibly included in the Project Gutenberg transcriptions.

### Registration numbers and dates

Handling of registration numbers and dates. Every registration has a registration number. These numbers are not unique, since the numbering starts over with the end of the "new series" volumes and begining of the "3rd series" in 1947. Therefore registrations need to be referenced by registration number _and_ date. For instance, `A100018` is not unique, we need to distinguish between `A100018/1936-09-15` and `A100018/1953-07-03.` In addition, books published outside the US often have an "interim" (class AI) or foreign (class AF) registration, followed by a regular, class A, registration. Both these registrations may be referenced in the renewal as they are, for instance, in the renewal `R201484`: `© 10Apr30, AI-13947; 22Aug30, A27120.` In these cases Stanford's data may only record the interim date with the regular registration number, that is `A27120/1930-04-10` which doesn't match either of our CCE project records `AI13947/1930-04-10` (where the date matches the renewal) or `A27120/1930-08-22` (where the number matches).


