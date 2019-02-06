#THIS CODE PLOTS AND ANALYZES SACCADE-RELATED KINEMATICS FOR CRET STUDY
#Statistics are calculated in R after exporting the data from here
#Author: James Wilmott, Spring 2019

# ALL ANALYSES ASSUME THERE IS A LIST OF BLOCKS ALREADY CREATED
# TO DO SO, USE THE FUNCTION getAllSubjectBlocks() or equivalent in
# cret_analysis.py


from pylab import *
import shelve #for database writing and reading
from scipy.io import loadmat #used to load .mat files in as dictionaries
from scipy import stats
from glob import glob #for use in searching for/ finding data files
import random #general purpose
import pandas as pd
import math
import matplotlib.lines as mlines
import matplotlib.pyplot as pyplot
import scipy.signal as ssignal
from mpl_toolkits.axes_grid.inset_locator import inset_axes
import time
import re #string parsing, etc
import os.path

############################################
## Specify some universal parameters ##
############################################

# Trial types: 1 = high C, high A; 2 = High C, low A; 3 = low C, high A; 4 = low C, lowA 
# 
# datapath = '/Users/jameswilmott/Documents/MATLAB/data/CRET/'; #
# savepath =  '/Users/jameswilmott/Documents/Python/CRET/data/';  # #/'/Users/james/Documents/Python/CRET/data/';  # 
# shelvepath =  '/Users/jameswilmott/Documents/Python/CRET/data/'; # # #  #'/Users/james/Documents/Python/CRET/data/'; # 
# figurepath = '/Users/jameswilmott/Documents/Python/CRET/figures/'; # #'/Users/james/Documents/Python/CRET/figures/'; #


datapath = '/Volumes/WORK_HD/data/CRET/'; #'/Users/jameswilmott/Documents/MATLAB/data/CRET/'; #
savepath =  '/Volumes/WORK_HD/code/Python/CRET/data/'; #'/Users/jameswilmott/Documents/Python/CRET/data/';  # #/'/Users/james/Documents/Python/CRET/data/';  # 
shelvepath =  '/Volumes/WORK_HD/code/Python/CRET/data/'; #'/Users/jameswilmott/Documents/Python/CRET/data/'; # # #  #'/Users/james/Documents/Python/CRET/data/'; # 
figurepath = '/Volumes/WORK_HD/code/Python/CRET/figures/'; #'/Users/jameswilmott/Documents/Python/CRET/figures/'; # #'/Users/james/Documents/Python/CRET/figures/'; #

#import database (shelve) for saving processed data and a .csv for saving the velocity threshold criterion data
subject_data = shelve.open(shelvepath+'data');
#subject_saccade_criteria = pd.read_csv(savepath+'subject_saccade_criteria_each_trial.csv');
#completed_velocity_ids = unique(subject_saccade_criteria['sub_id']);

ids=['cret03','cret04','cret05','cret06','cret07','cret08','cret09','cret10','cret11', 'cret14','cret15','cret16',
	 'cret17','cret18','cret19','cret21','cret22','cret24','cret25','cret26','cret27','cret28','cret29','cret30',
	 'cret33','cret36','cret37','cret38','cret39']; #   'cret01'   ,'cret13'     ['cret15']; 

subjective_prefs = [('cret03','cigarette'),('cret04','cigarette'),('cret05','cigarette'),('cret06','alcohol'),('cret07','cigarette'),('cret08','cigarette'),
	('cret09','cigarette'),('cret11','cigarette'),('cret14','cigarette'),('cret15','cigarette'),('cret16','cigarette'),
	 ('cret17','cigarette'),('cret18','cigarette'),('cret19','cigarette'),('cret20','cigarette'),('cret21','cigarette'),
	 ('cret22','cigarette'),('cret23','cigarette'),('cret24','cigarette'),('cret25','cigarette'),('cret26','cigarette'),
	 ('cret27','alcohol'),('cret28','cigarette'),('cret29','cigarette'),('cret30','cigarette'),('cret31','alcohol'),
	 ('cret32','alcohol'),('cret33','cigarette'),('cret34','alcohol'),('cret35','cigarette'),('cret36','alcohol'),('cret37','alcohol')]; #14 ids ('cret13','cigarette'),

display_size = array([22.80, 17.10]); #width, height of the screen used to present the images in degrees of visual angle

image_size = array([6,6]); #width, and height of the presented images in degress of visual angle

left_pic_coors = array([-5.20,-3.0]); #in dva
right_pic_coors = array([5.20,-3]);
up_pic_coors = array([0,6]);

distance_threshold = 4.0; #threshold for how far away eye position can be from the coordinates to be considered looking at that item

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
############################################
## Data Analysis Methods ##
############################################
############################################

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
## Trial Exclusion Information ##
############################################

def calculateExcludedTrialInformation(block_matrix):
# This function determines how many trials are excluded
# according to the following criteria:
# 1. Blinks/looking down at the keyboard
# 2. Didn't move their eyes
# 3. Eyes were not focused within 2.5 degrees of visual angle at trial start

# 1. Calculate the percentage and raw number of trials excluded for a dropped sample
# I will do this for each trial type and aggregated

#aggregated
	# Pre-allocate data structure holders
	nr_trials_excluded = [[0] for su in block_matrix];
	total_nr_trials = [[0] for su in block_matrix];

	#loop through each trial and score whether trial was excluded because of a dropped sample
	for subj_nr, blocks in enumerate(block_matrix):
		for b in blocks:
			for t in b.trials:
				total_nr_trials[subj_nr][0] += 1;
				if t.dropped_sample == 1:
					nr_trials_excluded[subj_nr][0] += 1;

	# Calculate percentages
	perc_trials_excluded = array([float(nr[0])/tot[0] if tot>0 else 0 for nr,tot in zip(nr_trials_excluded, total_nr_trials)]);
	
	mew_raw = mean(array(nr_trials_excluded));
	raw_sem = compute_BS_SEM(array(nr_trials_excluded));
	mew_perc = mean(perc_trials_excluded);
	perc_sem = compute_BS_SEM(perc_trials_excluded);
	
	print('\n\n DROPPED SAMPLE (BLINKS OR LOOKED DOWN AT THE KEYBOARD) EXCLUSION INFORMATION \n\n\n')
	print('\n Average nr of trials excluded for %s subjects: %4.1f \n'%(len(block_matrix),mew_raw));
	print('\n Between-subjects standard error of the mean: %4.1f \n\n'%(raw_sem));
	print('\n Average percentage of trials excluded for %s subjects: %4.3f \n'%(len(block_matrix),mew_perc));
	print('\n Between-subjects standard error of the mean: %4.3f \n\n\n'%(perc_sem));

#broken down by trial type
	for name,ttype in zip(['high_pref', 'highC_lowA','lowC_highA','lowC_lowA'],[1,2,3,4]):
		nr_trials_excluded_tt = [[0] for su in block_matrix];
		total_nr_trials_tt = [[0] for su in block_matrix];
	
		#loop through each trial and score whether trial was excluded because of a dropped sample
		for subj_nr, blocks in enumerate(block_matrix):
			for b in blocks:
				for t in b.trials:
					if t.trial_type==ttype:
						total_nr_trials_tt[subj_nr][0] += 1;
						if t.dropped_sample == 1:
							nr_trials_excluded_tt[subj_nr][0] += 1;
	
		# Calculate percentages		
		perc_trials_excluded_tt = [float(nr[0])/tot[0] if (tot[0]>0) else 0 for nr,tot in zip(nr_trials_excluded_tt, total_nr_trials_tt)];

		# if ttype==4:	
		# 	1/0
		mew_raw = mean(array(nr_trials_excluded_tt));
		raw_sem = compute_BS_SEM(array(nr_trials_excluded_tt));
		mew_perc = mean(perc_trials_excluded_tt);
		perc_sem = compute_BS_SEM(perc_trials_excluded_tt);
		
		print('\n\n TRIAL TYPE %s \n\n'%name)
		print('\n Average nr of trials excluded for %s subjects: %4.1f \n'%(len(block_matrix),mew_raw));
		print('\n Between-subjects standard error of the mean: %4.1f \n\n'%(raw_sem));
		print('\n Average percentage of trials excluded for %s subjects: %4.3f \n'%(len(block_matrix),mew_perc));
		print('\n Between-subjects standard error of the mean: %4.3f \n\n\n\n'%(perc_sem));


# 2. Calculate percentage and raw number of trials excluded for not looking at anything

# I will do this for each trial type and aggregated

# Pre-allocate data structure holders
	nr_trials_excluded = [[0] for su in block_matrix];
	total_nr_trials = [[0] for su in block_matrix];

#loop through each trial and score whether trial was excluded because of a dropped sample
	for subj_nr, blocks in enumerate(block_matrix):
		for b in blocks:
			for t in b.trials:
				total_nr_trials[subj_nr][0] += 1;
				if (t.dropped_sample==0) & (t.didntLookAtAnyItems == 1):  #hold the dropped samples to zero to make sure I am getting the marginal values here
					nr_trials_excluded[subj_nr][0] += 1;

# Calculate percentages
	perc_trials_excluded = [float(nr[0])/tot[0] for nr,tot in zip(nr_trials_excluded, total_nr_trials)];
	
	mew_raw = mean(array(nr_trials_excluded));
	raw_sem = compute_BS_SEM(array(nr_trials_excluded));
	mew_perc = mean(perc_trials_excluded);
	perc_sem = compute_BS_SEM(perc_trials_excluded);
	
	print('\n\n DIDNT LOOK AT ANY ITEMS EXCLUSION INFORMATION \n\n\n')
	print('\n Average nr of trials excluded for %s subjects: %4.1f \n'%(len(block_matrix),mew_raw));
	print('\n Between-subjects standard error of the mean: %4.1f \n\n'%(raw_sem));
	print('\n Average percentage of trials excluded for %s subjects: %4.3f \n'%(len(block_matrix),mew_perc));
	print('\n Between-subjects standard error of the mean: %4.3f \n\n\n'%(perc_sem));

#broken down by trial type
	for name,ttype in zip(['high_pref', 'highC_lowA','lowC_highA','lowC_lowA'],[1,2,3,4]):
		nr_trials_excluded_tt = [[0] for su in block_matrix];
		total_nr_trials_tt = [[0] for su in block_matrix];
	
		#loop through each trial and score whether trial was excluded because of a dropped sample
		for subj_nr, blocks in enumerate(block_matrix):
			for b in blocks:
				for t in b.trials:
					if t.trial_type==ttype:
						total_nr_trials_tt[subj_nr][0] += 1;
						if (t.dropped_sample==0) & (t.didntLookAtAnyItems == 1):
							nr_trials_excluded_tt[subj_nr][0] += 1;
	
		# Calculate percentages		
		perc_trials_excluded_tt = [float(nr[0])/tot[0] if (tot[0]>0) else 0 for nr,tot in zip(nr_trials_excluded_tt, total_nr_trials_tt)];

		# if ttype==4:	
		# 	1/0

		mew_raw = mean(array(nr_trials_excluded_tt));
		raw_sem = compute_BS_SEM(array(nr_trials_excluded_tt));
		mew_perc = mean(perc_trials_excluded_tt);
		perc_sem = compute_BS_SEM(perc_trials_excluded_tt);
		
		print('\n\n TRIAL TYPE %s \n\n'%name)
		print('\n Average nr of trials excluded for %s subjects: %4.1f \n'%(len(block_matrix),mew_raw));
		print('\n Between-subjects standard error of the mean: %4.1f \n\n'%(raw_sem));
		print('\n Average percentage of trials excluded for %s subjects: %4.3f \n'%(len(block_matrix),mew_perc));
		print('\n Between-subjects standard error of the mean: %4.3f \n\n\n\n'%(perc_sem));

#3. Calculate the nr of trials where eyes were not focused within 2.5 degrees of visual angle at trial start
# Pre-allocate data structure holders
	nr_trials_excluded = [[0] for su in block_matrix];
	total_nr_trials = [[0] for su in block_matrix];

#loop through each trial and score whether trial was excluded because of a dropped sample
	for subj_nr, blocks in enumerate(block_matrix):
		for b in blocks:
			for t in b.trials:
				total_nr_trials[subj_nr][0] += 1;
				if (t.dropped_sample==0) & (t.didntLookAtAnyItems == 0) & (sqrt(t.eyeX[0]**2 + t.eyeY[0]**2) > 2.5):  #hold the dropped samples to zero to make sure I am getting the marginal values here
					nr_trials_excluded[subj_nr][0] += 1;

# Calculate percentages
	perc_trials_excluded = [float(nr[0])/tot[0] for nr,tot in zip(nr_trials_excluded, total_nr_trials)];
	
	mew_raw = mean(array(nr_trials_excluded));
	raw_sem = compute_BS_SEM(array(nr_trials_excluded));
	mew_perc = mean(perc_trials_excluded);
	perc_sem = compute_BS_SEM(perc_trials_excluded);
	
	print('\n\n INITIAL FIXATION NOT AT CENTER OF DISPLAY EXCLUSION INFORMATION \n\n\n')
	print('\n Average nr of trials excluded for %s subjects: %4.1f \n'%(len(block_matrix),mew_raw));
	print('\n Between-subjects standard error of the mean: %4.1f \n\n'%(raw_sem));
	print('\n Average percentage of trials excluded for %s subjects: %4.3f \n'%(len(block_matrix),mew_perc));
	print('\n Between-subjects standard error of the mean: %4.3f \n\n\n'%(perc_sem));
	
#broken down by trial type
	for name,ttype in zip(['high_pref', 'highC_lowA','lowC_highA','lowC_lowA'],[1,2,3,4]):
		nr_trials_excluded_tt = [[0] for su in block_matrix];
		total_nr_trials_tt = [[0] for su in block_matrix];
	
		#loop through each trial and score whether trial was excluded because of a dropped sample
		for subj_nr, blocks in enumerate(block_matrix):
			for b in blocks:
				for t in b.trials:
					if t.trial_type==ttype:
						total_nr_trials_tt[subj_nr][0] += 1;
						if (t.dropped_sample==0) & (t.didntLookAtAnyItems == 0) & (sqrt(t.eyeX[0]**2 + t.eyeY[0]**2) > 2.5):
							nr_trials_excluded_tt[subj_nr][0] += 1;
	
		# Calculate percentages		
		perc_trials_excluded_tt = [float(nr[0])/tot[0] if (tot[0]>0) else 0 for nr,tot in zip(nr_trials_excluded_tt, total_nr_trials_tt)];

		# if ttype==4:	
		# 	1/0

		mew_raw = mean(array(nr_trials_excluded_tt));
		raw_sem = compute_BS_SEM(array(nr_trials_excluded_tt));
		mew_perc = mean(perc_trials_excluded_tt);
		perc_sem = compute_BS_SEM(perc_trials_excluded_tt);
		
		print('\n\n TRIAL TYPE %s \n\n'%name)
		print('\n Average nr of trials excluded for %s subjects: %4.1f \n'%(len(block_matrix),mew_raw));
		print('\n Between-subjects standard error of the mean: %4.1f \n\n'%(raw_sem));
		print('\n Average percentage of trials excluded for %s subjects: %4.3f \n'%(len(block_matrix),mew_perc));
		print('\n Between-subjects standard error of the mean: %4.3f \n\n\n\n'%(perc_sem));


############################################
## Saccade Kinematic Data ##
############################################

# Determine the saccdic latency for first and all saccades:
# 1. Distribution of onsets latencies
# 2. Average onset latencies

def computeFirstSaccadeKinetmatics(block_matrix):

# Start with computing saccadic onset latencies for first saccades only
	# Pre-allocate data structure holders
	onset_latencies = [[] for su in block_matrix];
	amplitudes = [[] for su in block_matrix];

	#loop through each trial and score whether trial was excluded because of a dropped sample
	for subj_nr, blocks in enumerate(block_matrix):
		for b in blocks:
			for t in b.trials:
				if ((t.dropped_sample == 0)&(t.didntLookAtAnyItems == 0)&
					(t.skip == 0)&(sqrt(t.eyeX[0]**2 + t.eyeY[0]**2) < 2.5)):      #&(t.trial_type==ttype)
					
					if (t.nr_saccades > 0):  #this conditional is used to ensure that no trials without saccades sneak through
						
						sac_start_time = 0;
						sac_start_pos = array([]);						
						sac_end_time = 0;
						sac_end_pos = array([]);
						
						#Below here goes through each trial and pulls out the first saccde
						# the while loop below runs through until a saccade is found (saccade_counter = 1) or
						# we get to the end of the trial
						
						saccade_counter = 0;
						while saccade_counter==0:
							for ii,xx,yy,issac in zip(range(len(t.sample_times)),
																 t.eyeX, t.eyeY, t.isSaccade):
								#if no saccade has been made yet, keep running through the isSaccade array
								# issac < 1 will be zero at all non-saccading time points, including the start
								if issac == 0:
									#if the previous sample was saccading and now it isn't, the first saccade is complete and we can grab the data
									if (t.isSaccade[ii-1]==True)&(ii>0):
										sac_end_time = t.sample_times[ii];
										sac_end_pos = array([xx,yy]);
										saccade_counter+=1;
									
									#if there is no saccade, this will trigger the stop I need to move out of the infinite loop	
									if (ii == range(len(t.sample_times))[-1]):
										saccade_counter = 100;
										
								elif issac == 1:
									#get the starting point for this saccade as well as the time
									#the first transition between 0 and 1 will be the first saccade start
									if (t.isSaccade[ii-1]==False)&(ii>0)&(saccade_counter==0):
										sac_start_time = t.sample_times[ii];
										sac_start_pos = array([xx,yy]);
						
						#calculate the latency and amplitude, then save to the subject's array
						onset_latencies[subj_nr].append(sac_start_time);
						amplitudes[subj_nr].append(sqrt((sac_start_pos[0] - sac_end_pos[0])**2+(sac_start_pos[1] - sac_end_pos[1])**2));
											
	#now calculate population stats for latency and amplitude, and plot
	all_lats = [l for lat in onset_latencies for l in lat];
	all_amps = [a for am in amplitudes for a in am];
	mew_latencies = array([mean(lat) for lat in onset_latencies]);
	latencies_sems = compute_BS_SEM(mew_latencies);
	mew_amps = array([mean(lat) for lat in amplitudes]);
	amps_sems = compute_BS_SEM(mew_amps);


	#plot the distribution of saccadid latencies across all participants
	
	fig = figure(figsize = (12.8,7.64)); ax1=gca(); #grid(True);
	#ax1.set_ylim(0, 0.8); ax1.set_yticks(arange(0, 0.81, 0.1)); #ax1.set_xlim([0.5,1.7]); ax1.set_xticks([0.85, 1.15, 1.45]);
	ax1.set_ylabel('Frequency',size=18); ax1.set_xlabel('Onset latency',size=18,labelpad=15);
	ax1.hist(all_lats);

	ax1.spines['right'].set_visible(False); ax1.spines['top'].set_visible(False);
	ax1.spines['bottom'].set_linewidth(2.0); ax1.spines['left'].set_linewidth(2.0);
	ax1.yaxis.set_ticks_position('left'); ax1.xaxis.set_ticks_position('bottom');
	title('Population average saccadic latencies for first saccades', fontsize = 22);
	
	#add text detailing the mean saccadic latency
	fig.text(0.7, 0.48, 'MEAN LATENCY:\n %s +- %s ms '%(round(mean(mew_latencies)),round(latencies_sems)),size=16,weight='bold');

	#save the figure
	savefig(figurepath+ 'SaccadeKinematics/' + 'FIRST_SACCADE_ONSET_DISTRIBUTION_ALLSUBJECTS.png');	



	#now plot distribution of amplitudes
	
	fig = figure(figsize = (12.8,7.64)); ax=gca(); #grid(True);
	#ax1.set_ylim(0, 0.8); ax1.set_yticks(arange(0, 0.81, 0.1)); #ax1.set_xlim([0.5,1.7]); ax1.set_xticks([0.85, 1.15, 1.45]);
	ax.set_ylabel('Frequency',size=18); ax.set_xlabel('Saccade amplitude',size=18,labelpad=15);
	ax.hist(all_amps, color = 'darkgray');

	ax.spines['right'].set_visible(False); ax.spines['top'].set_visible(False);
	ax.spines['bottom'].set_linewidth(2.0); ax.spines['left'].set_linewidth(2.0);
	ax.yaxis.set_ticks_position('left'); ax.xaxis.set_ticks_position('bottom');
	title('Population average saccadic amplitudes for first saccades', fontsize = 22);
	
	#add text detailing the mean saccadic latency
	fig.text(0.75, 0.48, 'MEAN AMPLITUDE:\n %s +- %s degrees '%(round(mean(mew_amps)),round(amps_sems)),size=16,weight='bold');

	#save the figure
	savefig(figurepath+ 'SaccadeKinematics/' + 'FIRST_SACCADE_AMPLITUDE_DISTRIBUTION_ALLSUBJECTS.png');	

	
def computeAllSaccadeKinetmatics(block_matrix):

# Start with computing saccadic onset latencies for first saccades only
	# Pre-allocate data structure holders
	onset_latencies = [[] for su in block_matrix];
	amplitudes = [[] for su in block_matrix];

	#loop through each trial and score whether trial was excluded because of a dropped sample
	for subj_nr, blocks in enumerate(block_matrix):
		for b in blocks:
			for t in b.trials:
				if ((t.dropped_sample == 0)&(t.didntLookAtAnyItems == 0)&
					(t.skip == 0)&(sqrt(t.eyeX[0]**2 + t.eyeY[0]**2) < 2.5)):      #&(t.trial_type==ttype)
					
					if (t.nr_saccades > 0):  #this conditional is used to ensure that no trials without saccades sneak through
						
						sac_start_time = 0;
						sac_start_pos = array([]);						
						sac_end_time = 0;
						sac_end_pos = array([]);
						
						#Below here goes through each trial and pulls out the first saccde
						# the while loop below runs through until a saccade is found (saccade_counter = 1) or
						# we get to the end of the trial
						
						saccade_counter = 0;
						for ii,xx,yy,issac in zip(range(len(t.sample_times)),
															 t.eyeX, t.eyeY, t.isSaccade):
							#if no saccade has been made yet, keep running through the isSaccade array
							# issac < 1 will be zero at all non-saccading time points, including the start
							if issac == 0:
								#if the previous sample was saccading and now it isn't, the first saccade is complete and we can grab the data
								if (t.isSaccade[ii-1]==True)&(ii>0):
									sac_end_time = t.sample_times[ii];
									sac_end_pos = array([xx,yy]);
									amplitudes[subj_nr].append(sqrt((sac_start_pos[0] - sac_end_pos[0])**2+(sac_start_pos[1] - sac_end_pos[1])**2));
									sac_lat_start_calculation = sac_end_time; #set this variable as the first onset latency
									saccade_counter+=1;
								
								#if there is no saccade, this will trigger the stop I need to move out of the infinite loop	
								if (ii == range(len(t.sample_times))[-1]):
									saccade_counter = 100;
									
							elif issac == 1:
								#get the starting point for this saccade as well as the time
								#the first transition between 0 and 1 will be the first saccade start
								if (t.isSaccade[ii-1]==False)&(ii>0)&(saccade_counter==0):
									sac_start_time = t.sample_times[ii];
									sac_start_pos = array([xx,yy]);
									onset_latencies[subj_nr].append(sac_start_time);
									
								elif (t.isSaccade[ii-1]==False)&(ii>0):
									sac_start_time = t.sample_times[ii];
									sac_start_pos = array([xx,yy]);
									onset_latencies[subj_nr].append(sac_start_time-sac_lat_start_calculation);
											
	#now calculate population stats for latency and amplitude, and plot
	all_lats = [l for lat in onset_latencies for l in lat];
	all_amps = [a for am in amplitudes for a in am];
	mew_latencies = array([mean(lat) for lat in onset_latencies]);
	latencies_sems = compute_BS_SEM(mew_latencies);
	mew_amps = array([mean(lat) for lat in amplitudes]);
	amps_sems = compute_BS_SEM(mew_amps);

	1/0;


	
	
	

############################################
## Saccadic Endpoint Heat Map ##
############################################

def createFirstSaccadeEndpointMap(block_matrix, ttype):
# This function creates fixation frequency maps according to
# the procedure detailed in Henderson & Hayes (2017) Nature Human Behavior:
# Each location is standardized so that alcohol is the bottom left,
# cigarette us in top center location, and neutral is bottom left
# For each x,y coordinate for each stimulus array, denote a +1 if a saccade endpoint
# occurred at that location.
# Note, this is currently designed to only include trials where the
# participant fixated within 2.5 dva of the center of the screen at
# the start of the trial (timepoint = 0)

#0. Get the trial type to compute a saccade endpoint map for

	name = ['high_pref', 'highC_lowA','lowC_highA','lowC_lowA'][ttype-1];
	
	start_time = time.time(); #start recording how long this takes

#1. Create data holders for the analyses

	#first, get the individual eye traces for each item for each trial where the selected_item was chosen
	# store each item's eye traces (adding a +1 for the trace being in that location at any time point in the trial) by creating little windows
	# e.g., a 4-degree by 4-degree square around each picture
	#compare against reference X,Y coordinates and place the values into each matrrix accordingly
	#aggregate this for each participant into a combined map
		
	#these are holder arrays for each participant, for each item.
	# Each list holds a 40 by 40 matrix that will hold the aggregated 1's associated with an eye trace at that location according to it's distance wrt the reference array
	# this gives me 0.5 degree resolution for the 20 dva by 20 dva square I am creating
	subj_arrays = [zeros((40,40)) for su in block_matrix];
	trial_counters = [[0] for su in block_matrix]; #to count how many trial are counted for this participant
	
	#these are arrays for the aggregated data
	agg_array = zeros((40,40));
	
	#get reference arrays for the display. these are used to create a meshgrid for determinging where to place a 1
	#NOTE: I am using a square for this matrix to make sure the placement of saccade endpoints is not stretched in one postion
	# due to differences in size between the vertical and horizontal size of the display: display_size = array([22.80, 17.10]); 
	
	xx_vec = linspace(-10,10,40);
	yy_vec = linspace(10,-10,40); #NOTE the flipped signs for y axis: positive to negative. Otherwise, this wouldn't correspond to the positive y values on the top of screen
	
#2. Iterate through for each subject and get the ending positions of each first saccade, storing appropriately, then create individual maps	

	for subj_nr, blocks in enumerate(block_matrix):
		for b in blocks:
			for i in arange(0,len(b.trials)):
				
				if ((b.trials[i].dropped_sample == 0)&(b.trials[i].didntLookAtAnyItems == 0)&
					(b.trials[i].skip == 0)&(sqrt(b.trials[i].eyeX[0]**2 + b.trials[i].eyeY[0]**2) < 2.5)&(b.trials[i].trial_type==ttype)):
					
					if (b.trials[i].nr_saccades > 0):  #this conditional is used to ensure that no trials without saccades sneak through

						trial_counters[subj_nr][0] +=1; 
						#Below here goes through each trial and pulls out the ending point of the first saccde
						# the while loop below runs through until a saccade is found (saccade_counter = 1) or
						# we get to the end of the trial
						
						saccade_counter = 0;
						while saccade_counter==0:
							for ii,xx,yy,issac in zip(range(len(b.trials[i].sample_times)),
																 b.trials[i].eyeX, b.trials[i].eyeY, b.trials[i].isSaccade):
								#if no saccade has been made yet, keep running through the isSaccade array
								# issac < 1 will be zero at all non-saccading time points, including the start
								if issac == 0:
									#if the previous sample was saccading and now it isn't, the first saccade is complete and we can grab the ending position
									if (b.trials[i].isSaccade[ii-1]==True)&(ii>0):
										first_sac_end = array([xx,yy]);
										saccade_counter+=1;
									
									#if there is no saccade, this will trigger the stop I need to move out of the infinite loop	
									if (ii == range(len(b.trials[i].sample_times))[-1]):
										saccade_counter = 100;
		
						#at this point, I have the ending x,y position for the first saccade from trial N.
						# Now, need to incorporate it into the corresponding position holder matrices.
		
						#after this, add a 1 to the appropriate location in this subjects' aggregated alcohol 'map'
						# note that this computation is stored here in the outer For loop (rather than indented more)
						# because I am only grabbing the first saccade endpoint. Further computations with all saccades
						# will need to do this inside the for loop (while loop as well)
						
						#now check where in the spatial array is the closest distane to the X,Y position of this data point
						#this will be the minimum of the distance between each xx point and yy point
						x_x, y_y = meshgrid(xx_vec, yy_vec);
						minimum = 10000; coors = array([nan,nan]); #this pre-allocates a very large minimum and an array to hold the indices for the spatial position array
						#loop through and keep checking against each x,y pair
						for ex,why in zip(flatten(x_x),flatten(y_y)):
							comparison = sqrt((first_sac_end[0]-ex)**2 + (first_sac_end[1]-why)**2);
							if comparison < minimum:
								minimum = comparison;
								coors[0] = ex; coors[1] = why;
						
						#here, add a 1 to the ending point of each first saccade
						x_loc = where(coors[0]==xx_vec)[0][0]; #x coordinate
						y_loc = where(coors[1]==yy_vec)[0][0]; #y coordinate
						subj_arrays[subj_nr][y_loc, x_loc] += 1; #add the 1 to the location in the corresponding map.
						# NOTE the yloc, xloc coordinate system for indexing with this array. This must be done to get x-Loc to correspond to horizontal axis
						#below, I will aggregate all individual subject's heat maps together in the agg array

			end_time = time.time();
			print '\n Aggregated total time = %4.2f minutes, completed subject %s block nr %s '%((end_time-start_time)/60.0,subj_nr, b.block_nr)  # trial nr %sb.trials[i].trial_nr)

			#save each subject's first saccade endpoint heat maps
			if b.block_nr==len(blocks):
				#save the 'raw' heat maps
				figure(); imshow(subj_arrays[subj_nr], cmap='hot'); title('%s_FIRST_SACCADE_heatmap_subj_%s'%(name, subj_nr));
				savefig(figurepath+'heatmaps/SACCADE_HEATMAPS/'+'%s_FIRSTSACCADE_heatmap_subj_%s.png'%(name, subj_nr));
				
# 3. Aggregate across subjects by finding the average fixation accumulation		
			
	for su in zip(subj_arrays):
		agg_array += su[0]; #add each subjects' heat maps together	
	agg_array = agg_array/len(block_matrix); #to get the average
	
	#create and save the figure
	figure(); imshow(agg_array, cmap='hot'); title('%s_FIRST_SACCADE_heatmap_subj_%s'%(name,'ALLSUBJECTS'));
	savefig(figurepath+'heatmaps/SACCADE_HEATMAPS/'+'%s_FIRST_SACCADES_heatmap_subj_%s.png'%(name,'ALLSUBJECTS'));
	
	
def createFirstSaccadeEndpointMapAllTrialTypesTogether(block_matrix):
# This function does the same as above, but does so by collapsing across trial types

	start_time = time.time(); #start recording how long this takes

#0. Create data holders for the analyses

	#first, get the individual eye traces for each item for each trial where the selected_item was chosen
	# store each item's eye traces (adding a +1 for the trace being in that location at any time point in the trial) by creating little windows
	# e.g., a 4-degree by 4-degree square around each picture
	#compare against reference X,Y coordinates and place the values into each matrrix accordingly
	#aggregate this for each participant into a combined map
		
	#these are holder arrays for each participant, for each item.
	# Each list holds a 40 by 40 matrix that will hold the aggregated 1's associated with an eye trace at that location according to it's distance wrt the reference array
	# this gives me 0.5 degree resolution for the 20 dva by 20 dva square I am creating
	subj_arrays = [zeros((40,40)) for su in block_matrix];
	trial_counters = [[0] for su in block_matrix]; #to count how many trial are counted for this participant
	
	#these are arrays for the aggregated data
	agg_array = zeros((40,40));
	
	#get reference arrays for the display. these are used to create a meshgrid for determinging where to place a 1
	#NOTE: I am using a square for this matrix to make sure the placement of saccade endpoints is not stretched in one postion
	# due to differences in size between the vertical and horizontal size of the display: display_size = array([22.80, 17.10]); 
	
	xx_vec = linspace(-10,10,40);
	yy_vec = linspace(10,-10,40); #NOTE the flipped signs for y axis: positive to negative. Otherwise, this wouldn't correspond to the positive y values on the top of screen
	
#2. Iterate through for each subject and get the ending positions of each first saccade, storing appropriately, then create individual maps	

	for subj_nr, blocks in enumerate(block_matrix):
		for b in blocks:
			for i in arange(0,len(b.trials)):
				
				if ((b.trials[i].dropped_sample == 0)&(b.trials[i].didntLookAtAnyItems == 0)&
					(b.trials[i].skip == 0)&(sqrt(b.trials[i].eyeX[0]**2 + b.trials[i].eyeY[0]**2) < 2.5)):
					
					if (b.trials[i].nr_saccades > 0): #this conditional is used to ensure that no trials without saccades sneak through

						trial_counters[subj_nr][0] +=1; 
						#Below here goes through each trial and pulls out the ending point of the first saccde
						# the while loop below runs through until a saccade is found (saccade_counter = 1) or
						# we get to the end of the trial
						
						saccade_counter = 0;
						while saccade_counter==0:
							for ii,xx,yy,issac in zip(range(len(b.trials[i].sample_times)),
																 b.trials[i].eyeX, b.trials[i].eyeY, b.trials[i].isSaccade):
								#if no saccade has been made yet, keep running through the isSaccade array
								# issac < 1 will be zero at all non-saccading time points, including the start
								if issac == 0:
									#if the previous sample was saccading and now it isn't, the first saccade is complete and we can grab the ending position
									if (b.trials[i].isSaccade[ii-1]==True)&(ii>0):
										first_sac_end = array([xx,yy]);
										saccade_counter+=1;
									
									#if there is no saccade, this will trigger the stop I need to move out of the infinite loop	
									if (ii == range(len(b.trials[i].sample_times))[-1]):
										saccade_counter = 100;
		
						#at this point, I have the ending x,y position for the first saccade from trial N.
						# Now, need to incorporate it into the corresponding position holder matrices.
		
						#after this, add a 1 to the appropriate location in this subjects' aggregated alcohol 'map'
						# note that this computation is stored here in the outer For loop (rather than indented more)
						# because I am only grabbing the first saccade endpoint. Further computations with all saccades
						# will need to do this inside the for loop (while loop as well)
						
						#now check where in the spatial array is the closest distane to the X,Y position of this data point
						#this will be the minimum of the distance between each xx point and yy point
						x_x, y_y = meshgrid(xx_vec, yy_vec);
						minimum = 10000; coors = array([nan,nan]); #this pre-allocates a very large minimum and an array to hold the indices for the spatial position array
						#loop through and keep checking against each x,y pair
						for ex,why in zip(flatten(x_x),flatten(y_y)):
							comparison = sqrt((first_sac_end[0]-ex)**2 + (first_sac_end[1]-why)**2);
							if comparison < minimum:
								minimum = comparison;
								coors[0] = ex; coors[1] = why;
						
						#here, add a 1 to the ending point of each first saccade
						x_loc = where(coors[0]==xx_vec)[0][0]; #x coordinate
						y_loc = where(coors[1]==yy_vec)[0][0]; #y coordinate
						subj_arrays[subj_nr][y_loc, x_loc] += 1; #add the 1 to the location in the corresponding map.
						# NOTE the yloc, xloc coordinate system for indexing with this array. This must be done to get x-Loc to correspond to horizontal axis
						#below, I will aggregate all individual subject's heat maps together in the agg array

			end_time = time.time();
			print '\n Aggregated total time = %4.2f minutes, completed subject %s block nr %s '%((end_time-start_time)/60.0,subj_nr, b.block_nr)  # trial nr %sb.trials[i].trial_nr)

			#save each subject's first saccade endpoint heat maps
			if b.block_nr==len(blocks):
				#save the 'raw' heat maps
				figure(); imshow(subj_arrays[subj_nr], cmap='hot'); title('ALLTRIALTYPES_FIRST_SACCADE_heatmap_subj_%s'%(subj_nr));
				savefig(figurepath+'heatmaps/SACCADE_HEATMAPS/'+'ALLTRIALTYPES_FIRSTSACCADE_heatmap_subj_%s.png'%(subj_nr));				
			
				
# 3. Aggregate across subjects by finding the average fixation accumulation		
			
	for su in zip(subj_arrays):
		agg_array += su[0]; #add each subjects' heat maps together	
	agg_array = agg_array/len(block_matrix); #to get the average
	
	#create and save the figure
	figure(); imshow(agg_array, cmap='hot'); title('ALLTRIALTYPES_FIRST_SACCADE_heatmap_subj_%s'%('ALLSUBJECTS'));
	savefig(figurepath+'heatmaps/SACCADE_HEATMAPS/'+'ALLTRIALTYPES_FIRSTSACCADE_heatmap_subj_%s.png'%('ALLSUBJECTS'));
	


def createAllSaccadeEndpointMap(block_matrix, ttype):
# Same as above, but for all saccadic endpoints
# This function splits saccadic endpoints according to trial type

#0. Get the trial type to compute a saccade endpoint map for

	name = ['high_pref', 'highC_lowA','lowC_highA','lowC_lowA'][ttype-1];
	
	start_time = time.time(); #start recording how long this takes

#1. Create data holders for the analyses

	#first, get the individual eye traces for each item for each trial where the selected_item was chosen
	# store each item's eye traces (adding a +1 for the trace being in that location at any time point in the trial) by creating little windows
	# e.g., a 4-degree by 4-degree square around each picture
	#compare against reference X,Y coordinates and place the values into each matrrix accordingly
	#aggregate this for each participant into a combined map
		
	#these are holder arrays for each participant, for each item.
	# Each list holds a 40 by 40 matrix that will hold the aggregated 1's associated with an eye trace at that location according to it's distance wrt the reference array
	# this gives me 0.5 degree resolution for the 20 dva by 20 dva square I am creating
	subj_arrays = [zeros((40,40)) for su in block_matrix];
	trial_counters = [[0] for su in block_matrix]; #to count how many trial are counted for this participant
	saccade_counters = [[0] for su in block_matrix]; #to count how many saccades are counted for this participant
	
	#these are arrays for the aggregated data
	agg_array = zeros((40,40));
	
	#get reference arrays for the display. these are used to create a meshgrid for determinging where to place a 1
	#NOTE: I am using a square for this matrix to make sure the placement of saccade endpoints is not stretched in one postion
	# due to differences in size between the vertical and horizontal size of the display: display_size = array([22.80, 17.10]); 
	
	xx_vec = linspace(-10,10,40);
	yy_vec = linspace(10,-10,40); #NOTE the flipped signs for y axis: positive to negative. Otherwise, this wouldn't correspond to the positive y values on the top of screen
	
#2. Iterate through for each subject and get the ending positions of each first saccade, storing appropriately, then create individual maps	

	for subj_nr, blocks in enumerate(block_matrix):
		
		#pre-define this meshgrid for use in determining where to place 1's for fixation 
		x_x, y_y = meshgrid(xx_vec, yy_vec);
		for b in blocks:
			for i in arange(0,len(b.trials)):
				
				if ((b.trials[i].dropped_sample == 0)&(b.trials[i].didntLookAtAnyItems == 0)&
					(b.trials[i].skip == 0)&(sqrt(b.trials[i].eyeX[0]**2 + b.trials[i].eyeY[0]**2) < 2.5)&(b.trials[i].trial_type==ttype)):
					
					if (b.trials[i].nr_saccades > 0):  #this conditional is used to ensure that no trials without saccades sneak through

						trial_counters[subj_nr][0] +=1; 
						#Below here goes through each trial and pulls out the ending point of the first saccde
						# the while loop below runs through until a saccade is found (saccade_counter = 1) or
						# we get to the end of the trial

						for ii,xx,yy,issac in zip(range(len(b.trials[i].sample_times)),
															 b.trials[i].eyeX, b.trials[i].eyeY, b.trials[i].isSaccade):
							#if no saccade has been made yet, keep running through the isSaccade array
							# issac < 1 will be zero at all non-saccading time points, including the start
							if issac == 0:
								#if the previous sample was saccading and now it isn't, the saccade is complete and we can grab the ending position
								if (b.trials[i].isSaccade[ii-1]==True)&(ii>0):
									sac_end = array([xx,yy]);
									saccade_counters[subj_nr][0] +=1;
									
									#we have the saccadic endpoints, now let's determine where to store them in the array
									#the detailed breakdown of what I'm doing here is desribes in the functions above

									minimum = 10000; coors = array([nan,nan]); #this pre-allocates a very large minimum and an array to hold the indices for the spatial position array
									#loop through and keep checking against each x,y pair
									for ex,why in zip(flatten(x_x),flatten(y_y)):
										comparison = sqrt((sac_end[0]-ex)**2 + (sac_end[1]-why)**2);
										if comparison < minimum:
											minimum = comparison;
											coors[0] = ex; coors[1] = why;

									#here, add a 1 to the ending point of each first saccade
									x_loc = where(coors[0]==xx_vec)[0][0]; #x coordinate
									y_loc = where(coors[1]==yy_vec)[0][0]; #y coordinate
									subj_arrays[subj_nr][y_loc, x_loc] += 1; #add the 1 to the location in the corresponding map.
									# NOTE the yloc, xloc coordinate system for indexing with this array. This must be done to get x-Loc to correspond to horizontal axis
									#below, I will aggregate all individual subject's heat maps together in the agg array

			end_time = time.time();
			print '\n Aggregated total time = %4.2f minutes, completed subject %s block nr %s '%((end_time-start_time)/60.0,subj_nr, b.block_nr)  # trial nr %sb.trials[i].trial_nr)

			#save each subject's first saccade endpoint heat maps
			if b.block_nr==len(blocks):
				#save the 'raw' heat maps
				figure(); imshow(subj_arrays[subj_nr], cmap='hot'); title('%s_ALL_SACCADES_heatmap_subj_%s'%(name, subj_nr));
				savefig(figurepath+'heatmaps/SACCADE_HEATMAPS/'+'%s_ALL_SACCADES_heatmap_subj_%s.png'%(name, subj_nr));
				
# 3. Aggregate across subjects by finding the average fixation accumulation		
			
	for su in zip(subj_arrays):
		agg_array += su[0]; #add each subjects' heat maps together	
	agg_array = agg_array/len(block_matrix); #to get the average
	
	#create and save the figure
	figure(); imshow(agg_array, cmap='hot'); title('%s_ALL_SACCADE_heatmap_subj_%s'%(name,'ALLSUBJECTS'));
	savefig(figurepath+'heatmaps/SACCADE_HEATMAPS/'+'%s_ALL_SACCADES_heatmap_subj_%s.png'%(name,'ALLSUBJECTS'));
	
	
def createAllSaccadeEndpointMapAllTrialTypesTogether(block_matrix):
# Same as above, but for all saccadic endpoints and collapsing across trial types

	start_time = time.time(); #start recording how long this takes

#0. Create data holders for the analyses

	#first, get the individual eye traces for each item for each trial where the selected_item was chosen
	# store each item's eye traces (adding a +1 for the trace being in that location at any time point in the trial) by creating little windows
	# e.g., a 4-degree by 4-degree square around each picture
	#compare against reference X,Y coordinates and place the values into each matrrix accordingly
	#aggregate this for each participant into a combined map
		
	#these are holder arrays for each participant, for each item.
	# Each list holds a 40 by 40 matrix that will hold the aggregated 1's associated with an eye trace at that location according to it's distance wrt the reference array
	# this gives me 0.5 degree resolution for the 20 dva by 20 dva square I am creating
	subj_arrays = [zeros((40,40)) for su in block_matrix];
	trial_counters = [[0] for su in block_matrix]; #to count how many trial are counted for this participant
	saccade_counters = [[0] for su in block_matrix]; #to count how many saccades are counted for this participant
	
	#these are arrays for the aggregated data
	agg_array = zeros((40,40));
	
	#get reference arrays for the display. these are used to create a meshgrid for determinging where to place a 1
	#NOTE: I am using a square for this matrix to make sure the placement of saccade endpoints is not stretched in one postion
	# due to differences in size between the vertical and horizontal size of the display: display_size = array([22.80, 17.10]); 
	
	xx_vec = linspace(-10,10,40);
	yy_vec = linspace(10,-10,40); #NOTE the flipped signs for y axis: positive to negative. Otherwise, this wouldn't correspond to the positive y values on the top of screen
	
#2. Iterate through for each subject and get the ending positions of each first saccade, storing appropriately, then create individual maps	

	for subj_nr, blocks in enumerate(block_matrix):
		
		#pre-define this meshgrid for use in determining where to place 1's for fixation 
		x_x, y_y = meshgrid(xx_vec, yy_vec);
		for b in blocks:
			for i in arange(0,len(b.trials)):
				
				if ((b.trials[i].dropped_sample == 0)&(b.trials[i].didntLookAtAnyItems == 0)&
					(b.trials[i].skip == 0)&(sqrt(b.trials[i].eyeX[0]**2 + b.trials[i].eyeY[0]**2) < 2.5)):
					
					if (b.trials[i].nr_saccades > 0):  #this conditional is used to ensure that no trials without saccades sneak through

						trial_counters[subj_nr][0] +=1; 
						#Below here goes through each trial and pulls out the ending point of the first saccde
						# the while loop below runs through until a saccade is found (saccade_counter = 1) or
						# we get to the end of the trial

						for ii,xx,yy,issac in zip(range(len(b.trials[i].sample_times)),
															 b.trials[i].eyeX, b.trials[i].eyeY, b.trials[i].isSaccade):
							#if no saccade has been made yet, keep running through the isSaccade array
							# issac < 1 will be zero at all non-saccading time points, including the start
							if issac == 0:
								#if the previous sample was saccading and now it isn't, the saccade is complete and we can grab the ending position
								if (b.trials[i].isSaccade[ii-1]==True)&(ii>0):
									sac_end = array([xx,yy]);
									saccade_counters[subj_nr][0] +=1;
									
									#we have the saccadic endpoints, now let's determine where to store them in the array
									#the detailed breakdown of what I'm doing here is desribes in the functions above

									minimum = 10000; coors = array([nan,nan]); #this pre-allocates a very large minimum and an array to hold the indices for the spatial position array
									#loop through and keep checking against each x,y pair
									for ex,why in zip(flatten(x_x),flatten(y_y)):
										comparison = sqrt((sac_end[0]-ex)**2 + (sac_end[1]-why)**2);
										if comparison < minimum:
											minimum = comparison;
											coors[0] = ex; coors[1] = why;

									#here, add a 1 to the ending point of each first saccade
									x_loc = where(coors[0]==xx_vec)[0][0]; #x coordinate
									y_loc = where(coors[1]==yy_vec)[0][0]; #y coordinate
									subj_arrays[subj_nr][y_loc, x_loc] += 1; #add the 1 to the location in the corresponding map.
									# NOTE the yloc, xloc coordinate system for indexing with this array. This must be done to get x-Loc to correspond to horizontal axis
									#below, I will aggregate all individual subject's heat maps together in the agg array

			end_time = time.time();
			print '\n Aggregated total time = %4.2f minutes, completed subject %s block nr %s '%((end_time-start_time)/60.0,subj_nr, b.block_nr)  # trial nr %sb.trials[i].trial_nr)

			#save each subject's first saccade endpoint heat maps
			if b.block_nr==len(blocks):
				#save the 'raw' heat maps
				figure(); imshow(subj_arrays[subj_nr], cmap='hot'); title('ALLTRIALTYPES_ALL_SACCADES_heatmap_subj_%s'%(subj_nr));
				savefig(figurepath+'heatmaps/SACCADE_HEATMAPS/'+'ALLTRIALTYPES_ALL_SACCADES_heatmap_subj_%s.png'%(subj_nr));
				
# 3. Aggregate across subjects by finding the average fixation accumulation		
			
	for su in zip(subj_arrays):
		agg_array += su[0]; #add each subjects' heat maps together	
	agg_array = agg_array/len(block_matrix); #to get the average
	
	#create and save the figure
	figure(); imshow(agg_array, cmap='hot'); title('ALLTRIALTYPES_ALL_SACCADE_heatmap_subj_%s'%('ALLSUBJECTS'));
	savefig(figurepath+'heatmaps/SACCADE_HEATMAPS/'+'ALLTRIALTYPES_ALL_SACCADES_heatmap_subj_%s.png'%('ALLSUBJECTS'));					