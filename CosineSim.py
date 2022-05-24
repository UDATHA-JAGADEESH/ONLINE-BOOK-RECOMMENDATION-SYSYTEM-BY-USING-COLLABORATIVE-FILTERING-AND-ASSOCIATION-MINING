import re, math
import numpy as np
from collections import Counter
class CosineSim:   

   WORD = re.compile(r'\w+')

def cosineSimilarity(input, query):
     intersection = set(input.keys()) & set(query.keys())
     numerator = sum([input[x] * query[x] for x in intersection])

     sum1 = sum([input[x]**2 for x in input.keys()])
     sum2 = sum([query[x]**2 for x in query.keys()])
     denominator = math.sqrt(sum1) * math.sqrt(sum2)

     if not denominator:
        return 0.0
     else:
        return float(numerator) / denominator

def text_to_vector(text):
     WORD = re.compile(r'\w+')
     words = WORD.findall(text)
     return Counter(words)

