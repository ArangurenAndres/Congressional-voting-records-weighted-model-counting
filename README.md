# Congressional-voting-records-weighted-model-counting
Given the congressional voting records consisting on the votes for each of the US representatives congressmen on 16 votes, compute the weights of the given set of formulas

## Dataset
 Number of observations : 435
 Votes: 16



The applied procedure consists on:

1. Transforms formulas into CNF form
2. Create a boolean matrix based on the input proposition 
3. Based on the selected formula and the boolean matrix create a column vector which contains whether the formula satisfies or not.
4. Using the boolean column vector filter the dataset and extract the true values
5. Calculate weight of the selected formula: 
