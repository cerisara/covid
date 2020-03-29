import glob
import json

curfile=""

def loadData():
    global curfile
    files = [f for f in glob.glob("../sampdata/*.json")]
    for f in files:
        curfile=f
        with open(f,"r") as ff: o=json.load(ff)
        # print(o.keys())
        # [u'body_text', u'bib_entries', u'abstract', u'back_matter', u'paper_id', u'ref_entries', u'metadata']
        txt = o['body_text']
        utts = []
        for oo in txt:
            utts.append(oo['text'])
        yield utts

