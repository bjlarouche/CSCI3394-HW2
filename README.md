# CSCI3394-HW2
## Q2. Blockchain Puzzle (5 pt)

Write a program that estimates the time of solving hash-based puzzle given a specific difficulty. Draw a box-plot which has x-axis as difficulty (specified as a 256-bit unsigned integer), and y-axis as time consumed. Concretely:
1. Create a data structure for the bitcoin block header (as specified in lecture slide).
2. You can use some random number as the hash parts of the header.
3. Solve the puzzle under different difficulty level and record the data point. For each difficulty, get at least five data points.
4. I don’t want to burn your laptop, so if you cannot solve a puzzle in ~5 minutes for difficulty d, you don’t need to collect the data for any difficulty beyond d.
5. Generate a box plot.

What to submit:
- Upload your code to Github
- Include the link to the code and the plot in your solution. Moreover, you need to include the specification of your machine.
- BONUS (up to 1pt): conduct this part on different machines with different computation power (or changing number of core used) and draw a meaningful plot that demonstrate the difference.

