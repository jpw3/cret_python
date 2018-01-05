# Plotting script for the data analyses run in CRET_analysis.py
# Author: James Wilmott, Winter 2018

#Designed to plot data from a persistent database
from pylab import *
from matplotlib import patches
from matplotlib import pyplot as plt
from matplotlib import cm
import matplotlib.lines as mlines
import shelve #for database writing and reading

############################################
## Specify some universal parameters ##
############################################

savepath =  '/Users/james/Documents/Python/CRET/figures/'; # '/Users/jameswilmott/Documents/Python/CRET/figures/';  #
shelvepath =  '/Users/james/Documents/Python/CRET/data/'; # '/Users/jameswilmott/Documents/Python/CRET/data/';  #

db = shelve.open(shelvepath+'data'); 

ids=['cret01','cret03','cret04','cret05','cret06','cret07','cret08','cret09','cret10','cret11'];

#set parameters for plots
matplotlib.rcParams['ytick.labelsize']=20; matplotlib.rcParams['xtick.labelsize']=10;
matplotlib.rcParams['xtick.major.width']=2.0; matplotlib.rcParams['ytick.major.width']=2.0;
matplotlib.rcParams['xtick.major.size']=10.0; matplotlib.rcParams['ytick.major.size']=10.0;
matplotlib.rcParams['hatch.linewidth'] = 9.0; #set the hatch width to larger than the default case
matplotlib.rcParams['hatch.color'] = 'black';
matplotlib.pyplot.rc('font',weight='bold');

############################################
## Figure plotting ##
############################################

### Plotting percentage of time spent fixating the eventually chosen item data ###
fig = figure(figsize = (12.8,7.64)); ax1=gca(); #grid(True);
ax1.set_ylim(0.25,0.75); ax1.set_yticks(arange(0.30,0.751,0.05)); ax1.set_xlim([0.7,3.7]); ax1.set_xticks([1,1.6,2.2,2.8,3.4]);
ax1.set_ylabel('Proportion of time fixating preferred item',size=18); ax1.set_xlabel('Condition',size=18,labelpad=40);
ax1.set_xticklabels(['Not APAC Trials','All APAC Trials','APAC, Alcohol Trials','APAC, Cigarette Trials','APAC, Neutral Trials']);
colors=['blue'];
ax1.bar(1,db['%s_%s_mean_perc_time_at_pref'%('agg','non_high_pref')],color=colors[0],width=0.3);
ax1.errorbar(1,db['%s_%s_mean_perc_time_at_pref'%('agg','non_high_pref')],
			 yerr=[[db['%s_%s_bs_sems_perc_time_at_pref'%('agg','non_high_pref')]],[db['%s_%s_bs_sems_perc_time_at_pref'%('agg','non_high_pref')]]],color='black',lw=6.0);
ax1.bar(1.6,db['%s_%s_mean_perc_time_at_pref'%('agg','high_pref')],color=colors[0],width=0.3);
ax1.errorbar(1.6,db['%s_%s_mean_perc_time_at_pref'%('agg','high_pref')],
			 yerr=[[db['%s_%s_bs_sems_perc_time_at_pref'%('agg','high_pref')]],[db['%s_%s_bs_sems_perc_time_at_pref'%('agg','high_pref')]]],color='black',lw=6.0);
ax1.bar(2.2,db['%s_high_pref_%s_mean_perc_time_at_pref'%('agg','alcohol')],color=colors[0],width=0.3);
ax1.errorbar(2.2,db['%s_high_pref_%s_mean_perc_time_at_pref'%('agg','alcohol')],
			 yerr=[[db['%s_high_pref_%s_bs_sems_perc_time_at_pref'%('agg','alcohol')]],[db['%s_high_pref_%s_bs_sems_perc_time_at_pref'%('agg','alcohol')]]],color='black',lw=6.0);
ax1.bar(2.8,db['%s_high_pref_%s_mean_perc_time_at_pref'%('agg','cigarette')],color=colors[0],width=0.3);
ax1.errorbar(2.8,db['%s_high_pref_%s_mean_perc_time_at_pref'%('agg','cigarette')],
			 yerr=[[db['%s_high_pref_%s_bs_sems_perc_time_at_pref'%('agg','cigarette')]],[db['%s_high_pref_%s_bs_sems_perc_time_at_pref'%('agg','cigarette')]]],color='black',lw=6.0);
ax1.bar(3.4,db['%s_high_pref_%s_mean_perc_time_at_pref'%('agg','neutral')],color=colors[0],width=0.3);
ax1.errorbar(3.4,db['%s_high_pref_%s_mean_perc_time_at_pref'%('agg','neutral')],
			 yerr=[[db['%s_high_pref_%s_bs_sems_perc_time_at_pref'%('agg','neutral')]],[db['%s_high_pref_%s_bs_sems_perc_time_at_pref'%('agg','neutral')]]],color='black',lw=6.0);
ax1.spines['right'].set_visible(False); ax1.spines['top'].set_visible(False);
ax1.spines['bottom'].set_linewidth(2.0); ax1.spines['left'].set_linewidth(2.0);
ax1.yaxis.set_ticks_position('left'); ax1.xaxis.set_ticks_position('bottom');
#save the labeled figure as a .png	
filename = 'percentage_time_fixate_preferred_item_labeled';
savefig(savepath+filename+'.png',dpi=400);
# #then get rid of labels and save as a .eps
# labels = [item.get_text() for item in ax1.get_xticklabels()]; labels[0]=''; labels[1]=''; labels[2]=''; labels[3]=''; labels[4]='';#have to do this to center the x ticks on correct spot without incurring ticks at every spot
# ax1.set_xticklabels(labels);
# ax1.set_yticklabels(['','','','','','','','','','','','','','']);
# ax1.set_ylabel(''); ax1.set_xlabel('');
# filename = 'percentage_time_fixate_preferred_item';
# savefig(savepath+filename+'.eps',dpi=400);
show();
