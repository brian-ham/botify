import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer, util
import math
import random
from torch import tensor

# this is CONTENT BASED FILTERING using key, danceablity, etc.
# combatting the cold start problem
# use softmax instead?
# part 2: collaborative filtering: looking into playlists and playlist names
# will require using the Spotify API to draw playlist names

def calc_similarities(input):
    '''str -> array(24): 
    Calculates cosine similarity scores for given string and the 24 descriptions.'''
    model = SentenceTransformer('stsb-roberta-large') # most up-to-date model
    input_embed = model.encode([input], convert_to_tensor=True)
    df = pd.read_csv("key_embeddings.csv")
    return util.pytorch_cos_sim(input_embed, tensor(np.float32(df.values).T))
    # print("shape of input_embed:", input_embed.shape)
    # print("shape of df values:", tensor(df.values.T).shape)
    # print("type of input_embed:", type(input_embed))
    # print("type of df values:", type(tensor(df.values).T))
    # return 0

def keys_alloc(array):
    '''array(24) -> array(24):
    Converts decimal cosine similarity values to allocations into integer values adding up to 24.
    Returns null if no value is significantly high, array of size 24 otherwise.'''

    # convert tensor into 1x24 array
    array = np.array(array[0])

    # if no significant similarity to any of the keys
    if (all(x < 0.1 for x in array)):
        return None
    
    # turn all negative cosine similarities to 0
    array = [(0 if i < 0 else i) for i in array]

    # weight to sum to 24
    array = [math.floor(array[i] * 24/(sum(array))) for i in range(len(array))]

    # adjusting for rounding errors
    if (sum(array) < 24):
        nonzero_index = np.nonzero(array)[0] # get list of keys that have relation to text
        nonzero_list = [array[i] for i in nonzero_index]
  
        random_list = random.choices(nonzero_index, weights=nonzero_list, k=24-sum(array))

        for i in range(24 - sum(array)):
            array[random_list[i]] += 1

    assert(sum(array) == 24) # sum should have been adjusted to be exactly 24
    return array
    
# redo all to use numpy? is it worth?
# experiment with values other than 24
# redo the above function to not make a list before applying random

print("random")
# print(calc_similarities("And God created great whales, and every living creature that moveth, which the waters brought forth abundantly, after their kind, and every winged fowl after his kind: and God saw that it was good."))
results = calc_similarities("Happiness is the most important thing in life. It is an emotion that can only be felt or lived. As human beings, we feel happy when we feel satisfied and content inside. I feel happiest when I play with friends in school and at home or go out with my parents on weekends")
print(keys_alloc(results))

# How's your day going?