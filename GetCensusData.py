#!/usr/bin/env python
# coding: utf-8

# In[2]:


# Dependencies
# Dependencies
import pandas as pd
import numpy as np
import requests
import json
import xmltodict

# GreatSchools API Key
from keys import api_keys


# In[3]:


df = pd.read_csv("data/AustinSchools.csv", index_col=0)
df.head()


# In[21]:


def get_census_data(gsId):   
    census_url = "https://api.greatschools.org/school/census/TX/{0}?key={1}".format(gsId,api_keys.api_key)
    census = xmltodict.parse(requests.get(census_url).content)['census-data']
    return census


# In[ ]:


df["census"] = df["gsId"].apply(get_census_data)


# In[ ]:


df["freeAndReducedPriceLunch"] = df["census"].freeAndReducedPriceLunch


# In[ ]:


df.head()

