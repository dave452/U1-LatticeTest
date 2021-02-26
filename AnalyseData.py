# -*- coding: utf-8 -*-
"""
Created on Fri Jan 22 10:55:41 2021

@author: David
"""

import numpy as np
import matplotlib.pyplot as plt

    
def findPlaq(filename, N_obs):
    file = open(filename)
    Plaq = np.zeros((N_obs))
    line = file.readline()
    i = 0
    while line[:3] != 'END':
        if(line[:19] == 'Average Plaquette: '):
            Plaq[i] = float(line[19:])
            i += 1
        line = file.readline()
    file.close()
    print(filename, 'complete,', i, 'measurements')
    return Plaq

def VEV(Plaq, plot = False, func = np.mean):
    Plaq = Plaq.flatten()
    VEV = func(Plaq)
    VEV_error = bootstrap(Plaq,plot = plot,func = func)
    return VEV, VEV_error

def CVPlaq(Plaq):
    VEV = Plaq.flatten().mean()
    VEV2 = (Plaq.flatten() ** 2).mean()
    CV = (VEV2 - (VEV ** 2)) * (4*4*4*4*6)
    return CV

def jackknife(P,M):
    P = P.flatten()
    VEV_P = P.mean()
    np.random.shuffle(P)
    block_len = int(np.floor(P.shape[0] / M))
    P.shape = (M, block_len)
    mask = np.ones((M),dtype=bool)
    err = 0.
    for i in range(M):
        mask[i] = 0
        err += ((P[mask,:].mean() - VEV_P) ** 2)
        mask[i] = 1
    err = (err * ((M-1) / M)) ** 0.5
    print(err)
    return err

def bootstrap( P,M = 500, Nb = 10000, con_int =0.68, plot = False, func = np.mean):
    P = P.flatten()
    VEV_P = func(P)
    #np.random.shuffle(P)
    block_len = int(np.floor(P.shape[0] / M))
    P.shape = (M, block_len)
    P_func = np.zeros((Nb))
    for i in range(Nb):
        P_func[i] = func(P[np.random.randint(0,M, size = (M)),:])
    P_func.sort()
    j = 0
    a = P_func[j]
    while (P_func[P_func < a].shape[0] < (((1-con_int)/2) * Nb)) :
        j += 1
        a = P_func[j]
    
    j = P_func.shape[0] - 1
    b = P_func[j]
    while (P_func[P_func > b].shape[0] < (((1-con_int)/2) * Nb)) :
        j -= 1
        b = P_func[j]
    
    a = VEV_P - a
    b -= VEV_P
    if plot:
        print(a,b)
        plt.hist(P_func, bins = 25)
        plt.axvline(x=VEV_P, c='r')
        plt.axvline(x=VEV_P - a,  c='r')
        plt.axvline(x=VEV_P + b,c ='r')
        plt.show()

    return np.array([a, b])
    
files = np.array(["./output/4444b0.94s345.txt","./output/4444b0.94s94.txt",
                  "./output/4444b0.95s5678.txt","./output/4444b0.95s1700.txt",
                  "./output/4444b0.96s7.txt","./output/4444b0.96s8.txt",
                  "./output/4444b0.97s34.txt","./output/4444b0.97s10000.txt",
                  "./output/4444b0.98s5.txt","./output/4444b0.98s6.txt",
                  "./output/4444b0.99s987.txt","./output/4444b0.99s760.txt",
                  "./output/4444b1s1.txt","./output/4444b1s2.txt","./output/4444b1s3.txt","./output/4444b1s4.txt",
                  "./output/4444b1.01s3454.txt", "./output/4444b1.01s205.txt"])

N_f = np.array([2,2,2,2,2,2,4,2])
beta = [0.94,0.95,0.96,0.97,0.98,0.99,1,1.01]
cols = ['b', 'g', 'r', 'c','m','y','k','b', 'g', 'r', 'c','m','y','k']
N_obs = 10000
N_seeds = files.shape[0]
full_Plaq = np.array([])
VEV_P = np.zeros((N_f.shape[0]))
VEV_P_err = np.zeros((2, N_f.shape[0]))
CV_P = np.zeros((N_f.shape[0]))
CV_P_err = np.zeros((2, N_f.shape[0]))

count = 0

for j in range(N_f.shape[0]):
    full_Plaq = np.array([])
    for i in range(N_f[j]):
        print(beta[j])
        full_Plaq = np.append(full_Plaq, [findPlaq(files[count], N_obs)])
        count += 1
    VEV_P[j], VEV_P_err[:,j] = VEV(full_Plaq)
    CV_P[j], CV_P_err[:,j] = VEV(full_Plaq, func = CVPlaq)




plt.errorbar( beta,VEV_P, VEV_P_err,fmt = 'k.')
beta_px = np.array([125.,131.,137.,144.,149.,156.,161.,167.,172.,178.,183.,187.,192.,196.,201.,205.,208.,
           213.,216.,220.,223.,226.,230.,233.,236.,239.,242.,245.,248.,251.,254.,257.,261.,264.,
           267.,271.,274.,278.,282.,286.,290.,295.,299.,304.,309.,315.,320.,326.,332.,339.])
beta_px = ((beta_px - 124.) * (0.02 / 61.25)) + 0.94 
P_px = np.array([485.,480.,474.,467.,462.,455.,449.,442.,436.,428.,421.,414.,407.,400.,392.,384.,376.,
        368.,360.,353.,344.,336.,328.,320.,312.,304.,296.,287.,280.,271.,263.,255.,247.,239.,
        231.,223.,215.,207.,199.,191.,184.,176.,169.,162.,155.,148.,141.,135.,128.,123.])
P_px = ((547. - P_px) * (0.02 / 46.3)) + 0.48 
plt.plot( beta_px,P_px, 'b--')
plt.xlabel('$\\beta$')
plt.ylabel('$\langle \overline{u} \\rangle $')
plt.show()

plt.errorbar( beta,CV_P, CV_P_err,fmt = 'k.')

beta_px = np.array([210.,230.,283.,275.,298.,320.,342.,366.,387.,409.,431.,453.,475.,497.,
                    519.,542.,560.,584.,605.,627.,648.,668.,692.,713.,732.,757.,780.,801.,
                    824.,845.,866.,889.,910.,933.,955.,976.,998.,1019.,1041.,1064.,1087.,
                    1108.,1132.,1153.,1176.])
beta_px = ((beta_px - 205.) * (0.02 / 282.25)) + 0.94 
CV_px = np.array([212.,211.,210.,209.,209.,207.,206.,206.,204.,202.,200.,198.,195.,194.,190.,
                  187.,184.,181.,177.,174.,171.,169.,165.,164.,162.,161.,162.,164.,165.,168.,
                  171.,175.,178.,182.,185.,188.,192.,195.,199.,201.,203.,206.,207.,209.,210.])
CV_px = ((237. - CV_px) * (10. / 212.)) 
plt.plot( beta_px,CV_px, 'b--')
plt.xlabel('$\\beta$')
plt.ylabel('$C_v$')






