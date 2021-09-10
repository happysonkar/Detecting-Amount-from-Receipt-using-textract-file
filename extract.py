# Your imports go here
import logging
import json
import re

logger = logging.getLogger(__name__)
'''
    Given a directory with receipt file and OCR output, this function should extract the amount

    Parameters:
    dirpath (str): directory path containing receipt and ocr output

    Returns:
    float: returns the extracted amount

'''
def extract_amount(dirpath: str) -> float:
    logger.info('extract_amount called for dir %s', dirpath)
    # your logic goes here
    with open(dirpath+'/ocr.json','r') as f:
        data=json.load(f)
        count=0
        a=[d for d in data.values()]
        b=[a[1][i] for i in range(len(a[1]))]
        text = [b[i].get(j) for i in range(len(b)) for j in b[i].keys() if j=="Text"]
        for i in range(len(text)):
            if text[i] in ('DEBIT','CREDIT','AMOUNT','Order Total','TOTAL','Total','Total:','Payment','Total Payments:','PAID'):
                count+=1
                if any(q.isdigit() for q in text[i+1]) and len(text[i+1])<11 and len(text[i+1])>1:
                    result=text[i+1]
                    break
                else:
                    a=0
                    if any(q.isdigit() for q in text[i+2]) and len(text[i+2])<7:
                        result=text[i+2]
                        break
            else:
                for j in range(len(text[i])):
                    if text[i][j]=='$' and count==0:
                        if any(q.isdigit() for q in text[i]):
                            count+=1
                            result=text[i]
                            break
    c,w=0,"\d+\.\d+"
    result=result.replace(",","")
    for j in range(len(result)):
        if result[j].isdigit():
            c+=1
            if c==len(result):
                result=str(float(result))    
    result=re.findall(w,result)
    result=float(str(result[0]))
    return result
