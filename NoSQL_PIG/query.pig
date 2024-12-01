-- Load data from the triples.txt file using comma as a delimiter
data = LOAD '/Users/varshithvattikuti/Desktop/NoSQL_PIG/triples.txt' USING PigStorage(',') AS (subject:chararray, predicate:chararray, object:chararray);

-- Filter data to find a specific subject
queried_data = FILTER data BY subject == '$subject';

-- Dump the filtered results to the console
DUMP queried_data;

