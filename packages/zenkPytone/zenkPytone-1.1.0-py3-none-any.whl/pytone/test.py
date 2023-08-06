import kintone

kintone = kintone.Kintone('7hsBARXLyxMxTU2VrtRan9MWp4qye9yfUdRJjdYS', 'develfhvn', 5)
mention = [{
    "code": "m_tsuruya@zenk.co.jp",
    "type": "USER"
}]
rec = kintone.selectComment(recordID=19)
print(rec)