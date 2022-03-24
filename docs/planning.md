# Structure

## Barchart
The Barchart object stores all the information in an eBird bar chart data text file.

## Summarizer
The Summarizer stores data from multiple Barcharts.
This has a bunch of core observation data, and then a bunch of metadata
### Core data
This includes:
 - Loc_ids for each included hotspot
 - names for each included hotspot
 - observation data for each included hotspot
### Metadata
 - A name for the overall summary
 - whether each hotspot is currently included or excluded from the analysis
 - a set of species included in the summary
 - a set of sub species level taxa in the summary

## CLI
The CLI can collect barchart files, read their filenames and contents, and use that information to instantiate Barchart objects
 - get folder with barcharts in itS
 - identify ebird Batcharts
 - read them all and pass their info to Barchart objects
 - construct a Summary object from those barcharts.
 -
