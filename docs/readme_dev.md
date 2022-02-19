# README for devs
This is an attempt to explain the way some important parts of this project work. Until I actually write this, it's going to be very sketchy, and only capture the key stuff.

## Barcharts 
 - Converts fractional information in eBird bar chart files to integers
 - One list of sample sizes, with one entry per period.
 - A list of observations per taxa, one entry per period.
    - The sample sizes are the total number of checklists submitted during that period
    - The observations are the number of those checklists that contained this species.

## Summary