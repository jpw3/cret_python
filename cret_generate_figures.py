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

savepath =  '/Volumes/WORK_HD/code/Python/CRET/figures/'; #'/Users/james/Documents/Python/CRET/figures/'; #'/Users/jameswilmott/Documents/Python/CRET/figures/';  # 
shelvepath =  '/Volumes/WORK_HD/code/Python/CRET/data/'; # '/Users/james/Documents/Python/CRET/data/'; # '/Users/jameswilmott/Documents/Python/CRET/data/';  #

eyed = 'agg'; #raw_input('ID for plotting (agg for all subjects): ');
ttype = int(raw_input('Which trial type? 1 = HighC/HighA, 2 = HighC/LowA, 3 = LowC/HighA, 4 = LowC/LowA: '));
name = ['high_pref', 'highC_lowA','lowC_highA','lowC_lowA'][ttype-1];


db = shelve.open(shelvepath+'data'); 


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


# 
# #mean proportion selected for each substance
# fig = figure(figsize = (12.8,7.64)); ax1=gca(); #grid(True);
# #title('Average proportion of time fixating each item in a trial \n all trials aggregated together, subject %s'%eyed, fontsize = 22);
# ax1.set_ylim(0, 0.8); ax1.set_yticks(arange(0, 0.81, 0.1)); ax1.set_xlim([0.5,1.7]); ax1.set_xticks([0.85, 1.15, 1.45]);
# ax1.set_ylabel('Proportion selected',size=18); ax1.set_xlabel('Selected Item',size=18,labelpad=15);
# ax1.set_xticklabels(['Alcohol','Cigarette','Neutral']);
# colors=['red','blue','green'];
# ax1.bar(0.85,db['%s_%s_all_hp_mean_chose_alc'%(eyed,name)], color = colors[0], width = 0.25);
# ax1.errorbar(0.85, db['%s_%s_all_hp_mean_chose_alc'%(eyed,name)],
#              yerr=[[db['%s_%s_all_hp_bs_sems_chose_alc'%(eyed,name)]],[db['%s_%s_all_hp_bs_sems_chose_alc'%(eyed,name)]]],color='black',lw=6.0,capsize = 0);
# ax1.bar(1.15,db['%s_%s_all_hp_mean_chose_cig'%(eyed,name)], color = colors[1], width = 0.25);
# ax1.errorbar(1.15, db['%s_%s_all_hp_mean_chose_cig'%(eyed,name)],
#              yerr=[[db['%s_%s_all_hp_bs_sems_chose_cig'%(eyed,name)]],[db['%s_%s_all_hp_bs_sems_chose_cig'%(eyed,name)]]],color='black',lw=6.0,capsize = 0);
# ax1.bar(1.45,db['%s_%s_all_hp_mean_chose_neu'%(eyed,name)], color = colors[2], width = 0.25);
# ax1.errorbar(1.45, db['%s_%s_all_hp_mean_chose_neu'%(eyed,name)],
#              yerr=[[db['%s_%s_all_hp_bs_sems_chose_neu'%(eyed,name)]],[db['%s_%s_all_hp_bs_sems_chose_neu'%(eyed,name)]]],color='black',lw=6.0,capsize = 0);
# ax1.spines['right'].set_visible(False); ax1.spines['top'].set_visible(False);
# ax1.spines['bottom'].set_linewidth(2.0); ax1.spines['left'].set_linewidth(2.0);
# ax1.yaxis.set_ticks_position('left'); ax1.xaxis.set_ticks_position('bottom');
# #save the labeled figure as a .png	
# filename = '%s_prop_chosen_item_labeled'%name;
# savefig(savepath+filename+'.png',dpi=400);
# 
# 1/0
# 
# #then get rid of labels and save as a .eps
# labels = [item.get_text() for item in ax1.get_xticklabels()]; labels[0]=''; labels[1]=''; labels[2]=''; #labels[3]=''; labels[4]='';#have to do this to center the x ticks on correct spot without incurring ticks at every spot
# ax1.set_xticklabels(labels);
# ax1.set_yticklabels(['','','','','','','','','','','','','','']);
# ax1.set_ylabel(''); ax1.set_xlabel(''); title('');
# filename = '%s_prop_chosen_item'%name;
# savefig(savepath+filename+'.eps',dpi=400);
# show();



# ##Plot proportion depending on which item was selected
# fig = figure(figsize = (12.8,7.64)); ax1=gca(); #grid(True);
# title('Average proportion of time fixating each item in a trial \n depending on which item was selected, subject %s'%eyed, fontsize = 22);
# ax1.set_ylim(0.0,0.70); ax1.set_yticks(arange(0.0,0.701,0.1)); ax1.set_xlim([0.4,3.0]); ax1.set_xticks([1,1.7,2.4]);
# ax1.set_ylabel('Average proportion of time spent fixating during a trial',size=18); ax1.set_xlabel('Selected Item',size=18,labelpad=8);
# ax1.set_xticklabels(['Alcohol Selected','Cigarette Selected','Neutral Selected']); #'All PAPC Trials',
# colors=['red','blue','green'];
# #alcohol selected first
# ax1.bar(0.8,db['%s_%s_selected_alc_look_at_alc_mean_perc_time_at_pref'%(eyed,name)], color = colors[0], width = 0.2);
# ax1.errorbar(0.8, db['%s_%s_selected_alc_look_at_alc_mean_perc_time_at_pref'%(eyed,name)],
#              yerr=[[db['%s_%s_selected_alc_look_at_alc_bs_sems_perc_time_at_pref'%(eyed,name)]],[db['%s_%s_selected_alc_look_at_alc_bs_sems_perc_time_at_pref'%(eyed,name)]]],color='black',lw=6.0); #, capsize = 7.0
# ax1.bar(1.0,db['%s_%s_selected_alc_look_at_cig_mean_perc_time_at_pref'%(eyed,name)], color = colors[1], width = 0.2);
# ax1.errorbar(1.0, db['%s_%s_selected_alc_look_at_cig_mean_perc_time_at_pref'%(eyed,name)],
#              yerr=[[db['%s_%s_selected_alc_look_at_cig_bs_sems_perc_time_at_pref'%(eyed,name)]],[db['%s_%s_selected_alc_look_at_cig_bs_sems_perc_time_at_pref'%(eyed,name)]]],color='black',lw=6.0);
# ax1.bar(1.2,db['%s_%s_selected_alc_look_at_neutral_mean_perc_time_at_pref'%(eyed,name)], color = colors[2], width = 0.2);
# ax1.errorbar(1.2, db['%s_%s_selected_alc_look_at_neutral_mean_perc_time_at_pref'%(eyed,name)],
#              yerr=[[db['%s_%s_selected_alc_look_at_neutral_bs_sems_perc_time_at_pref'%(eyed,name)]],[db['%s_%s_selected_alc_look_at_neutral_bs_sems_perc_time_at_pref'%(eyed,name)]]],color='black',lw=6.0);
# 
# #next, when the cigarette was selected
# ax1.bar(1.5,db['%s_%s_selected_cig_look_at_alc_mean_perc_time_at_pref'%(eyed,name)], color = colors[0], width = 0.2);
# ax1.errorbar(1.5, db['%s_%s_selected_cig_look_at_alc_mean_perc_time_at_pref'%(eyed,name)],
#              yerr=[[db['%s_%s_selected_cig_look_at_alc_bs_sems_perc_time_at_pref'%(eyed,name)]],[db['%s_%s_selected_cig_look_at_alc_bs_sems_perc_time_at_pref'%(eyed,name)]]],color='black',lw=6.0);
# ax1.bar(1.7,db['%s_%s_selected_cig_look_at_cig_mean_perc_time_at_pref'%(eyed,name)], color = colors[1], width = 0.2);
# ax1.errorbar(1.7, db['%s_%s_selected_cig_look_at_cig_mean_perc_time_at_pref'%(eyed,name)],
#              yerr=[[db['%s_%s_selected_cig_look_at_cig_bs_sems_perc_time_at_pref'%(eyed,name)]],[db['%s_%s_selected_cig_look_at_cig_bs_sems_perc_time_at_pref'%(eyed,name)]]],color='black',lw=6.0);
# ax1.bar(1.9,db['%s_%s_selected_cig_look_at_neutral_mean_perc_time_at_pref'%(eyed,name)], color = colors[2], width = 0.2);
# ax1.errorbar(1.9, db['%s_%s_selected_cig_look_at_neutral_mean_perc_time_at_pref'%(eyed,name)],
#              yerr=[[db['%s_%s_selected_cig_look_at_neutral_bs_sems_perc_time_at_pref'%(eyed,name)]],[db['%s_%s_selected_cig_look_at_neutral_bs_sems_perc_time_at_pref'%(eyed,name)]]],color='black',lw=6.0);
# 
# #finally when they selected neutral trials
# ax1.bar(2.2,db['%s_%s_selected_neutral_look_at_alc_mean_perc_time_at_pref'%(eyed,name)], color = colors[0], width = 0.2);
# ax1.errorbar(2.2, db['%s_%s_selected_neutral_look_at_alc_mean_perc_time_at_pref'%(eyed,name)],
#              yerr=[[db['%s_%s_selected_neutral_look_at_alc_bs_sems_perc_time_at_pref'%(eyed,name)]],[db['%s_%s_selected_neutral_look_at_alc_bs_sems_perc_time_at_pref'%(eyed,name)]]],color='black',lw=6.0);
# ax1.bar(2.4,db['%s_%s_selected_neutral_look_at_cig_mean_perc_time_at_pref'%(eyed,name)],  color = colors[1], width = 0.2);
# ax1.errorbar(2.4, db['%s_%s_selected_neutral_look_at_cig_mean_perc_time_at_pref'%(eyed,name)],
#              yerr=[[db['%s_%s_selected_neutral_look_at_cig_bs_sems_perc_time_at_pref'%(eyed,name)]],[db['%s_%s_selected_neutral_look_at_cig_bs_sems_perc_time_at_pref'%(eyed,name)]]],color='black',lw=6.0);
# ax1.bar(2.6,db['%s_%s_selected_neutral_look_at_neutral_mean_perc_time_at_pref'%(eyed,name)], color = colors[2], width = 0.2);
# ax1.errorbar(2.6, db['%s_%s_selected_neutral_look_at_neutral_mean_perc_time_at_pref'%(eyed,name)],
#              yerr=[[db['%s_%s_selected_neutral_look_at_neutral_bs_sems_perc_time_at_pref'%(eyed,name)]],[db['%s_%s_selected_neutral_look_at_neutral_bs_sems_perc_time_at_pref'%(eyed,name)]]],color='black',lw=6.0);
# 
# 
# #plot RTs for each type of trial in an inset
# # ia = inset_axes(ax1, width="25%", height="30%", loc=1); #set the inset axes as percentages of the original axis size
# # ia.set_xlim([0.85,2.35]); ia.set_xticks([1,1.6,2.2]); ia.set_ylim([850,1400]); ia.set_yticks(arange(900,1601,100));
# # ia.set_xticklabels(['Alc','Cig','Neutral'], size = 10);
# # ia.set_ylabel('Reaction time (ms)',size=10); ia.set_xlabel('Selected Item',size=10); ia.yaxis.set_label_position('right'); ia.yaxis.set_ticks_position('right');
# # ia.set_yticklabels(['900','1000','1100','1200','1300','1400','1500','1600'], size = 10);
# # ia.bar(1.0,db['agg_high_pref_selected_alc_mean_rt'], color = 'grey', width = 0.3);
# # ia.errorbar(1.0, db['agg_high_pref_selected_alc_mean_rt'],
# #              yerr=[[db['agg_high_pref_selected_alc_bs_sems_rt']],[db['agg_high_pref_selected_alc_bs_sems_rt']]],color='black',lw=2.0,capsize = 3.0);
# # ia.bar(1.6,db['agg_high_pref_selected_cig_mean_rt'], color = 'grey', width = 0.3);
# # ia.errorbar(1.6, db['agg_high_pref_selected_cig_mean_rt'],
# #              yerr=[[db['agg_high_pref_selected_cig_bs_sems_rt']],[db['agg_high_pref_selected_cig_bs_sems_rt']]],color='black',lw=2.0,capsize = 3.0);
# # ia.bar(2.2,db['agg_high_pref_selected_neutral_mean_rt'], color = 'grey', width = 0.3);
# # ia.errorbar(2.2, db['agg_high_pref_selected_neutral_mean_rt'],
# #              yerr=[[db['agg_high_pref_selected_neutral_bs_sems_rt']],[db['agg_high_pref_selected_neutral_bs_sems_rt']]],color='black',lw=2.0,capsize = 3.0);
# # title('Mean RT', fontsize = 14);
# 
# ax1.spines['right'].set_visible(False); ax1.spines['top'].set_visible(False);
# ax1.spines['bottom'].set_linewidth(2.0); ax1.spines['left'].set_linewidth(2.0);
# ax1.yaxis.set_ticks_position('left'); ax1.xaxis.set_ticks_position('bottom');
# legend_lines = [mlines.Line2D([],[],color=colors[0],lw=6,alpha = 1, label='looked at alcohol'),
#                  mlines.Line2D([],[],color=colors[1],lw=6,alpha = 1, label='looked at cigarettes'),
#                  mlines.Line2D([],[],color=colors[2],lw=6,alpha = 1, label='looked at neutral')];
# #ax1.legend(handles=[legend_lines[0],legend_lines[1], legend_lines[2]],loc = 0,ncol=1,fontsize = 14);
# #save the labeled figure as a .png	
# filename = '%s_by_choice_fixate_preferred_item_labeled'%name;
# savefig(savepath+filename+'.png',dpi=400);
# #then get rid of labels and save as a .eps
# labels = [item.get_text() for item in ax1.get_xticklabels()]; labels[0]=''; labels[1]=''; labels[2]='';# labels[3]=''; labels[4]='';#have to do this to center the x ticks on correct spot without incurring ticks at every spot
# ax1.set_xticklabels(labels);
# ax1.set_yticklabels(['','','','','','','','','','','','','','']);
# ax1.set_ylabel(''); ax1.set_xlabel(''); title('');
# filename = '%s_by_choice_fixate_preferred_item'%name;
# savefig(savepath+filename+'.eps',dpi=400);
# show();
# 
# 1/0

# 
# 
# 
# ##Plot proportion for all trials aggregated together
# fig = figure(figsize = (12.8,7.64)); ax1=gca(); #grid(True);
# #title('Average proportion of time fixating each item in a trial \n all trials aggregated together, subject %s'%eyed, fontsize = 22);
# ax1.set_ylim(0.0,0.70); ax1.set_yticks(arange(0.0,0.701,0.1)); ax1.set_xlim([0.5,1.7]); ax1.set_xticks([0.85, 1.15, 1.45]);
# ax1.set_ylabel('Average proportion of time spent fixating during a trial',size=18); ax1.set_xlabel('Item',size=18,labelpad=15);
# ax1.set_xticklabels(['Alcohol','Cigarette','Neutral']); #'All PAPC Trials',
# #alcohol first
# ax1.bar(0.85,db['%s_%s_all_hp_look_at_alc_mean_perc_time_at_pref'%(eyed,name)], color = colors[0], width = 0.25);
# ax1.errorbar(0.85, db['%s_%s_all_hp_look_at_alc_mean_perc_time_at_pref'%(eyed,name)],
#              yerr=[[db['%s_%s_all_hp_look_at_alc_bs_sems_perc_time_at_pref'%(eyed,name)]],[db['%s_%s_all_hp_look_at_alc_bs_sems_perc_time_at_pref'%(eyed,name)]]],color='black',lw=6.0);
# #cigarettes next
# ax1.bar(1.15,db['%s_%s_all_hp_look_at_cig_mean_perc_time_at_pref'%(eyed,name)], color = colors[1], width = 0.25);
# ax1.errorbar(1.15, db['%s_%s_all_hp_look_at_cig_mean_perc_time_at_pref'%(eyed,name)],
#              yerr=[[db['%s_%s_all_hp_look_at_cig_bs_sems_perc_time_at_pref'%(eyed,name)]],[db['%s_%s_all_hp_look_at_cig_bs_sems_perc_time_at_pref'%(eyed,name)]]],color='black',lw=6.0);
# #finally neutral
# ax1.bar(1.45,db['%s_%s_all_hp_look_at_neutral_mean_perc_time_at_pref'%(eyed,name)], color = colors[2], width = 0.25);
# ax1.errorbar(1.45, db['%s_%s_all_hp_look_at_neutral_mean_perc_time_at_pref'%(eyed,name)],
#              yerr=[[db['%s_%s_all_hp_look_at_neutral_bs_sems_perc_time_at_pref'%(eyed,name)]],[db['%s_%s_all_hp_look_at_neutral_bs_sems_perc_time_at_pref'%(eyed,name)]]],color='black',lw=6.0);
# ax1.spines['right'].set_visible(False); ax1.spines['top'].set_visible(False);
# ax1.spines['bottom'].set_linewidth(2.0); ax1.spines['left'].set_linewidth(2.0);
# ax1.yaxis.set_ticks_position('left'); ax1.xaxis.set_ticks_position('bottom');
# #save the labeled figure as a .png	
# filename = '%s_fixate_preferred_item_labeled'%name;
# savefig(savepath+filename+'.png',dpi=400);
# #then get rid of labels and save as a .eps
# labels = [item.get_text() for item in ax1.get_xticklabels()]; labels[0]=''; labels[1]=''; labels[2]=''; #labels[3]=''; labels[4]='';#have to do this to center the x ticks on correct spot without incurring ticks at every spot
# ax1.set_xticklabels(labels);
# ax1.set_yticklabels(['','','','','','','','','','','','','','']);
# ax1.set_ylabel(''); ax1.set_xlabel(''); title('');
# filename = '%s_fixate_preferred_item'%name;
# savefig(savepath+filename+'.eps',dpi=400);
# show();
# 
# 
# #then mean RT for each condition
# fig = figure(figsize = (12.8,7.64)); ax1=gca(); #grid(True);
# #title('Average proportion of time fixating each item in a trial \n all trials aggregated together, subject %s'%eyed, fontsize = 22);
# ax1.set_ylim(850, 1700); ax1.set_yticks(arange(900, 1601, 100)); ax1.set_xlim([0.5,1.7]); ax1.set_xticks([0.85, 1.15, 1.45]);
# ax1.set_ylabel('Mean RT',size=18); ax1.set_xlabel('Selected Item',size=18,labelpad=15);
# ax1.set_xticklabels(['Alcohol','Cigarette','Neutral']);
# ax1.bar(0.85,db['%s_%s_selected_alc_mean_rt'%(eyed,name)], color = colors[0], width = 0.25);
# ax1.errorbar(0.85, db['%s_%s_selected_alc_mean_rt'%(eyed,name)],
#              yerr=[[db['%s_%s_selected_alc_bs_sems_rt'%(eyed,name)]],[db['%s_%s_selected_alc_bs_sems_rt'%(eyed,name)]]],color='black',lw=6.0,capsize = 0);
# ax1.bar(1.15,db['%s_%s_selected_cig_mean_rt'%(eyed,name)], color = colors[1], width = 0.25);
# ax1.errorbar(1.15, db['%s_%s_selected_cig_mean_rt'%(eyed,name)],
#              yerr=[[db['%s_%s_selected_cig_bs_sems_rt'%(eyed,name)]],[db['%s_%s_selected_cig_bs_sems_rt'%(eyed,name)]]],color='black',lw=6.0,capsize = 0);
# ax1.bar(1.45,db['%s_%s_selected_neutral_mean_rt'%(eyed,name)], color = colors[2], width = 0.25);
# ax1.errorbar(1.45, db['%s_%s_selected_neutral_mean_rt'%(eyed,name)],
#              yerr=[[db['%s_%s_selected_neutral_bs_sems_rt'%(eyed,name)]],[db['%s_%s_selected_neutral_bs_sems_rt'%(eyed,name)]]],color='black',lw=6.0,capsize = 0);
# ax1.spines['right'].set_visible(False); ax1.spines['top'].set_visible(False);
# ax1.spines['bottom'].set_linewidth(2.0); ax1.spines['left'].set_linewidth(2.0);
# ax1.yaxis.set_ticks_position('left'); ax1.xaxis.set_ticks_position('bottom');
# #save the labeled figure as a .png	
# filename = '%s_rt_by_chosen_item_labeled'%name;
# savefig(savepath+filename+'.png',dpi=400);
# #then get rid of labels and save as a .eps
# labels = [item.get_text() for item in ax1.get_xticklabels()]; labels[0]=''; labels[1]=''; labels[2]=''; #labels[3]=''; labels[4]='';#have to do this to center the x ticks on correct spot without incurring ticks at every spot
# ax1.set_xticklabels(labels);
# ax1.set_yticklabels(['','','','','','','','','','','','','','']);
# ax1.set_ylabel(''); ax1.set_xlabel(''); title('');
# filename = '%s_rt_by_chosen_item'%name;
# savefig(savepath+filename+'.eps',dpi=400);
# show();



# ############################################
# ## Plotting proportion of trials the first fixated items was the preferred item   ##
# ############################################

# ##Plot proportion for PAPC trials based on whetehr they chose the cue or not item for items when they chose alohol or cigarette
# fig = figure(figsize = (12.8,7.64)); ax1=gca(); #grid(True);
# ax1.set_ylim(0.,0.5); ax1.set_yticks(arange(0,0.501,0.05)); ax1.set_xlim([0.7,2.5]); ax1.set_xticks([1,1.6,2.2]); #,2.8]); ax1.set_xlim([0.7,3.1]);
# ax1.set_ylabel('Proportion of trials last fixated item',size=18); ax1.set_xlabel('Substance',size=18,labelpad=15);
# ax1.set_xticklabels(['Alcohol','Cigarette','Neutral']); #'All PAPC Trials',
# 
# ax1.bar(1.0,db['%s_%s_alc_mean_prop_first_fixated_item'%(eyed,name)],color='gray',width=0.4);
# ax1.errorbar(1.0,db['%s_%s_alc_mean_prop_first_fixated_item'%(eyed,name)],
# 			 yerr=[[db['%s_%s_alc_bs_sems_prop_first_fixated_item'%(eyed,name)]],[db['%s_%s_alc_bs_sems_prop_first_fixated_item'%(eyed,name)]]],color='black',lw=6.0);
# ax1.bar(1.6,db['%s_%s_cig_mean_prop_first_fixated_item'%(eyed,name)],color='gray',width=0.4);
# ax1.errorbar(1.6,db['%s_%s_cig_mean_prop_first_fixated_item'%(eyed,name)],
# 			 yerr=[[db['%s_%s_cig_bs_sems_prop_first_fixated_item'%(eyed,name)]],[db['%s_%s_cig_bs_sems_prop_first_fixated_item'%(eyed,name)]]],color='black',lw=6.0);
# ax1.bar(2.2,db['%s_%s_neu_mean_prop_last_fixated_item'%(eyed,name)],color='gray',width=0.4);
# ax1.errorbar(2.2,db['%s_%s_neu_mean_prop_first_fixated_item'%(eyed,name)],
# 			 yerr=[[db['%s_%s_neu_bs_sems_prop_first_fixated_item'%(eyed,name)]],[db['%s_%s_neu_bs_sems_prop_first_fixated_item'%(eyed,name)]]],color='black',lw=6.0);
# 
# ax1.spines['right'].set_visible(False); ax1.spines['top'].set_visible(False);
# ax1.spines['bottom'].set_linewidth(2.0); ax1.spines['left'].set_linewidth(2.0);
# ax1.yaxis.set_ticks_position('left'); ax1.xaxis.set_ticks_position('bottom');
# title('Average proportion of trials the selected item \n was the last item fixated', fontsize = 22);
# #save the labeled figure as a .png	
# filename = '%s_prop_last_fixated_labeled'%name;
# savefig(savepath+filename+'.png',dpi=400);
# # #then get rid of labels and save as a .eps
# # labels = [item.get_text() for item in ax1.get_xticklabels()]; labels[0]=''; labels[1]=''; labels[2]=''; labels[3]=''; labels[4]='';#have to do this to center the x ticks on correct spot without incurring ticks at every spot
# # ax1.set_xticklabels(labels);
# # ax1.set_yticklabels(['','','','','','','','','','','','','','']);
# # ax1.set_ylabel(''); ax1.set_xlabel(''); title('');
# # filename = 'cue_vs_not_cue_percentage_trials_last_fixated_item';
# # savefig(savepath+filename+'.eps',dpi=400);
# show();


#now the break down by each type of substanc chosen
fig = figure(figsize = (12.8,7.64)); ax1=gca(); #grid(True);
ax1.set_ylim(0.,0.6); ax1.set_yticks(arange(0,0.601,0.05)); ax1.set_xlim([0.4,3.0]); ax1.set_xticks([1,1.7,2.4]); 
ax1.set_ylabel('Proportion of trials first fixated item',size=18); ax1.set_xlabel('Substance',size=18,labelpad=15);
ax1.set_xticklabels(['Alcohol Selected','Cigarette Selected','Neutral Selected']);
colors=['red','blue','green'];

#alcohol selected first
ax1.bar(0.8,db['%s_%s_chose_alc_alc_mean_prop_first_fixated_item'%(eyed,name)], color = colors[0], width = 0.2);
ax1.errorbar(0.8, db['%s_%s_chose_alc_alc_mean_prop_first_fixated_item'%(eyed,name)],
             yerr=[[db['%s_%s_chose_alc_alc_bs_sems_prop_first_fixated_item'%(eyed,name)]],[db['%s_%s_chose_alc_alc_bs_sems_prop_first_fixated_item'%(eyed,name)]]],color='black',lw=6.0); #, capsize = 7.0
ax1.bar(1.0,db['%s_%s_chose_alc_cig_mean_prop_first_fixated_item'%(eyed,name)], color = colors[1], width = 0.2);
ax1.errorbar(1.0, db['%s_%s_chose_alc_cig_mean_prop_first_fixated_item'%(eyed,name)],
             yerr=[[db['%s_%s_chose_alc_cig_bs_sems_prop_first_fixated_item'%(eyed,name)]],[db['%s_%s_chose_alc_cig_bs_sems_prop_first_fixated_item'%(eyed,name)]]],color='black',lw=6.0); 
ax1.bar(1.2,db['%s_%s_chose_alc_neu_mean_prop_first_fixated_item'%(eyed,name)], color = colors[2], width = 0.2);
ax1.errorbar(1.2, db['%s_%s_chose_alc_neu_mean_prop_first_fixated_item'%(eyed,name)],
             yerr=[[db['%s_%s_chose_alc_neu_bs_sems_prop_first_fixated_item'%(eyed,name)]],[db['%s_%s_chose_alc_neu_bs_sems_prop_first_fixated_item'%(eyed,name)]]],color='black',lw=6.0); 

#cigarettes next
ax1.bar(1.5,db['%s_%s_chose_cig_alc_mean_prop_first_fixated_item'%(eyed,name)], color = colors[0], width = 0.2);
ax1.errorbar(1.5, db['%s_%s_chose_cig_alc_mean_prop_first_fixated_item'%(eyed,name)],
             yerr=[[db['%s_%s_chose_cig_alc_bs_sems_prop_first_fixated_item'%(eyed,name)]],[db['%s_%s_chose_cig_alc_bs_sems_prop_first_fixated_item'%(eyed,name)]]],color='black',lw=6.0); #, capsize = 7.0
ax1.bar(1.7,db['%s_%s_chose_cig_cig_mean_prop_first_fixated_item'%(eyed,name)], color = colors[1], width = 0.2);
ax1.errorbar(1.7, db['%s_%s_chose_cig_cig_mean_prop_first_fixated_item'%(eyed,name)],
             yerr=[[db['%s_%s_chose_cig_cig_bs_sems_prop_first_fixated_item'%(eyed,name)]],[db['%s_%s_chose_cig_cig_bs_sems_prop_first_fixated_item'%(eyed,name)]]],color='black',lw=6.0); 
ax1.bar(1.9,db['%s_%s_chose_cig_neu_mean_prop_first_fixated_item'%(eyed,name)], color = colors[2], width = 0.2);
ax1.errorbar(1.9, db['%s_%s_chose_cig_neu_mean_prop_first_fixated_item'%(eyed,name)],
             yerr=[[db['%s_%s_chose_cig_neu_bs_sems_prop_first_fixated_item'%(eyed,name)]],[db['%s_%s_chose_cig_neu_bs_sems_prop_first_fixated_item'%(eyed,name)]]],color='black',lw=6.0); 

#neutral finally
ax1.bar(2.2,db['%s_%s_chose_neu_alc_mean_prop_first_fixated_item'%(eyed,name)], color = colors[0], width = 0.2);
ax1.errorbar(2.2, db['%s_%s_chose_neu_alc_mean_prop_first_fixated_item'%(eyed,name)],
             yerr=[[db['%s_%s_chose_neu_alc_bs_sems_prop_first_fixated_item'%(eyed,name)]],[db['%s_%s_chose_neu_alc_bs_sems_prop_first_fixated_item'%(eyed,name)]]],color='black',lw=6.0); #, capsize = 7.0
ax1.bar(2.4,db['%s_%s_chose_neu_cig_mean_prop_first_fixated_item'%(eyed,name)], color = colors[1], width = 0.2);
ax1.errorbar(2.4, db['%s_%s_chose_neu_cig_mean_prop_first_fixated_item'%(eyed,name)],
             yerr=[[db['%s_%s_chose_neu_cig_bs_sems_prop_first_fixated_item'%(eyed,name)]],[db['%s_%s_chose_neu_cig_bs_sems_prop_first_fixated_item'%(eyed,name)]]],color='black',lw=6.0); 
ax1.bar(2.6,db['%s_%s_chose_neu_neu_mean_prop_first_fixated_item'%(eyed,name)], color = colors[2], width = 0.2);
ax1.errorbar(2.6, db['%s_%s_chose_neu_neu_mean_prop_first_fixated_item'%(eyed,name)],
             yerr=[[db['%s_%s_chose_neu_neu_bs_sems_prop_first_fixated_item'%(eyed,name)]],[db['%s_%s_chose_neu_neu_bs_sems_prop_first_fixated_item'%(eyed,name)]]],color='black',lw=6.0); 

ax1.spines['right'].set_visible(False); ax1.spines['top'].set_visible(False);
ax1.spines['bottom'].set_linewidth(2.0); ax1.spines['left'].set_linewidth(2.0);
ax1.yaxis.set_ticks_position('left'); ax1.xaxis.set_ticks_position('bottom');
legend_lines = [mlines.Line2D([],[],color=colors[0],lw=6,alpha = 1, label='looked at alcohol'),
                 mlines.Line2D([],[],color=colors[1],lw=6,alpha = 1, label='looked at cigarettes'),
                 mlines.Line2D([],[],color=colors[2],lw=6,alpha = 1, label='looked at neutral')];
ax1.legend(handles=[legend_lines[0],legend_lines[1], legend_lines[2]],loc='upper center', bbox_to_anchor=(0.5, 1.1),ncol=3,fontsize = 14);
#save the labeled figure as a .png	
filename = '%s_by_choice_prop_first_fixated_labeled'%name;
savefig(savepath+filename+'.png',dpi=400);
#then get rid of labels and save as a .eps
labels = [item.get_text() for item in ax1.get_xticklabels()]; labels[0]=''; labels[1]=''; labels[2]='';#have to do this to center the x ticks on correct spot without incurring ticks at every spot
ax1.set_xticklabels(labels);
ax1.set_yticklabels(['','','','','','','','','','','','','','']);
ax1.legend();
ax1.set_ylabel(''); ax1.set_xlabel(''); title('');
filename = '%s_by_choice_prop_first_fixated';
savefig(savepath+filename+'.eps',dpi=400);
show();




# ############################################
# ## Plotting proportion of trials the last fixted items was the preferred item figure  ##
# ############################################
# 
# ##Plot proportion for PAPC trials based on whetehr they chose the cue or not item for items when they chose alohol or cigarette
# fig = figure(figsize = (12.8,7.64)); ax1=gca(); #grid(True);
# ax1.set_ylim(0.,0.5); ax1.set_yticks(arange(0,0.501,0.05)); ax1.set_xlim([0.7,2.5]); ax1.set_xticks([1,1.6,2.2]); #,2.8]); ax1.set_xlim([0.7,3.1]);
# ax1.set_ylabel('Proportion of trials last fixated item',size=18); ax1.set_xlabel('Substance',size=18,labelpad=15);
# ax1.set_xticklabels(['Alcohol','Cigarette','Neutral']); #'All PAPC Trials',
# 
# ax1.bar(1.0,db['%s_%s_alc_mean_prop_last_fixated_item'%(eyed,name)],color='gray',width=0.4);
# ax1.errorbar(1.0,db['%s_%s_alc_mean_prop_last_fixated_item'%(eyed,name)],
# 			 yerr=[[db['%s_%s_alc_bs_sems_prop_last_fixated_item'%(eyed,name)]],[db['%s_%s_alc_bs_sems_prop_last_fixated_item'%(eyed,name)]]],color='black',lw=6.0);
# ax1.bar(1.6,db['%s_%s_cig_mean_prop_last_fixated_item'%(eyed,name)],color='gray',width=0.4);
# ax1.errorbar(1.6,db['%s_%s_cig_mean_prop_last_fixated_item'%(eyed,name)],
# 			 yerr=[[db['%s_%s_cig_bs_sems_prop_last_fixated_item'%(eyed,name)]],[db['%s_%s_cig_bs_sems_prop_last_fixated_item'%(eyed,name)]]],color='black',lw=6.0);
# ax1.bar(2.2,db['%s_%s_neu_mean_prop_last_fixated_item'%(eyed,name)],color='gray',width=0.4);
# ax1.errorbar(2.2,db['%s_%s_neu_mean_prop_last_fixated_item'%(eyed,name)],
# 			 yerr=[[db['%s_%s_neu_bs_sems_prop_last_fixated_item'%(eyed,name)]],[db['%s_%s_neu_bs_sems_prop_last_fixated_item'%(eyed,name)]]],color='black',lw=6.0);
# 
# ax1.spines['right'].set_visible(False); ax1.spines['top'].set_visible(False);
# ax1.spines['bottom'].set_linewidth(2.0); ax1.spines['left'].set_linewidth(2.0);
# ax1.yaxis.set_ticks_position('left'); ax1.xaxis.set_ticks_position('bottom');
# title('Average proportion of trials the selected item \n was the last item fixated', fontsize = 22);
# #save the labeled figure as a .png	
# filename = '%s_prop_last_fixated_labeled'%name;
# savefig(savepath+filename+'.png',dpi=400);
# # #then get rid of labels and save as a .eps
# # labels = [item.get_text() for item in ax1.get_xticklabels()]; labels[0]=''; labels[1]=''; labels[2]=''; labels[3]=''; labels[4]='';#have to do this to center the x ticks on correct spot without incurring ticks at every spot
# # ax1.set_xticklabels(labels);
# # ax1.set_yticklabels(['','','','','','','','','','','','','','']);
# # ax1.set_ylabel(''); ax1.set_xlabel(''); title('');
# # filename = 'cue_vs_not_cue_percentage_trials_last_fixated_item';
# # savefig(savepath+filename+'.eps',dpi=400);
# show();
# 
# 
# 
# #now the break down by each type of substanc chosen
# fig = figure(figsize = (12.8,7.64)); ax1=gca(); #grid(True);
# ax1.set_ylim(0.,0.5); ax1.set_yticks(arange(0,0.501,0.05)); ax1.set_xlim([0.4,3.0]); ax1.set_xticks([1,1.7,2.4]); 
# ax1.set_ylabel('Proportion of trials last fixated item',size=18); ax1.set_xlabel('Substance',size=18,labelpad=15);
# ax1.set_xticklabels(['Alcohol Selected','Cigarette Selected','Neutral Selected']);
# colors=['red','blue','green'];
# 
# #alcohol selected first
# ax1.bar(0.8,db['%s_%s_chose_alc_alc_mean_prop_last_fixated_item'%(eyed,name)], color = colors[0], width = 0.2);
# ax1.errorbar(0.8, db['%s_%s_chose_alc_alc_mean_prop_last_fixated_item'%(eyed,name)],
#              yerr=[[db['%s_%s_chose_alc_alc_bs_sems_prop_last_fixated_item'%(eyed,name)]],[db['%s_%s_chose_alc_alc_bs_sems_prop_last_fixated_item'%(eyed,name)]]],color='black',lw=6.0); #, capsize = 7.0
# ax1.bar(1.0,db['%s_%s_chose_alc_cig_mean_prop_last_fixated_item'%(eyed,name)], color = colors[1], width = 0.2);
# ax1.errorbar(1.0, db['%s_%s_chose_alc_cig_mean_prop_last_fixated_item'%(eyed,name)],
#              yerr=[[db['%s_%s_chose_alc_cig_bs_sems_prop_last_fixated_item'%(eyed,name)]],[db['%s_%s_chose_alc_cig_bs_sems_prop_last_fixated_item'%(eyed,name)]]],color='black',lw=6.0); 
# ax1.bar(1.2,db['%s_%s_chose_alc_neu_mean_prop_last_fixated_item'%(eyed,name)], color = colors[2], width = 0.2);
# ax1.errorbar(1.2, db['%s_%s_chose_alc_neu_mean_prop_last_fixated_item'%(eyed,name)],
#              yerr=[[db['%s_%s_chose_alc_neu_bs_sems_prop_last_fixated_item'%(eyed,name)]],[db['%s_%s_chose_alc_neu_bs_sems_prop_last_fixated_item'%(eyed,name)]]],color='black',lw=6.0); 
# 
# #cigarettes next
# ax1.bar(1.5,db['%s_%s_chose_cig_alc_mean_prop_last_fixated_item'%(eyed,name)], color = colors[0], width = 0.2);
# ax1.errorbar(1.5, db['%s_%s_chose_cig_alc_mean_prop_last_fixated_item'%(eyed,name)],
#              yerr=[[db['%s_%s_chose_cig_alc_bs_sems_prop_last_fixated_item'%(eyed,name)]],[db['%s_%s_chose_cig_alc_bs_sems_prop_last_fixated_item'%(eyed,name)]]],color='black',lw=6.0); #, capsize = 7.0
# ax1.bar(1.7,db['%s_%s_chose_cig_cig_mean_prop_last_fixated_item'%(eyed,name)], color = colors[1], width = 0.2);
# ax1.errorbar(1.7, db['%s_%s_chose_cig_cig_mean_prop_last_fixated_item'%(eyed,name)],
#              yerr=[[db['%s_%s_chose_cig_cig_bs_sems_prop_last_fixated_item'%(eyed,name)]],[db['%s_%s_chose_cig_cig_bs_sems_prop_last_fixated_item'%(eyed,name)]]],color='black',lw=6.0); 
# ax1.bar(1.9,db['%s_%s_chose_cig_neu_mean_prop_last_fixated_item'%(eyed,name)], color = colors[2], width = 0.2);
# ax1.errorbar(1.9, db['%s_%s_chose_cig_neu_mean_prop_last_fixated_item'%(eyed,name)],
#              yerr=[[db['%s_%s_chose_cig_neu_bs_sems_prop_last_fixated_item'%(eyed,name)]],[db['%s_%s_chose_cig_neu_bs_sems_prop_last_fixated_item'%(eyed,name)]]],color='black',lw=6.0); 
# 
# #neutral finally
# ax1.bar(2.2,db['%s_%s_chose_neu_alc_mean_prop_last_fixated_item'%(eyed,name)], color = colors[0], width = 0.2);
# ax1.errorbar(2.2, db['%s_%s_chose_neu_alc_mean_prop_last_fixated_item'%(eyed,name)],
#              yerr=[[db['%s_%s_chose_neu_alc_bs_sems_prop_last_fixated_item'%(eyed,name)]],[db['%s_%s_chose_neu_alc_bs_sems_prop_last_fixated_item'%(eyed,name)]]],color='black',lw=6.0); #, capsize = 7.0
# ax1.bar(2.4,db['%s_%s_chose_neu_cig_mean_prop_last_fixated_item'%(eyed,name)], color = colors[1], width = 0.2);
# ax1.errorbar(2.4, db['%s_%s_chose_neu_cig_mean_prop_last_fixated_item'%(eyed,name)],
#              yerr=[[db['%s_%s_chose_neu_cig_bs_sems_prop_last_fixated_item'%(eyed,name)]],[db['%s_%s_chose_neu_cig_bs_sems_prop_last_fixated_item'%(eyed,name)]]],color='black',lw=6.0); 
# ax1.bar(2.6,db['%s_%s_chose_neu_neu_mean_prop_last_fixated_item'%(eyed,name)], color = colors[2], width = 0.2);
# ax1.errorbar(2.6, db['%s_%s_chose_neu_neu_mean_prop_last_fixated_item'%(eyed,name)],
#              yerr=[[db['%s_%s_chose_neu_neu_bs_sems_prop_last_fixated_item'%(eyed,name)]],[db['%s_%s_chose_neu_neu_bs_sems_prop_last_fixated_item'%(eyed,name)]]],color='black',lw=6.0); 
# 
# 
# ax1.spines['right'].set_visible(False); ax1.spines['top'].set_visible(False);
# ax1.spines['bottom'].set_linewidth(2.0); ax1.spines['left'].set_linewidth(2.0);
# ax1.yaxis.set_ticks_position('left'); ax1.xaxis.set_ticks_position('bottom');
# legend_lines = [mlines.Line2D([],[],color=colors[0],lw=6,alpha = 1, label='looked at alcohol'),
#                  mlines.Line2D([],[],color=colors[1],lw=6,alpha = 1, label='looked at cigarettes'),
#                  mlines.Line2D([],[],color=colors[2],lw=6,alpha = 1, label='looked at neutral')];
# ax1.legend(handles=[legend_lines[0],legend_lines[1], legend_lines[2]],loc = 0,ncol=1,fontsize = 14);
# #save the labeled figure as a .png	
# filename = '%s_by_choice_prop_last_fixated_labeled'%name;
# #savefig(savepath+filename+'.png',dpi=400);
# # #then get rid of labels and save as a .eps
# # labels = [item.get_text() for item in ax1.get_xticklabels()]; labels[0]=''; labels[1]=''; labels[2]=''; labels[3]=''; labels[4]='';#have to do this to center the x ticks on correct spot without incurring ticks at every spot
# # ax1.set_xticklabels(labels);
# # ax1.set_yticklabels(['','','','','','','','','','','','','','']);
# # ax1.set_ylabel(''); ax1.set_xlabel(''); title('');
# # filename = 'cue_vs_not_cue_percentage_time_fixate_preferred_item';
# # savefig(savepath+filename+'.eps',dpi=400);
# show();
# 
# 
# ### Inset axes object, originally designed for RT
# # #plot RTs for each type of trial in an inset
# # ia = inset_axes(ax1, width="25%", height="30%", loc=1); #set the inset axes as percentages of the original axis size
# # ia.tick_params(width = 1.0);
# # ia.set_xlim([0.85,2.35]); ia.set_xticks([1,1.6,2.2]); ia.set_ylim([850,1400]); ia.set_yticks(arange(900,1601,100));
# # ia.set_xticklabels(['Alc','Cig','Neutral'], size = 10);
# # ia.set_xticklabels(['','',''], size = 10);
# # #ia.set_ylabel('Reaction time (ms)',size=10); ia.set_xlabel('Selected Item',size=10);
# # ia.yaxis.set_label_position('right'); ia.yaxis.set_ticks_position('right');
# # ia.set_yticklabels(['900','1000','1100','1200','1300','1400','1500','1600'], size = 10);
# # ia.set_yticklabels(['','','','','','','',''], size = 10);
# # ia.bar(1.0,db['agg_high_pref_selected_alc_mean_rt'], color = 'grey', width = 0.3);
# # ia.errorbar(1.0, db['agg_high_pref_selected_alc_mean_rt'],
# #              yerr=[[db['agg_high_pref_selected_alc_bs_sems_rt']],[db['agg_high_pref_selected_alc_bs_sems_rt']]],color='black',lw=2.0,capsize = 0);
# # ia.bar(1.6,db['agg_high_pref_selected_cig_mean_rt'], color = 'grey', width = 0.3);
# # ia.errorbar(1.6, db['agg_high_pref_selected_cig_mean_rt'],
# #              yerr=[[db['agg_high_pref_selected_cig_bs_sems_rt']],[db['agg_high_pref_selected_cig_bs_sems_rt']]],color='black',lw=2.0,capsize = 0);
# # ia.bar(2.2,db['agg_high_pref_selected_neutral_mean_rt'], color = 'grey', width = 0.3);
# # ia.errorbar(2.2, db['agg_high_pref_selected_neutral_mean_rt'],
# #              yerr=[[db['agg_high_pref_selected_neutral_bs_sems_rt']],[db['agg_high_pref_selected_neutral_bs_sems_rt']]],color='black',lw=2.0,capsize = 0);
# # # title('Mean RT', fontsize = 14);
# 
# 
