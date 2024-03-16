import sympy, pandas
from config.settings import list_name

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

def split_1d_data (input:str, data:pandas.DataFrame):

    data_input = []
    
    split1 = input.split(';')
    try:
        for i in split1:
            try:
                try:data_input.extend(eval(str(sympy.sympify(i))))
                except:data_input.append(eval(str(sympy.sympify(i))))
            except:
                try:
                    try:data_input.extend(eval('math.'+i))
                    except:data_input.append(eval('math.'+i))
                except:
                    try:
                        try:data_input.extend(eval('math.'+str(sympy.sympify(i))))
                        except:data_input.append(eval('math.'+str(sympy.sympify(i))))
                    except:
                        try:
                            try:data_input.extend(eval(i))
                            except:data_input.append(eval(i))
                        except:
                            start_point = i.split(":")[0]
                            end_point = i.split(":")[-1]
                            start_point1 = (start_point.split(".")[0]).lower()
                            start_point2 = start_point.split('.')[-1]
                            end_point1 = (end_point.split(".")[0]).lower()
                            end_point2 = end_point.split(".")[-1]
                            if ":" in i:
                                if start_point1 == end_point1:
                                    if check_integer(start_point2) and check_integer(end_point2):
                                        start_point2 = int(start_point2)
                                        end_point2 = int(end_point2)
                                    elif check_integer(start_point2): 
                                        end_point2 = None
                                        start_point2 = int(start_point2)
                                    elif check_integer(end_point2):
                                        start_point2 = 1
                                        end_point2 = int(end_point2)
                                    else:
                                        start_point2 = 1
                                        end_point2 = None
                                    data_input.extend(data[data.columns[list_name.index(start_point1)]][start_point2-1:end_point2])
                                    
                                elif start_point2 == end_point2:
                                    if start_point2.isdigit() and end_point2.isdigit():
                                        data_input.extend(data.iloc[int(start_point2)-1][list_name.index(start_point1):list_name.index(end_point1)+1])
                        
                                
                            elif check_float(i):
                                data_input.append(float(i))
                            elif "." in i:
                                data_input.append(data[data.columns[list_name.index(start_point1)]][int(start_point2)-1])
                            elif i != '':
                                data_input.append(i)
                                pass
    except Exception as e: print(e)
    return data_input

def split_input(input:str, data:pandas.DataFrame):
    data_input = []
    input = input.replace(" ","")
    if "|" in input:
        split1 = input.split("|")
        for i in split1:
            data_input.append(split_1d_data(i, data))
    else:
        data_input = split_1d_data(input, data)
            
    return data_input
