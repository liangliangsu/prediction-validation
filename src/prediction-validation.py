import sys
import re

# Check extracted values is numerical.
def check_value(time,price):
    try:
        time=int(time)
        price=float(price)
        return (price,0)
    except ValueError:
        print ('Warning: Time or Price is not numerical!')
        return (price,1)

# Read inputdate, preprocess the data and store value in dictionary
def make_dict(filepath):
    price_dict={}
    try:
        f = open(filepath, 'r') 
    except:
        print ('Error: Input dataset directory can not be opened!')
        return price_dict,1
    line = f.readline()
    while line:
        temp=line.strip('\n').split("|") # Extract value from each line
        flag=0
        # Check line is splitted correctly
        if len(temp)!=3: 
            flag=1
            print ('Warning: More than 3 entries in one line!')
        else:
            time=temp[0].strip()
            stock=temp[1].strip()
            price=temp[2].strip()
            price,flag = check_value(time,price)
        
        # Store extracted values into designed dictionary
        # Hour number is first key, stock name is second key
        if flag==0:
            if time in price_dict.keys():
                price_dict[time][stock]=price
            else:                
                price_dict[time]={}
                price_dict[time][stock]=price                       
        line = f.readline()        
    f.close()
    
    if len(price_dict)>0:
        return price_dict,0
    else:
        print ('Error: Cannot extract useful information!')
        return price_dict,1

# Compute sum error, count of matched stocks in each hour
# Store results in time stream order
def compute_error(act_dict,pre_dict):
    hour=[]
    error=[]
    count=[]
    timelist = list(map(int, list(pre_dict.keys())))
    for h in range(min(timelist),(max(timelist)+1)):
        if (str(h) in pre_dict.keys())&(str(h) in act_dict.keys()):
            hour.append(h)
            temp_error=0
            temp_count=0
            for stock in pre_dict[str(h)].keys():
                if stock in act_dict[str(h)].keys():
                    temp_error=temp_error+abs(pre_dict[str(h)][stock]-act_dict[str(h)][stock])
                    temp_count=temp_count+1            
            error.append(temp_error)
            count.append(temp_count)            
        else:
            hour.append(h)
            error.append(0)
            count.append(0)
    return hour,error,count 

# Compute average error for each sliding window 
# and covert results to desired format for writing to output file.
def slide_windows(filepath,hour,error,count):
    # Read window size from inputfile
    window=1
    try:
        f = open(filepath, 'r')
    except:
        print ('Error: Cannot open window file')
    line = f.readline()
    window=line.strip('\n').strip()
    f.close()
    try:
        window=int(window)
    except:
        print ('Warning: Window size is not numerical!')
        
    lines=[]
    startindex=0
    while (startindex+window)<=len(hour):
        temp_count=sum(count[startindex:startindex+window])
        temp_error=sum(error[startindex:startindex+window])
        if temp_count!=0:
            avg_error=temp_error/temp_count
            line=str(hour[startindex])+'|'+str(hour[startindex+window-1])+'|'+str('{0:.2f}'.format(avg_error))+'\n'
        else:
            line=str(hour[startindex])+'|'+str(hour[startindex+window-1])+'|'+'NA'+'\n'
        startindex=startindex+1
        lines.append(line)
    return lines

#############
# Setup input and output directory from argumnets.
#inputfile1 = './input/actual.txt'
#inputfile2 = './input/predicted.txt'
#inputfile3 = './input/window.txt'
#outputfile = './output/comparison.txt'
inputfile1=sys.argv[2] 
inputfile2=sys.argv[3]
inputfile3=sys.argv[1]
outputfile=sys.argv[4]

act_dict,flag1=make_dict(inputfile1) # Read actual.txt and store value in dictionary
pre_dict,flag2=make_dict(inputfile2) # Read predicted.txt and store value in dictionary

if (flag1+flag2)==0:
    # Compute sum error, count of matched stocks in each hour
    hour,error,count=compute_error(act_dict,pre_dict) 
    
    # Compute average error for each sliding window 
    # and covert results to desired format for writing to output file.
    lines=slide_windows(inputfile3,hour,error,count) 

try:
    f = open(outputfile, "w")
except:
    print ('Error: Output directory can not be opened!')
f.writelines(lines)
f.close()