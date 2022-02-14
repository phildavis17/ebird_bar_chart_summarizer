# Structure

## Barchart
The Barchart object stores all the information in an eBird bar chart data text file.

## Summarizer
The Summarizer stores data from multiple Barcharts. 

## CLI
The CLI can collect barchart files, read their filenames and contents, and use that information to instantiate Barchart objects
 - get folder with barcharts in itS
 - identify ebird Batcharts
 - read them all and pass their info to Barchart objects
 - construct a Summary object from those barcharts.
 - 