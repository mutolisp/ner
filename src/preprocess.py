# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <headingcell level=1>

# Preprocess of CWB auto-observed stations

# <codecell>

import pandas as pd

class cwb_preproc(object):
    
    def __init__(self):
        pass
        
    def fread(self, infile=None, ctype=None, header=None):
        self.ctype = ctype
        if self.ctype == 'a1':
            # CWB_A1_stno 自動測站觀測資料第一型
            # from 1987-06-01 to 2009-10-31 
            self.ncolspec = [(0, 6), (7, 11), (11, 13), (13, 15), 
                        (15, 17), (17, 24), (24, 31), (31, 38), 
                        (38, 45), (45, 52), (52, 59)]
            self.colnames = ['std_code','yr','mm','dd','hr',
                             'ps01','tx01','wd01','wd02','pp01','ss01']
        elif self.ctype == 'a2':
            # CWB_A2_stno 自動測站觀測資料第二型
            # from 2009-11-01 
            self.ncolspec = [(0, 6), (7, 11), (11, 13), (13, 15), 
                        (15, 17), (17, 24), (24, 31), (31, 38), 
                        (38, 45), (45, 52), (52, 59), (59,66)]
            self.colnames = ['std_code','yr','mm','dd','hr',
                             'ps01','tx01','rh01','wd01','wd02','pp01','ss01']
            
        elif self.ctype == 'h1':
            # CWB_H1_stno 局屬逐時觀測資料第一型
            # from 1897-01-01 to 2011-08-31
            self.ncolspec = [(0, 6), (7, 11), (11, 13), (13, 15), 
                        (15,17), (17,24)]
            self.colnames = ['std_code','yr','mm','dd','hr','pp01']
        
        elif self.ctype == 'h2':
            # CWB_H2_stno 局屬逐時觀測資料第二型
            self.ncolspec = [(0, 6), (6, 10), (10, 12), (12, 14), (14, 16), (16, 22), 
                 (22, 28), (28, 33), (33, 38), (38, 41), (41, 45), (45, 49), (49, 54), (54, 58), 
                 (58, 63), (63, 68), (68, 71), (71, 74), (74, 78), (78, 82), (82, 85), (85, 89), 
                 (89, 91), (91, 93), (93, 95), (95, 96), (96, 97), (97, 98), (98, 102), (102, 107), 
                 (107, 112), (112, 117), (117, 122), (122, 127), (127, 132), (132, 133), (133, 134), 
                 (134, 135), (135, 136), (136, 137), (137, 138), (138, 139), (139, 140), (140, 141), 
                 (141, 142), (142, 143), (143, 147), (147, 148), (148, 152)]
            self.colnames = ['stn_code','yr','mm','dd','hr','ps01','ps02','tx','tx05','rh01','rh02','wd01', 
                        'wd02','wd05','wd06','pp01','pp02','ss01','vs01','cd01','cd02','cd03','cd04', 
                        'cd05','cd06','cd07','cd08','cd09','cd10','cd11','ts01','ts02','ts03','ts04', 
                        'ts05','st02','st03','st04','st05','st06','st07','st08','st09','st10','st11', 
                        'st12','ss02','ps03','rh03']
        
        elif self.ctype == 'h3':
            # CWB_H3_stno 局屬逐時觀測資料第三型
            self.ncolspec = [(0, 6), (7, 11), (11, 13), (13, 15), (15, 17), (17, 24),  
                (24, 31), (31, 38), (38, 45), (45, 52), (52, 59), (59, 66), (66, 73),  
                (73, 80), (80, 87), (87, 94), (94, 101), (101, 108), (108, 115),  
                (115, 122), (122, 129), (129, 136), (136, 143), (143, 150), (150, 157), 
                (157, 164), (164, 171), (171, 178), (178, 185), (185, 192), (192, 199), 
                (199, 206), (206, 213), (213, 220), (220, 227), (227, 234), (234, 241), 
                (241, 248), (248, 255), (255, 262), (262, 269), (269, 276), (276, 283), 
                (283, 290), (290, 297), (297, 304), (304, 311), (311, 318), (318, 325), 
                (325, 332), (332,339)]
            self.colnames = ['stn_no','yr','mm','dd','hr','ps01','ps02','tx01','tx04','tx05','rh01','rh02', 
                        'wd01','wd02','wd03','wd04','wd05','wd06','pp01','pp02','ss01','ss02','vs01', 
                        'cd01','cd02','cd03','cd04','cd05','cd06','cd07','cd08','cd09','cd10','cd11', 
                        'ts01','ts02','ts03','ts04','ts05','st01','st02','st03','st04','st05','st06', 
                        'st07','st08','st09','st10','st11','st12']
        else:
            print("Please specify the input file type")
        cwb_data = pd.read_fwf(infile, colspecs=self.ncolspec, header=header)
        colnames_dict = {key: self.colnames[key] for key in range(0,len(self.colnames))}
        cwb_data.rename(columns=colnames_dict, inplace=True)
        return(cwb_data)

