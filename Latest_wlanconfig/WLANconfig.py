import matplotlib.pyplot as plt
import matplotlib.dates as md
import numpy as np
import re
from itertools import chain
from collections import Counter
from  datetime import datetime

def graphs(x,y,title,yaxis):                                            #plots data over time
    ax=plt.gca()
    xfmt = md.DateFormatter('%Y-%m-%d %H:%M:%S')
    ax.xaxis.set_major_formatter(xfmt)
    plt.xticks( rotation=30, horizontalalignment='right' )
    plt.plot(x,y,'.', color='blue')
    plt.title(title)
    plt.xlabel('Time')
    plt.ylabel(yaxis)
    plt.show()                                                             
    plt.savefig('.png')   

def dataspecific(catch_start, catch_end,logfile,inter):                 #extracts required data, processes and sends it for plotting
    results = []
    mac =[]
    m=[]
    uniq=[]
    c=[]
    per=[]
    t=0
    time1=[]
    clients_no=[]
    tim=[]
    p=re.compile(r'(?:[0-9a-fA-F]:?){12}')
    with open(logfile, 'r') as f1:
        lines = f1.readlines()
    i = 0
    while i < len(lines):
        if catch_start in lines[i]:
            t+=1
            for j in range(i + 1, len(lines)):
                if catch_end in lines[j] or j == len(lines)-1:
                    results.append(lines[i:j])
                    i = j
                    break
        else:
            i += 1
    for a in results:
        for b in a:
            if re.findall(p,b):
               m.append(b)
    for x in m:
        mac.append(re.split(r'[|\s]\s*', x))
    singlelist = list(chain.from_iterable(mac))
    for ti in mac:
        tim.append(ti[26]+" "+ti[27])
    date_obj = []
    for temp in tim:
        date_obj.append(datetime.strptime(temp, '%Y-%m-%d %H:%M:%S.%f'))
    dates = md.date2num(date_obj)
    length=len(singlelist[0::29])                                 #length gives the no. of clients connected to ath interface
    s = Counter(singlelist[0::29])
    for uniquemac in s:
        uniq.append(uniquemac)                                     #uniq : list of unique clients connected to ath interface
        c.append(s[uniquemac])
    for x in c:
        percent= (x/t)*100
        per.append(percent)                                      #per : list of % duration of unique clients connected to ath interface
    no_of_clients = Counter(dates)
    for client in no_of_clients:
        time1.append(client)
        clients_no.append(no_of_clients[client])
    print("Number of clients connected to "+inter+" is: ",length)
    print("The unique clients connected to "+inter+" is: ")
    print (" \n" .join(str(x) for x in uniq))
    print("The Percentage duration of unique clients connected to "+inter+" is: ")
    print (" \n" .join(str(x) for x in per))
    graphs(dates,singlelist[0::29],"wlanconfig "+inter+" list sta","Mac Address")
    graphs(time1,clients_no,"No. of clients connected to "+inter+" over time","No. of clients")

def Call_dataspecific(interface_list,fname):                        #interface_list takes the values from config
  for interface in interface_list:
     dataspecific("root@RBR850:/# wlanconfig "+interface+" list sta",  "root@RBR850:/# ",fname,interface)


