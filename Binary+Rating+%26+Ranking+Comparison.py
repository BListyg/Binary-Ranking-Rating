
# coding: utf-8

# # Motivation / Background

# This write-up was inspired by Evan Miller's [excellent article on why average ratings shouldn't be used](http://www.evanmiller.org/how-not-to-sort-by-average-rating.html) when ranking internet comments, ranking items in an online marketplaces, etc. I was curious about the relationship between these "incorrect" ranking approaches and the Wilson Lower Bound he suggested. Essentially, I was curious about the rank-order correlation between these different approaches.
# 
# Below, I simulated random interger thumbs up / thumbs down data and computed four different scores:
# * Net positive (Positive scores minus negative scores)
# * Average rating (thumbs up scores divided by total ratings)
# * Positive per Negative (ratio of positive score to negative scores)
# * WLB
# 
# Next, I constructed a Spearman Rank-Order correlation matrix between these 4 values. Given the random data, it appears they are highly correlated with each other and produce essentially the same rank-ordered lists. This simulation leaves out highly skewed ratings of items (either positively or negatively), so that would be a potential future direction to address and would, given Evan's post, demonstrate how the WLB is superior to the other approches.

# # Analysis

# In[25]:


#importing modules
import numpy as np
import scipy.stats as st
import pandas as pd
import random
import string
import matplotlib.pyplot as plt


# In[26]:


#Creating ratings dataframe
#ID is random alphanumeric variable
#Postive/thumbs-up ratings
#Negative/thumbs-down ratings
ratings = pd.DataFrame({'id' : map(lambda x: ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(5)]), range(1000)), 
    'positive' : map(lambda x: random.randint(a=0,b=1000), range(1000)),
    'negative' : map(lambda x: random.randint(a=0,b=1000), range(1000))
})

#Incorrect solution 1, positive minus negative
ratings['score_!'] = ratings['positive'] - ratings['negative']

#Incorrect solution 2, positive divided by total
ratings['score_2'] = ratings['positive'] / (ratings['positive'] + ratings['negative'])

#Incorrect (potentially) solution 3, positive divided by negative
ratings['score_3'] = ratings['positive'] / ratings['negative']


# In[27]:


#Defining WLB function
def wlb(pos,n,confidence):
    if n == 0:
        return 0
    if n != 0:
        z = float(st.norm.ppf(1-((1-confidence)/2)))
        phat = float(pos)/float(n)
        return (phat + z*z/(2*n) - z * np.sqrt((phat*(1-phat)+z*z/(4*n))/n))/(1+z*z/n)


# In[28]:


#Obtaining 95% lower bound on proportion of positive ratings
ratings['lower_bound'] = np.vectorize(wlb)(ratings['positive'], ratings['positive']+ratings['negative'], 0.95)


# In[29]:


#Viewing data
ratings.head()


# In[34]:


#Confirming values are equal
wlb(pos=1000,n=1596,confidence=0.95) #confirming WLB with rating data


# In[31]:


#Changing column names for ranking dataframe to differentiate from rating df
rankings = pd.DataFrame.rank(ratings.iloc[:,3:7])

rankings.columns = "rankings_" + rankings.columns

rankings.head()


# # Final data

# In[32]:


#Combining ratings and rankings dataframes
final_data = pd.concat([ratings.reset_index(drop=True), rankings], axis=1)

final_data.head()


# # Results

# In[33]:


#Rank-order correlation matrix between 4 rating approaches
pd.DataFrame(st.spearmanr(final_data.iloc[:,7:11])[0])


# # Conclusions

# Given the random data I generated, it appears that these 4 approaches yield nearly identical rank-ordered lists (completely identical in the case of score_2 and score_3). One thing to note is that these four ranking approaches may return different rank-orders with items that have highly skewed ratings. Additionally, examining rank-order changes over time (i.e. if any item being ranked undergoes changes in product features) would be interesting to observe as well.
