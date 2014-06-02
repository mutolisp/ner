# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import potential_wind
import psycopg2 as pg
from psycopg2.extras import DictCursor
import pandas as pd
import numpy as np

# create a ws object
ws = potential_wind.ws()

# <codecell>

station_id = 'C0A520'
sql_find_stn = '''
SELECT 
    distinct stn_code,yr,mm,dd,hr,tx01,rh01,ps01,wd01
FROM 
    stn_auto_r 
WHERE
    stn_code = '%s'
ORDER BY yr,mm,dd,hr;
''' % station_id
conn = pg.connect(database='cwbdb', host='localhost')
frame = pd.read_sql(sql_find_stn, conn)
wpresult_test = []
for i in range(0,len(frame)):
    f = ws.calc_pw(tx=frame.tx01[i],rh=frame.rh01[i],ps=frame.ps01[i],wd=frame.wd01[i])
    sql = 'update stn_c0a520 set density=%'
    wpresult_test.append([frame.yr[i],frame.mm[i],frame.dd[i],frame.hr[i], frame.wd01[i],f[0],f[1]])


# <codecell>

result_frame = pd.DataFrame(wpresult_test, columns=['yr', 'mm', 'dd', 'hr', 'wd', 'density', 'wp'])
re2f = result_frame.replace({-1:np.nan})


# <codecell>

re2f['wp'].mean()

# <codecell>

re2f

# <codecell>

from preprocess import cwb_preproc

# <codecell>

cp = cwb_preproc('path', 1)

# <codecell>

cp.cwb_read('path2')

# <codecell>

a = [1,2,3,4,5]

# <codecell>


# <codecell>


