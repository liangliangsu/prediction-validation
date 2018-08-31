# The prediction validation challenge

## Run
You can run the code with the following command: ./run.sh       
Code is involved in folder src. Code is written in Python3 langauge. No external library is imported, only sys and re library are imported. 

## Testing
This code is fully tested with different sliding window sizes. Check process is passed in run_tests.sh!

## Steps of solution
1. Read dataset from input folder line by line.
2. Split the records from each line and check the line is splited correctly.
3. Preprocess the data and store value in designed dictionary. Hour number is first key, stock name is second key.
4. Compute sum error, count of matched stocks in each hour. The results are stored in lists based on time stream order.
5. Read sliding window size from inputfile. Compute average error for each sliding window from previous results.
6. Convert results to desired format and write outputs into output file.
