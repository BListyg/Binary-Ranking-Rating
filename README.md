# Binary-Ranking-Rating
Comparing rank orders of different binary scoring approaches for arbitrary "items" (comments on a message board, widgets in an online marketplace, etc.)

This small write-up examines the similarity between ranked lists of items that have been rated using four different approaches:

* A net positive score (positive ratings minus negative ratings)
* A positive proportion (positive ratings divided by total ratings)
* A positive per negative ratio (positive ratings divided by negative ratings)
* The Wilson Lower Bound

I find that, when applied to randomly generated data, all approaches yield essentially the same rank-ordering. 
