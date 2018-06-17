import numpy as np, json

with open('good_comments.json', 'r') as good_file:
    good_json = json.load(good_file)

with open('bad_comments.json', 'r') as bad_file:
    bad_json = json.load(bad_file)

good_comments = good_json['comments']
bad_comments = bad_json['comments']

np.random.shuffle(good_comments)
np.random.shuffle(bad_comments)

dataset_len = np.minimum(len(good_comments), len(bad_comments))
dataset_good = good_comments[:dataset_len]
dataset_bad = bad_comments[:dataset_len]

with open('good_comments_shuffle.json', 'w') as good_file:
    json.dump({'comments': dataset_good}, good_file, indent=4, ensure_ascii=False)

with open('bad_comments_shuffle.json', 'w') as bad_file:
    json.dump({'comments': dataset_bad}, bad_file, indent=4, ensure_ascii=False)
