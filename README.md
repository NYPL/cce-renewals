# Catalog of Copyright Entries Renewals

## Tab-delimited Copyright Renewals, 1950–1991

These files contain, in tab-delimited format, copyright renewals from the US Copyright Office's _Catalog of Copyright Entries_ for the years 1950–1977 (based on [Project Gutenberg transcriptions](https://www.gutenberg.org/ebooks/search/?query=11800) and data from the [Copyright Office's database](https://cocatalog.loc.gov/cgi-bin/Pwebrecon.cgi?DB=local&PAGE=First) for 1978–1991, with a sprinkling of later years (based on [data made available by Google](https://booksearch.blogspot.com/2008/06/us-copyright-renewal-records-available.html)). Renewals from 1950 are not strictly relevant since all books renewed that year are now public domain, but they are included here for completeness.

## Differences from Stanford Copyright Renewals

In 2007 Stanford University Libraries and Academic Information Resources launched a [copyright renewals database](https://exhibits.stanford.edu/copyrightrenewals) covering the same material. You can download a comma-delimited copy of their underlying data ([latest version](http://web.stanford.edu/dept/SUL/collections/copyrightrenewals/files/20170427-copyright-renewals-records.csv.zip)) which contaiins 246,448 renewal records. The Stanford database is intended to make it simple to a book by published before 1964 author or title and see whether or not its copyright haf been renewed. While [transcribing and parsing the original book registration entries](https://github.com/NYPL/catalog_of_copyright_entries_project) (CCE Project) at NYPL we have worked extensively with this data, but our task is a little different since we would like to accurately match every registered entry with a renewal _or not_. The data in this repository is organized to make it easier to match a registration ID and date with a renewal if it exists, so it differs from the Stanford data in a few areas.

### Non-book entries

Stanford's data includes only "Book" or "Class A" registrations. In our CCE project we are transcribing the Book volumes (Part 1, Group 1, 1923–1946; Part 1A, 1947–1953; Part 1, 1953–1964) which include some non-book registrations (about 2% of registration entries). If any of these have renewals, they would be excluded from the Stanford data.

This dataset contains all the Part 1, Group 1 and 2 (1923–1946), Part 1A and 1B (1947–1953) and Part 1 (1953–1964, two previous groups combined) renewals transcribed by Project Gutenberg as well as renewals for _all_ classes from the Google dataset (almost 445,000 renewals altogether).

### Unrolling of batch renewals

Many renewal entries actually contain multiple renewals or registrations. These might be multiples of both registrations and renewals, or they might be multiple registrations renewed under a single renewal ID (the reverse is also possible). Special effort has been made to "unroll" these entries so that every row contains a unique combination of registration id, registration date and renewal id, and so that every id is accounted for. For example, this entry ([1958, vol. 12.1.1 p. 764](https://archive.org/stream/catalogofcopyrig3121lib#page/764/mode/1up))

    RULING CASE LAW. 1930 supplement,
      continuing Permanent supplement
      ed. Vol. 1-28. © 24May30; A23877-23904.
      Lawyers Co-operative Pub.
      Co. & Bancroft-Whitney Co. (PCW);
      28Apr58; R213954-213981.

Is converted into 28 rows, each with the proper registration and renewal id so that they can all be matched to our registration data entries. A unique ID is assigned to each entry before unrolling, so each of these 28 rows carries an ID tying them back to the original entry.

In the Stanford data, each renewal id is separate, but they are all assigned to the same registration id, [`A23877`](https://exhibits.stanford.edu/copyrightrenewals/catalog?utf8=%E2%9C%93&exhibit_id=copyrightrenewals&search_field=search&q=A23877).

_Conversely_ many records in this dataset do not have authors or titles parsed into the proper fields, so it is less useful for that kind of searching.

### Registration numbers and dates

Similar to how multiple registrations are handled, when a renewal records an "interim" (class AI) or foreign (class AF) registration followed by a regular, class A, registration, the Stanford data usually has the date from the earlier registration with the id from the later one. This leads to false negatives when matching registrations because registration numbers are not unique and each entry must be matched by registration id _and_ date. For instance, this renewal ([1962, vol 16.1.1, p. 914](https://archive.org/stream/catalogofcopyrig3161libr#page/914/mode/1up):

    THIRKELL, ANGELA.

      The demon in the house. © 29Oct34,
        AI-19786; 4Mar35, A79921. Lancelot
        George Thirkell, Colin McInnes &
        Graham Campbell McInnes (C);
        30Mar62; R294052.
		
In the Stanford data, `R294052` is linked to the registration id [`A79921`](https://exhibits.stanford.edu/copyrightrenewals/catalog?utf8=%E2%9C%93&exhibit_id=copyrightrenewals&search_field=search&q=A79921) and date `29Oct34`. This is not an issue for the ways in which someone is likely to use this database: to look up by author's name, title, or registration id if they have it.

However, in the CCE registration data there are two relevant entries but we need to be able to link them to this renewal by the correct number _and_ date pairs: [`AI-19786/1934-10-29`](https://archive.org/stream/catalogueofcopy311libr#page/1790/mode/1up) and [`A79921/1935-03-04`](https://archive.org/stream/catalogofcopyri321libr#page/223/mode/1up). There is no CCE registration with the combination `A79921/1934-10-29` so the Stanford data gives a false negative in this case.  In this dataset there are two rows for `R294052`, one for each of the proper date/number pairs.

Registration entries don't always indicate that there was a previous interim registration, so it is a happy side-effect that we can link the two via their common renewal.

Also, note that all dates are converted to `YYYY-MM-DD` format.
