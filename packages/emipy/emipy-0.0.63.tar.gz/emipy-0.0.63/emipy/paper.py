# -*- coding: utf-8 -*-
"""
Created on Thu Oct 22 10:46:17 2020

@author: Morgenthaler

This file contains the figures we use for our paper....
"""


import emipy
import matplotlib.pyplot as plt

db = emipy.read_db()

data3 = emipy.f_db(db, CountryName=['France', 'Germany', 'Italy'], ReportingYear=[2014, 2015, 2016], PollutantName=['Carbon dioxide (CO2)'])

fig, ax = plt.subplots(2, 2, figsize=(8.27, (1.5/3)*11.69))
emipy.plot_PollutantVolume(data3, FirstOrder='ReportingYear', ax=ax[0, 0], legend=False, rot=0)
#ax[0, 0].set_title('emipy.plot_PollutantVolume\n(data3, FirstOrder=\'ReportingYear\')', y=1.05)
ax[0, 0].set_title('(a)', loc='right')
ax[0, 0].set_ylabel(r'CO$_2$ emissions [kg]')
ax[0, 0].set_xlabel('')

emipy.plot_PollutantVolume(data3, FirstOrder='CountryName', ax=ax[0, 1], legend=False, rot=0)
#ax[0, 1].set_title('emipy.plot_PollutantVolume\n(data3, FirstOrder=\'CountryName\')', y=1.05)
ax[0, 1].set_title('(b)', loc='right')
ax[0, 1].set_ylabel(r'CO$_2$ emissions [kg]')
ax[0, 1].set_xlabel('')

emipy.plot_PollutantVolume(data3, FirstOrder='ReportingYear', SecondOrder='CountryName', ax=ax[1, 0], rot=0)
#ax[1, 0].set_title('emipy.plot_PollutantVolume\n(data3, FirstOrder=\'ReportingYear\',\nSecondOrder=\'CountryName\')')
ax[1, 0].set_title('(c)', loc='right')
ax[1, 0].set_xlabel('')
ax[1, 0].set_ylabel(r'CO$_2$ emissions [kg]')
ax[1, 0].legend(loc='lower center', ncol=3, bbox_to_anchor=(0.5, -0.3))

emipy.plot_PollutantVolumeChange(data3, FirstOrder='ReportingYear', ax=ax[1,1], legend=False, rot=0)
ax[1, 1].set_title('(d)', loc='right')
ax[1, 1].set_xlabel('')
ax[1, 1].set_ylabel(r'Change of CO$_2$ emissions' + '\nto previous year [kg]')

plt.subplots_adjust(hspace=0.3, wspace=0.3)

fig.savefig('plotting_example_1.pdf', bbox_inches='tight')

