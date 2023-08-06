class mathError(Exception):
    pass

def calculate(math):
    banned = list('qwertyuiopasdfghjklzxcvbnm<,>?\'";:[]\\{}&^%$#@!=')
    for one in math:
        if one in banned:
            raise mathError('Only support "1234567890()*/-+"')
        else:
            pass
    return eval(math)