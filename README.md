# Catalog of Copyright Entries Renewals

## Tab-delimited Copyright Renewals, 1950–1991

These files contain, in tab-delimited format, copyright renewals from the US Copyright Office's _Catalog of Copyright Entries_ for the years 1950–1977 (based on [Project Gutenberg transcriptions](https://www.gutenberg.org/ebooks/search/?query=11800) and data from the [Copyright Office's database](https://cocatalog.loc.gov/cgi-bin/Pwebrecon.cgi?DB=local&PAGE=First) for 1978–1991, with a sprinkling of later years (based on [data made available by Google](https://booksearch.blogspot.com/2008/06/us-copyright-renewal-records-available.html)). Renewals from 1950 are not strictly relevant since all books renewed that year are now (2019) public domain, but they are included here for completeness.

Though similar to Stanford's [Copyright Renewals](https://exhibits.stanford.edu/copyrightrenewals) database, the primary aim of this dataset is to fully parse out all the registration and renewal ids and dates so that we can better (and automatically) match renewals to the registrations we have been transcribing for our [Catalog of Copyright Entries project](https://github.com/NYPL/catalog_of_copyright_entries_project).

## Anatomy of a Renewal

Most renewal entries simply contain a title and author followed the date and id number of the copyright registration being renewed, the "claimant" or rights-holder making the renewal with a code such as `(A)` (author) or `(C)` (child or children), and finally the renewal date and id. For example:

      Strangers on a train. By Mary Patricia
    Highsmith. © 15Mar50; A41904. Mary
    Patricia Highsmith (A); 6Jun77; R663598.

This renewal corresponds to a registration:

    HIGHSMITH, PATRICIA.
      Strangers on a train. [1st ed.] New 
      York, Harper. 299 p. © Mary Patricia 
      Highsmith; 15Mar50; A41904.
      
Together, these two entries record that the copyright for this book was registerd on March 15, 1950 and renewed by the author on June 6, 1977.

Registration ids like `A41904` are not unique because the numbering started over in 1947 with the beginning of the 3rd series of the _Catalog_, so in order to match a renewal with a registration it is necessary to match _both_ the id number (`A41904`) _and_ date (`15Mar50`)

This is converted into a row of tab-delimtied data (not all fields shown):

| author | title | oreg | odat | rdat | id | claimants |
| ------ | ----- | ---- | ---- | ---- | --- | --------- |
| Mary Patricia Highsmith | Strangers on a train. | A41904 | 1950-03-15 | R663598 | 1977-06-06 | Mary Patricia Highsmith\|A |


Often more than one registration is involved, such as when a book is first published outside the United States and has an "interim" registration (class AI) before it's final registration:

    First crossing of the Polar Sea, by
      Roald Amundsen and Lincoln Ellsworth;
      with additional chapters by
      other members of the expedition.
      (Pub. abroad under title: The first
      flight across the Polar Sea)
      © 15Apr27; (pub. abroad 25Feb27,
      AI-9217); A972756. Mary-Louise
      Ellsworth (W); 19Apr54; R129296.
      
This renewal refers to both the interim registration, `AI-9217`, and final registration `A972756`. This illustrates the importance of the id numbers, since the two original registrations have two different titles and wouldn't be clear otherwise that they are the same book. This would be converted into _two_ rows of data (again, not all fields shown):

| author | title | oreg | odat | rdat | id | claimants |
| --- | --- | --- | --- | --- | --- | --- |
| Roald Amundsen and Lincoln Ellsworth | First crossing of the Polar Sea | A972756 | 1927-04-15 | R129296 | 1954-04-19 | Mary-Louise Ellsworth\|W |
| Roald Amundsen and Lincoln Ellsworth | First crossing of the Polar Sea | AI9217 | 1927-02-25 | R129296 | 1954-04-19 | Mary-Louise Ellsworth\|W |

This allows us to easily match the two registrations found in the _Catalog_.

Note that dates are converted to `YYYY-MM-DD` format and there is some regularization of id numbers (for instance `AI-9217` changed to `AI9217`).

## Differences from Stanford Copyright Renewals

In 2007 Stanford University Libraries and Academic Information Resources launched a [copyright renewals database](https://exhibits.stanford.edu/copyrightrenewals) covering the same material.  The Stanford database is intended to make it simple to find a book by published before 1964 by author or title and see whether or not its copyright has been renewed. While [transcribing and parsing the original book registration entries](https://github.com/NYPL/catalog_of_copyright_entries_project) at NYPL we have relied extensively on this data, but our task is a little different since we would like to accurately match every registered entry with a renewal _or not_. The data in this repository is organized to make it easier to accurately match a registration ID and date with a renewal if it exists and to reduce the number of false negatives so that we can be confident the _lack_ of a match means the copyright wasn't renewed. It differs from the Stanford data in a few areas.

You can download a comma-delimited copy of Stanford's data ([latest version](http://web.stanford.edu/dept/SUL/collections/copyrightrenewals/files/20170427-copyright-renewals-records.csv.zip)) which contains 246,448 renewal records.

### Non-book entries

Stanford's data includes only "Book" or "Class A" registrations. In our CCE project we are transcribing the "Book" volumes of the _Catalog_ (Part 1, Group 1, 1923–1946; Part 1A, 1947–1953; Part 1, 1953–1964) which include some registrations for classes other than "A" (about 2% of registration entries), though many of these would be considered books despite the classification. If any of these have renewals, they would be excluded from the Stanford data, creating false negatives.

This dataset contains all the Part 1, Group 1 and 2 (1923–1946), Part 1A and 1B (1947–1953) and Part 1 (1953–1964, two previous groups combined) renewals transcribed by Project Gutenberg as well as renewals for _all_ classes from the Google dataset (over 445,000 renewals altogether) derived from the Copyright Office database.

### Unrolling of batch renewals

Many renewal entries actually contain multiple renewals or registrations. These might be multiples of both registrations and renewals, or they might be multiple registrations renewed under a single renewal ID (the reverse is also possible). Special effort has been made to "unroll" these entries so that every row contains a unique combination of registration id, registration date and renewal id, and so that every id is accounted for. For example, this entry ([1958, vol. 12.1.1 p. 764](https://archive.org/stream/catalogofcopyrig3121lib#page/764/mode/1up))

    RULING CASE LAW. 1930 supplement,
      continuing Permanent supplement
      ed. Vol. 1-28. © 24May30; A23877-23904.
      Lawyers Co-operative Pub.
      Co. & Bancroft-Whitney Co. (PCW);
      28Apr58; R213954-213981.

Is converted into 28 rows, each with the proper registration and renewal id so that they can all be matched to our registration data entries. A unique ID is assigned to each entry before unrolling, so each of these 28 rows carries an ID tying them back to the original entry.

In the Stanford data for this entry each renewal id is separate, but they are all assigned to the same registration id, [`A23877`](https://exhibits.stanford.edu/copyrightrenewals/catalog?utf8=%E2%9C%93&exhibit_id=copyrightrenewals&search_field=search&q=A23877), allowing one match but causing 27 false negatives.

_Conversely_ many records in this dataset do not have authors or titles parsed into the proper fields, so it is less useful for that kind of searching.

### Registration numbers and dates

Similar to how multiple registrations are handled, when a renewal records an "interim" (class AI) or foreign (class AF) registration followed by a regular, class A, registration, the Stanford data usually has the date from the earlier registration with the id from the later one. This leads to false negatives when matching registrations because registration must be matched by registration id _and_ date. For instance, this renewal ([1962, vol 16.1.1, p. 914](https://archive.org/stream/catalogofcopyrig3161libr#page/914/mode/1up)) `R294052` is linked in the Stanford data to the registration id [`A79921` and date `29Oct34`](https://exhibits.stanford.edu/copyrightrenewals/catalog?utf8=%E2%9C%93&exhibit_id=copyrightrenewals&search_field=search&q=A79921).

    THIRKELL, ANGELA.

      The demon in the house. © 29Oct34,
        AI-19786; 4Mar35, A79921. Lancelot
        George Thirkell, Colin McInnes &
        Graham Campbell McInnes (C);
        30Mar62; R294052.
		
This is not an issue for the ways in which someone is likely to use Stanford's database to look up by author's name, title, or registration id if they have it.

However, in the CCE registration data there are two relevant entries and we need to be able to link them to this renewal by the correct number _and_ date pairs: [`AI-19786/1934-10-29`](https://archive.org/stream/catalogueofcopy311libr#page/1790/mode/1up) and [`A79921/1935-03-04`](https://archive.org/stream/catalogofcopyri321libr#page/223/mode/1up). There is no CCE registration with the combination `A79921/1934-10-29` so the Stanford data gives a false negative in this case (actually two).  In this dataset there are two rows for `R294052`, one for each of the proper date/number pairs.

Registration entries in the _Catalog_ don't always indicate that there was a previous interim registration, so it is a happy side-effect that we can link the two via their common renewal.

## Data Structure

Tab-delimited files have the following structure:

| Field | Explanation | Example |
|--- | --- | --- |
| entry\_id | A UUID for the entry from which the row was parsed | 2e8b17ae-d4a9-52f3-8774-0ec7597cb93d |
| volume | Source volume | 8 |
| part | Source volume part | 1 |
| number | Source volume number | 1 |
| page	| Source volume page | |
| author |  |
| title | |
| oreg | Original registration id number. | A972756 |
| odat | Original registration date, in YYYY-MM-DD format | 1927-04-15 |
| id | Renewal id number | R129296 |
| rdat | Renewal date, in YYYY-MM-DD format | 1954-04-19 |
| claimants | Copyright claimants of the renewal and class code. Claimants and code separated by a pipe (\|), multiple claimaints separated by a double pipe (\|\|) |Mary-Louise Ellsworth\|W |
| new_matter | Indicates material being renewed if it not the text as a whole| pref. and revisions |
| see\_also\_ren | Related renewal ids | |
| see\_also\_reg | Related registration ids | |
| notes | |
| full\_text | Full text of the source entry | |

Every row is guaranteed to have `entry_id`, `volume`, `part`, `number`, `page`, and `full_text` fields. If all other fields are empty it means that the entry could not be parsed.

Except for entries that could not be parsed at all, every row will have `oreg`, `odat`, `id`, `rdat` fields, which are sufficient for matching to registration data.

Wherever possible, the remaining fields are parsed and populated.

All dates are converted to `YYYY-MM-DD` format.

In registration ids, all hyphens are removed except those that separate a class ending with a digit from the serial number part of the id. For instance `AI-9217` is normalized to `AI9217`, but the hyphen is kept in `B5-73742`.

The class code `RE` in later renewal ids is normalized to `R`.

In the database derived data (1978-) ids are padded internally with 0's, which are removed. For instance `A00000366051` is normalized to `A366051` and, combined with the previous rule, `RE0000736790` is normalized to `R736790`.

## Corrections

Some errors in the transcription become apparent either because they cause the parsing to fail or because they are easy to detect once the data can be queried. Where errors have been found in the Project Gutenberg transcriptions, these are fixed by applying patches (found in the `data/pre-patches` directory) before processing the files. Using patches means there is a clear record of what is being changed and we don't have to maintain a separate, corrected copy of the files. It will be apparent if the source files are ever updated because applying the patches will fail.

Some rows are simply difficult to parse automatically. Rather than adding complexity to the parsing code to a handle a small number of cases, another set of patches (from the `data/post-patches` directory) are applied _after_ processing to the generated TSV files. This is a very fidgety process, however, and it kept to a minimum.

## Building the dataset yourself

It should be possible to rebuild the dataset on any sufficiently Unix-like system, by cloning this repository, switching to the `data` directory and running `make`. This will:

- For Gutenberg files
  - Download the Gutenberg source files
  - Apply patches in the `data/pre-patch` directory to the Gutenberg files to correct errors and typos
  - "Unnest" the Guteberg files (by running them through `unnest.py`
  - Concatenate parts into one file for each volume
  - Parse each volume file (by running them through `parse.py`) to generate tab-delimited files
  - Apply patches in the `data/post-patch` directory to the tab-delimited files.
- For Google data
  - Download and unzip the Google data
  - Generate a tab-delimited file for each year, starting with 1978, from the XML (by running `expl-google-cce` once for each year)

This pipline requires:

- `make`
- `wget`
- `python` 3.5 or greater 
- `patch`
