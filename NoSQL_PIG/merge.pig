-- Load data from two files
data1 = LOAD '/home/iiitb/Downloads/nosqlproject/input/file1.txt' USING PigStorage(',') AS (subject:chararray, predicate:chararray, object:chararray);
data2 = LOAD '/home/iiitb/Downloads/nosqlproject/input/file2.txt' USING PigStorage(',') AS (subject:chararray, predicate:chararray, object:chararray);

-- Combine the data from both files
combined_data = UNION data1, data2;

-- Remove duplicates
deduped_data = DISTINCT combined_data;

-- Store the merged data temporarily
STORE deduped_data INTO '/home/iiitb/Downloads/nosqlproject/output/merged_triples' USING PigStorage(',');

