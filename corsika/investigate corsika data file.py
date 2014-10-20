# -*- coding: utf-8 -*-
"""
Created on Mon Oct 13 17:27:40 2014

@author: Tom
"""
import tables

#FILENAME = 'corsika_834927089_144221120.h5'    # 1e14 p theta = 0 
#FILENAME = 'corsika_713335232_854491062.h5'    # 1e14 p theta = 0
FILENAME = 'corsika_77102826_200916071.h5'     # 1e14 p theta = 22.5

data = tables.open_file(FILENAME, 'r')
gp = data.root.groundparticles
x = gp.col('x')
y = gp.col('y')
plot(x,y,'o')
data.close()