import glob
import json

curfile=""

def loadData(full=False):
    global curfile
    if full:
        files = []
        files += [f for f in glob.glob("/data/xtof/corpus/covid/biorxiv_medrxiv/*.json")]
        files += [f for f in glob.glob("/data/xtof/corpus/covid/comm_use_subset/*.json")]
        files += [f for f in glob.glob("/data/xtof/corpus/covid/custom_license/*.json")]
        files += [f for f in glob.glob("/data/xtof/corpus/covid/noncomm_use_subset/*.json")]
    else:
        files = [f for f in glob.glob("../sampdata/*.json")]
    for f in files:
        curfile=f
        try:
            with open(f,"r") as ff: o=json.load(ff)
            # print(o.keys())
            # [u'body_text', u'bib_entries', u'abstract', u'back_matter', u'paper_id', u'ref_entries', u'metadata']
            txt = o['body_text']
            utts = []
            for oo in txt:
                utts.append(oo['text'])
            yield utts
        except:
            print("ERROR file "+f)

"""
distrib de la longueur des chiffres sur tout le corpus:
Counter({1: 3745400, 2: 2617545, 4: 997545, 3: 789312, 0: 187201, 6: 22878, 5: 18303, 8: 5994, 7: 2921, 9: 629, 10: 194, 11: 141, 12: 57, 13: 39, 14: 26, 15: 18, 16: 8, 19: 1, 17: 1, 38: 1, 48: 1, 25: 1})

"""

