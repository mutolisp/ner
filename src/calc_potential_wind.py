# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

from preprocess import cwb_preproc
import potential_wind as pw
import pandas as pd
import numpy as np

# <codecell>

# initialization
pws = pw.ws_array()
pws_orig = pw.ws()
cwb = cwb_preproc()

# <codecell>

%time dataf = cwb.fread('data/type_a/CWB_A1_C0A510.txt', ctype='a1'); pws.psatw(dataf, 'tx01')

# <codecell>

%time o = pws.psatw(dataf, 'tx01')

# <codecell>

idx_t = dataf[(dataf['tx01']+273.15 < 300.096)].index
len(idx_t)
#dataf['densold'] = pd.DataFrame([100.0]*len(idx_t), index=idx_t)

# <codecell>

def update_densold(i):
    if i in list(idx_t):
        return(100.0)
    else:
        return(600.0)
list_idx = (1,3,5,7,9)

# <codecell>

for i in list_idx:
    dataf['densold'][i] = 100.0

# <codecell>

df = dataf[['psatw','tx01','wd01']][0:30]

# <codecell>

dataf1[ (dataf1<0) ].index

# <codecell>

df = pd.DataFrame(np.random.randn(20)*100, columns=['random'])

# <codecell>

df['random'] = pd.DataFrame(np.random.randn(20)*100, columns=['random'])
df['converg'] = np.nan

# <codecell>

for i in range(0,100):
    df['random'] = pd.DataFrame(np.random.randn(20)*100, columns=['random'])
    df['converg'][df['random'] == 15] = 1
    idx = df['converg'][df['converg'] != 1].index
    if len(idx) > 0:
        df['random'] = pd.DataFrame(np.random.randn(len(idx)), index=idx.tolist())
    else:
        print(i)

# <codecell>

df['new'] = np.nan

# <codecell>

df['new'] = df['wd01'][(df['tx01'] > 15)]

# <codecell>

pws_orig.__densreg3__(628, 175.32)

# <codecell>

pws_orig.psatw(628)-1e-05

# <codecell>

pws_orig.calc_pw(tx=283.15, ps=1000.6, rh=86, wd=2)

# <codecell>

for i in df['tx01']+273.15:
    print(pws_orig.dens_sat_vaptw(i))

# <codecell>

df['psatw']

# <codecell>


