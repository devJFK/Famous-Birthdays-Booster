from models.status import Status
import codecs

def readList(path):
    try:
        return [line.strip() for line in codecs.open(path, 'r', encoding='utf-8', errors='ignore').readlines()]
    except:
        return Status.FAILURE