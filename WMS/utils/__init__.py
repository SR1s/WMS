def md5(str):
    import hashlib
    m = hashlib.md5()
    m.update(str)
    return m.hexdigest()
    
def readXls(file_path,mode=1):
    import json, xlrd
    from datetime import datetime
    info = dict()
    data = xlrd.open_workbook(file_path)
    table = data.sheet_by_index(0)
    
    number = table.cell(0,8).value.split()[-1]
    date = xlrd.xldate_as_tuple(table.cell(3, 11).value, data.datemode)

    info['number'] = number
    info['date'] = str(datetime(*date).date())
    info['items'] = dict()
    if table.cell(12,0).value != 'Item Number':
        info['error'] = True
        info['error_message'] = 'table format incorrect'
    else:
        isEnd = False
        row=13
        size_list = list()
        while not isEnd:
            if table.cell(row,0).ctype==0 \
               and table.cell(row,1).ctype==0 \
               and table.cell(row,2).ctype!=0:
                size_list = list()
                for n in range(2,8):
                    size_list.append(table.cell(row,n).value)
            elif table.cell(row,0).ctype!=0:
                if len(size_list)<=0:
                    info['error'] = True
                    info['error_message'] = 'table format incorrect'
                    break
                else:
                    number=table.cell(row,0).value
                    description=table.cell(row,1).value
                    item=dict()
                    item['number'] = number
                    item['description']=description
                    item['columns'] = list()
                    for n in range(2,8):
                        if table.cell(row,n).ctype == 0:
                            continue
                        else:
                            value=table.cell(row,n).value
                        size=size_list[n-2]
                        amount=int(value)
                        col = dict(size=size, amount=amount)
                        item['columns'].append(col)
                    info['items'].setdefault(number, item)
            else:
                break
            row = row + 1
    if mode==0:
        return info
    elif mode==1: 
        return json.dumps(info)