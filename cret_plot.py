# Plotting script for the data analyses run in CRET_analysis.py
# Author: James Wilmott, Winter 2018

#Designed to plot data from a persistent database
from pylab import *
from matplotlib import patches
from matplotlib import pyplot as plt
from matplotlib import cm
import matplotlib.lines as mlines
import shelve #for database writing and reading
from mpl_toolkits.axes_grid.inset_locator import inset_axes

############################################
## Specify some universal parameters ##
############################################

savepath =  '/Users/jameswilmott/Documents/Python/CRET/figures/';  #'/Users/james/Documents/Python/CRET/figures/'; # 
shelvepath =  '/Users/jameswilmott/Documents/Python/CRET/data/';  #'/Users/james/Documents/Python/CRET/data/'; # 

db = shelve.open(shelvepath+'data'); 

ids=['cret01','cret03','cret04','cret05','cret06','cret07','cret08','cret09','cret10','cret11'];

#set parameters for plots
matplotlib.rcParams['ytick.labelsize']=20; matplotlib.rcParams['xtick.labelsize']=18;
matplotlib.rcParams['xtick.major.width']=2.0; matplotlib.rcParams['ytick.major.width']=2.0;
matplotlib.rcParams['xtick.major.size']=10.0; matplotlib.rcParams['ytick.major.size']=10.0;
matplotlib.rcParams['hatch.linewidth'] = 9.0; #set the hatch width to larger than the default case
matplotlib.rcParams['hatch.color'] = 'black';
matplotlib.pyplot.rc('font',weight='bold');

############################################
## Plotting proportion of time spent fixating the eventually chosen item figure  ##
############################################

##Plot proportion for PAPC trials based on whetehr they chose the cue or not item for items when they chose alohol or cigarette
fig = figure(figsize = (12.8,7.64)); ax1=gca(); #grid(True);
title('Average proportion of time fixating each item in a trial \n depending on which item was selected', fontsize = 22);
ax1.set_ylim(0.0,1.1); ax1.set_yticks(arange(0.0,1.01,0.1)); ax1.set_xlim([0.7,3.0]); ax1.set_xticks([1,1.6,2.2]);
ax1.set_ylabel('Average proportion of time spent fixating during a trial',size=18); ax1.set_xlabel('Selected Item',size=18,labelpad=15);
ax1.set_xticklabels(['Cue Selected','Non-Cue Selected','Neutral Selected']); #'All PAPC Trials',
colors=['red','blue','green'];
#first plot the cases where the cue was selected. order will be cue, not_cue, neutral
ax1.bar(1.0,db['agg_high_pref_selected_cue_look_at_cue_mean_perc_time_at_pref'], color = colors[0], width = 0.3);
ax1.errorbar(1.0, db['agg_high_pref_selected_cue_look_at_cue_mean_perc_time_at_pref'],
             yerr=[[db['agg_high_pref_selected_cue_look_at_cue_bs_sems_perc_time_at_pref']],[db['agg_high_pref_selected_cue_look_at_cue_bs_sems_perc_time_at_pref']]],color='black',lw=6.0, capsize = 7.0);
ax1.bar(1.0,db['agg_high_pref_selected_cue_look_at_not_cue_mean_perc_time_at_pref'], bottom = db['agg_high_pref_selected_cue_look_at_cue_mean_perc_time_at_pref'], color = colors[1], width = 0.3);
ax1.errorbar(1.0, db['agg_high_pref_selected_cue_look_at_cue_mean_perc_time_at_pref']+db['agg_high_pref_selected_cue_look_at_not_cue_mean_perc_time_at_pref'],
             yerr=[[db['agg_high_pref_selected_cue_look_at_not_cue_bs_sems_perc_time_at_pref']],[db['agg_high_pref_selected_cue_look_at_not_cue_bs_sems_perc_time_at_pref']]],color='black',lw=6.0,capsize = 7.0);
ax1.bar(1.0,db['agg_high_pref_selected_cue_look_at_neutral_mean_perc_time_at_pref'], bottom = db['agg_high_pref_selected_cue_look_at_cue_mean_perc_time_at_pref']+db['agg_high_pref_selected_cue_look_at_not_cue_mean_perc_time_at_pref'], color = colors[2], width = 0.3);
ax1.errorbar(1.0, db['agg_high_pref_selected_cue_look_at_cue_mean_perc_time_at_pref']+db['agg_high_pref_selected_cue_look_at_not_cue_mean_perc_time_at_pref']+db['agg_high_pref_selected_cue_look_at_neutral_mean_perc_time_at_pref'],
             yerr=[[db['agg_high_pref_selected_cue_look_at_neutral_bs_sems_perc_time_at_pref']],[db['agg_high_pref_selected_cue_look_at_neutral_bs_sems_perc_time_at_pref']]],color='black',lw=6.0,capsize = 7.0);
#now selected not cue
ax1.bar(1.6,db['agg_high_pref_selected_not_cue_look_at_cue_mean_perc_time_at_pref'], color = colors[0], width = 0.3);
ax1.errorbar(1.6, db['agg_high_pref_selected_not_cue_look_at_cue_mean_perc_time_at_pref'],
             yerr=[[db['agg_high_pref_selected_not_cue_look_at_cue_bs_sems_perc_time_at_pref']],[db['agg_high_pref_selected_not_cue_look_at_cue_bs_sems_perc_time_at_pref']]],color='black',lw=6.0,capsize = 7.0);
ax1.bar(1.6,db['agg_high_pref_selected_not_cue_look_at_not_cue_mean_perc_time_at_pref'], bottom = db['agg_high_pref_selected_not_cue_look_at_cue_mean_perc_time_at_pref'], color = colors[1], width = 0.3);
ax1.errorbar(1.6, db['agg_high_pref_selected_not_cue_look_at_cue_mean_perc_time_at_pref']+db['agg_high_pref_selected_not_cue_look_at_not_cue_mean_perc_time_at_pref'],
             yerr=[[db['agg_high_pref_selected_not_cue_look_at_not_cue_bs_sems_perc_time_at_pref']],[db['agg_high_pref_selected_not_cue_look_at_not_cue_bs_sems_perc_time_at_pref']]],color='black',lw=6.0,capsize = 7.0);
ax1.bar(1.6,db['agg_high_pref_selected_not_cue_look_at_neutral_mean_perc_time_at_pref'], bottom = db['agg_high_pref_selected_not_cue_look_at_cue_mean_perc_time_at_pref']+db['agg_high_pref_selected_not_cue_look_at_not_cue_mean_perc_time_at_pref'], color = colors[2], width = 0.3);
ax1.errorbar(1.6, db['agg_high_pref_selected_not_cue_look_at_cue_mean_perc_time_at_pref']+db['agg_high_pref_selected_not_cue_look_at_not_cue_mean_perc_time_at_pref']+db['agg_high_pref_selected_not_cue_look_at_neutral_mean_perc_time_at_pref'],
             yerr=[[db['agg_high_pref_selected_not_cue_look_at_neutral_bs_sems_perc_time_at_pref']],[db['agg_high_pref_selected_not_cue_look_at_neutral_bs_sems_perc_time_at_pref']]],color='black',lw=6.0,capsize = 7.0);
#finally when they selected neutral trials
ax1.bar(2.2,db['agg_high_pref_selected_neutral_look_at_cue_mean_perc_time_at_pref'], color = colors[0], width = 0.3);
ax1.errorbar(2.2, db['agg_high_pref_selected_neutral_look_at_cue_mean_perc_time_at_pref'],
             yerr=[[db['agg_high_pref_selected_neutral_look_at_cue_bs_sems_perc_time_at_pref']],[db['agg_high_pref_selected_neutral_look_at_cue_bs_sems_perc_time_at_pref']]],color='black',lw=6.0,capsize = 7.0);
ax1.bar(2.2,db['agg_high_pref_selected_neutral_look_at_not_cue_mean_perc_time_at_pref'], bottom = db['agg_high_pref_selected_neutral_look_at_cue_mean_perc_time_at_pref'], color = colors[1], width = 0.3);
ax1.errorbar(2.2, db['agg_high_pref_selected_neutral_look_at_cue_mean_perc_time_at_pref']+db['agg_high_pref_selected_neutral_look_at_not_cue_mean_perc_time_at_pref'],
             yerr=[[db['agg_high_pref_selected_neutral_look_at_not_cue_bs_sems_perc_time_at_pref']],[db['agg_high_pref_selected_neutral_look_at_not_cue_bs_sems_perc_time_at_pref']]],color='black',lw=6.0,capsize = 7.0);
ax1.bar(2.2,db['agg_high_pref_selected_neutral_look_at_neutral_mean_perc_time_at_pref'], bottom = db['agg_high_pref_selected_neutral_look_at_cue_mean_perc_time_at_pref']+db['agg_high_pref_selected_neutral_look_at_not_cue_mean_perc_time_at_pref'], color = colors[2], width = 0.3);
ax1.errorbar(2.2, db['agg_high_pref_selected_neutral_look_at_cue_mean_perc_time_at_pref']+db['agg_high_pref_selected_neutral_look_at_not_cue_mean_perc_time_at_pref']+db['agg_high_pref_selected_neutral_look_at_neutral_mean_perc_time_at_pref'],
             yerr=[[db['agg_high_pref_selected_neutral_look_at_neutral_bs_sems_perc_time_at_pref']],[db['agg_high_pref_selected_neutral_look_at_neutral_bs_sems_perc_time_at_pref']]],color='black',lw=6.0,capsize = 7.0);

#plot RTs for each type of trial in an inset
ia = inset_axes(ax1, width="25%", height="30%", loc=1); #set the inset axes as percentages of the original axis size
ia.set_xlim([0.85,2.35]); ia.set_xticks([1,1.6,2.2]); ia.set_ylim([750,1100]); ia.set_yticks(arange(800,1201,100));
ia.set_xticklabels(['Cue Selected','Non-Cue Selected','Neutral Selected'], size = 10);
ia.set_ylabel('Reaction time (ms)',size=10); ia.set_xlabel('Selected Item',size=10); ia.yaxis.set_label_position('right'); ia.yaxis.set_ticks_position('right');
ia.set_yticklabels(['800','900','1000','1100','1200'], size = 10);
ia.bar(1.0,db['agg_high_pref_selected_cue_mean_rt'], color = 'grey', width = 0.3);
ia.errorbar(1.0, db['agg_high_pref_selected_cue_mean_rt'],
             yerr=[[db['agg_high_pref_selected_cue_bs_sems_rt']],[db['agg_high_pref_selected_cue_bs_sems_rt']]],color='black',lw=2.0,capsize = 3.0);
ia.bar(1.6,db['agg_high_pref_selected_not_cue_mean_rt'], color = 'grey', width = 0.3);
ia.errorbar(1.6, db['agg_high_pref_selected_not_cue_mean_rt'],
             yerr=[[db['agg_high_pref_selected_not_cue_bs_sems_rt']],[db['agg_high_pref_selected_not_cue_bs_sems_rt']]],color='black',lw=2.0,capsize = 3.0);
ia.bar(2.2,db['agg_high_pref_selected_neutral_mean_rt'], color = 'grey', width = 0.3);
ia.errorbar(2.2, db['agg_high_pref_selected_neutral_mean_rt'],
             yerr=[[db['agg_high_pref_selected_neutral_bs_sems_rt']],[db['agg_high_pref_selected_neutral_bs_sems_rt']]],color='black',lw=2.0,capsize = 3.0);
title('Mean RT', fontsize = 14);

ax1.spines['right'].set_visible(False); ax1.spines['top'].set_visible(False);
ax1.spines['bottom'].set_linewidth(2.0); ax1.spines['left'].set_linewidth(2.0);
ax1.yaxis.set_ticks_position('left'); ax1.xaxis.set_ticks_position('bottom');
legend_lines = [mlines.Line2D([],[],color=colors[0],lw=6,alpha = 1, label='looked at cue'),
                 mlines.Line2D([],[],color=colors[1],lw=6,alpha = 1, label='looked at not_cue'),
                 mlines.Line2D([],[],color=colors[2],lw=6,alpha = 1, label='looked at neutral')];
ax1.legend(handles=[legend_lines[0],legend_lines[1], legend_lines[2]],loc = 4,ncol=1,fontsize = 14);
#save the labeled figure as a .png	
filename = 'fixate_preferred_item_labeled';
#savefig(savepath+filename+'.png',dpi=400);
# #then get rid of labels and save as a .eps
# labels = [item.get_text() for item in ax1.get_xticklabels()]; labels[0]=''; labels[1]=''; labels[2]=''; labels[3]=''; labels[4]='';#have to do this to center the x ticks on correct spot without incurring ticks at every spot
# ax1.set_xticklabels(labels);
# ax1.set_yticklabels(['','','','','','','','','','','','','','']);
# ax1.set_ylabel(''); ax1.set_xlabel(''); title('');
# filename = 'cue_vs_not_cue_percentage_time_fixate_preferred_item';
# savefig(savepath+filename+'.eps',dpi=400);
show();



############################################
## Plotting proportion of trials the last fixted items was the preferred item figure  ##
############################################

# ##Plot proportion for PAPC trials based on whetehr they chose the cue or not item for items when they chose alohol or cigarette
# fig = figure(figsize = (12.8,7.64)); ax1=gca(); #grid(True);
# ax1.set_ylim(0.25,0.75); ax1.set_yticks(arange(0.30,0.751,0.05)); ax1.set_xlim([0.7,2.5]); ax1.set_xticks([1,1.6,2.2]); #,2.8]); ax1.set_xlim([0.7,3.1]);
# ax1.set_ylabel('Proportion of trials last fixated item was selected',size=18); ax1.set_xlabel('Trial Type',size=18,labelpad=15);
# ax1.set_xticklabels(['Cue Selected','Non-Cue Selected','Neutral Selected']); #'All PAPC Trials',
# colors=['green'];
# # ax1.bar(1.0,db['%s_%s_mean_prop_last_fixated_item'%('agg','high_pref')],color=colors[0],width=0.3);
# # ax1.errorbar(1.0,db['%s_%s_mean_prop_last_fixated_item'%('agg','high_pref')],
# # 			 yerr=[[db['%s_%s_bs_sems_prop_last_fixated_item'%('agg','high_pref')]],[db['%s_%s_bs_sems_prop_last_fixated_item'%('agg','high_pref')]]],color='black',lw=6.0);
# ax1.bar(1.0,db['%s_%s_selected_%s_mean_prop_last_fixated_item'%('agg','high_pref','cue')],color=colors[0],width=0.3);
# ax1.errorbar(1.0,db['%s_%s_selected_%s_mean_prop_last_fixated_item'%('agg','high_pref','cue')],
# 			 yerr=[[db['%s_%s_selected_%s_bs_sems_prop_last_fixated_item'%('agg','high_pref','cue')]],[db['%s_%s_selected_%s_bs_sems_prop_last_fixated_item'%('agg','high_pref','cue')]]],color='black',lw=6.0);
# ax1.bar(1.6,db['%s_%s_selected_%s_mean_prop_last_fixated_item'%('agg','high_pref','not_cue')],color=colors[0],width=0.3);
# ax1.errorbar(1.6,db['%s_%s_selected_%s_mean_prop_last_fixated_item'%('agg','high_pref','not_cue')],
# 			 yerr=[[db['%s_%s_selected_%s_bs_sems_prop_last_fixated_item'%('agg','high_pref','not_cue')]],[db['%s_%s_selected_%s_bs_sems_prop_last_fixated_item'%('agg','high_pref','not_cue')]]],color='black',lw=6.0);
# ax1.bar(2.2,db['%s_high_pref_%s_mean_prop_last_fixated_item'%('agg','neutral')],color=colors[0],width=0.3);
# ax1.errorbar(2.2,db['%s_high_pref_%s_mean_prop_last_fixated_item'%('agg','neutral')],
# 			 yerr=[[db['%s_high_pref_%s_bs_sems_prop_last_fixated_item'%('agg','neutral')]],[db['%s_high_pref_%s_bs_sems_prop_last_fixated_item'%('agg','neutral')]]],color='black',lw=6.0);
# ax1.spines['right'].set_visible(False); ax1.spines['top'].set_visible(False);
# ax1.spines['bottom'].set_linewidth(2.0); ax1.spines['left'].set_linewidth(2.0);
# ax1.yaxis.set_ticks_position('left'); ax1.xaxis.set_ticks_position('bottom');
# title('Average proportion of trials the selected item \n was the last item fixated', fontsize = 22);
# #save the labeled figure as a .png	
# filename = 'cue_vs_not_cue_percentage_trials_last_fixated_item_labeled';
# savefig(savepath+filename+'.png',dpi=400);
# # #then get rid of labels and save as a .eps
# # labels = [item.get_text() for item in ax1.get_xticklabels()]; labels[0]=''; labels[1]=''; labels[2]=''; labels[3]=''; labels[4]='';#have to do this to center the x ticks on correct spot without incurring ticks at every spot
# # ax1.set_xticklabels(labels);
# # ax1.set_yticklabels(['','','','','','','','','','','','','','']);
# # ax1.set_ylabel(''); ax1.set_xlabel(''); title('');
# # filename = 'cue_vs_not_cue_percentage_trials_last_fixated_item';
# # savefig(savepath+filename+'.eps',dpi=400);
# show();


# ##Plot the proportions for hgh pref trials based on what they chose (alcohol, cig, neutral)
# fig = figure(figsize = (12.8,7.64)); ax1=gca(); #grid(True);
# ax1.set_ylim(0.25,0.8); ax1.set_yticks(arange(0.3,0.81,0.05)); ax1.set_xlim([0.7,3.7]); ax1.set_xticks([1,1.6,2.2,2.8,3.4]);
# ax1.set_ylabel('Proportion of trials last fixated item was selected',size=18); ax1.set_xlabel('Condition',size=18,labelpad=40);
# ax1.set_xticklabels(['Not PAPC Trials','All PAPC Trials','PAPC, Alcohol Trials','PAPC, Cigarette Trials','PAPC, Neutral Trials']);
# colors=['green'];
# ax1.bar(1,db['%s_%s_mean_prop_last_fixated_item'%('agg','non_high_pref')],color=colors[0],width=0.3);
# ax1.errorbar(1,db['%s_%s_mean_prop_last_fixated_item'%('agg','non_high_pref')],
# 			 yerr=[[db['%s_%s_bs_sems_prop_last_fixated_item'%('agg','non_high_pref')]],[db['%s_%s_bs_sems_prop_last_fixated_item'%('agg','non_high_pref')]]],color='black',lw=6.0);
# ax1.bar(1.6,db['%s_%s_mean_prop_last_fixated_item'%('agg','high_pref')],color=colors[0],width=0.3);
# ax1.errorbar(1.6,db['%s_%s_mean_prop_last_fixated_item'%('agg','high_pref')],
# 			 yerr=[[db['%s_%s_bs_sems_prop_last_fixated_item'%('agg','high_pref')]],[db['%s_%s_bs_sems_prop_last_fixated_item'%('agg','high_pref')]]],color='black',lw=6.0);
# ax1.bar(2.2,db['%s_high_pref_%s_mean_prop_last_fixated_item'%('agg','alcohol')],color=colors[0],width=0.3);
# ax1.errorbar(2.2,db['%s_high_pref_%s_mean_prop_last_fixated_item'%('agg','alcohol')],
# 			 yerr=[[db['%s_high_pref_%s_bs_sems_prop_last_fixated_item'%('agg','alcohol')]],[db['%s_high_pref_%s_bs_sems_prop_last_fixated_item'%('agg','alcohol')]]],color='black',lw=6.0);
# ax1.bar(2.8,db['%s_high_pref_%s_mean_prop_last_fixated_item'%('agg','cigarette')],color=colors[0],width=0.3);
# ax1.errorbar(2.8,db['%s_high_pref_%s_mean_prop_last_fixated_item'%('agg','cigarette')],
# 			 yerr=[[db['%s_high_pref_%s_bs_sems_prop_last_fixated_item'%('agg','cigarette')]],[db['%s_high_pref_%s_bs_sems_prop_last_fixated_item'%('agg','cigarette')]]],color='black',lw=6.0);
# ax1.bar(3.4,db['%s_high_pref_%s_mean_prop_last_fixated_item'%('agg','neutral')],color=colors[0],width=0.3);
# ax1.errorbar(3.4,db['%s_high_pref_%s_mean_prop_last_fixated_item'%('agg','neutral')],
# 			 yerr=[[db['%s_high_pref_%s_bs_sems_prop_last_fixated_item'%('agg','neutral')]],[db['%s_high_pref_%s_bs_sems_prop_last_fixated_item'%('agg','neutral')]]],color='black',lw=6.0);
# ax1.spines['right'].set_visible(False); ax1.spines['top'].set_visible(False);
# ax1.spines['bottom'].set_linewidth(2.0); ax1.spines['left'].set_linewidth(2.0);
# ax1.yaxis.set_ticks_position('left'); ax1.xaxis.set_ticks_position('bottom');
# title('Proportion of trials fixating the selected item last \n for preferred alcohol/preferred cigarette (PAPC) trials', fontsize = 22);
# #save the labeled figure as a .png	
# filename = 'percentage_trials_last_fixated_item_labeled';
# savefig(savepath+filename+'.png',dpi=400);
# # #then get rid of labels and save as a .eps
# # labels = [item.get_text() for item in ax1.get_xticklabels()]; labels[0]=''; labels[1]=''; labels[2]=''; labels[3]=''; labels[4]='';#have to do this to center the x ticks on correct spot without incurring ticks at every spot
# # ax1.set_xticklabels(labels);
# # ax1.set_yticklabels(['','','','','','','','','','','','','','']);
# # ax1.set_ylabel(''); ax1.set_xlabel(''); title('');
# # filename = 'percentage_trials_last_fixated_item';
# # savefig(savepath+filename+'.eps',dpi=400);
# show();

############################################
## Legacy code for plotting proportion of time spent looking at each item, whetehr its alcohol, cig, or neutral/cue vs. not cue  ##
############################################

# ##Plot proportion for PAPC trials based on whetehr they chose the cue or not item for items when they chose alohol or cigarette
# fig = figure(figsize = (12.8,7.64)); ax1=gca(); #grid(True);
# ax1.set_ylim(0.25,0.75); ax1.set_yticks(arange(0.30,0.751,0.05)); ax1.set_xlim([0.7,2.5]); ax1.set_xticks([1,1.6,2.2]); #,2.8]); ax1.set_xlim([0.7,3.1]);
# ax1.set_ylabel('Proportion of time fixating selected item',size=18); ax1.set_xlabel('Trial Type',size=18,labelpad=15);
# ax1.set_xticklabels(['Cue Selected','Non-Cue Selected','Neutral Selected']); #'All PAPC Trials',
# colors=['gray'];
# # ax1.bar(1.0,db['%s_%s_mean_perc_time_at_pref'%('agg','high_pref')],color=colors[0],width=0.3);
# # ax1.errorbar(1.0,db['%s_%s_mean_perc_time_at_pref'%('agg','high_pref')],
# # 			 yerr=[[db['%s_%s_bs_sems_perc_time_at_pref'%('agg','high_pref')]],[db['%s_%s_bs_sems_perc_time_at_pref'%('agg','high_pref')]]],color='black',lw=6.0);
# ax1.bar(1.0,db['%s_%s_selected_%s_mean_perc_time_at_pref'%('agg','high_pref','cue')],color=colors[0],width=0.3);
# ax1.errorbar(1.0,db['%s_%s_selected_%s_mean_perc_time_at_pref'%('agg','high_pref','cue')],
# 			 yerr=[[db['%s_%s_selected_%s_bs_sems_perc_time_at_pref'%('agg','high_pref','cue')]],[db['%s_%s_selected_%s_bs_sems_perc_time_at_pref'%('agg','high_pref','cue')]]],color='black',lw=6.0);
# ax1.bar(1.6,db['%s_%s_selected_%s_mean_perc_time_at_pref'%('agg','high_pref','not_cue')],color=colors[0],width=0.3);
# ax1.errorbar(1.6,db['%s_%s_selected_%s_mean_perc_time_at_pref'%('agg','high_pref','not_cue')],
# 			 yerr=[[db['%s_%s_selected_%s_bs_sems_perc_time_at_pref'%('agg','high_pref','not_cue')]],[db['%s_%s_selected_%s_bs_sems_perc_time_at_pref'%('agg','high_pref','not_cue')]]],color='black',lw=6.0);
# ax1.bar(2.2,db['%s_high_pref_%s_mean_perc_time_at_pref'%('agg','neutral')],color=colors[0],width=0.3);
# ax1.errorbar(2.2,db['%s_high_pref_%s_mean_perc_time_at_pref'%('agg','neutral')],
# 			 yerr=[[db['%s_high_pref_%s_bs_sems_perc_time_at_pref'%('agg','neutral')]],[db['%s_high_pref_%s_bs_sems_perc_time_at_pref'%('agg','neutral')]]],color='black',lw=6.0);
# ax1.spines['right'].set_visible(False); ax1.spines['top'].set_visible(False);
# ax1.spines['bottom'].set_linewidth(2.0); ax1.spines['left'].set_linewidth(2.0);
# ax1.yaxis.set_ticks_position('left'); ax1.xaxis.set_ticks_position('bottom');
# title('Average proportion of time fixating selected item in each trial', fontsize = 22);
# #save the labeled figure as a .png	
# filename = 'cue_vs_not_cue_percentage_time_fixate_preferred_item_labeled';
# savefig(savepath+filename+'.png',dpi=400);
# # #then get rid of labels and save as a .eps
# # labels = [item.get_text() for item in ax1.get_xticklabels()]; labels[0]=''; labels[1]=''; labels[2]=''; labels[3]=''; labels[4]='';#have to do this to center the x ticks on correct spot without incurring ticks at every spot
# # ax1.set_xticklabels(labels);
# # ax1.set_yticklabels(['','','','','','','','','','','','','','']);
# # ax1.set_ylabel(''); ax1.set_xlabel(''); title('');
# # filename = 'cue_vs_not_cue_percentage_time_fixate_preferred_item';
# # savefig(savepath+filename+'.eps',dpi=400);
# show();

# 
# ##Plot the proportions for hgh pref trials based on what they chose (alcohol, cig, neutral)
# fig = figure(figsize = (12.8,7.64)); ax1=gca(); #grid(True);
# ax1.set_ylim(0.25,0.75); ax1.set_yticks(arange(0.30,0.751,0.05)); ax1.set_xlim([0.7,3.7]); ax1.set_xticks([1,1.6,2.2,2.8,3.4]);
# ax1.set_ylabel('Proportion of time fixating preferred item',size=18); ax1.set_xlabel('Condition',size=18,labelpad=40);
# ax1.set_xticklabels(['Not PAPC Trials','All PAPC Trials','PAPC, Alcohol Trials','PAPC, Cigarette Trials','PAPC, Neutral Trials']);
# colors=['blue'];
# ax1.bar(1,db['%s_%s_mean_perc_time_at_pref'%('agg','non_high_pref')],color=colors[0],width=0.3);
# ax1.errorbar(1,db['%s_%s_mean_perc_time_at_pref'%('agg','non_high_pref')],
# 			 yerr=[[db['%s_%s_bs_sems_perc_time_at_pref'%('agg','non_high_pref')]],[db['%s_%s_bs_sems_perc_time_at_pref'%('agg','non_high_pref')]]],color='black',lw=6.0);
# ax1.bar(1.6,db['%s_%s_mean_perc_time_at_pref'%('agg','high_pref')],color=colors[0],width=0.3);
# ax1.errorbar(1.6,db['%s_%s_mean_perc_time_at_pref'%('agg','high_pref')],
# 			 yerr=[[db['%s_%s_bs_sems_perc_time_at_pref'%('agg','high_pref')]],[db['%s_%s_bs_sems_perc_time_at_pref'%('agg','high_pref')]]],color='black',lw=6.0);
# ax1.bar(2.2,db['%s_high_pref_%s_mean_perc_time_at_pref'%('agg','alcohol')],color=colors[0],width=0.3);
# ax1.errorbar(2.2,db['%s_high_pref_%s_mean_perc_time_at_pref'%('agg','alcohol')],
# 			 yerr=[[db['%s_high_pref_%s_bs_sems_perc_time_at_pref'%('agg','alcohol')]],[db['%s_high_pref_%s_bs_sems_perc_time_at_pref'%('agg','alcohol')]]],color='black',lw=6.0);
# ax1.bar(2.8,db['%s_high_pref_%s_mean_perc_time_at_pref'%('agg','cigarette')],color=colors[0],width=0.3);
# ax1.errorbar(2.8,db['%s_high_pref_%s_mean_perc_time_at_pref%('agg','cigarette')],
# 			 yerr=[[db['%s_high_pref_%s_bs_sems_perc_time_at_pref'%('agg','cigarette')]],[db['%s_high_pref_%s_bs_sems_perc_time_at_pref'%('agg','cigarette')]]],color='black',lw=6.0);
# ax1.bar(3.4,db['%s_high_pref_%s_mean_perc_time_at_pref'%('agg','neutral')],color=colors[0],width=0.3);
# ax1.errorbar(3.4,db['%s_high_pref_%s_mean_perc_time_at_pref'%('agg','neutral')],
# 			 yerr=[[db['%s_high_pref_%s_bs_sems_perc_time_at_pref'%('agg','neutral')]],[db['%s_high_pref_%s_bs_sems_perc_time_at_pref'%('agg','neutral')]]],color='black',lw=6.0);
# ax1.spines['right'].set_visible(False); ax1.spines['top'].set_visible(False);
# ax1.spines['bottom'].set_linewidth(2.0); ax1.spines['left'].set_linewidth(2.0);
# ax1.yaxis.set_ticks_position('left'); ax1.xaxis.set_ticks_position('bottom');
# title('Proportion of time fixating preferred item \n for preferred alcohol/preferred cigarette (PAPC) trials', fontsize = 22);
# #save the labeled figure as a .png	
# filename = 'percentage_time_fixate_preferred_item_labeled';
# savefig(savepath+filename+'.png',dpi=400);
# # #then get rid of labels and save as a .eps
# # labels = [item.get_text() for item in ax1.get_xticklabels()]; labels[0]=''; labels[1]=''; labels[2]=''; labels[3]=''; labels[4]='';#have to do this to center the x ticks on correct spot without incurring ticks at every spot
# # ax1.set_xticklabels(labels);
# # ax1.set_yticklabels(['','','','','','','','','','','','','','']);
# # ax1.set_ylabel(''); ax1.set_xlabel(''); title('');
# # filename = 'percentage_time_fixate_preferred_item';
# # savefig(savepath+filename+'.eps',dpi=400);
# show();




