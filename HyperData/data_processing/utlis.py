import sympy, pandas, math, numpy, re
from config.settings import list_name, logger

def check_integer (input:str):
    try:
        int(input)
        return True
    except:
        return False

def check_float (input:str):
    try:
        float(input)
        return True
    except:
        return False
    
def evaluate_func (input:str,var):
    x=var
    y=var
    z=var
    data_input = None
    try:data_input = eval(str(sympy.sympify(input)))
    except:
        try:data_input = eval('math.'+input)     
        except:
            try:data_input = eval('math.'+str(sympy.sympify(input)))
            except:
                try:data_input = eval(input)
                except:pass
    return data_input

def process_1d_data (input:str, data:pandas.DataFrame):
    """ this function accepts input as a string of 1d data
    in which element is separated by a comma
    """
    data_input = []
    split = input.split(',')

    try:
        for i in split:
            try: 
                _d = eval(i, {"numpy":numpy, "np": numpy, "math":math})
            except:
                # process input
                start_point = i.split(":")[0]
                end_point = i.split(":")[-1]
                start_col = list_name.index(''.join(re.findall(r'[a-zA-Z]', start_point)).lower())
                start_row = int(''.join(re.findall(r'\d', start_point))) - 1
                end_col = list_name.index(''.join(re.findall(r'[a-zA-Z]', end_point)).lower()) + 1
                end_row = int(''.join(re.findall(r'\d', end_point)))

                _d = data.iloc[start_row : end_row, start_col : end_col].to_numpy()
            
            data_input.append(_d)
            data_input = list(numpy.ravel(data_input))

    except Exception as e: 
        logger.exception("Cannot process input string.")
        logger.exception(e)
    
    return data_input

def split_input(input:str, data:pandas.DataFrame):
    """ this function will split a string input and
    try to evaluate math expression from the string """
  
    data_input = []
    input = input.replace(" ","")
   
    # if input is 2d data, which is separated by "|"
    # split this input into a list of 1d data
    if "|" in input:
        split = input.split("|")
        for i in split:
            data_input.append(process_1d_data(i, data))
    else:
        data_input = process_1d_data(input, data)
    print(data_input)
    return data_input
