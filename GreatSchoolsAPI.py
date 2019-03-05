#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Dependencies
# Dependencies
import pandas as pd
import numpy as np
import requests
import json
import xmltodict

# GreatSchools API Key
from keys import api_keys


# In[2]:


f = open('output/fieldErrors.txt','w')

def extract(school, field):
    try:
        return school[field]
    except Exception as e:
        f.write("{}: {}".format(type(e), e))
        return np.nan


# In[6]:



def get_schools(school_type):
    base_url = "https://api.greatschools.org/schools/TX/Austin/{0}?key={1}&limit=-1&sort=parent_rating".format(school_type, api_keys.api_key)
    params = {
    "key": api_keys.api_key,
    }
    # assemble url and make API request
    schools = xmltodict.parse(requests.get(base_url).content)['schools']
    df = pd.DataFrame(schools, columns=schools.keys())
    df["name"] = df.school.map(lambda x: extract(x, "name"))
    df["gsId"] = df.school.map(lambda x: extract(x, "gsId"))
    df['type'] = df.school.map(lambda x: extract(x, "type"))
    df['gradeRange'] = df.school.map(lambda x: extract(x,"gradeRange"))
    df['enrollment'] = df.school.map(lambda x: extract(x, "enrollment"))
    df['address'] = df.school.map(lambda x: extract(x, "address"))
    df['ncesId'] = df.school.map(lambda x: extract(x, "ncesId"))
    df['lat'] = df.school.map(lambda x: extract(x, "lat"))
    df['lon'] = df.school.map(lambda x: extract(x, "lon"))
    df['gsRating'] = df.school.map(lambda x: extract(x, "gsRating"))
    df['parentRating'] = df.school.map(lambda x: extract(x, "parentRating"))
    del(df['school'])
    return df


# In[7]:


df_public = get_schools("public")
df_private = get_schools("private")
df_charter = get_schools("charter")


# In[8]:


df_public


# In[9]:


df_private


# In[10]:


df_charter


# In[11]:


df = df_public.append(df_private)


# In[13]:


df = df.append(df_charter)


# In[14]:


df.to_csv("data/AustinSchools.csv")


# In[15]:


get_ipython().system('open "data/AustinSchools.csv"')

