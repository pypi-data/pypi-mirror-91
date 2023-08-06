def _TEST_IMPORT(printing: bool):
    if printing is True:
        print("XTRMTH:XTRMTH:connected:True")
        return True
    else:
        return True

        
def summation(count: int, bottom_var: str, expression: str):
    var, value = bottom_var.split('=')
    var = var.strip()
    
    value = int(eval(value))
    
        
    res = 0
    for i in range(value, count+1):
        res += eval(expression.replace(var, str(i)))

    return res

def sq(value):
    return value*value

def sqrt(value, _print_unround: bool=False): 
        x = value
        y = 1
          
        # e decides the accuracy level 
        e = 0.00000000001
        while(x - y > e): 
      
            x = (x + y)/2
            y = value / x 
            
        if _print_unround is True:
            print(x)
        if type(x) is float:
            if round(x, 10) == int(round(x, 10)): return int(round(x, 10))
            else: return round(x, 10)
        else:
            return x

def cb(value):
    return value*value*value

def cbrt(value, _print_unround: bool=False):
    x = value**(1/3)
    
    if _print_unround is True:
        print(x)
        
    if type(x) is float:
        if round(x, 10) == int(round(x, 10)): return int(round(x, 10))
        else: return round(x, 10)
    else:
        return x
    