from datetime import datetime

def md5(str):
    import hashlib
    m = hashlib.md5()
    m.update(str)
    return m.hexdigest()

'''
@param
    date_str: String
        String of date format as 'MM/DD/YYYY'

@return
    datetime: datetime
        datetime object
'''
def str2datetime(date_str):
    date_p = date_str.split('/')
    if len(date_p) == 3:
        return datetime(int(date_p[2]),int(date_p[0]),int(date_p[1]))
    else:
        return None
    
def readXls(file_path,mode=1):
    import json, xlrd
    from datetime import datetime
    info = dict()
    data = xlrd.open_workbook(file_path)
    table = data.sheet_by_index(0)
    
    number = table.cell(0,8).value.split()[-1]
    date = xlrd.xldate_as_tuple(table.cell(3, 11).value, data.datemode)

    info['order_no'] = number
    info['error'] = True
    if mode==1:
        info['date'] = str(datetime(*date).date())
    elif mode==0:
        info['date'] = datetime(*date)
    info['items'] = dict()
    if table.cell(12,0).value != 'Item Number':
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
                    size = table.cell(row,n).value
                    if table.cell(row,n).ctype == 2:
                        size = int(size)
                    size_list.append(size)
            elif table.cell(row,0).ctype!=0:
                if len(size_list)<=0:
                    info['error_message'] = 'table format incorrect'
                    break
                else:
                    number=table.cell(row,0).value
                    description=table.cell(row,1).value
                    item = info['items'].setdefault(number, dict())
                    item['number'] = number
                    item['description']=description
                    item.setdefault('columns', dict())
                    for n in range(2,8):
                        if table.cell(row,n).ctype == 0:
                            continue
                        else:
                            value=table.cell(row,n).value
                        size=size_list[n-2]
                        amount=int(value)
                        item['columns'].setdefault(size, 0)
                        item['columns'][size] += amount 
            else:
                break
            row = row + 1
    info['error'] = False
    if mode==0:
        return info
    elif mode==1: 
        return json.dumps(info)

class Log:
    '''
    function set to log data on page or raise error for debug
    '''
    @staticmethod
    def json(data):
        '''
        dump data in json format
        '''
        if data:
            return '<pre>%s</pre>' % json.dumps(data, ensure_ascii=False, indent=2)
        else:
            return 'no data for log'

    @staticmethod
    def rasise_error():
        '''
        raise error for debug
        '''
        raise ValueError
