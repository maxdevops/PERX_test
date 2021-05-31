def findN(a,b):
    if len(a.list) > len(b.list): 
        Lmax, Lmin = a, b
    elif len(a.list) < len(b.list):
        Lmax, Lmin = b, a
    else:
        raise Exception('Equal sets length', 400) 

    prefix = 'added' if Lmin.name == 'before' else 'removed'
    Lmax.list.sort()
    Lmin.list.sort()

    for idx, val in enumerate(Lmin.list):
        if val != Lmax.list[idx]:
            return '{}:{}'.format(prefix, Lmax.list[idx])
    return '{}:{}'.format(prefix, Lmax.list[-1])


def get_index_of_first_val(l, val):
    try:
        n = next(i for i,v in enumerate(l) if v == val)
    except StopIteration:
        n = len(l)
    return n


def trim_iterable_to_first_val(l, val=''):
    n = get_index_of_first_val(l, val)
    return l[:n]


def get_book_sheet(book_dict):
    try:
        return next(v for k,v in book_dict.items() if set(["before", 'after']).issubset(trim_iterable_to_first_val(v[0])))
    except StopIteration:
        return None


def process_book_dict(book_dict):
    book_sheet = get_book_sheet(book_dict)
    if book_sheet:
        title = book_sheet[0]
        rows = book_sheet[1:]
        idx_before = get_index_of_first_val(title, 'before')
        idx_after = get_index_of_first_val(title, 'after')
        before = o('before', trim_iterable_to_first_val([row[idx_before] for row in rows]))
        after = o('after', trim_iterable_to_first_val([row[idx_after] for row in rows]))
        return findN(before, after)
    return None


class o(object):
    
    def __init__(self, name, l):
        self.name = name
        self.list = l
