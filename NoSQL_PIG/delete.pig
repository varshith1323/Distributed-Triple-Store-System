-- Load data
data = LOAD '/Users/varshithvattikuti/Desktop/NoSQL_PIG/triples.txt' USING PigStorage(',') AS (subject:chararray, predicate:chararray, object:chararray);

-- Filter out the specific triplet
filtered_data = FILTER data BY NOT (subject == '$subject' AND predicate == '$predicate' AND object == '$object');

-- Store the filtered data temporarily
STORE filtered_data INTO '/Users/varshithvattikuti/Desktop/NoSQL_PIG/deleted_triples' USING PigStorage(',');

