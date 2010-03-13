from bisect import bisect
from math import log

from django.db import models

def linear(count, most, levels):
    return count

def logarithmic(count, most, levels):
    if most == 1:
        return count

    return log(count) * most / log(most)

def make_cloud(tags=None, levels=6, distribution=linear):
    if not tags:
        return tags
        

    levels -= 1

    tags = tags.annotate(count = models.Count('items'))
    counts = [tag.count for tag in tags]

    least, most = min(counts), max(counts)
    delta = (most - least) / float(levels)

    thresholds = [int(round(least + (i + 1) * delta)) for i in range(levels)]

    for tag in tags :
        tag.weight = bisect(thresholds, distribution(tag.count, most, levels))

    return tags
