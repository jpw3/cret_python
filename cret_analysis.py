#Data anlaysis code for CRET study collaboration with CAAS
#Author: James Wilmott, Fall/Winter 2017-18

from pylab import *
import shelve #for database writing and reading
from scipy.io import loadmat #used to load .mat files in as dictionaries
from scipy import stats
from glob import glob #for use in searching for/ finding data files
import random #general purpose
import pandas as pd
import math
import matplotlib.lines as mlines
import scipy.signal as ssignal
from mpl_toolkits.axes_grid.inset_locator import inset_axes

############################################
## Specify some universal parameters ##
############################################

datapath = '/Users/jameswilmott/Documents/MATLAB/data/CRET/'; #'/Users/james/Documents/MATLAB/data/CRET/'; #
savepath =  '/Users/jameswilmott/Documents/Python/CRET/data/';  #'/Users/james/Documents/Python/CRET/data/'; # 
shelvepath =  '/Users/jameswilmott/Documents/Python/CRET/data/';  #'/Users/james/Documents/Python/CRET/data/'; # 

subject_data = shelve.open(shelvepath+'data');

ids=['cret03','cret04','cret05','cret06','cret07','cret08','cret09','cret10','cret11']; #'cret01',

display_size = array([22.80, 17.10]); #width, height of the screen used to present the images in degrees of visual angle

image_size = array([6,6]); #width, and height of the presented images in degress of visual angle

left_pic_coors = array([-5.20,-3.0]); #in dva
right_pic_coors = array([5.20,-3]);
up_pic_coors = array([0,6]);

distance_threshold = 4; #threshold for how far away eye position can be from the coordinates to be considered looking at that item

#define the possible filenames for each class of pictures
alcohol_filenames = ['bacardi','brandy','budweiser','captainmorgan','corona','greygoose','heineken','jackdaniels','jimbeam','josecuervo','kahlua','naturallight','newamsterdam','skyy','smirnoff','sutter'];
cigarette_filenames = ['americanspirit','camelcrush','luckystrike','newport','marlboro','maverick'];
neutral_filenames = ['selzter','waterbottle','waterglass']; #note the incorrect spelling in the filename.. this is consistent with what the file name actully is

time_bin_spacing = 0.001;
time_duration = 1.0;

#set parameters for plots
matplotlib.rcParams['ytick.labelsize']=20; matplotlib.rcParams['xtick.labelsize']=20;
matplotlib.rcParams['xtick.major.width']=2.0; matplotlib.rcParams['ytick.major.width']=2.0;
matplotlib.rcParams['xtick.major.size']=10.0; matplotlib.rcParams['ytick.major.size']=10.0;
matplotlib.rcParams['hatch.linewidth'] = 9.0; #set the hatch width to larger than the default case
matplotlib.rcParams['hatch.color'] = 'black';
matplotlib.pyplot.rc('font',weight='bold');

############################################
## Data Analysis Methods ##
############################################

#define a method that computes, for each subject, the average percentage of time spent looking at each of the items, including the preferred item
#do this for all trials, and then for trials where their two stated preferred items (e.g., trial type 1)
#assign each subject's data to a .csv and save it, and then campute the averages and plot for my use.

def computePercentageLookingTimes(blocks, eyed = 'agg'):
	db = subject_data;
	#loop through and get all the trials for each subject
	trial_matrix = [[tee for b in bl for tee in b.trials] for bl in blocks];
	
	#find each subjects' cue substance based on which item them chose more often during PAPC trials where they selected the alcohol or cigarette
	all_substances = [[tee.preferred_category for tee in subject if (((tee.preferred_category=='alcohol')|(tee.preferred_category=='cigarette'))&
		(tee.dropped_sample == 0)&(tee.didntLookAtAnyItems == 0)&(tee.trial_type == 1))] for subject in trial_matrix]; #first get all the selected categories
	prop_chose_alc = [sum([val == 'alcohol' for val in subject])/float(len([val == 'alcohol' for val in subject])) for subject in all_substances]; #now get proportion of time seleteced alcohol
	prop_chose_cig = [sum([val == 'cigarette' for val in subject])/float(len([val == 'alcohol' for val in subject])) for subject in all_substances]; #then proportion of times selecting cigarette
	#then find which proportion is greater and define whether that subject's cue is alcohol or cigarette
	subject_cues = ['alcohol' if (a>c) else 'cigarette' for a,c in zip(prop_chose_alc,prop_chose_cig)];
	#
	##Build an average database instance of each value for each subject for high vs low preferred trials and the subsets of high preferred trials
	
	data = pd.DataFrame(columns = ['sub_id','subject_cue','selected','neu_mean_time_looking_at_pref','neu_mean_percentage_looking_at_pref',
								   'cue_mean_time_looking_at_pref','cue_mean_percentage_looking_at_pref','not_cue_mean_time_looking_at_pref','not_cue_mean_percentage_looking_at_pref', 'mean_response_time']);
		
	for high_pref_trial,name in zip([0,1],['non_high_pref','high_pref']):
		#for now, only run this analysis for the high preference (preferred alcohol, preferred cigarette) trials
		if high_pref_trial==0:
			continue;
		#below here, run the proportion of looking time analysis for cue, not cue, and neutral for each subset of trials where they chose each type
		counter = 0; #counter for indexing appended data into the Pandas DataFrame
		for cue_or_not, selected_item in zip([1,0,0],['cue','not_cue','neutral']):
			neu_subject_times = []; #these are holders for the mean times and proportions for each subject, given the subset of trials 
			neu_subject_percs = [];
			cue_subject_times = [];
			cue_subject_percs = [];
			not_cue_subject_times = [];
			not_cue_subject_percs = [];
			all_rts = [];
			#loop through the cues and trials for each subject
			for subj,cue,sub_id in zip(trial_matrix, subject_cues, ids):
				neu_time_at_pref = [];
				neu_perc_at_pref = [];
				cue_time_at_pref = [];
				cue_perc_at_pref = [];
				not_cue_time_at_pref = [];
				not_cue_perc_at_pref = [];
				rts = [];
				for t in subj:
					#conditional to differentiate between not-cue trials when selecteing the non-cue or not
					if ((selected_item=='cue')|(selected_item=='not_cue')):
						if((tee.dropped_sample == 0)&(tee.didntLookAtAnyItems == 0)&((tee.trial_type == 1)==high_pref_trial)&((t.preferred_category == cue)==cue_or_not)&((t.preferred_category == 'alcohol')|(t.preferred_category == 'cigarette'))):
							neu_time_at_pref.append(t.timeLookingAtNeutral);
							neu_perc_at_pref.append(t.percentageTimeLookingAtNeutral);
							rts.append(t.response_time)
						if (cue=='alcohol'):
							cue_time_at_pref.append(t.timeLookingAtAlcohol);
							cue_perc_at_pref.append(t.percentageTimeLookingAtAlcohol);
							not_cue_time_at_pref.append(t.timeLookingAtCigarette);
							not_cue_perc_at_pref.append(t.percentageTimeLookingAtCigarette);							
							rts.append(t.response_time)							
						elif (cue=='cigarette'):
							cue_time_at_pref.append(t.timeLookingAtCigarette);
							cue_perc_at_pref.append(t.percentageTimeLookingAtCigarette);
							not_cue_time_at_pref.append(t.timeLookingAtAlcohol);
							not_cue_perc_at_pref.append(t.percentageTimeLookingAtAlcohol);							
							rts.append(t.response_time)																				
					#this second conditional include neutral trials that were preferred only
					elif (selected_item=='neutral'):
						if((tee.dropped_sample == 0)&(tee.didntLookAtAnyItems == 0)&((tee.trial_type == 1)==high_pref_trial)&((t.preferred_category == cue)==cue_or_not)&(t.preferred_category == 'neutral')):
							neu_time_at_pref.append(t.timeLookingAtNeutral);
							neu_perc_at_pref.append(t.percentageTimeLookingAtNeutral);
							rts.append(t.response_time)
						if (cue=='alcohol'):
							cue_time_at_pref.append(t.timeLookingAtAlcohol);
							cue_perc_at_pref.append(t.percentageTimeLookingAtAlcohol);
							not_cue_time_at_pref.append(t.timeLookingAtCigarette);
							not_cue_perc_at_pref.append(t.percentageTimeLookingAtCigarette);							
							rts.append(t.response_time)							
						elif (cue=='cigarette'):
							cue_time_at_pref.append(t.timeLookingAtCigarette);
							cue_perc_at_pref.append(t.percentageTimeLookingAtCigarette);
							not_cue_time_at_pref.append(t.timeLookingAtAlcohol);
							not_cue_perc_at_pref.append(t.percentageTimeLookingAtAlcohol);							
							rts.append(t.response_time)									
					#append this subjects' data to the holder list and calculate the nanmeans to store in the database
					neu_subject_times.append(nanmean(neu_time_at_pref)); 
					neu_subject_percs.append(nanmean(neu_perc_at_pref));
					cue_subject_times.append(nanmean(cue_time_at_pref));
					cue_subject_percs.append(nanmean(cue_perc_at_pref));
					not_cue_subject_times.append(nanmean(not_cue_time_at_pref));
					not_cue_subject_percs.append(nanmean(not_cue_perc_at_pref));
					all_rts.append(nanmean(rts));
					
					1/0
					
					db['%s_high_pref_selected_%s_look_at_neutral_mean_time_at_pref'%(sub_id,selected_item)] = nanmean(neu_time_at_pref); 
					db['%s_high_pref_selected_%s_look_at_neutral_mean_perc_time_at_pref'%(sub_id,selected_item)] = nanmean(neu_perc_at_pref);
					db['%s_high_pref_selected_%s_look_at_cue_mean_time_at_pref'%(sub_id,selected_item)] = nanmean(cue_time_at_pref); 
					db['%s_high_pref_selected_%s_look_at_cue_mean_perc_time_at_pref'%(sub_id,selected_item)] = nanmean(cue_perc_at_pref);
					db['%s_high_pref_selected_%s_look_at_not_cue_mean_time_at_pref'%(sub_id,selected_item)] = nanmean(not_cue_time_at_pref); 
					db['%s_high_pref_selected_%s_look_at_not_cuel_mean_perc_time_at_pref'%(sub_id,selected_item)] = nanmean(not_cue_perc_at_pref); 					
					db['%s_high_pref_selected_%s_mean_rt'%(sub_id,selected_item)] = nanmean(rts);
					#add this data to the DataFrame for use in .csv creation
					data.loc[counter] = [sub_id,cue,selected_item,nanmean(neu_time_at_pref),nanmean(neu_perc_at_pref),nanmean(cue_time_at_pref),nanmean(cue_perc_at_pref),nanmean(not_cue_time_at_pref),nanmean(not_cue_perc_at_pref),nanmean(rts)];
					counter+=1;
			
			#now here aggregate all the data together and append it to the database
			db['agg_high_pref_selected_%s_look_at_neutral_mean_time_at_pref'%(selected_item)] = nanmean(neu_subject_times); db['agg_high_pref_selected_%s_look_at_neutral_bs_sems_time_at_pref'%(selected_item)] = compute_BS_SEM(neu_subject_times);
			db['agg_high_pref_selected_%s_look_at_neutral_mean_perc_time_at_pref'%(sub_id,selected_item)] = nanmean(neu_subject_percs); db['agg_high_pref_selected_%s_look_at_neutral_bs_sems_perc_time_at_pref'%(sub_id,selected_item)] = compute_BS_SEM(neu_subject_percs);				
			db['agg_high_pref_selected_%s_look_at_cue_mean_time_at_pref'%(selected_item)] = nanmean(cue_subject_times); db['agg_high_pref_selected_%s_look_at_cue_bs_sems_time_at_pref'%(selected_item)] = compute_BS_SEM(cue_subject_times);
			db['agg_high_pref_selected_%s_look_at_cue_mean_perc_time_at_pref'%(sub_id,selected_item)] = nanmean(cue_subject_percs); db['agg_high_pref_selected_%s_look_at_cue_bs_sems_perc_time_at_pref'%(sub_id,selected_item)] = compute_BS_SEM(cue_subject_percs);			
			db['agg_high_pref_selected_%s_look_at_not_cue_mean_time_at_pref'%(selected_item)] = nanmean(not_cue_subject_times); db['agg_high_pref_selected_%s_look_at_not_cue_bs_sems_time_at_pref'%(selected_item)] = compute_BS_SEM(not_cue_subject_times);
			db['agg_high_pref_selected_%s_look_at_not_cue_mean_perc_time_at_pref'%(sub_id,selected_item)] = nanmean(not_cue_subject_percs); db['agg_high_pref_selected_%s_look_at_not_cue_bs_sems_perc_time_at_pref'%(sub_id,selected_item)] = compute_BS_SEM(not_cue_subject_percs);				
			db['agg_high_pref_selected_%s_mean_rt'%(sub_id,selected_item)] = nanmean(all_rts); db['agg_high_pref_selected_%s_bs_sems_rt'%(sub_id, selected_item)] = compute_BS_SEM(all_rts);		


	#write the data to csv files
	high_vs_other_pref_data.to_csv(savepath+'perc_time_avg_high_vs_nothigh_pref_trial_data.csv',index=False); 



def computeLastItemLookedAt(blocks, eyed = 'agg'):
	#this function computes the average proportion of trials that the last item that was looked at was the selected item
	db = subject_data;
	
	#loop through and get all the trials for each subject
	trial_matrix = [[tee for b in bl for tee in b.trials] for bl in blocks];

	#find each subjects' cue substance based on which item them chose more often during PAPC trials where they selected the alcohol or cigarette
	all_substances = [[tee.preferred_category for tee in subject if (((tee.preferred_category=='alcohol')|(tee.preferred_category=='cigarette'))&
		(tee.dropped_sample == 0)&(tee.didntLookAtAnyItems == 0)&(tee.trial_type == 1))] for subject in trial_matrix]; #first get all the selected categories
	prop_chose_alc = [sum([val == 'alcohol' for val in subject])/float(len([val == 'alcohol' for val in subject])) for subject in all_substances]; #now get proportion of time seleteced alcohol
	prop_chose_cig = [sum([val == 'cigarette' for val in subject])/float(len([val == 'alcohol' for val in subject])) for subject in all_substances]; #then proportion of times selecting cigarette
	#then find which proportion is greater and define whether that subject's cue is alcohol or cigarette
	subject_cues = ['alcohol' if (a>c) else 'cigarette' for a,c in zip(prop_chose_alc,prop_chose_cig)];
	
	high_vs_other_pref_data = pd.DataFrame(columns = ['sub_id','trial_type','percentage_last_fixated_item_was_selected', 'mean_response_time']);
	high_pref_only_data = pd.DataFrame(columns = ['sub_id','preferred_pic','percentage_last_fixated_item_was_selected', 'mean_response_time']);
	cue_vs_not_cue_data = pd.DataFrame(columns = ['sub_id','cue_type','percentage_last_fixated_item_was_selected', 'mean_response_time']);
	
	#store all the trial data for each subject in a master DB
	hl_index_counter = 0;
	all_high_index_counter = 0;
	cv_counter = 0;
	for high_pref_trial,name in zip([0,1],['non_high_pref','high_pref']):	
		raw_prop_last_fixated_item = [[(tee.lastItemLookedAt == tee.preferred_item) for tee in subj
			if((tee.dropped_sample == 0)&(tee.didntLookAtAnyItems == 0)&((tee.trial_type == 1)==high_pref_trial))] for subj in trial_matrix];
		rts = [mean([tee.response_time for tee in subj
			if((tee.dropped_sample == 0)&(tee.didntLookAtAnyItems == 0)&((tee.trial_type == 1)==high_pref_trial))]) for subj in trial_matrix];
		prop_last_fixated_item = [sum(subj)/float(len(subj)) for subj in raw_prop_last_fixated_item];
		db['%s_%s_mean_prop_last_fixated_item'%(eyed,name)] = nanmean(prop_last_fixated_item); db['%s_%s_bs_sems_prop_last_fixated_item'%(eyed,name)] = compute_BS_SEM(prop_last_fixated_item);
		db['%s_%s_mean_rt'%(eyed,name)] = nanmean(rts); db['%s_%s_bs_sems_rt'%(eyed,name)] = compute_BS_SEM(rts);		
		for id,pp,rt in zip(ids, prop_last_fixated_item, rts):
			#add the data to a pandas.DataFrame object to write it to a file for use in R to run the stats
			high_vs_other_pref_data.loc[hl_index_counter] = [id,name,nanmean(pp),nanmean(rt)];
			hl_index_counter+=1;		
		
		#cycle through the different types of high preference trials (where each one could be selected):
		#1. all high-pref trials, 2. all not high pref trials, 3. alcohol high pref trials
		#4. cigarette high pref trials, and 5. neutral high pref trials
		if high_pref_trial==1:		
			for pref_category in ['alcohol','cigarette','neutral']:
				raw_prop_last_fixated_item = [[(tee.lastItemLookedAt == tee.preferred_item) for tee in subj
					if((tee.dropped_sample == 0)&(tee.didntLookAtAnyItems == 0)&((tee.trial_type == 1)==high_pref_trial))&(tee.preferred_category == pref_category)] for subj in trial_matrix];
				rts = [mean([tee.response_time for tee in subj
					if((tee.dropped_sample == 0)&(tee.didntLookAtAnyItems == 0)&((tee.trial_type == 1)==high_pref_trial))&(tee.preferred_category == pref_category)]) for subj in trial_matrix];
				prop_last_fixated_item = [sum(subj)/float(len(subj)) for subj in raw_prop_last_fixated_item];
				db['%s_high_pref_%s_mean_prop_last_fixated_item'%(eyed,pref_category)] = nanmean(prop_last_fixated_item); db['%s_high_pref_%s_bs_sems_prop_last_fixated_item'%(eyed,pref_category)] = compute_BS_SEM(prop_last_fixated_item);
				db['%s_high_pref_%s_mean_rt'%(eyed,pref_category)] = nanmean(rts); db['%s_high_pref_%s_bs_sems_rt'%(eyed,pref_category)] = compute_BS_SEM(rts);
				for id,pp,rt in zip(ids, prop_last_fixated_item, rts):
					#add the data to a pandas.DataFrame object to write it to a file for use in R to run the stats
					high_pref_only_data.loc[all_high_index_counter] = [id,name,nanmean(pp),nanmean(rt)];
					all_high_index_counter+=1;
										
			#now run this analysis for the trials where the subject selected the cue item, as defined above, vs the non cued item 
					
			for cue_or_not, cue_name in zip([1,0],['cue','not_cue']):	
				raw_prop_last_fixated_item = [[(tee.lastItemLookedAt == tee.preferred_item) for tee in subj
					if((tee.dropped_sample == 0)&(tee.didntLookAtAnyItems == 0)&((tee.trial_type == 1)==high_pref_trial))&((tee.preferred_category == cue)==cue_or_not)
					&((tee.preferred_category == 'alcohol')|(tee.preferred_category == 'cigarette'))] for subj,cue in zip(trial_matrix,subject_cues)];
				rts = [mean([tee.response_time for tee in subj
					if((tee.dropped_sample == 0)&(tee.didntLookAtAnyItems == 0)&((tee.trial_type == 1)==high_pref_trial))&((tee.preferred_category == cue)==cue_or_not)
					&((tee.preferred_category == 'alcohol')|(tee.preferred_category == 'cigarette'))]) for subj,cue in zip(trial_matrix,subject_cues)];
				prop_last_fixated_item = [sum(subj)/float(len(subj)) for subj in raw_prop_last_fixated_item];
				db['%s_high_pref_selected_%s_mean_prop_last_fixated_item'%(eyed,cue_name)] = nanmean(prop_last_fixated_item); db['%s_high_pref_selected_%s_bs_sems_prop_last_fixated_item'%(eyed,cue_name)] = compute_BS_SEM(prop_last_fixated_item);
				db['%s_high_pref_selected_%s_mean_rt'%(eyed,cue_name)] = nanmean(rts); db['%s_high_pref_selected_%s_bs_sems_rt'%(eyed,cue_name)] = compute_BS_SEM(rts);				
				for id,pp,rt in zip(ids, prop_last_fixated_item, rts):
					#add the data to a pandas.DataFrame object to write it to a file for use in R to run the stats				
					cue_vs_not_cue_data.loc[all_high_index_counter] = [id,cue_name,nanmean(pp),nanmean(rt)];
					cv_counter+=1;
				
	#write the data to csv files
	high_vs_other_pref_data.to_csv(savepath+'last_item_avg_high_vs_nothigh_pref_trial_data.csv',index=False); 
	high_pref_only_data.to_csv(savepath+'last_item_avg_high_pref_only_trial_data.csv',index=False);
	cue_vs_not_cue_data.to_csv(savepath+'last_item_cue_not_cue_high_pref_trial_data.csv',index=False);
	
	
def computeTemporalGazeProfile(blocks, id = 'agg'):
	#this function compute the temporal gaze profile with respect to the preferred item
	#for each subject and each trial type, find the average proportion of time spent looking
	#at the perferred tem or not. This will be the 'likelihood' of fixating the preferred item
	#with respect to time to the decision
	
	db = subject_data;
	
	#loop through and get all the trials for each subject
	trial_matrix = [[tee for b in bl for tee in b.trials] for bl in blocks];
	
	#find each subjects' cue substance based on which item them chose more often during PAPC trials where they selected the alcohol or cigarette
	all_substances = [[tee.preferred_category for tee in subject if (((tee.preferred_category=='alcohol')|(tee.preferred_category=='cigarette'))&
		(tee.dropped_sample == 0)&(tee.didntLookAtAnyItems == 0)&(tee.trial_type == 1))] for subject in trial_matrix]; #first get all the selected categories
	prop_chose_alc = [sum([val == 'alcohol' for val in subject])/float(len([val == 'alcohol' for val in subject])) for subject in all_substances]; #now get proportion of time seleteced alcohol
	prop_chose_cig = [sum([val == 'cigarette' for val in subject])/float(len([val == 'alcohol' for val in subject])) for subject in all_substances]; #then proportion of times selecting cigarette
	#then find which proportion is greater and define whether that subject's cue is alcohol or cigarette
	subject_cues = ['alcohol' if (a>c) else 'cigarette' for a,c in zip(prop_chose_alc,prop_chose_cig)];		

	# #at some point store this data into a database/csv
		
	#calculate the temporal gaze profiles for each subset of rials: selected the cue, selected the not cue, and selected the neutral
	#then for each of these subsets, find and plot the probability of looking at each item through the trial
	for cue_or_not, selected_item in zip([1,0,0],['cue','not_cue','neutral']):
		fig = figure(); ax1 = gca();
		ax1.set_ylim(0.0, 1.0); ax1.set_yticks(arange(0,1.01,0.1)); ax1.set_xlim([0,1000]);
		ax1.set_ylabel('Likelihood of fixating',size=18); ax1.set_xlabel('Time with respect to decision, ms',size=18,labelpad=11);
		ax1.set_xticks([0,200,400,600,800,1000]);
		ax1.set_xticklabels(['-1000','-800','-600','-400','-200','0']);
		colors = ['red','blue', 'green']; alphas = [1.0, 1.0, 1.0]; legend_lines = [];		count = 0;
		#define arrays for the neutral, cue, and not_cue items
		neu_gaze_array = zeros(time_duration/time_bin_spacing);
		neu_counts = zeros(shape(neu_gaze_array));
		neu_subject_means_array = [[] for i in range(1000)]; #use this to store each individual subjects' mean for each time point			
		cue_gaze_array = zeros(time_duration/time_bin_spacing);
		cue_counts = zeros(shape(cue_gaze_array));
		cue_subject_means_array = [[] for i in range(1000)]; 		
		not_cue_gaze_array = zeros(time_duration/time_bin_spacing);
		not_cue_counts = zeros(shape(not_cue_gaze_array));
		not_cue_subject_means_array = [[] for i in range(1000)]; 		
		for subj,cue in zip(trial_matrix, subject_cues):
			neu_individ_subject_sum = zeros(time_duration/time_bin_spacing);
			neu_individ_subject_counts = zeros(time_duration/time_bin_spacing);
			cue_individ_subject_sum = zeros(time_duration/time_bin_spacing);
			cue_individ_subject_counts = zeros(time_duration/time_bin_spacing);
			not_cue_individ_subject_sum = zeros(time_duration/time_bin_spacing);
			not_cue_individ_subject_counts = zeros(time_duration/time_bin_spacing);	
			for t in subj:
				#conditional to differentiate between not-cue trials when selecteing the non-cue or not
				#the second conditional include nuetral trials that were preferred only
				if ((selected_item=='cue')|(selected_item=='not_cue')):
					if ((t.dropped_sample == 0)&(t.didntLookAtAnyItems == 0)&((t.trial_type == 1)==1)&((t.preferred_category == cue)==cue_or_not)&((t.preferred_category == 'alcohol')|(t.preferred_category == 'cigarette'))):
						#neutral is always the same...
						#cycle through each time point, going backward through the array (e.g., -1, -2..) and aggregating the data accordingly
						for i in (arange(1000)+1):
							if (i>len(t.lookedAtNeutral)):
								continue;
							elif (isnan(t.lookedAtNeutral[-i])):
								continue;
							neu_gaze_array[-i] += t.lookedAtNeutral[-i];
							neu_counts[-i] += 1;
							#put the individual subject data together
							neu_individ_subject_sum[-i] += t.lookedAtNeutral[-i];
							neu_individ_subject_counts[-i] += 1;
						if cue=='alcohol':
							for i in (arange(1000)+1):
								if (i>len(t.lookedAtAlcohol)):
									continue;
								elif (isnan(t.lookedAtAlcohol[-i])):
									continue;
								#store the alcohol gaze patterns as the cue item
								cue_gaze_array[-i] += t.lookedAtAlcohol[-i];
								cue_counts[-i] += 1;
								#put the individual subject data together
								cue_individ_subject_sum[-i] += t.lookedAtAlcohol[-i];
								cue_individ_subject_counts[-i] += 1;
								
								#and store the cigarette items as the not_cue item
								not_cue_gaze_array[-i] += t.lookedAtCigarette[-i];
								not_cue_counts[-i] += 1;
								#put the individual subject data together
								not_cue_individ_subject_sum[-i] += t.lookedAtCigarette[-i];
								not_cue_individ_subject_counts[-i] += 1;
							
						elif cue=='cigarette':
							for i in (arange(1000)+1):
								if (i>len(t.lookedAtAlcohol)):
									continue;
								elif (isnan(t.lookedAtAlcohol[-i])):
									continue;							
								#store the cigarette items as the not_cue item
								cue_gaze_array[-i] += t.lookedAtCigarette[-i];
								cue_counts[-i] += 1;
								#put the individual subject data together
								cue_individ_subject_sum[-i] += t.lookedAtCigarette[-i];
								cue_individ_subject_counts[-i] += 1;							
	
								#and store the alcohol gaze patterns as the cue item
								not_cue_gaze_array[-i] += t.lookedAtAlcohol[-i];
								not_cue_counts[-i] += 1;
								#put the individual subject data together
								not_cue_individ_subject_sum[-i] += t.lookedAtAlcohol[-i];
								not_cue_individ_subject_counts[-i] += 1;
								
				if (selected_item=='neutral'):
					if ((t.dropped_sample == 0)&(t.didntLookAtAnyItems == 0)&((t.trial_type == 1)==1)&((t.preferred_category == cue)==cue_or_not)&(t.preferred_category == 'neutral')):
						#neutral is always the same...
						#cycle through each time point, going backward through the array (e.g., -1, -2..) and aggregating the data accordingly
						for i in (arange(1000)+1):
							if (i>len(t.lookedAtNeutral)):
								continue;
							elif (isnan(t.lookedAtNeutral[-i])):
								continue;
							neu_gaze_array[-i] += t.lookedAtNeutral[-i];
							neu_counts[-i] += 1;
							#put the individual subject data together
							neu_individ_subject_sum[-i] += t.lookedAtNeutral[-i];
							neu_individ_subject_counts[-i] += 1;
						if cue=='alcohol':
							for i in (arange(1000)+1):
								if (i>len(t.lookedAtAlcohol)):
									continue;
								elif (isnan(t.lookedAtAlcohol[-i])):
									continue;
								#store the alcohol gaze patterns as the cue item
								cue_gaze_array[-i] += t.lookedAtAlcohol[-i];
								cue_counts[-i] += 1;
								#put the individual subject data together
								cue_individ_subject_sum[-i] += t.lookedAtAlcohol[-i];
								cue_individ_subject_counts[-i] += 1;
								
								#and store the cigarette items as the not_cue item
								not_cue_gaze_array[-i] += t.lookedAtCigarette[-i];
								not_cue_counts[-i] += 1;
								#put the individual subject data together
								not_cue_individ_subject_sum[-i] += t.lookedAtCigarette[-i];
								not_cue_individ_subject_counts[-i] += 1;
							
						elif cue=='cigarette':
							for i in (arange(1000)+1):
								if (i>len(t.lookedAtAlcohol)):
									continue;
								elif (isnan(t.lookedAtAlcohol[-i])):
									continue;							
								#store the cigarette items as the not_cue item
								cue_gaze_array[-i] += t.lookedAtCigarette[-i];
								cue_counts[-i] += 1;
								#put the individual subject data together
								cue_individ_subject_sum[-i] += t.lookedAtCigarette[-i];
								cue_individ_subject_counts[-i] += 1;							
	
								#and store the alcohol gaze patterns as the cue item
								not_cue_gaze_array[-i] += t.lookedAtAlcohol[-i];
								not_cue_counts[-i] += 1;
								#put the individual subject data together
								not_cue_individ_subject_sum[-i] += t.lookedAtAlcohol[-i];
								not_cue_individ_subject_counts[-i] += 1;								
								
							
			neu_individ_subject_mean = neu_individ_subject_sum/neu_individ_subject_counts; #calculate the mean for this subject at each time point
			[neu_subject_means_array[index].append(ind_mew) for index,ind_mew in zip(arange(1000),neu_individ_subject_mean)]; #append this to the array for each subject   			
			cue_individ_subject_mean = cue_individ_subject_sum/cue_individ_subject_counts; #calculate the mean for this subject at each time point
			[cue_subject_means_array[index].append(ind_mew) for index,ind_mew in zip(arange(1000),cue_individ_subject_mean)]; #append this to the array for each subject
			not_cue_individ_subject_mean = not_cue_individ_subject_sum/not_cue_individ_subject_counts; #calculate the mean for this subject at each time point
			[not_cue_subject_means_array[index].append(ind_mew) for index,ind_mew in zip(arange(1000),not_cue_individ_subject_mean)]; #append this to the array for each subject   					
							
		#plot each likelihood looking at items				
		for  subj_ms, cue_name, c, a in zip([cue_subject_means_array, not_cue_subject_means_array, neu_subject_means_array], ['cue','not_cue','neutral'], colors, alphas):							
			mews = array([nanmean(subj) for subj in subj_ms]); # gaze_array/counts
			sems = array([compute_BS_SEM(subj) for subj in subj_ms]);
			ax1.plot(linspace(0,1000,1000), mews, lw = 4.0, color = c, alpha = a);
			#plot the errorbars
			#for x,m,s in zip(linspace(0,1000,1000),mews,sems):
			ax1.fill_between(linspace(0,1000,1000), mews-sems, mews+sems, color = c, alpha = a*0.4);
			legend_lines.append(mlines.Line2D([],[],color=c,lw=6,alpha = a, label='likelihood(time looking at %s) '%cue_name));
		#plot the sum of each fora sanity emasure to ensure they equate to one
		agg = [(nanmean(a)+nanmean(b)+nanmean(c)) for a,b,c in zip(cue_subject_means_array, not_cue_subject_means_array, neu_subject_means_array)];
		ax1.plot(linspace(0,1000,1000),agg,color = 'gray', lw = 3.0);
		legend_lines.append(mlines.Line2D([],[],color='gray',lw=4, alpha = 1.0, label='sum of all'));
		ax1.plot(linspace(0,1000,1000),linspace(0.33,0.333,1000),color = 'gray', lw = 3.0, ls='dashed');
		legend_lines.append(mlines.Line2D([],[],color='gray',lw=4, alpha = 1.0, ls = 'dashed', label='random'));	
		ax1.spines['right'].set_visible(False); ax1.spines['top'].set_visible(False);
		ax1.spines['bottom'].set_linewidth(2.0); ax1.spines['left'].set_linewidth(2.0);
		ax1.yaxis.set_ticks_position('left'); ax1.xaxis.set_ticks_position('bottom');
		ax1.legend(handles=[legend_lines[0],legend_lines[1], legend_lines[2], legend_lines[3], legend_lines[4]],loc = 2,ncol=1,fontsize = 11); #, legend_lines[2]
		title('Average Temporal Gaze Profile, \n Chose %s Trials'%(selected_item), fontsize = 22);
	show();

def compute_BS_SEM(data_matrix):
    #calculate the between-subjects standard error of the mean. trial_matrix should be matrix of trials including each subject
    #should only pass trials matrix into this function after segmenting into relevant conditions
	
	#for now until otherwise decided, find the BS-sems using only the point estimates that I have for each conditions
	#This involves cutting out the items that are NaNs
	
	nan_truth_arr = [isnan(d) for d in data_matrix]; #find where a Nan exists in the array
	data = [r for r,l in zip(data_matrix,nan_truth_arr) if (l==False)]; #this collects only the non-Nans in the datamatrix and makes a list of them
	
	n = len(data);	 #data_matrix
	grand_mew = mean(data); 
	err = data - grand_mew; #_matrix
	squared_err = err**2;
	MSE = sum(squared_err)/(n-1);	
	denom = sqrt(n);
	standard_error_estimate=sqrt(MSE)/float(denom);
	return standard_error_estimate;

############################################
## Data Importing Functions ##
############################################

#define a function to import individual .mat data files
def loadBlock(subid,block_type,block_nr):
	#returns a single Block object corresponding to the block number and subject id
	#block type should be a string corresponding to the task type(e.g. 'Discrim')
	filename = glob(datapath+'%s'%subid+'/'+'*_%s_%d.mat'%(subid,block_nr)); #use Regular expressions to find the filename
	matdata = loadmat(filename[0],struct_as_record=False,squeeze_me=True)['block']; #use scipy loadmat() to load in the files
	block=Block(matdata); #here, create Block object with dictionary of trial data in matdata
	return block;

#define a function to import all .mat data files for a given subject
def loadAllBlocks(subid):
    filenames = glob(datapath+'%s'%subid+'/'+'*_%s_[1-9].mat'%subid); #got to check that this regex works here
    blocks = []; #empty list to hold loaded blocks
    for filename in filenames:
        matdata=loadmat(filename,struct_as_record=False,squeeze_me=True)['block'];
        block=Block(matdata);
        blocks.append(block);
    return blocks #return the loaded blocks as a list for later purposes..

#define functions to get subject specific blocks and aggregate blocks together for analysis, respectively
def getAllSubjectBlocks():
    blocks = [[] for i in range(len(ids))]; #create a list of empty lists to append the individual blocks to
    for i,sub_id in enumerate(ids):
        blocks[i] = loadAllBlocks(sub_id);
        print "Imported data for subject %s\n"%sub_id;
    #print "Done getting all subject blocks..\n";
    return blocks;

############################################
## Data Structures ###
############################################

#define a Block object that will hold the Trials for each block along with relevant data (e.g. date)
class Block(object):
	#object being passed into this class should be a scipy mat_structure of data from the block
	def __init__(self, matStructure=None):
		self.block_nr= matStructure.block_nr;
		self.date = str(matStructure.date);
		self.sub_id = str(matStructure.sub_id);
		self.sp = matStructure.sp;
		self.dp = matStructure.dp;
		self.trials = [trial(trialData) for trialData in matStructure.trial_data];

#define a Trial object that will hold the individual trial data 
class trial(object):
	#object being passed into this Trial instance should be a dictionary corresponding to the trial data for this given trial
	def __init__(self, trialData):
		self.sub_id = str(trialData.saved_id);
		self.block_nr = trialData.block_nr;
		self.trial_nr = trialData.trial_nr;
		self.trial_type = trialData.trial_type; #determines the pictures that were presented
		self.response_time = trialData.trial_times.response_time*1000; #put reaction time into seconds
		self.alcohol_pref = str(trialData.alcohol_pref);
		self.cigarette_pref = str(trialData.cigarette_pref);
		self.presented_pics = [str(t)[:-23] for t in trialData.corresponding_names];
		self.picture_order = trialData.picture_ordering;
		self.presented_up = str(trialData.presented_up)[:-23]; #slice the string to cut off the '_grayscaled_resizde.png' portion of the string
		self.presented_left = str(trialData.presented_left)[:-23];
		self.presented_right = str(trialData.presented_right)[:-23];
		#conditionals to define where each item was stored
		if self.presented_up in alcohol_filenames:
			self.alcohol_loc = 'up';
		elif self.presented_up in cigarette_filenames:
			self.cigarette_loc = 'up';
		elif self.presented_up in neutral_filenames:
			self.neutral_loc = 'up';
			
		if self.presented_left in alcohol_filenames:
			self.alcohol_loc = 'left';
		elif self.presented_left in cigarette_filenames:
			self.cigarette_loc = 'left';
		elif self.presented_left in neutral_filenames:
			self.neutral_loc = 'left';
			
		if self.presented_right in alcohol_filenames:
			self.alcohol_loc = 'right';
		elif self.presented_right in cigarette_filenames:
			self.cigarette_loc = 'right';
		elif self.presented_right in neutral_filenames:
			self.neutral_loc = 'right';			
		
		#response and results
		self.reponse = str(trialData.response); #letter corresponding to presented
		self.selected_loc = trialData.selected_loc; 
		self.preferred_item = str(trialData.preferred_item)[:-23];
		#finally, eye position and pupil size information
		self.drift_shift = trialData.drift_shift;

		#loop through to get only unique samples, e.g. sampling at 1000 Hz 
		all_sample_times = trialData.sampleTimes-trialData.sampleTimes[0]; #get sample times
		prev_time = -1;
		eyeX = []; eyeY = []; pSize = []; samp_times = [];
		self.dropped_sample = 0; #pre-allocate this and change it if I find one
		
		for time,x_pos,y_pos,pup_s in zip(all_sample_times,trialData.eyeX,trialData.eyeY,trialData.pSize):
			if time==prev_time:
				continue;
			else:
				samp_times.append(time);
				#check if the sample was very large (e.g., blink or look away) and set the corresponding values to NaNs
				if (abs(x_pos)>100)|(abs(y_pos)>100):
					x_pos = nan; y_pos = nan; pup_s = nan;
					self.dropped_sample = 1;
				eyeX.append(x_pos);
				eyeY.append(y_pos);
				pSize.append(pup_s);
				prev_time = time;
			
		#get the data together	
		self.sample_times = array(samp_times); #[::sampStep];
		self.eyeX = array(eyeX); #[::sampStep];
		self.eyeY = array(eyeY); #[::sampStep];
		self.p_size = array(pSize); #[::sampStep];
		
		#find when the subject was saccading in each trial
		#first use a differentiation method to define the velocity (eye position change/time change) for each time point in the trial
		timeChange = 0.001; #diff(self.sample_times); #difference in time, in seconds 
		xChange = -diff(self.eyeX);
		yChange = -diff(self.eyeY);
		totalChange = sqrt(xChange**2+yChange**2);
		temp = totalChange/timeChange; #calculate the velocity for each time point
		self.velocities = insert(temp,0,0); #insert a 0 at the beginning of the array for the first time point
		
		#Next filter the velocities... this may or may not be necessary/advisable
		#get params for a butterworth filter and bandpass it at 10 Hz
		trialTime = self.sample_times[-1]-self.sample_times[0]; #get total time for the trial
		samplingRate = 1000.0; #round(len(self.sample_times)/float(trialTime)); #get the downsampled sampling rate
		halfSRate = samplingRate/2; freqCut = 10; 
		butterwindow = freqCut/halfSRate; nthOrder = 2; #defining parameters for the butterworth filter
		[b,a] = ssignal.butter(nthOrder,butterwindow); #fit the butterworth filter
		y = ssignal.filtfilt(b,a,self.velocities,padtype='odd'); #get the filtered velocity data		
		self.filtered_velocities = y; #append the filtered velocities to this trial instance
		
		#now determine where the eye was in motion by using an (arbitrary) criterion for saccade velocity
		self.saccadeCriterion = 30; #degrees/sec
		self.isSaccade = self.filtered_velocities > self.saccadeCriterion;
		
		# if self.dropped_sample < 1:
		# 	self.plotSaccadeDebug();
				
		self.get_ET_data(); #call this method defined below
		
	#define a function that takes a trial object and determines the proportion of time was looking at each item
	#this should find arrays of length(trial time) for each item/location, marking a 0 if not looking at that loc
	#and a 1 if it is. also should aggregate this together in a succint manner (e.g., proportion of trial spent looking at each item)
	#will call this in the Trial definition function
	
	def plotSaccadeDebug(self):
	#plots the different saccades for the given trial for use in debugging	
		fig = figure(figsize = (12.8,7.64)); ax = gca(); ax.set_xlim([-display_size[0]/2,display_size[0]/2]); ax.set_ylim([-display_size[1]/2,display_size[1]/2]);
		ax.set_ylabel('Y Position, Degrees of Visual Angle',size=18); ax.set_xlabel('X Position, Degrees of Visual Angle',size=18,labelpad=11); hold(True);
		legend_lines = []; colors = ['red','green','blue','purple','orange','brown','grey','crimson','deepskyblue','lime','salmon','deeppink','lightsteelblue'];
		#first plot the eye traces with respect to the velocity data
		#if the eye is in movements, use the color array above. otheriwse use black to denote fixation
		saccade_counter = 0; nr_saccades = 0;
		for i,xx,yy,issac in zip(range(len(self.sample_times)),
											 self.eyeX, self.eyeY, self.isSaccade):
			#plot the eye trace in black if not saccading
			if issac < 1:
				ax.plot(xx,yy, color = 'black', marker = 'o', ms = 4);
				#conditional to switch to the next saccade color
				#if the previous sample was saccading and now it isn't time for a swtch (add a number to saccades, switch the color for next time)
				if self.isSaccade[i-1]==True:
					nr_saccades+=1
					legend_lines.append(mlines.Line2D([],[],color=colors[saccade_counter],lw=6,alpha = 1.0, label='saccade  %s'%(nr_saccades)));					
					saccade_counter+=1;
					if saccade_counter > len(colors):
						saccade_counter=0;
			else:
				ax.plot(xx, yy, color = colors[saccade_counter], marker = 'o', ms = 4);
				
		ax.spines['right'].set_visible(False); ax.spines['top'].set_visible(False);
		ax.spines['bottom'].set_linewidth(2.0); ax.spines['left'].set_linewidth(2.0);
		ax.yaxis.set_ticks_position('left'); ax.xaxis.set_ticks_position('bottom');
		ax.legend(handles=[hand for hand in legend_lines],loc = 2,ncol=3,fontsize = 10); 
		title('Eye Trace and Position Velocity, Degrees per Second,\nSubject %s, Block %s, Trial %s'%(self.sub_id, self.block_nr, self.trial_nr), fontsize = 22);
		
		#now plot the velocity data in an inset plot	
		ia = inset_axes(ax, width="30%", height="30%", loc=1); #set the inset axes as percentages of the original axis size
		saccade_counter = 0; nr_saccades = 0;
		for i,filt_vel,orig_vel,issac in zip(range(len(self.sample_times)),
											 self.filtered_velocities, self.velocities, self.isSaccade):
			#plot the eye trace in black if not saccading
			plot(i, orig_vel, color = 'gray', marker = '*', ms = 1.0, alpha = 0.5),
			if issac < 1:
				plot(i, filt_vel, color = 'black', marker = '*', ms = 1.5);
				#conditional to switch to the next saccade color
				#if the previous sample was saccading and now it isn't time for a swtch (add a number to saccades, switch the color for next time)
				if self.isSaccade[i-1]==1:
					nr_saccades+=1				
					saccade_counter+=1;
					if saccade_counter > len(colors):
						saccade_counter=0;
			else:
				plot(i, filt_vel, color = colors[saccade_counter], marker = '*', ms = 1.5);		
		#plot the velocity trheshold and set labels
		plot(linspace(0,len(self.sample_times),len(self.sample_times)), linspace(self.saccadeCriterion,self.saccadeCriterion+0.01,len(self.sample_times)), color = 'red', ls = 'dashed', lw = 1.0);
		ia.set_xlabel('Velocity', fontsize = 14); ia.set_ylabel('Time', fontsize = 14); title('Velocity Profile', fontsize = 14);
		
		bool = raw_input();	#wait for the button press to move to next trial
		close('all');	

	def get_ET_data(self):
		lookedUp = zeros(len(self.sample_times)); #truth arrays
		lookedLeft = zeros(len(self.sample_times));
		lookedRight = zeros(len(self.sample_times));
		
		#0. loop through the time points and determine whether they were looking at each item at each time point
		
		for i,data in enumerate(zip(self.sample_times,self.eyeX,self.eyeY)):

			time = data[0]; xx = data[1]; yy = data[2]; #pull out the data from the data tuple
			
			#conditional to check if eye position was within the threshold for each image loc			
			if sqrt((xx-up_pic_coors[0])**2 + (yy-up_pic_coors[1])**2)<distance_threshold:
				lookedUp[i] = 1;
			elif sqrt((xx-left_pic_coors[0])**2 + (yy-left_pic_coors[1])**2)<distance_threshold:	
				lookedLeft[i] = 1;
			elif sqrt((xx-right_pic_coors[0])**2 + (yy-right_pic_coors[1])**2)<distance_threshold:	
				lookedRight[i] = 1;
				
		#1.0 assign the truth arrays to the appropriate image type.		
							
		if self.alcohol_loc ==  'up':
			self.lookedAtAlcohol = lookedUp;
		elif self.alcohol_loc == 'left':
			self.lookedAtAlcohol = lookedLeft;
		elif self.alcohol_loc == 'right':
			self.lookedAtAlcohol = lookedRight;

		if self.cigarette_loc ==  'up':
			self.lookedAtCigarette = lookedUp;
		elif self.cigarette_loc == 'left':
			self.lookedAtCigarette = lookedLeft;
		elif self.cigarette_loc == 'right':
			self.lookedAtCigarette = lookedRight;			
			
		if self.neutral_loc ==  'up':
			self.lookedAtNeutral = lookedUp;
		elif self.neutral_loc == 'left':
			self.lookedAtNeutral = lookedLeft;
		elif self.neutral_loc == 'right':
			self.lookedAtNeutral = lookedRight;
			
		#1.1 find the timepoints where the subject wasn't looking at any item and replace it with nan
		
		notLookingAtAnyItem = where((self.lookedAtAlcohol==0)&(self.lookedAtCigarette==0)&(self.lookedAtNeutral==0))[0]; #this is an array of indices where the overlap between arrays exists
		self.lookedAtAlcohol[notLookingAtAnyItem] = nan;
		self.lookedAtCigarette[notLookingAtAnyItem] = nan;
		self.lookedAtNeutral[notLookingAtAnyItem] = nan;
			
		#2. compute the amount and percentage of time spent looking at each item in each trial
		
		self.timeLookingAtAlcohol = nansum(self.lookedAtAlcohol);
		self.percentageTimeLookingAtAlcohol = nansum(self.lookedAtAlcohol)/float(len(self.lookedAtAlcohol)-len(notLookingAtAnyItem));
		if isnan(self.percentageTimeLookingAtAlcohol): self.percentageTimeLookingAtAlcohol = 0.0; #conditional in case the subject never looked at any of the items
		self.timeLookingAtCigarette = nansum(self.lookedAtCigarette);
		self.percentageTimeLookingAtCigarette = nansum(self.lookedAtCigarette)/float(len(self.lookedAtCigarette)-len(notLookingAtAnyItem));
		if isnan(self.percentageTimeLookingAtCigarette): self.percentageTimeLookingAtCigarette = 0.0;
		self.timeLookingAtNeutral = nansum(self.lookedAtNeutral);
		self.percentageTimeLookingAtNeutral = nansum(self.lookedAtNeutral)/float(len(self.lookedAtNeutral)-len(notLookingAtAnyItem));
		if isnan(self.percentageTimeLookingAtNeutral): self.percentageTimeLookingAtNeutral = 0.0;
		
		#2.1 Flag if the subject didn't looked at any of the items in the trial
		
		if (self.percentageTimeLookingAtAlcohol+self.percentageTimeLookingAtCigarette+self.percentageTimeLookingAtNeutral == 0):
			self.didntLookAtAnyItems = 1;
		else:
			self.didntLookAtAnyItems = 0;
		
		#3. assign the array and stats that corresponded to the chosen item to a unique array	
			
		if self.preferred_item in alcohol_filenames:
			self.preferred_category = 'alcohol';
			self.lookedAtPreferred = self.lookedAtAlcohol;
			self.timeLookingAtPreferred = self.timeLookingAtAlcohol;
			self.percentageTimeLookingAtPreferred = self.percentageTimeLookingAtAlcohol;
		elif self.preferred_item in cigarette_filenames:
			self.preferred_category = 'cigarette';
			self.lookedAtPreferred = self.lookedAtCigarette;
			self.timeLookingAtPreferred = self.timeLookingAtCigarette;
			self.percentageTimeLookingAtPreferred = self.percentageTimeLookingAtCigarette;
		elif self.preferred_item in neutral_filenames:
			self.preferred_category = 'neutral';
			self.lookedAtPreferred = self.lookedAtNeutral;			
			self.timeLookingAtPreferred = self.timeLookingAtNeutral;
			self.percentageTimeLookingAtPreferred = self.percentageTimeLookingAtNeutral;
			
		#4. Determine which item was looked at last (alcohol, neutral, or cigarette)
		#4.0 get the latest time point that each item was looked at (alcohol, cigarette, and neutral)
		#use a conditional to catch trials where the item wasn't looked at at all. If so, then the
		#Lookedat*item* array will be all zeros and the resultant truth array for greater than 0 will be empty
		if nansum(self.lookedAtAlcohol) == 0:
			latestAlc = -1;
		else:
			latestAlc = max(where(self.lookedAtAlcohol > 0)[0]);
		if nansum(self.lookedAtCigarette) == 0:
			latestCig = -1;
		else:
			latestCig = max(where(self.lookedAtCigarette > 0)[0]);
		if nansum(self.lookedAtNeutral) == 0:	
			latestNeu = -1;
		else:
			latestNeu = max(where(self.lookedAtNeutral > 0)[0]);
		
		#get the ranking of the values. The last rank (3) will be the largest value, and correspond the latest item looked at
		ranks = stats.rankdata(array([latestAlc, latestCig, latestNeu]), method = 'min'); #method = min assures that a value of 1 is asigned to all ranks if the items tie (for example, when no items were looked at)
		
		#conditional to determine which item had the largest rank and thus latest time in the trial it was looked at
		if ranks[0] == 3:
			self.lastCategoryLookedAt = 'alcohol';
			self.lastItemLookedAt = self.presented_pics[where([name in alcohol_filenames for name in self.presented_pics])[0][0]];
			self.timeLastItemLookedAt = self.sample_times[latestAlc];
		elif ranks[1] == 3:
			self.lastCategoryLookedAt = 'cigarette';
			self.lastItemLookedAt = self.presented_pics[where([name in cigarette_filenames for name in self.presented_pics])[0][0]];
			self.timeLastItemLookedAt = self.sample_times[latestCig];
		elif ranks[2] == 3:
			self.lastCategoryLookedAt = 'neutral';
			self.lastItemLookedAt = self.presented_pics[where([name in neutral_filenames for name in self.presented_pics])[0][0]];
			self.timeLastItemLookedAt = self.sample_times[latestNeu];
		else:
			self.lastCategoryLookedAt = 'none';
			self.lastItemLookedAt = 'none';
			self.timeLastItemLookedAt = -1;



############################################
## Previous code that may be useful but not using currently ###
############################################			
	
## Legacy code for parsing percentage of looking time at preferred items
	# 
	# 
	# #now build a .csv with the averages for each subject 	
	# all_trial_data = pd.DataFrame(columns = ['sub_id','avg_time_looking_at_pref','avg_percentage_looking_at_pref','avg_time_looking_at_alc','avg_percentage_looking_at_alc',
	# 										 'avg_time_looking_at_cig','avg_percentage_looking_at_cig','avg_time_looking_at_neu','avg_percentage_looking_at_neu', 'avg_response_time']);
	# individual_preferred_percentages = []; #preallocate a list to store the percentages of time spent looking at the preferred items
	# #apply a filter to get only the trials where there are nop dropped samples (i.e., no blinks)
	# times_looking_at_preferred = [[t.timeLookingAtPreferred for t in trials if (t.dropped_sample == 0)&(t.didntLookAtAnyItems == 0)] for trials in trial_matrix];
	# percs_looking_at_preferred = [[t.percentageTimeLookingAtPreferred for t in trials if (t.dropped_sample == 0)&(t.didntLookAtAnyItems == 0)] for trials in trial_matrix];
	# times_looking_at_alcohol = [[t.timeLookingAtAlcohol for t in trials if (t.dropped_sample == 0)&(t.didntLookAtAnyItems == 0)] for trials in trial_matrix];
	# percs_looking_at_alcohol = [[t.percentageTimeLookingAtAlcohol for t in trials if (t.dropped_sample == 0)&(t.didntLookAtAnyItems == 0)] for trials in trial_matrix];
	# times_looking_at_cig = [[t.timeLookingAtCigarette for t in trials if (t.dropped_sample == 0)&(t.didntLookAtAnyItems == 0)] for trials in trial_matrix];
	# percs_looking_at_cig = [[t.percentageTimeLookingAtCigarette for t in trials if (t.dropped_sample == 0)&(t.didntLookAtAnyItems == 0)] for trials in trial_matrix];
	# times_looking_at_neutral = [[t.timeLookingAtNeutral for t in trials if (t.dropped_sample == 0)&(t.didntLookAtAnyItems == 0)] for trials in trial_matrix];
	# percs_looking_at_neutral = [[t.percentageTimeLookingAtNeutral for t in trials if (t.dropped_sample == 0)&(t.didntLookAtAnyItems == 0)] for trials in trial_matrix];
	# response_times = [[t.response_time for t in trials if (t.dropped_sample == 0)&(t.didntLookAtAnyItems == 0)] for trials in trial_matrix];
	# index_counter = 0;
	# #now go through and find the means of the times and percentages looking at the items
	# for id,tp,pp,ta,pa,tc,pc,tn,pn,rt in zip(ids, times_looking_at_preferred, percs_looking_at_preferred, times_looking_at_alcohol,
	# 								   percs_looking_at_alcohol, times_looking_at_cig, percs_looking_at_cig,
	# 								   times_looking_at_neutral, percs_looking_at_neutral, response_times):
	# 	individual_preferred_percentages.append(mean(pp)); #append the pecentages of time spejt looking at preferred item
	# 	all_trial_data.loc[index_counter] = [id, mean(tp), mean(pp), mean(ta), mean(pa), mean(tc), mean(pc), mean(tn), mean(pn), mean(rt)];
	# 	index_counter+=1;		
	# 
	# #write the csv file
	# all_trial_data.to_csv(savepath+'individual_subject_all_trials_mean_preference_data.csv',index=False); #got to make sure if this works
	# 
	# #### Now do this for the trials where the two preferred substances were present (e.g., trial type 1)
	# high_preference_trials_data = pd.DataFrame(columns = ['sub_id','avg_time_looking_at_pref','avg_percentage_looking_at_pref','avg_time_looking_at_alc','avg_percentage_looking_at_alc',
	# 										 'avg_time_looking_at_cig','avg_percentage_looking_at_cig','avg_time_looking_at_neu','avg_percentage_looking_at_neu', 'avg_response_time']);
	# hp_individual_preferred_percentages = []; #preallocate a list to store the percentages of time spent looking at the preferred items
	# #apply a filter to get only the trials where there are nop dropped samples (i.e., no blinks)
	# hp_times_looking_at_preferred = [[t.timeLookingAtPreferred for t in trials if (t.dropped_sample == 0)&(t.didntLookAtAnyItems == 0)&(t.trial_type == 1)] for trials in trial_matrix];
	# hp_percs_looking_at_preferred = [[t.percentageTimeLookingAtPreferred for t in trials if (t.dropped_sample == 0)&(t.didntLookAtAnyItems == 0)&(t.trial_type == 1)] for trials in trial_matrix];
	# hp_times_looking_at_alcohol = [[t.timeLookingAtAlcohol for t in trials if (t.dropped_sample == 0)&(t.didntLookAtAnyItems == 0)&(t.trial_type == 1)] for trials in trial_matrix];
	# hp_percs_looking_at_alcohol = [[t.percentageTimeLookingAtAlcohol for t in trials if (t.dropped_sample == 0)&(t.didntLookAtAnyItems == 0)&(t.trial_type == 1)] for trials in trial_matrix];
	# hp_times_looking_at_cig = [[t.timeLookingAtCigarette for t in trials if (t.dropped_sample == 0)&(t.didntLookAtAnyItems == 0)&(t.trial_type == 1)] for trials in trial_matrix];
	# hp_percs_looking_at_cig = [[t.percentageTimeLookingAtCigarette for t in trials if (t.dropped_sample == 0)&(t.didntLookAtAnyItems == 0)&(t.trial_type == 1)] for trials in trial_matrix];
	# hp_times_looking_at_neutral = [[t.timeLookingAtNeutral for t in trials if (t.dropped_sample == 0)&(t.didntLookAtAnyItems == 0)&(t.trial_type == 1)] for trials in trial_matrix];
	# hp_percs_looking_at_neutral = [[t.percentageTimeLookingAtNeutral for t in trials if (t.dropped_sample == 0)&(t.didntLookAtAnyItems == 0)&(t.trial_type == 1)] for trials in trial_matrix];
	# hp_response_times = [[t.response_time for t in trials if (t.dropped_sample == 0)&(t.didntLookAtAnyItems == 0)&(t.trial_type == 1)] for trials in trial_matrix];
	# index_counter = 0;
	# #now go through and find the means of the times and percentages looking at the items
	# for id,tp,pp,ta,pa,tc,pc,tn,pn,rt in zip(ids, hp_times_looking_at_preferred, hp_percs_looking_at_preferred, hp_times_looking_at_alcohol,
	# 								   hp_percs_looking_at_alcohol, hp_times_looking_at_cig, hp_percs_looking_at_cig,
	# 								   hp_times_looking_at_neutral, hp_percs_looking_at_neutral, hp_response_times):
	# 	hp_individual_preferred_percentages.append(mean(pp)); #append the pecentages of time spejt looking at preferred item
	# 	high_preference_trials_data.loc[index_counter] = [id, mean(tp), mean(pp), mean(ta), mean(pa), mean(tc), mean(pc), mean(tn), mean(pn), mean(rt)];
	# 	index_counter+=1;
	# 	
	# #write the csv file
	# high_preference_trials_data.to_csv(savepath+'individual_subject_high_pref_trials_mean_preference_data.csv',index=False); #got to make sure if this works

###############################################################
## Original formulation fo cue vs not cue temporal gaze profile
###############################################################
	# 	
	# #now run this analysis for the trials where the subject selected the cue item, as defined above, vs the non cued item 		
	# fig = figure(); ax1 = gca();
	# ax1.set_ylim(0.0, 1.0); ax1.set_yticks(arange(0,1.01,0.1)); ax1.set_xlim([0,1000]);
	# ax1.set_ylabel('Likelihood of fixating selected item',size=18); ax1.set_xlabel('Time with respect to decision, ms',size=18,labelpad=11);
	# ax1.set_xticks([0,200,400,600,800,1000]);
	# ax1.set_xticklabels(['-1000','-800','-600','-400','-200','0']);
	# colors = ['red','blue']; alphas = [1.0, 1.0]; legend_lines = [];		count = 0;
	# # Plotting of the nuetral items is stored below under the section 'Plot temporal gaze profile of neutral items'
	# 
	# for cue_or_not, cue_name, c, a in zip([1,0],['cue','not_cue'], colors, alphas):
	# 	#not sure whether the appropriate way to calculate this it to take the nanmean of the means for each subject, or else to
	# 	#treat all subjects equally as one 'subject' and aggregate across all data points. Have to figure this out still
	# 	#for now, using the nanmean of the means across each subject
	# 	gaze_array = zeros(time_duration/time_bin_spacing);
	# 	counts = zeros(shape(gaze_array));	
	# 	subject_means_array = [[] for i in range(1000)]; #use this to store each individual subjects' mean for each time point
	# 	# subject_counts = [[] for i in range(1000)];
	# 	# subject_sums = [[] for i in range(1000)];	
	# 	for subj,cue in zip(trial_matrix, subject_cues):
	# 		individ_subject_sum = zeros(time_duration/time_bin_spacing);
	# 		individ_subject_counts = zeros(time_duration/time_bin_spacing);
	# 		for t in subj:		
	# 			if ((t.dropped_sample == 0)&(t.didntLookAtAnyItems == 0)&((t.trial_type == 1)==1)&((t.preferred_category == cue)==cue_or_not)
	# 				&((t.preferred_category == 'alcohol')|(t.preferred_category == 'cigarette'))):
	# 				#cycle throgh each time point, going backward through the array (e.g., -1, -2..) and aggregating the data accordingly
	# 				for i in (arange(1000)+1):
	# 					if (i>len(t.lookedAtPreferred)):
	# 						continue;
	# 					elif (isnan(t.lookedAtPreferred[-i])):
	# 						continue;
	# 					gaze_array[-i] += t.lookedAtPreferred[-i];
	# 					counts[-i] += 1;
	# 					#put the individual subject data together
	# 					individ_subject_sum[-i] += t.lookedAtPreferred[-i];
	# 					individ_subject_counts[-i] += 1;
	# 
	# 		individ_subject_mean = individ_subject_sum/individ_subject_counts; #calculate the mean for this subject at each time point
	# 		[subject_means_array[index].append(ind_mew) for index,ind_mew in zip(arange(1000),individ_subject_mean)]; #append this to the array for each subject     if(not(isnan(ind_mew)))
	# 		# for index,ind_mew in zip(arange(1000),individ_subject_mean):
	# 		# 	if isnan(ind_mew):
	# 		# 		subject_means_array[index].append(0);
	# 		# 	else:
	# 		# 		subject_means_array[index].append(ind_mew)			
	# 		# [subject_counts[index].append(ct) for index,ct in zip(arange(1000), individ_subject_counts)];
	# 		# [subject_sums[index].append(su) for index,su in zip(arange(1000), individ_subject_sum)];
	# 		#count+=1;
	# 		#if count > 1:
	# 		#	1/0
	# 	#at this point I need to calculate the standard error for each time point
	# 	
	# 	mews = array([nanmean(subj) for subj in subject_means_array]); # gaze_array/counts
	# 	sems = array([compute_BS_SEM(subj) for subj in subject_means_array]);
	# 	ax1.plot(linspace(0,1000,1000), mews, lw = 6.0, color = c, alpha = a);
	# 	#plot the errorbars
	# 	#for x,m,s in zip(linspace(0,1000,1000),mews,sems):
	# 	ax1.fill_between(linspace(0,1000,1000), mews-sems, mews+sems, color = c, alpha = 0.33);
	# 	
	# 	legend_lines.append(mlines.Line2D([],[],color=c,lw=6,alpha = a, label='chose '+cue_name));	
	# 	
	# ax1.spines['right'].set_visible(False); ax1.spines['top'].set_visible(False);
	# ax1.spines['bottom'].set_linewidth(2.0); ax1.spines['left'].set_linewidth(2.0);
	# ax1.yaxis.set_ticks_position('left'); ax1.xaxis.set_ticks_position('bottom');
	# ax1.legend(handles=[legend_lines[0],legend_lines[1]],loc = 'best',ncol=1,fontsize = 14); #, legend_lines[2]
	# title('Average Temporal Gaze Profile, \n Preferred Alcohol/Preferred Cigarette Trials', fontsize = 22);			
	# 	

###############################################################
## Temporal gaze profile code for selecting alcohol vs. cigarette
###############################################################

## Plot temporal gaze profile of neutral items			
	# subject_means_array = [[] for i in range(1000)];
	# #now neutral selected trials
	# for subj,cue in zip(trial_matrix, subject_cues):
	# 	individ_subject_sum = zeros(time_duration/time_bin_spacing);
	# 	individ_subject_counts = zeros(time_duration/time_bin_spacing);
	# 	for t in subj:		
	# 		if ((t.dropped_sample == 0)&(t.didntLookAtAnyItems == 0)&((t.trial_type == 1)==1)&(t.preferred_category == 'neutral')):
	# 			#cycle throgh each time point, going backward through the array (e.g., -1, -2..) and aggregating the data accordingly
	# 			for i in (arange(1000)+1):
	# 				if (i>len(t.lookedAtPreferred)):
	# 					continue;
	# 				elif (isnan(t.lookedAtPreferred[-i])):
	# 					continue;
	# 				# gaze_array[-i] += t.lookedAtPreferred[-i];
	# 				# counts[-i] += 1;
	# 				#put the individual subject data together
	# 				individ_subject_sum[-i] += t.lookedAtPreferred[-i];
	# 				individ_subject_counts[-i] += 1;
	# 
	# 	individ_subject_mean = individ_subject_sum/individ_subject_counts; #calculate the mean for this subject at each time point
	# 	[subject_means_array[index].append(ind_mew) for index,ind_mew in zip(arange(1000),individ_subject_mean)]; #append this to the array for each subject 
	# 
	# mews = array([nanmean(subj) for subj in subject_means_array]); # gaze_array/counts
	# sems = array([compute_BS_SEM(subj) for subj in subject_means_array]);
	# ax1.plot(linspace(0,1000,1000), mews, lw = 6.0, color = 'black', alpha = 1.0);
	# #plot the errorbars
	# #for x,m,s in zip(linspace(0,1000,1000),mews,sems):
	# ax1.fill_between(linspace(0,1000,1000), mews-sems, mews+sems, color = 'gray', alpha = 0.33);
	# legend_lines.append(mlines.Line2D([],[],color='black',lw=6,alpha = a, label='chose neutral'));
	
## Plot temporal gaze profile whether they selected alcohol, cigarettes, or nrutral
## do so for all trials and then for high-preference trials only
	# 
	# fig = figure(); ax1 = gca();
	# ax1.set_ylim(0.0, 1.0); ax1.set_yticks(arange(0,1.01,0.1)); ax1.set_xlim([0,1000]);
	# ax1.set_ylabel('Likelihood of fixating preferred item',size=18); ax1.set_xlabel('Time with respect to decision, ms',size=18,labelpad=15);
	# ax1.set_xticks([0,200,400,600,800,1000]);
	# ax1.set_xticklabels(['-1000','-800','-600','-400','-200','0']);
	# colors = ['red','blue']; legend_lines = [];
	# for high_pref_trial,name,c,lab in zip([0,1],['non_high_pref','high_pref'], colors, ['All Other Trials','PAPC Trials']):
	# 	#define an array the length 1000 ms (for one second before the decision)
	# 	gaze_array = zeros(time_duration/time_bin_spacing);
	# 	counts = zeros(shape(gaze_array));
	# 	#iterate through the trials for each subject, getting the average temporal gaze profile for each subject 
	# 	for subj in trial_matrix:
	# 		#define arrays for this subject
	# 		# subj_gaze_array = zeros(shape(gaze_array));
	# 		# subj_counts = zeros(shape(counts));
	# 		#cycle throuhg each trial for this subject
	# 		for t in subj:
	# 			if ((t.dropped_sample == 0)&(t.didntLookAtAnyItems == 0)&((t.trial_type == 1)==high_pref_trial)):
	# 				#cycle throgh each time point, going backward through the array (e.g., -1, -2..) and aggregating the data accordingly
	# 				for i in (arange(1000)+1):
	# 					if (i>len(t.lookedAtPreferred)):
	# 						continue;
	# 					elif (isnan(t.lookedAtPreferred[-i])):
	# 						continue;
	# 					gaze_array[-i] += t.lookedAtPreferred[-i];
	# 					counts[-i] += 1;
	# 	ax1.plot(linspace(0,1000,1000), gaze_array/counts, lw = 6.0, color = c);
	# 	legend_lines.append(mlines.Line2D([],[],color=c,lw=6, label=lab));
	# ax1.spines['right'].set_visible(False); ax1.spines['top'].set_visible(False);
	# ax1.spines['bottom'].set_linewidth(2.0); ax1.spines['left'].set_linewidth(2.0);
	# ax1.yaxis.set_ticks_position('left'); ax1.xaxis.set_ticks_position('bottom');
	# ax1.legend(handles=[legend_lines[0],legend_lines[1]],loc = 'best',ncol=1,fontsize = 14);
	# title('Average Temporal Gaze Profile, \n Preferred Alcohol/Preferred Ciagerte Trials vs. Not Trials', fontsize = 22);
	# 	
	# 	
	# #now run the temporal gaze analysis for the three types of trials for the high pref trials
	# #plot them all together for this...		
	# fig = figure(); ax1 = gca();
	# ax1.set_ylim(0.0, 1.0); ax1.set_yticks(arange(0,1.01,0.1)); ax1.set_xlim([0,1000]);
	# ax1.set_ylabel('Likelihood of fixating preferred item',size=18); ax1.set_xlabel('Time with respect to decision, ms',size=18,labelpad=15);
	# ax1.set_xticks([0,200,400,600,800,1000]);
	# ax1.set_xticklabels(['-1000','-800','-600','-400','-200','0']);
	# color = 'blue'; alphas = [1.0, 0.67, 0.33]; legend_lines = [];
	# for pref_category,a in zip(['alcohol','cigarette','neutral'],alphas):
	# 	gaze_array = zeros(time_duration/time_bin_spacing);
	# 	counts = zeros(shape(gaze_array));		
	# 	for subj in trial_matrix:		
	# 		for t in subj:
	# 			if ((t.dropped_sample == 0)&(t.didntLookAtAnyItems == 0)&((t.trial_type == 1)==1)&(t.preferred_category == pref_category)):
	# 				#cycle throgh each time point, going backward through the array (e.g., -1, -2..) and aggregating the data accordingly
	# 				for i in (arange(1000)+1):
	# 					if (i>len(t.lookedAtPreferred)):
	# 						continue;
	# 					elif (isnan(t.lookedAtPreferred[-i])):
	# 						continue;
	# 					gaze_array[-i] += t.lookedAtPreferred[-i];
	# 					counts[-i] += 1;
	# 	ax1.plot(linspace(0,1000,1000), gaze_array/counts, lw = 6.0, color = color, alpha = a);
	# 	legend_lines.append(mlines.Line2D([],[],color=color,lw=6,alpha = a, label='chose '+pref_category));
	# ax1.spines['right'].set_visible(False); ax1.spines['top'].set_visible(False);
	# ax1.spines['bottom'].set_linewidth(2.0); ax1.spines['left'].set_linewidth(2.0);
	# ax1.yaxis.set_ticks_position('left'); ax1.xaxis.set_ticks_position('bottom');
	# ax1.legend(handles=[legend_lines[0],legend_lines[1],legend_lines[2]],loc = 'best',ncol=1,fontsize = 14);
	# title('Average Temporal Gaze Profile, \n Preferred Alcohol/Preferred Cigarette Trials', fontsize = 22);

###############################################################
## original computation of proportion of looking time at preferred item data
###############################################################	
	
## Proportion fo looking time computation
	# ##Build a trial by trial instance of each value for each subject for all trials
	# all_data = pd.DataFrame(columns = ['sub_id','trial_type','time_looking_at_pref','percentage_looking_at_pref','time_looking_at_alc','percentage_looking_at_alc',
	# 										 'time_looking_at_cig','percentage_looking_at_cig','time_looking_at_neu','percentage_looking_at_neu', 'response_time',
	# 										 'last_item_looked_at','last_category_looked_at','time_last_item_looked_at','selected_item','selected_category','alcohol_pref','cig_pref']);
	# #store all the trial data for each subject in a master DB
	# index_counter = 0;
	# for trials in trial_matrix:
	# 	for t in trials:
	# 		if (t.dropped_sample == 0)&(t.didntLookAtAnyItems == 0):
	# 			all_data.loc[index_counter] = [t.sub_id, t.trial_type, t.timeLookingAtPreferred, t.percentageTimeLookingAtPreferred,
	# 										   t.timeLookingAtAlcohol, t.percentageTimeLookingAtAlcohol, t.timeLookingAtCigarette,
	# 										   t.percentageTimeLookingAtCigarette, t.timeLookingAtNeutral, t.percentageTimeLookingAtNeutral,
	# 										   t.response_time, t.lastItemLookedAt, t.lastCategoryLookedAt, t.timeLastItemLookedAt,
	# 										   t.preferred_item, t.preferred_category, t.alcohol_pref, t.cigarette_pref];
	# 			index_counter+=1;
	# 
	# #write the csv file
	# all_data.to_csv(savepath+'individual_subject_all_trials_trial_by_trial_data.csv',index=False); 

	# ##Build an average database instance of each value for each subject for high vs low preferred trials and the subsets of high preferred trials
	# 	#store all the trial data for each subject in a master DB
	# hl_index_counter = 0;
	# all_high_index_counter = 0;
	# cv_counter = 0;
	# high_vs_other_pref_data = pd.DataFrame(columns = ['sub_id','trial_type','mean_time_looking_at_pref','mean_percentage_looking_at_pref', 'mean_response_time']);
	# high_pref_only_data = pd.DataFrame(columns = ['sub_id','preferred_pic','mean_time_looking_at_pref','mean_percentage_looking_at_pref', 'mean_response_time']);
	# cue_vs_not_cue_data = pd.DataFrame(columns = ['sub_id','cue_type','mean_time_looking_at_pref','mean_percentage_looking_at_pref', 'mean_response_time']);
	# for high_pref_trial,name in zip([0,1],['non_high_pref','high_pref']):
	# 	time_at_pref = [mean([tee.timeLookingAtPreferred for tee in subj
	# 			   if((tee.dropped_sample == 0)&(tee.didntLookAtAnyItems == 0)&((tee.trial_type == 1)==high_pref_trial))]) for subj in trial_matrix];
	# 	perc_time_at_pref = [mean([tee.percentageTimeLookingAtPreferred for tee in subj
	# 			   if((tee.dropped_sample == 0)&(tee.didntLookAtAnyItems == 0)&((tee.trial_type == 1)==high_pref_trial))]) for subj in trial_matrix];					
	# 	rts = [mean([tee.response_time for tee in subj
	# 			   if((tee.dropped_sample == 0)&(tee.didntLookAtAnyItems == 0)&((tee.trial_type == 1)==high_pref_trial))]) for subj in trial_matrix];
	# 	db['%s_%s_mean_time_at_pref'%(eyed,name)] = nanmean(time_at_pref); db['%s_%s_bs_sems_time_at_pref'%(eyed,name)] = compute_BS_SEM(time_at_pref);
	# 	db['%s_%s_mean_perc_time_at_pref'%(eyed,name)] = nanmean(perc_time_at_pref); db['%s_%s_bs_sems_perc_time_at_pref'%(eyed,name)] = compute_BS_SEM(perc_time_at_pref);
	# 	db['%s_%s_mean_rt'%(eyed,name)] = nanmean(rts); db['%s_%s_bs_sems_rt'%(eyed,name)] = compute_BS_SEM(rts);
	# 	
	# 	for id,tp,pp,rt in zip(ids, time_at_pref, perc_time_at_pref, rts):
	# 		#add the data to a pandas.DataFrame object to write it to a file for use in R to run the stats
	# 		high_vs_other_pref_data.loc[hl_index_counter] = [id,name,nanmean(tp),nanmean(pp),nanmean(rt)];
	# 		hl_index_counter+=1;
	# 		
	# 	#cycle through the different types of high preference trials (where each one could be selected):
	# 	#1. all high-pref trials, 2. all not high pref trials, 3. alcohol high pref trials
	# 	#4. cigarette high pref trials, and 5. neutral high pref trials
	# 	if high_pref_trial==1:
	# 		for pref_category in ['alcohol','cigarette','neutral']:
	# 			time_at_pref = [mean([tee.timeLookingAtPreferred for tee in subj
	# 					   if((tee.dropped_sample == 0)&(tee.didntLookAtAnyItems == 0)&((tee.trial_type == 1)==high_pref_trial))&(tee.preferred_category == pref_category)]) for subj in trial_matrix];
	# 			perc_time_at_pref = [mean([tee.percentageTimeLookingAtPreferred for tee in subj
	# 					   if((tee.dropped_sample == 0)&(tee.didntLookAtAnyItems == 0)&((tee.trial_type == 1)==high_pref_trial))&(tee.preferred_category == pref_category)]) for subj in trial_matrix];					
	# 			rts = [mean([tee.response_time for tee in subj
	# 					   if((tee.dropped_sample == 0)&(tee.didntLookAtAnyItems == 0)&((tee.trial_type == 1)==high_pref_trial))&(tee.preferred_category == pref_category)]) for subj in trial_matrix];					
	# 			db['%s_high_pref_%s_mean_time_at_pref'%(eyed,pref_category)] = nanmean(time_at_pref); db['%s_high_pref_%s_bs_sems_time_at_pref'%(eyed,pref_category)] = compute_BS_SEM(time_at_pref);
	# 			db['%s_high_pref_%s_mean_perc_time_at_pref'%(eyed,pref_category)] = nanmean(perc_time_at_pref); db['%s_high_pref_%s_bs_sems_perc_time_at_pref'%(eyed,pref_category)] = compute_BS_SEM(perc_time_at_pref);
	# 			db['%s_high_pref_%s_mean_rt'%(eyed,pref_category)] = nanmean(rts); db['%s_high_pref_%s_bs_sems_rt'%(eyed, pref_category)] = compute_BS_SEM(rts);
	# 			
	# 			for id,tp,pp,rt in zip(ids, time_at_pref, perc_time_at_pref, rts):
	# 				#add the data to a pandas.DataFrame object to write it to a file for use in R to run the stats
	# 				high_pref_only_data.loc[all_high_index_counter] = [id,pref_category,nanmean(tp),nanmean(pp),nanmean(rt)];
	# 				all_high_index_counter+=1;
	# 		
	# 		#now run this analysis for the trials where the subject selected the cue item, as defined above, vs the non cued item 
	# 				
	# 		for cue_or_not, cue_name in zip([1,0],['cue','not_cue']):
	# 			time_at_pref = [mean([tee.timeLookingAtPreferred for tee in subj
	# 					   if((tee.dropped_sample == 0)&(tee.didntLookAtAnyItems == 0)&((tee.trial_type == 1)==high_pref_trial))&((tee.preferred_category == cue)==cue_or_not)&
	# 					   ((tee.preferred_category == 'alcohol')|(tee.preferred_category == 'cigarette'))]) for subj,cue in zip(trial_matrix,subject_cues)];				
	# 			perc_time_at_pref = [mean([tee.percentageTimeLookingAtPreferred for tee in subj
	# 					   if((tee.dropped_sample == 0)&(tee.didntLookAtAnyItems == 0)&((tee.trial_type == 1)==high_pref_trial))&((tee.preferred_category == cue)==cue_or_not)&
	# 					   ((tee.preferred_category == 'alcohol')|(tee.preferred_category == 'cigarette'))]) for subj,cue in zip(trial_matrix,subject_cues)];				
	# 			rts = [mean([tee.response_time for tee in subj
	# 					   if((tee.dropped_sample == 0)&(tee.didntLookAtAnyItems == 0)&((tee.trial_type == 1)==high_pref_trial))&((tee.preferred_category == cue)==cue_or_not)&
	# 					   ((tee.preferred_category == 'alcohol')|(tee.preferred_category == 'cigarette'))]) for subj,cue in zip(trial_matrix,subject_cues)];
	# 			db['%s_high_pref_selected_%s_mean_time_at_pref'%(eyed,cue_name)] = nanmean(time_at_pref); db['%s_high_pref_selected_%s_bs_sems_time_at_pref'%(eyed,cue_name)] = compute_BS_SEM(time_at_pref);
	# 			db['%s_high_pref_selected_%s_mean_perc_time_at_pref'%(eyed,cue_name)] = nanmean(perc_time_at_pref); db['%s_high_pref_selected_%s_bs_sems_perc_time_at_pref'%(eyed,cue_name)] = compute_BS_SEM(perc_time_at_pref);				
	# 			db['%s_high_pref_selected_%s_mean_rt'%(eyed,cue_name)] = nanmean(rts); db['%s_high_pref_selected_%s_bs_sems_rt'%(eyed, cue_name)] = compute_BS_SEM(rts);
	# 			for id,tp,pp,rt in zip(ids, time_at_pref, perc_time_at_pref, rts):
	# 				#add the data to a pandas.DataFrame object to write it to a file for use in R to run the stats
	# 				cue_vs_not_cue_data.loc[all_high_index_counter] = [id,cue_name,nanmean(tp),nanmean(pp),nanmean(rt)];
	# 				cv_counter+=1;					
	# #write the data to csv files
	# high_vs_other_pref_data.to_csv(savepath+'perc_time_avg_high_vs_nothigh_pref_trial_data.csv',index=False); 
	# high_pref_only_data.to_csv(savepath+'perc_time_avg_high_pref_only_trial_data.csv',index=False);
	# cue_vs_not_cue_data.to_csv(savepath+'perc_time_cue_not_cue_high_pref_trial_data.csv',index=False);	
	
	
	