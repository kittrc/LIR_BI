""" custome modules for EM localization
Started on 15/09/2021 by Ruwan Abeywardhana;
Last update 09/2021
"""


from scipy.io import loadmat

def readEmData(fileName,cut1,cut2):
        mat_data = loadmat(fileName)
        data = mat_data.get("data")
        sig_time = data[:,0]
        dt = sig_time[2]-sig_time[1]
        sig = data[:,2:5]
        sig = sig[cut1 : cut2,:]
        return dt, sig
 
def readEmData(fileName,cut1,cut2):
        mat_data = loadmat(fileName)
        data = mat_data.get("data")
        sig_time = data[:,0]
        dt = sig_time[2]-sig_time[1]
        sig = data[:,2:5]
        sig = sig[cut1 : cut2,:]
        return dt, sig
 
 