-- Load original data
data = LOAD '/Users/varshithvattikuti/Desktop/NoSQL_PIG/triples.txt' USING PigStorage(',') AS (subject:chararray, predicate:chararray, object:chararray);

-- Debug: Dump initial data to verify it's being read correctly
DUMP data;

-- Separate existing triples that match the new subject and predicate
matching_triples = FILTER data BY (subject == '$new_subject' AND predicate == '$new_predicate');
non_matching_triples = FILTER data BY NOT (subject == '$new_subject' AND predicate == '$new_predicate');

-- Debug: Dump data after filtering to verify the filters are working as expected
DUMP matching_triples;
DUMP non_matching_triples;

-- Use a Pig Latin hack to create a single tuple from parameters
-- Generate the new or updated triple
new_triples = FOREACH (LIMIT data 1) GENERATE '$new_subject' AS subject, '$new_predicate' AS predicate, '$new_object' AS object;

-- Debug: Dump the new triples to ensure they are created correctly
DUMP new_triples;

-- Combine non-matching data with the new or updated triplet
combined_data = UNION non_matching_triples, new_triples;

-- Debug: Dump combined data to verify correct union of data
DUMP combined_data;

-- Store the updated data
STORE combined_data INTO '/Users/varshithvattikuti/Desktop/NoSQL_PIG/updated_triples.txt' USING PigStorage(',');
