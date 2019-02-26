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
from math import *
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
#matplotlib.rcParams['axes.titlepad'] = 2;
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

#here, find the individual the cut offs for each participant for saccadic latencies
# goal is to identify what the 'baseline' saccadic latency is
# another goal is to identify which first saccades are a result of an explicit strategy (direction), and have anticipatory latencies

# Determine the saccdic latency for first and all saccades:
# 1. Distribution of onsets latencies
# 2. Average onset latencies

def computeFirstSaccadeKinematics(block_matrix):

# Start with computing saccadic onset latencies for first saccades only
	# Pre-allocate data structure holders
	onset_latencies = [[] for su in block_matrix];
	anticipatory_latencies = [[] for su in block_matrix];
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
						if sac_start_time<100:
							anticipatory_latencies[subj_nr].append(sac_start_time);
						amplitudes[subj_nr].append(sqrt((sac_start_pos[0] - sac_end_pos[0])**2+(sac_start_pos[1] - sac_end_pos[1])**2));
											
	#here, get the mean onset latencies for each participant, also get the between-participants SEM
	mew_latencies = array([mean(lat) for lat in onset_latencies]);
	latencies_sems = compute_BS_SEM(mew_latencies);
	
	#now get the standard deviations of latencies for each participant
	var_latencies = array([var(lat) for lat in onset_latencies]);
	std_latencies = array([sqrt(v) for v in var_latencies]);
	
	#now find the cutoff latency criteria (2 standard deviations above and below the mean latency)
	early_latency_crit = mew_latencies - 2*std_latencies;
	early_latencies_sem = compute_BS_SEM(early_latency_crit);
	late_latency_crit = mew_latencies + 2*std_latencies;
	
	# #get the mean amplitudes of first saccades
	# mew_amps = array([mean(lat) for lat in amplitudes]);
	# amps_sems = compute_BS_SEM(mew_amps);


	#below here create two plots, one with 15 and the other 14, participant first saccade latency distributions
	#this is meant to provide a graphical representation for each participant. I will plot the latency criteria too

	#first, redefine the plotting parameters for the smaller plots I'm using here.
	matplotlib.rcParams['ytick.labelsize']=10; matplotlib.rcParams['xtick.labelsize']=10;
	matplotlib.rcParams['xtick.major.size']=5.0; matplotlib.rcParams['ytick.major.size']=5.0;

	#first figure is for the first 15 participants
	[fig1, ax_arrs1] = subplots(3,5);
	#subplots_adjust(hspace = 2.0)
	for ax,subject_dists,subject_mew,subject_early_crit,subject_late_crit,i in zip(flatten(ax_arrs1),onset_latencies,mew_latencies,early_latency_crit,late_latency_crit,
																				   range(15)):
		
		# set axis limits the same for easy comparison
		ax.set_ylim([0,55]); ax.set_xlim([0,750]);  #1000
		#format the axis
		if (i==10):  #(i==0)|(i==5)|
			ax.set_ylabel('Frequency',size=10);
		if (i==10):
			ax.set_xlabel('Onset latency',size=10);  #,size=18,labelpad=15);
		#now plot the distributions, then add the mean and cutoffs	
		ax.hist(subject_dists, bins = 20);
		ax.axvline(subject_mew, 0, 50, color = 'black'); #mean     , linewidth = 
		ax.axvline(subject_early_crit, 0, 50, color = 'black', linestyle = 'dashed'); #early cutoff
		ax.axvline(subject_late_crit, 0, 50, color = 'black', linestyle = 'dashed'); #late cutoff
		
		#format everything else
		ax.spines['right'].set_visible(False); ax.spines['top'].set_visible(False);
		ax.spines['bottom'].set_linewidth(2.0); ax.spines['left'].set_linewidth(2.0);
		ax.yaxis.set_ticks_position('left'); ax.xaxis.set_ticks_position('bottom');
		ax.set_title('subject %s'%i, size=10);
	
	fig1.tight_layout(); #change up the layout to make spacing between subplots more readable
	savefig(figurepath+ 'SaccadeKinematics/' + 'FIRST_SACCADE_ONSET_INDIVIDUAL_SUBJECTS0-14_DISTRIBUTIONS.png');
	
	#next is for the next 14 participants
	[fig2, ax_arrs2] = subplots(3,5);
	#delete the last axis
	#delax = [f for f in flatten(ax_arrs2)][-1];
	#fig.delaxes(delax);
	delax = [f for f in flatten(ax_arrs2)][-3:]; #for now with 27 participants
	test = [fig2.delaxes(d) for d in delax];
	#subplots_adjust(hspace = 2.0)
	for ax1,subject_dists,subject_mew,subject_early_crit,subject_late_crit,i in zip([f for f in flatten(ax_arrs2)][0:13],onset_latencies[15:],mew_latencies[15:],early_latency_crit[15:],late_latency_crit[15:],
																				   range(15,27)): #range(15,29)
		
		# set axis limits the same for easy comparison
		ax1.set_ylim([0,55]); ax1.set_xlim([0,750]);
		#format the axis
		if (i==10):  #(i==0)|(i==5)|
			ax1.set_ylabel('Frequency',size=10);
		if (i==10):
			ax1.set_xlabel('Onset latency',size=10);  #,size=18,labelpad=15);
		#now plot the distributions, then add the mean and cutoffs	
		ax1.hist(subject_dists, bins = 20);
		ax1.axvline(subject_mew, 0, 50, color = 'black'); #mean     , linewidth = 
		ax1.axvline(subject_early_crit, 0, 50, color = 'black', linestyle = 'dashed'); #early cutoff
		ax1.axvline(subject_late_crit, 0, 50, color = 'black', linestyle = 'dashed'); #late cutoff
		
		#format everything else
		ax1.spines['right'].set_visible(False); ax1.spines['top'].set_visible(False);
		ax1.spines['bottom'].set_linewidth(2.0); ax1.spines['left'].set_linewidth(2.0);
		ax1.yaxis.set_ticks_position('left'); ax1.xaxis.set_ticks_position('bottom');
		ax1.set_title('subject %s'%i, size=10);
	
	fig2.tight_layout(); #change up the layout to make spacing between subplots more readable
	savefig(figurepath+ 'SaccadeKinematics/' + 'FIRST_SACCADE_ONSET_INDIVIDUAL_SUBJECTS15-29_DISTRIBUTIONS.png');	
	
	#set the plotting params back to the standard
	matplotlib.rcParams['ytick.labelsize']=20; matplotlib.rcParams['xtick.labelsize']=20;
	matplotlib.rcParams['xtick.major.width']=2.0; matplotlib.rcParams['ytick.major.width']=2.0;
	matplotlib.rcParams['xtick.major.size']=10.0; matplotlib.rcParams['ytick.major.size']=10.0;

	#plot the distribution of average saccadic onset latencies
	
	fig = figure(figsize = (12.8,7.64)); ax1=gca(); #grid(True);
	#ax1.set_ylim(0, 0.8); ax1.set_yticks(arange(0, 0.81, 0.1)); #ax1.set_xlim([0.5,1.7]); ax1.set_xticks([0.85, 1.15, 1.45]);
	ax1.set_ylabel('Frequency',size=18); ax1.set_xlabel('Mean onset latency',size=18,labelpad=15);
	ax1.hist(mew_latencies, color = 'green', bins = 20);

	ax1.spines['right'].set_visible(False); ax1.spines['top'].set_visible(False);
	ax1.spines['bottom'].set_linewidth(2.0); ax1.spines['left'].set_linewidth(2.0);
	ax1.yaxis.set_ticks_position('left'); ax1.xaxis.set_ticks_position('bottom');
	title('Distribution of subject average saccadic latencies for first saccades', fontsize = 22);
	
	#add text detailing the mean saccadic latency
	fig.text(0.7, 0.48, 'MEAN LATENCY:\n %s +- %s ms '%(round(mean(mew_latencies)),round(latencies_sems)),size=16,weight='bold');
	savefig(figurepath+ 'SaccadeKinematics/' + 'FIRST_SACCADE_AVERAGE_ONSET_DISTRIBUTION_ALLSUBJECTS.png');	
	
	#also plot the distribution of early onset crits

	fig = figure(figsize = (12.8,7.64)); ax1=gca(); #grid(True);
	ax1.set_xlim([0, 250]); #ax1.set_ylim(0, 0.8); ax1.set_yticks(arange(0, 0.81, 0.1)); # ax1.set_xticks([0.85, 1.15, 1.45]);
	ax1.set_ylabel('Frequency',size=18); ax1.set_xlabel('Mean onset latency',size=18,labelpad=15);
	ax1.hist(early_latency_crit, color = 'orange', bins = 20);

	ax1.spines['right'].set_visible(False); ax1.spines['top'].set_visible(False);
	ax1.spines['bottom'].set_linewidth(2.0); ax1.spines['left'].set_linewidth(2.0);
	ax1.yaxis.set_ticks_position('left'); ax1.xaxis.set_ticks_position('bottom');
	title('Distribution of subject saccadic latency early cutoff criteria for first saccades', fontsize = 22);
	
	#add text detailing the mean saccadic latency
	fig.text(0.7, 0.48, 'MEAN LATENCY CUTOFF:\n %s +- %s ms '%(round(mean(early_latency_crit)),round(early_latencies_sem)),size=16,weight='bold');
	savefig(figurepath+ 'SaccadeKinematics/' + 'FIRST_SACCADE_AVERAGE_EARLY_CUTOFF_DISTRIBUTION_ALLSUBJECTS.png');	

	1/0

	
	
def computeAllSaccadeKinetmatics(block_matrix):

# Start with computing saccadic onset latencies for first saccades only
	# Pre-allocate data structure holders
	onset_latencies = [[] for su in block_matrix];
	amplitudes = [[] for su in block_matrix];
	nr_saccades = [[0] for su in block_matrix];

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
									nr_saccades[subj_nr][0] += 1;
									saccade_counter+=1;
									sac_end_time = t.sample_times[ii];
									sac_end_pos = array([xx,yy]);
									amplitudes[subj_nr].append(sqrt((sac_start_pos[0] - sac_end_pos[0])**2+(sac_start_pos[1] - sac_end_pos[1])**2));
									
									if saccade_counter>1:     #already have the onset latency for the first saccade
										onset_latencies[subj_nr].append(sac_start_time-sac_lat_start_calculation);
									
									sac_lat_start_calculation = sac_end_time; #set this variable as the first onset latency

									
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
	ax1.hist(all_lats, color = 'red');

	ax1.spines['right'].set_visible(False); ax1.spines['top'].set_visible(False);
	ax1.spines['bottom'].set_linewidth(2.0); ax1.spines['left'].set_linewidth(2.0);
	ax1.yaxis.set_ticks_position('left'); ax1.xaxis.set_ticks_position('bottom');
	title('Population average saccadic latencies for ALL saccades', fontsize = 22);
	
	#add text detailing the mean saccadic latency
	fig.text(0.7, 0.48, 'MEAN LATENCY:\n %s +- %s ms '%(round(mean(mew_latencies)),round(latencies_sems)),size=16,weight='bold');

	#save the figure
	savefig(figurepath+ 'SaccadeKinematics/' + 'ALL_SACCADE_ONSET_DISTRIBUTION_ALLSUBJECTS.png');	



	#now plot distribution of amplitudes
	
	fig = figure(figsize = (12.8,7.64)); ax=gca(); #grid(True);
	#ax1.set_ylim(0, 0.8); ax1.set_yticks(arange(0, 0.81, 0.1)); #ax1.set_xlim([0.5,1.7]); ax1.set_xticks([0.85, 1.15, 1.45]);
	ax.set_ylabel('Frequency',size=18); ax.set_xlabel('Saccade amplitude',size=18,labelpad=15);
	ax.hist(all_amps, color = 'darkgray');

	ax.spines['right'].set_visible(False); ax.spines['top'].set_visible(False);
	ax.spines['bottom'].set_linewidth(2.0); ax.spines['left'].set_linewidth(2.0);
	ax.yaxis.set_ticks_position('left'); ax.xaxis.set_ticks_position('bottom');
	title('Population average saccadic amplitudes for ALL saccades', fontsize = 22);
	
	#add text detailing the mean saccadic latency
	fig.text(0.75, 0.48, 'MEAN AMPLITUDE:\n %s +- %s degrees '%(round(mean(mew_amps)),round(amps_sems)),size=16,weight='bold');

	#save the figure
	savefig(figurepath+ 'SaccadeKinematics/' + 'ALL_SACCADE_AMPLITUDE_DISTRIBUTION_ALLSUBJECTS.png');	
	
	1/0;


def computeAllExceptFirstSaccadeKinetmatics(block_matrix):
#computes saccade information for all saccades, minus the first saccade
# Start with computing saccadic onset latencies for first saccades only
	# Pre-allocate data structure holders
	onset_latencies = [[] for su in block_matrix];
	amplitudes = [[] for su in block_matrix];
	nr_saccades = [[0] for su in block_matrix];
	
	#define a variable to store the amplitude for very fast saccades
	concurrent_amplitudes = [[] for su in block_matrix]; #concurrently planned witll be defined as less than 125 ms (a la McPeek et al. 2000)

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
									saccade_counter+=1;
									sac_end_time = t.sample_times[ii];
									sac_end_pos = array([xx,yy]);
									nr_saccades[subj_nr][0] += 1;
									#only dd amplitudes of there is more than the first saccade
									if saccade_counter > 1:
										onset_latencies[subj_nr].append(sac_start_time-sac_lat_start_calculation);
										amplitudes[subj_nr].append(sqrt((sac_start_pos[0] - sac_end_pos[0])**2+(sac_start_pos[1] - sac_end_pos[1])**2));
										
										#here is the conditional to determine if this is a concurrently planned saccade
										if sac_start_time-sac_lat_start_calculation < 125:
											concurrent_amplitudes[subj_nr].append(sqrt((sac_start_pos[0] - sac_end_pos[0])**2+(sac_start_pos[1] - sac_end_pos[1])**2));
											
									sac_lat_start_calculation = sac_end_time; #set this variable 
										
							elif issac == 1:
								#get the starting point for this saccade as well as the time
								#the first transition between 0 and 1 will be the first saccade start
								if (t.isSaccade[ii-1]==False)&(ii>0):
									sac_start_time = t.sample_times[ii];
									sac_start_pos = array([xx,yy]);
									
											
	#now calculate population stats for latency and amplitude, and plot
	all_lats = [l for lat in onset_latencies for l in lat];
	all_amps = [a for am in amplitudes for a in am];
	all_concurrent_amps = [a for am in concurrent_amplitudes for a in am];
	mew_latencies = array([mean(lat) for lat in onset_latencies]);
	latencies_sems = compute_BS_SEM(mew_latencies);
	mew_amps = array([mean(lat) for lat in amplitudes]);
	amps_sems = compute_BS_SEM(mew_amps);
	mew_concurrent_amps = array([mean(lat) for lat in concurrent_amplitudes]);
	concurrent_amps_sems = compute_BS_SEM(mew_concurrent_amps);
	
	#plot the distribution of saccadid latencies across all participants
	
	fig = figure(figsize = (12.8,7.64)); ax1=gca(); #grid(True);
	#ax1.set_ylim(0, 0.8); ax1.set_yticks(arange(0, 0.81, 0.1)); #ax1.set_xlim([0.5,1.7]); ax1.set_xticks([0.85, 1.15, 1.45]);
	ax1.set_ylabel('Frequency',size=18); ax1.set_xlabel('Onset latency',size=18,labelpad=15);
	ax1.hist(all_lats, color = 'red', bins = [0,50,100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,950,1000]);

	ax1.spines['right'].set_visible(False); ax1.spines['top'].set_visible(False);
	ax1.spines['bottom'].set_linewidth(2.0); ax1.spines['left'].set_linewidth(2.0);
	ax1.yaxis.set_ticks_position('left'); ax1.xaxis.set_ticks_position('bottom');
	title('Population average saccadic latencies for OTHER saccades', fontsize = 22);
	
	#add text detailing the mean saccadic latency
	fig.text(0.7, 0.48, 'MEAN LATENCY:\n %s +- %s ms '%(round(mean(mew_latencies)),round(latencies_sems)),size=16,weight='bold');

	#save the figure
	savefig(figurepath+ 'SaccadeKinematics/' + 'OTHER_SACCADE_ONSET_DISTRIBUTION_ALLSUBJECTS.png');	

	#now plot distribution of amplitudes
	
	fig = figure(figsize = (12.8,7.64)); ax=gca(); #grid(True);
	#ax1.set_ylim(0, 0.8); ax1.set_yticks(arange(0, 0.81, 0.1)); #ax1.set_xlim([0.5,1.7]); ax1.set_xticks([0.85, 1.15, 1.45]);
	ax.set_ylabel('Frequency',size=18); ax.set_xlabel('Saccade amplitude',size=18,labelpad=15);
	ax.hist(all_amps, color = 'darkgray');

	ax.spines['right'].set_visible(False); ax.spines['top'].set_visible(False);
	ax.spines['bottom'].set_linewidth(2.0); ax.spines['left'].set_linewidth(2.0);
	ax.yaxis.set_ticks_position('left'); ax.xaxis.set_ticks_position('bottom');
	title('Population average saccadic amplitudes for OTHER saccades', fontsize = 22);
	
	#add text detailing the mean saccadic latency
	fig.text(0.75, 0.48, 'MEAN AMPLITUDE:\n %s +- %s degrees '%(round(mean(mew_amps),2),round(amps_sems,2)),size=16,weight='bold');

	#save the figure
	savefig(figurepath+ 'SaccadeKinematics/' + 'OTHER_SACCADE_AMPLITUDE_DISTRIBUTION_ALLSUBJECTS.png');
	
	#finally, plot the distribution of amplitudes for very fast concurrently planned saccades (<125 ms)
	fig = figure(figsize = (12.8,7.64)); ax=gca(); #grid(True);
	#ax1.set_ylim(0, 0.8); ax1.set_yticks(arange(0, 0.81, 0.1)); #ax1.set_xlim([0.5,1.7]); ax1.set_xticks([0.85, 1.15, 1.45]);
	ax.set_ylabel('Frequency',size=18); ax.set_xlabel('Saccade amplitude',size=18,labelpad=15);
	ax.hist(all_concurrent_amps, color = 'orange');

	ax.spines['right'].set_visible(False); ax.spines['top'].set_visible(False);
	ax.spines['bottom'].set_linewidth(2.0); ax.spines['left'].set_linewidth(2.0);
	ax.yaxis.set_ticks_position('left'); ax.xaxis.set_ticks_position('bottom');
	title('Population average saccadic amplitudes for OTHER saccades \n only concurrently planned (<125 ms latency)', fontsize = 22);
	
	#add text detailing the mean saccadic latency
	fig.text(0.75, 0.48, 'MEAN AMPLITUDE:\n %2.1f +- %2.1f degrees '%(round(mean(mew_concurrent_amps),2),round(concurrent_amps_sems,2)),size=16,weight='bold');

	#save the figure
	savefig(figurepath+ 'SaccadeKinematics/' + 'OTHER_SACCADE_CONCURRENT_AMPLITUDE_DISTRIBUTION_ALLSUBJECTS.png');
	
	1/0





############################################
## Saccadic Endpoint Heat Map ##
############################################

def createStartingPositionMapOutsideofFixationAllTrialTypesTogether(block_matrix):
	#designed to plot where subjects were starting to look at when they weren't starting at the center of the screen
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
					(b.trials[i].skip == 0)&(sqrt(b.trials[i].eyeX[0]**2 + b.trials[i].eyeY[0]**2) > 2.5)):
						
						#here, we know they weren't looking at the center of the screen.
						#now determine where they were looking
						starting_loc = array([b.trials[i].eyeX[0],b.trials[i].eyeY[0]]);
						
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
							comparison = sqrt((starting_loc[0]-ex)**2 + (starting_loc[1]-why)**2);
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
				figure(); imshow(subj_arrays[subj_nr], cmap='hot'); title('ALLTRIALS_STARTINGPOSNOTFIXATION_heatmap_subj_%s'%(subj_nr));
				#set a legend. first, get the maximal value in the array to define a legend
				m = round(max(map(max,subj_arrays[subj_nr])),1);
				cb = colorbar(pad = 0.1, ticks = linspace(0,m,3)); cb.outline.set_linewidth(2.0);
				savefig(figurepath+'heatmaps/SACCADE_HEATMAPS/'+'ALLTRIALS_STARTINGPOSNOTFIXATION_heatmap_subj_%s.png'%(subj_nr));						
						
# 3. Aggregate across subjects by finding the average fixation accumulation		
			
	for su in zip(subj_arrays):
		agg_array += su[0]; #add each subjects' heat maps together	
	agg_array = agg_array/len(block_matrix); #to get the average
	
	#create and save the figure
	figure(); imshow(agg_array, cmap='hot'); title('ALLTRIALS_STARTINGPOSNOTFIXATION_heatmap_subj_%s'%('ALLSUBJECTS'));
	#set a legend. first, get the maximal value in the array to define a legend
	m = round(max(map(max,agg_array)),1);
	cb = colorbar(pad = 0.1, ticks = linspace(0,m,3), format = '%2.1f'); cb.outline.set_linewidth(2.0);
	savefig(figurepath+'heatmaps/SACCADE_HEATMAPS/'+'ALLTRIALS_STARTINGPOSNOTFIXATION_heatmap_subj_%s.png'%('ALLSUBJECTS'));
	
	1/0
	

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
				#set a legend. first, get the maximal value in the array to define a legend
				m = round(max(map(max,subj_arrays[subj_nr])),1);
				cb = colorbar(pad = 0.1, ticks = linspace(0,m,3)); cb.outline.set_linewidth(2.0);
				savefig(figurepath+'heatmaps/SACCADE_HEATMAPS/'+'%s_FIRSTSACCADE_heatmap_subj_%s.png'%(name, subj_nr));
				
# 3. Aggregate across subjects by finding the average fixation accumulation		
			
	for su in zip(subj_arrays):
		agg_array += su[0]; #add each subjects' heat maps together	
	agg_array = agg_array/len(block_matrix); #to get the average
	
	#create and save the figure
	figure(); imshow(agg_array, cmap='hot'); title('%s_FIRST_SACCADE_heatmap_subj_%s'%(name,'ALLSUBJECTS'));
	#set a legend. first, get the maximal value in the array to define a legend
	m = round(max(map(max,agg_array)),1);
	cb = colorbar(pad = 0.1, ticks = linspace(0,m,3), format = '%2.1f'); cb.outline.set_linewidth(2.0);
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
				#set a legend. first, get the maximal value in the array to define a legend
				m = round(max(map(max,subj_arrays[subj_nr])),1);
				cb = colorbar(pad = 0.1, ticks = linspace(0,m,3)); cb.outline.set_linewidth(2.0);
				savefig(figurepath+'heatmaps/SACCADE_HEATMAPS/'+'ALLTRIALTYPES_FIRSTSACCADE_heatmap_subj_%s.png'%(subj_nr));				
			
				
# 3. Aggregate across subjects by finding the average fixation accumulation		
			
	for su in zip(subj_arrays):
		agg_array += su[0]; #add each subjects' heat maps together	
	agg_array = agg_array/len(block_matrix); #to get the average
	
	#create and save the figure
	figure(); imshow(agg_array, cmap='hot'); title('ALLTRIALTYPES_FIRST_SACCADE_heatmap_subj_%s'%('ALLSUBJECTS'));
	#set a legend. first, get the maximal value in the array to define a legend
	m = round(max(map(max,agg_array)),1);
	cb = colorbar(pad = 0.1, ticks = linspace(0,m,3), format = '%2.1f'); cb.outline.set_linewidth(2.0);
	savefig(figurepath+'heatmaps/SACCADE_HEATMAPS/'+'ALLTRIALTYPES_FIRSTSACCADE_heatmap_subj_%s.png'%('ALLSUBJECTS'));
	
	
def createFastLatencyFirstSaccadeEndpointMap(block_matrix,  ttype):
# This function computes heat maps for landing positions of saccade with faster than early onset latency criterion (>2 s.d.s less than mean)
#broken down by trial type
	name = ['high_pref', 'highC_lowA','lowC_highA','lowC_lowA'][ttype-1];
	start_time = time.time(); #start recording how long this takes
	
#0.First the early cutoff criteria for each participant, using the code dervied in computeFirstSaccadeKinematics

	# Start by computing saccadic onset latencies for first saccades only
	# Pre-allocate data structure holders
	onset_latencies = [[] for su in block_matrix];
	anticipatory_latencies = [[] for su in block_matrix];
	amplitudes = [[] for su in block_matrix];

	#loop through each trial and score whether trial was excluded because of a dropped sample
	for subj_nr, blocks in enumerate(block_matrix):
		for b in blocks:
			for t in b.trials:
				if ((t.dropped_sample == 0)&(t.didntLookAtAnyItems == 0)&
					(t.skip == 0)&(sqrt(t.eyeX[0]**2 + t.eyeY[0]**2) < 2.5)&(b.trials[i].trial_type==ttype)):      #&(t.trial_type==ttype)
					
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
						if sac_start_time<100:
							anticipatory_latencies[subj_nr].append(sac_start_time);
						amplitudes[subj_nr].append(sqrt((sac_start_pos[0] - sac_end_pos[0])**2+(sac_start_pos[1] - sac_end_pos[1])**2));
											
	#here, get the mean onset latencies for each participant, also get the between-participants SEM
	mew_latencies = array([mean(lat) for lat in onset_latencies]);
	latencies_sems = compute_BS_SEM(mew_latencies);
	
	#now get the standard deviations of latencies for each participant
	var_latencies = array([var(lat) for lat in onset_latencies]);
	std_latencies = array([sqrt(v) for v in var_latencies]);
	
	#now find the cutoff latency criteria (2 standard deviations above and below the mean latency)
	early_latency_crit = mew_latencies - 2*std_latencies;

	#######################################################################################	
	## Here, I have the early onset latency criteria for each partcipants.
	## Now I can use this info to pull only those first sacades that are faster than this

#1 Create data holders for the analyses

	#first, get the individual eye traces for each item for each trial where the selected_item was chosen
	# store each item's eye traces (adding a +1 for the trace being in that location at any time point in the trial) by creating little windows
	# e.g., a 4-degree by 4-degree square around each picture
	#compare against reference X,Y coordinates and place the values into each matrrix accordingly
	#aggregate this for each participant into a combined map
		
	#these are holder arrays for each participant, for each item.
	# Each list holds a 40 by 40 matrix that will hold the aggregated 1's associated with an eye trace at that location according to it's distance wrt the reference array
	# this gives me 0.5 degree resolution for the 20 dva by 20 dva square I am creating
	subj_arrays = [zeros((40,40)) for su in block_matrix];
	subj_proportion_arrays = [zeros((40,40)) for su in block_matrix]; #to collect the proportion of trials from raw number
	trial_counters = [[0] for su in block_matrix]; #to count how many trial are counted for this participant
	
	#these are arrays for the aggregated data
	agg_array = zeros((40,40));
	
	#get reference arrays for the display. these are used to create a meshgrid for determinging where to place a 1
	#NOTE: I am using a square for this matrix to make sure the placement of saccade endpoints is not stretched in one postion
	# due to differences in size between the vertical and horizontal size of the display: display_size = array([22.80, 17.10]); 
	
	xx_vec = linspace(-10,10,40);
	yy_vec = linspace(10,-10,40); #NOTE the flipped signs for y axis: positive to negative. Otherwise, this wouldn't correspond to the positive y values on the top of screen
	
#2. Iterate through for each subject and get the ending positions of each first saccade, storing appropriately, then create individual maps	

	for subj_nr, data in enumerate(zip(block_matrix,early_latency_crit)):
		blocks = data[0]; early_lat = data[1];
		1/0;
		for b in blocks:
			for i in arange(0,len(b.trials)):
				
				if ((b.trials[i].dropped_sample == 0)&(b.trials[i].didntLookAtAnyItems == 0)&
					(b.trials[i].skip == 0)&(sqrt(b.trials[i].eyeX[0]**2 + b.trials[i].eyeY[0]**2) < 2.5)):
					
					if (b.trials[i].nr_saccades > 0): #this conditional is used to ensure that no trials without saccades sneak through

						trial_counters[subj_nr][0] +=1; 
						#Below here goes through each trial and pulls out the ending point of the first saccde
						# the while loop below runs through until a saccade is found (saccade_counter = 1) or
						# we get to the end of the trial
						sac_start_time = 0;	
						
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
										
								elif issac == 1:
									#get the starting point for this saccade as well as the time
									#the first transition between 0 and 1 will be the first saccade start
									if (b.trials[i].isSaccade[ii-1]==False)&(ii>0)&(saccade_counter==0):
										sac_start_time = b.trials[i].sample_times[ii];
		
						#at this point, I have the ending x,y position for the first saccade from trial N.
						# Now, need to incorporate it into the corresponding position holder matrices.
		
						#after this, add a 1 to the appropriate location in this subjects' aggregated alcohol 'map'
						# note that this computation is stored here in the outer For loop (rather than indented more)
						# because I am only grabbing the first saccade endpoint. Further computations with all saccades
						# will need to do this inside the for loop (while loop as well)
						
						#for this analysis, I only want to build a heat map for first saccades with very fast onsets (less than 100 ms)
						if sac_start_time<=100:				
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
			
			m = round(max(map(max,subj_arrays[subj_nr])),1); #get maximum nr of saccades here
			subj_proportion_arrays[subj_nr] = subj_arrays[subj_nr]/float(m);

			end_time = time.time();
			print '\n Aggregated total time = %4.2f minutes, completed subject %s block nr %s '%((end_time-start_time)/60.0,subj_nr, b.block_nr)  # trial nr %sb.trials[i].trial_nr)

			#save each subject's first saccade endpoint heat maps
			if b.block_nr==len(blocks):
				#save the 'raw' heat maps
				figure(); imshow(subj_proportion_array[subj_nr], cmap='hot'); title('%s_FASTLATENCY_ALLTRIALTYPES_FIRST_SACCADE_heatmap_subj_%s'%(name,subj_nr));
				#set a legend. first, get the maximal value in the array to define a legend
				mx = round(max(map(max,subj_proportion_arrays[subj_nr])),1);
				cb = colorbar(pad = 0.1, ticks = linspace(0,mx,3)); cb.outline.set_linewidth(2.0);
				
				#add text to 
				
				savefig(figurepath+'heatmaps/SACCADE_HEATMAPS/'+'%s_FASTLATENCY_ALLTRIALTYPES_FIRSTSACCADE_heatmap_subj_%s.png'%(name,subj_nr));				
			
				
# 3. Aggregate across subjects by finding the average fixation accumulation		
	
	for su in zip(subj_arrays):
		agg_array += su[0]; #add each subjects' heat maps together	
	agg_array = agg_array/len(block_matrix); #to get the average
	
	#create and save the figure
	figure(); imshow(agg_array, cmap='hot'); title('%s_FASTLATENCY_ALLTRIALTYPES_FIRST_SACCADE_heatmap_subj_%s'%(name,'ALLSUBJECTS'));
	#set a legend. first, get the maximal value in the array to define a legend
	m = round(max(map(max,agg_array)),1);
	cb = colorbar(pad = 0.1, ticks = linspace(0,m,3), format = '%2.1f'); cb.outline.set_linewidth(2.0);
	savefig(figurepath+'heatmaps/SACCADE_HEATMAPS/'+'%s_FASTLATENCY_ALLTRIALTYPES_FIRSTSACCADE_heatmap_subj_%s.png'%(name,'ALLSUBJECTS'));	
	
	
def createFastLatencyFirstSaccadeEndpointMapAllTrialTypesTogether(block_matrix):
# This function computes heat maps for landing positions of saccade with faster than early onset latency criterion (>2 s.d.s less than mean)

	start_time = time.time(); #start recording how long this takes

#0.First the early cutoff criteria for each participant, using the code dervied in computeFirstSaccadeKinematics

	# Start by computing saccadic onset latencies for first saccades only
	# Pre-allocate data structure holders
	onset_latencies = [[] for su in block_matrix];
	anticipatory_latencies = [[] for su in block_matrix];
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
						if sac_start_time<100:
							anticipatory_latencies[subj_nr].append(sac_start_time);
						amplitudes[subj_nr].append(sqrt((sac_start_pos[0] - sac_end_pos[0])**2+(sac_start_pos[1] - sac_end_pos[1])**2));
											
	#here, get the mean onset latencies for each participant, also get the between-participants SEM
	mew_latencies = array([mean(lat) for lat in onset_latencies]);
	latencies_sems = compute_BS_SEM(mew_latencies);
	
	#now get the standard deviations of latencies for each participant
	var_latencies = array([var(lat) for lat in onset_latencies]);
	std_latencies = array([sqrt(v) for v in var_latencies]);
	
	#now find the cutoff latency criteria (2 standard deviations above and below the mean latency)
	early_latency_crit = mew_latencies - 2*std_latencies;

	#######################################################################################	
	## Here, I have the early onset latency criteria for each partcipants.	
	## Now I can use this info to pull only those first sacades that are faster than this

#1 Create data holders for the analyses

	#first, get the individual eye traces for each item for each trial where the selected_item was chosen
	# store each item's eye traces (adding a +1 for the trace being in that location at any time point in the trial) by creating little windows
	# e.g., a 4-degree by 4-degree square around each picture
	#compare against reference X,Y coordinates and place the values into each matrrix accordingly
	#aggregate this for each participant into a combined map
		
	#these are holder arrays for each participant, for each item.
	# Each list holds a 40 by 40 matrix that will hold the aggregated 1's associated with an eye trace at that location according to it's distance wrt the reference array
	# this gives me 0.5 degree resolution for the 20 dva by 20 dva square I am creating
	subj_arrays = [zeros((40,40)) for su in block_matrix];
	subj_proportion_arrays = [zeros((40,40)) for su in block_matrix]; #to collect the proportion of trials from raw number
	trial_counters = [[0] for su in block_matrix]; #to count how many trial are counted for this participant
	
	#these are arrays for the aggregated data
	agg_array = zeros((40,40));
	
	#get reference arrays for the display. these are used to create a meshgrid for determinging where to place a 1
	#NOTE: I am using a square for this matrix to make sure the placement of saccade endpoints is not stretched in one postion
	# due to differences in size between the vertical and horizontal size of the display: display_size = array([22.80, 17.10]); 
	
	xx_vec = linspace(-10,10,40);
	yy_vec = linspace(10,-10,40); #NOTE the flipped signs for y axis: positive to negative. Otherwise, this wouldn't correspond to the positive y values on the top of screen
	
#2. Iterate through for each subject and get the ending positions of each first saccade, storing appropriately, then create individual maps	

	for subj_nr, data in enumerate(zip(block_matrix,early_latency_crit)):
		blocks = data[0]; early_lat = data[1];
		1/0;
		for b in blocks:
			for i in arange(0,len(b.trials)):
				
				if ((b.trials[i].dropped_sample == 0)&(b.trials[i].didntLookAtAnyItems == 0)&
					(b.trials[i].skip == 0)&(sqrt(b.trials[i].eyeX[0]**2 + b.trials[i].eyeY[0]**2) < 2.5)):
					
					if (b.trials[i].nr_saccades > 0): #this conditional is used to ensure that no trials without saccades sneak through

						trial_counters[subj_nr][0] +=1; 
						#Below here goes through each trial and pulls out the ending point of the first saccde
						# the while loop below runs through until a saccade is found (saccade_counter = 1) or
						# we get to the end of the trial
						sac_start_time = 0;	
						
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
										
								elif issac == 1:
									#get the starting point for this saccade as well as the time
									#the first transition between 0 and 1 will be the first saccade start
									if (b.trials[i].isSaccade[ii-1]==False)&(ii>0)&(saccade_counter==0):
										sac_start_time = b.trials[i].sample_times[ii];
		
						#at this point, I have the ending x,y position for the first saccade from trial N.
						# Now, need to incorporate it into the corresponding position holder matrices.
		
						#after this, add a 1 to the appropriate location in this subjects' aggregated alcohol 'map'
						# note that this computation is stored here in the outer For loop (rather than indented more)
						# because I am only grabbing the first saccade endpoint. Further computations with all saccades
						# will need to do this inside the for loop (while loop as well)
						
						#for this analysis, I only want to build a heat map for first saccades with very fast onsets (less than 100 ms)
						if sac_start_time<=100:				
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
			
			m = round(max(map(max,subj_arrays[subj_nr])),1); #get maximum nr of saccades here
			subj_proportion_arrays[subj_nr] = subj_arrays[subj_nr]/float(m);

			end_time = time.time();
			print '\n Aggregated total time = %4.2f minutes, completed subject %s block nr %s '%((end_time-start_time)/60.0,subj_nr, b.block_nr)  # trial nr %sb.trials[i].trial_nr)

			#save each subject's first saccade endpoint heat maps
			if b.block_nr==len(blocks):
				#save the 'raw' heat maps
				figure(); ax = imshow(subj_proportion_array[subj_nr], cmap='hot'); title('FASTLATENCY_ALLTRIALTYPES_FIRST_SACCADE_heatmap_subj_%s'%(subj_nr));
				#set a legend. first, get the maximal value in the array to define a legend
				mx = round(max(map(max,subj_proportion_arrays[subj_nr])),1);
				cb = colorbar(pad = 0.1, ticks = linspace(0,mx,3)); cb.outline.set_linewidth(2.0);
				
				#add text to say how many saccade (total and max)
				
				
				savefig(figurepath+'heatmaps/SACCADE_HEATMAPS/'+'FASTLATENCY_ALLTRIALTYPES_FIRSTSACCADE_heatmap_subj_%s.png'%(subj_nr));				
			
				
# 3. Aggregate across subjects by finding the average fixation accumulation		
	
	for su in zip(subj_arrays):
		agg_array += su[0]; #add each subjects' heat maps together	
	agg_array = agg_array/len(block_matrix); #to get the average
	
	#create and save the figure
	figure(); imshow(agg_array, cmap='hot'); title('FASTLATENCY_ALLTRIALTYPES_FIRST_SACCADE_heatmap_subj_%s'%('ALLSUBJECTS'));
	#set a legend. first, get the maximal value in the array to define a legend
	m = round(max(map(max,agg_array)),1);
	cb = colorbar(pad = 0.1, ticks = linspace(0,m,3), format = '%2.1f'); cb.outline.set_linewidth(2.0);
	savefig(figurepath+'heatmaps/SACCADE_HEATMAPS/'+'FASTLATENCY_ALLTRIALTYPES_FIRSTSACCADE_heatmap_subj_%s.png'%('ALLSUBJECTS'));






	
def createOtherSaccadeEndpointMaps(block_matrix, ttype):
# Same as above, but for all saccadic endpoints OTHER than the first saccade and broken down by trial types

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
						saccade_count = 0; #counter to detrmine nr of saccades for this trial specifically
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
									saccade_count += 1; #this determines how many saccades have been found in this trial	
									
									#we have the saccadic endpoints, now let's determine where to store them in the array
									#the detailed breakdown of what I'm doing here is desribes in the functions above
									
									#this condition allows me to only do saccade analyses for those occurring subsequent to 1st saccade 
									if saccade_count > 1:

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
										
										saccade_counters[subj_nr][0] +=1;
	

			end_time = time.time();
			print '\n Aggregated total time = %4.2f minutes, completed subject %s block nr %s '%((end_time-start_time)/60.0,subj_nr, b.block_nr)  # trial nr %sb.trials[i].trial_nr)

			#save each subject's first saccade endpoint heat maps
			if b.block_nr==len(blocks):
				#save the 'raw' heat maps
				figure(); imshow(subj_arrays[subj_nr], cmap='hot'); title('%s_OTHER_SACCADES_heatmap_subj_%s'%(name, subj_nr));
				#set a legend. first, get the maximal value in the array to define a legend
				m = round(max(map(max,subj_arrays[subj_nr])),1);
				cb = colorbar(pad = 0.1, ticks = linspace(0,m,3)); cb.outline.set_linewidth(2.0);
				savefig(figurepath+'heatmaps/SACCADE_HEATMAPS/'+'%s_OTHER_SACCADES_heatmap_subj_%s.png'%(name, subj_nr));
				
				
# 3. Aggregate across subjects by finding the average fixation accumulation		
			
	for su in zip(subj_arrays):
		agg_array += su[0]; #add each subjects' heat maps together	
	agg_array = agg_array/len(block_matrix); #to get the average
	
	#create and save the figure
	figure(); imshow(agg_array, cmap='hot'); title('%s_OTHER_SACCADE_heatmap_subj_%s'%(name, 'ALLSUBJECTS')); 
	#set a legend. first, get the maximal value in the array to define a legend
	m = round(max(map(max,agg_array))); #,1);
	cb = colorbar(pad = 0.1, ticks = linspace(0,m,3), format = '%2.1f'); cb.outline.set_linewidth(2.0);	
	savefig(figurepath+'heatmaps/SACCADE_HEATMAPS/'+'%s_OTHER_SACCADES_heatmap_subj_%s.png'%(name, 'ALLSUBJECTS'));						
	
	
	
def createOtherSaccadeEndpointMapAllTrialTypesTogether(block_matrix):
# Same as above, but for all saccadic endpoints OTHER than the first saccade and collapsing across trial types

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
						saccade_count = 0; #counter to detrmine nr of saccades for this trial specifically
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
									saccade_count += 1; #this determines how many saccades have been found in this trial	
									
									#we have the saccadic endpoints, now let's determine where to store them in the array
									#the detailed breakdown of what I'm doing here is desribes in the functions above
									
									#this condition allows me to only do saccade analyses for those occurring subsequent to 1st saccade 
									if saccade_count > 1:

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
										
										saccade_counters[subj_nr][0] +=1;
	

			end_time = time.time();
			print '\n Aggregated total time = %4.2f minutes, completed subject %s block nr %s '%((end_time-start_time)/60.0,subj_nr, b.block_nr)  # trial nr %sb.trials[i].trial_nr)

			#save each subject's first saccade endpoint heat maps
			if b.block_nr==len(blocks):
				#save the 'raw' heat maps
				figure(); imshow(subj_arrays[subj_nr], cmap='hot'); title('ALLTRIALTYPES_OTHER_SACCADES_heatmap_subj_%s'%(subj_nr));
				#set a legend. first, get the maximal value in the array to define a legend
				m = round(max(map(max,subj_arrays[subj_nr])),1);
				cb = colorbar(pad = 0.1, ticks = linspace(0,m,3)); cb.outline.set_linewidth(2.0);
				savefig(figurepath+'heatmaps/SACCADE_HEATMAPS/'+'ALLTRIALTYPES_OTHER_SACCADES_heatmap_subj_%s.png'%(subj_nr));
				
				
# 3. Aggregate across subjects by finding the average fixation accumulation		
			
	for su in zip(subj_arrays):
		agg_array += su[0]; #add each subjects' heat maps together	
	agg_array = agg_array/len(block_matrix); #to get the average
	
	#create and save the figure
	figure(); imshow(agg_array, cmap='hot'); title('ALLTRIALTYPES_OTHER_SACCADE_heatmap_subj_%s'%('ALLSUBJECTS')); 
	#set a legend. first, get the maximal value in the array to define a legend
	m = round(max(map(max,agg_array))); #,1);
	cb = colorbar(pad = 0.1, ticks = linspace(0,m,3), format = '%2.1f'); cb.outline.set_linewidth(2.0);	
	savefig(figurepath+'heatmaps/SACCADE_HEATMAPS/'+'ALLTRIALTYPES_OTHER_SACCADES_heatmap_subj_%s.png'%('ALLSUBJECTS'));						
	
	1/0;


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
				#set a legend. first, get the maximal value in the array to define a legend
				m = round(max(map(max,subj_arrays[subj_nr])),1);
				cb = colorbar(pad = 0.1, ticks = linspace(0,m,3)); cb.outline.set_linewidth(2.0);
				savefig(figurepath+'heatmaps/SACCADE_HEATMAPS/'+'%s_ALL_SACCADES_heatmap_subj_%s.png'%(name, subj_nr));
				
# 3. Aggregate across subjects by finding the average fixation accumulation		
			
	for su in zip(subj_arrays):
		agg_array += su[0]; #add each subjects' heat maps together	
	agg_array = agg_array/len(block_matrix); #to get the average
	
	#create and save the figure
	figure(); imshow(agg_array, cmap='hot'); title('%s_ALL_SACCADE_heatmap_subj_%s'%(name,'ALLSUBJECTS'));
	#set a legend. first, get the maximal value in the array to define a legend
	m = round(max(map(max,agg_array)),1);
	cb = colorbar(pad = 0.1, ticks = linspace(0,m,3), format = '%2.1f'); cb.outline.set_linewidth(2.0);
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
				#set a legend. first, get the maximal value in the array to define a legend
				m = round(max(map(max,subj_arrays[subj_nr])),1);
				cb = colorbar(pad = 0.1, ticks = linspace(0,m,3)); cb.outline.set_linewidth(2.0);
				savefig(figurepath+'heatmaps/SACCADE_HEATMAPS/'+'ALLTRIALTYPES_ALL_SACCADES_heatmap_subj_%s.png'%(subj_nr));
				
# 3. Aggregate across subjects by finding the average fixation accumulation		
			
	for su in zip(subj_arrays):
		agg_array += su[0]; #add each subjects' heat maps together	
	agg_array = agg_array/len(block_matrix); #to get the average
	
	#create and save the figure
	figure(); imshow(agg_array, cmap='hot'); title('ALLTRIALTYPES_ALL_SACCADE_heatmap_subj_%s'%('ALLSUBJECTS'));
	#set a legend. first, get the maximal value in the array to define a legend
	m = round(max(map(max,agg_array)),1);
	cb = colorbar(pad = 0.1, ticks = linspace(0,m,3), format = '%2.1f'); cb.outline.set_linewidth(2.0);
	savefig(figurepath+'heatmaps/SACCADE_HEATMAPS/'+'ALLTRIALTYPES_ALL_SACCADES_heatmap_subj_%s.png'%('ALLSUBJECTS'));
	
	
	
##### Old Code #####

### computation of first saccade latency data, looking at population distributions

	# #now calculate population stats for latency and amplitude, and plot
	# all_lats = [l for lat in onset_latencies for l in lat];
	# all_amps = [a for am in amplitudes for a in am];
	# mew_latencies = array([mean(lat) for lat in onset_latencies]);
	# latencies_sems = compute_BS_SEM(mew_latencies);
	# mew_amps = array([mean(lat) for lat in amplitudes]);
	# amps_sems = compute_BS_SEM(mew_amps);
	# 
	# 
	# #plot the distribution of saccadic latencies across all participants
	# 
	# fig = figure(figsize = (12.8,7.64)); ax1=gca(); #grid(True);
	# #ax1.set_ylim(0, 0.8); ax1.set_yticks(arange(0, 0.81, 0.1)); #ax1.set_xlim([0.5,1.7]); ax1.set_xticks([0.85, 1.15, 1.45]);
	# ax1.set_ylabel('Frequency',size=18); ax1.set_xlabel('Onset latency',size=18,labelpad=15);
	# ax1.hist(all_lats);
	# 
	# ax1.spines['right'].set_visible(False); ax1.spines['top'].set_visible(False);
	# ax1.spines['bottom'].set_linewidth(2.0); ax1.spines['left'].set_linewidth(2.0);
	# ax1.yaxis.set_ticks_position('left'); ax1.xaxis.set_ticks_position('bottom');
	# title('Population average saccadic latencies for first saccades', fontsize = 22);
	# 
	# #add text detailing the mean saccadic latency
	# fig.text(0.7, 0.48, 'MEAN LATENCY:\n %s +- %s ms '%(round(mean(mew_latencies)),round(latencies_sems)),size=16,weight='bold');
	# 
	# #save the figure
	# savefig(figurepath+ 'SaccadeKinematics/' + 'FIRST_SACCADE_ONSET_DISTRIBUTION_ALLSUBJECTS.png');	
	# 
	# #now plot distribution of amplitudes
	# 
	# fig = figure(figsize = (12.8,7.64)); ax=gca(); #grid(True);
	# #ax1.set_ylim(0, 0.8); ax1.set_yticks(arange(0, 0.81, 0.1)); #ax1.set_xlim([0.5,1.7]); ax1.set_xticks([0.85, 1.15, 1.45]);
	# ax.set_ylabel('Frequency',size=18); ax.set_xlabel('Saccade amplitude',size=18,labelpad=15);
	# ax.hist(all_amps, color = 'darkgray');
	# 
	# ax.spines['right'].set_visible(False); ax.spines['top'].set_visible(False);
	# ax.spines['bottom'].set_linewidth(2.0); ax.spines['left'].set_linewidth(2.0);
	# ax.yaxis.set_ticks_position('left'); ax.xaxis.set_ticks_position('bottom');
	# title('Population average saccadic amplitudes for first saccades', fontsize = 22);
	# 
	# #add text detailing the mean saccadic latency
	# fig.text(0.7, 0.48, 'MEAN AMPLITUDE:\n %s +- %s degrees '%(round(mean(mew_amps)),round(amps_sems)),size=16,weight='bold');
	# 
	# #save the figure
	# savefig(figurepath+ 'SaccadeKinematics/' + 'FIRST_SACCADE_AMPLITUDE_DISTRIBUTION_ALLSUBJECTS.png');
	# 
	# 
	# #Belwo here, check out fast latency saccades
	# 
	# #now, plot the distribution of very fast sacadic latencies, with a greater resoultion for anticipatory saccades:
	# 
	# fast_lats = [l for l in all_lats if l<250];
	# 
	# fig = figure(figsize = (12.8,7.64)); ax1=gca(); #grid(True);
	# #ax1.set_ylim(0, 0.8); ax1.set_yticks(arange(0, 0.81, 0.1)); #ax1.set_xlim([0.5,1.7]); ax1.set_xticks([0.85, 1.15, 1.45]);
	# ax1.set_ylabel('Frequency',size=18); ax1.set_xlabel('Onset latency',size=18,labelpad=15);
	# ax1.hist(fast_lats, bins = [0,25,50,75,100,125,150,175,200,225,250], color = 'green', edgecolor = 'black');
	# 
	# ax1.spines['right'].set_visible(False); ax1.spines['top'].set_visible(False);
	# ax1.spines['bottom'].set_linewidth(2.0); ax1.spines['left'].set_linewidth(2.0);
	# ax1.yaxis.set_ticks_position('left'); ax1.xaxis.set_ticks_position('bottom');
	# title('Population average saccadic latencies for \n FAST LATENCY (<250 ms) first saccades', fontsize = 22);
	# 
	# #add text detailing the mean saccadic latency
	# fig.text(0.15, 0.48, 'POPULATION MEAN LATENCY:\n %s '%(round(mean(fast_lats))),size=16,weight='bold');
	# 
	# #save the figure
	# savefig(figurepath+ 'SaccadeKinematics/' + 'FASTLATENCY_FIRST_SACCADE_ONSET_DISTRIBUTION_ALLSUBJECTS.png');		
	# 
	# # Now find the number of fast (< 100 ms) saccades for each participant, find an average, and SEMs
	# anticipatory_mews = [mean(o) for o in anticipatory_latencies];
	# anticipatory_lens = [len(o) for o in anticipatory_latencies];
	# 
	# mew_ant_lat = nanmean(anticipatory_mews);
	# sems_ant_lat = compute_BS_SEM(anticipatory_mews);
	# mew_ant_nr = nanmean(anticipatory_lens);
	# sems_ant_nr = compute_BS_SEM(anticipatory_lens);
	# 
	# print('\n\n #### ANTICIPATORY SACCADE DATA: #### \n\n\n');
	# print('\n\n MEAN LATENCY OF ANTICIPATORY 1ST SACCADES:\n %s +- %s\n\n'%(mew_ant_lat,sems_ant_lat));
	# print('\n\n MEAN NR ANTICIPATORY 1ST SACCADES:\n %s +- %s\n\n'%(mew_ant_nr, sems_ant_nr));


# def computeSaccadePolarCoordinateData(block_matrix):
# #This function is designed to find and plot the polar coordinate data (amplitude (r) and angle (theta))
# #This will be done for primary saccades (between objects) as well as corrective saccades (fast latencies)
# # here is the function for theta: degrees(atan((y2 - y1)/(x2 - x1))). x1 and y1 should be the origin, but
# # many saccades do not start from there
# 
# # #first, do this for only ANTICIPATORY first saccades
# # 
# # 	thetas = [[] for su in block_matrix];
# # 	amplitudes = [[] for su in block_matrix];
# # 	nr_saccades = [[0] for su in block_matrix];
# # 
# # 	#loop through each trial and score whether trial was excluded because of a dropped sample
# # 	for subj_nr, blocks in enumerate(block_matrix):
# # 		for b in blocks:
# # 			for t in b.trials:
# # 				if ((t.dropped_sample == 0)&(t.didntLookAtAnyItems == 0)&
# # 					(t.skip == 0)&(sqrt(t.eyeX[0]**2 + t.eyeY[0]**2) < 2.5)):
# # 					
# # 					if (t.nr_saccades > 0):  #this conditional is used to ensure that no trials without saccades sneak through
# # 						
# # 						#for each saccades, we have a starting and end point. This gives us a vector, which can be used to
# # 						#determine the angle of the saccade, relative to the saccade starting point. To do this, need to
# # 						# subtract the end point from starting point to find the difference, then use atan(y_length/x_length)
# # 						sac_start_pos = array([]);						
# # 						sac_end_pos = array([]);
# # 						sac_start_time = 0;
# # 						sac_end_time = 0;
# # 						
# # 						#Below here goes through each trial and pulls out the first saccde
# # 						# the while loop below runs through until a saccade is found (saccade_counter = 1) or
# # 						# we get to the end of the trial
# # 						
# # 						saccade_counter = 0;
# # 						while saccade_counter==0:
# # 							for ii,xx,yy,issac in zip(range(len(t.sample_times)),
# # 																 t.eyeX, t.eyeY, t.isSaccade):
# # 								#if no saccade has been made yet, keep running through the isSaccade array
# # 								# issac < 1 will be zero at all non-saccading time points, including the start
# # 								if issac == 0:
# # 									#if the previous sample was saccading and now it isn't, the first saccade is complete and we can grab the data
# # 									if (t.isSaccade[ii-1]==True)&(ii>0):
# # 										sac_end_time = t.sample_times[ii];
# # 										sac_end_pos = array([xx,yy]);
# # 										saccade_counter+=1;
# # 									
# # 									#if there is no saccade, this will trigger the stop I need to move out of the infinite loop	
# # 									if (ii == range(len(t.sample_times))[-1]):
# # 										saccade_counter = 100;
# # 										
# # 								elif issac == 1:
# # 									#get the starting point for this saccade as well as the time
# # 									#the first transition between 0 and 1 will be the first saccade start
# # 									if (t.isSaccade[ii-1]==False)&(ii>0)&(saccade_counter==0):
# # 										sac_start_time = t.sample_times[ii];
# # 										sac_start_pos = array([xx,yy]);						
# # 						
# # 						#calculate the latency and amplitude, then save to the subject's array
# # 						if sac_start_time<100:
# # 							nr_saccades[subj_nr][0]+=1;
# # 							y_length = sac_end_pos[1] - sac_start_pos[1]; #find the length of the y dimension of the saccade
# # 							x_length = sac_end_pos[0] - sac_start_pos[0]; #find the length of the x dimension of the saccade
# # 							#^ note that using end - start is important for the theta calculation below
# # 							amplitudes[subj_nr].append(sqrt((x_length)**2+(y_length)**2));
# # 							
# # 							#calculate theta
# # 							theta = degrees(atan(y_length/x_length));
# # 							#correct theta for 'being' in a Quadrant other than 1, i.e. having the corresponding x and y values
# # 							# simplfied explanation here: (https://www.mathsisfun.com/polar-cartesian-coordinates.html)
# # 							# if both x and y values are positivie (Q 1), no correction needed
# # 							# if x is negative and y is positive (Q2) or x is negative and y is negative (Q3), add 180
# # 							# if x is positive but y is negative (Q4), add 360
# # 							if (sign(x_length)==1)&(sign(y_length)==1): #Q1
# # 								theta = theta;
# # 							elif (sign(x_length)==-1)&(sign(y_length)==1): #Q2
# # 								theta = theta + 180;
# # 							elif (sign(x_length)==-1)&(sign(y_length)==-1): #Q3
# # 								theta = theta + 180;
# # 							elif (sign(x_length)==1)&(sign(y_length)==-1):	#Q4
# # 								theta = theta + 360;
# # 							thetas[subj_nr].append(theta);
# # 							
# # 											
# # 	#now calculate population stats for latency and amplitude, and plot
# # 	all_thetas = [l for lat in thetas for l in lat];
# # 	all_amps = [a for am in amplitudes for a in am];
# # 	mew_amps = array([mean(lat) for lat in amplitudes]);
# # 	amps_sems = compute_BS_SEM(mew_amps);
# # 	
# # 	#calculate the circular mean for angles
# # 	#mew_thetas = array([mean(t) for t in thetas]);
# # 	#thetas_sems = compute_BS_SEM(mew_thetas);
# # 	
# # 	#plot the angles
# # 	fig = figure(figsize = (11,6.5)); ax=subplot(111, polar=True); #gca(); #grid(True);
# # 	ax.set_ylim(0, 1.1); ax.set_yticks([]); 
# # 	ax.set_xlabel('Saccade angle',size=16,labelpad=7); #ax.set_ylabel('Frequency',size=18);
# # 	ax.plot(all_thetas, ones(len(all_thetas)), 'ro', markersize = 10);
# # 	#ax.spines['polar'].set_linewidth(2.0);  #couldn't get this to work
# # 	ax.yaxis.set_ticks_position('left'); ax.xaxis.set_ticks_position('bottom');
# # 	#ax.set_title('Population anticipatory saccade (<100 ms) angular direction', fontsize = 20);
# # 	title('Population anticipatory saccade (<100 ms) angular direction', fontsize = 18);	
# # 						
# # 	1/0;
# 
# 	#next, find the difference in angles between a first saccade and a subsequently executed, concurrently planned (<125 ms) saccade
# 	thetas = [[] for su in block_matrix];
# 	amplitudes = [[] for su in block_matrix];
# 	nr_saccades = [[0] for su in block_matrix];
# 
# 	#loop through each trial and score whether trial was excluded because of a dropped sample
# 	for subj_nr, blocks in enumerate(block_matrix):
# 		for b in blocks:
# 			for t in b.trials:
# 				if ((t.dropped_sample == 0)&(t.didntLookAtAnyItems == 0)&
# 					(t.skip == 0)&(sqrt(t.eyeX[0]**2 + t.eyeY[0]**2) < 2.5)):
# 					
# 					if (t.nr_saccades > 0):  #this conditional is used to ensure that no trials without saccades sneak through
# 
# 						#for each saccades, we have a starting and end point. This gives us a vector, which can be used to
# 						#determine the angle of the saccade, relative to the saccade starting point. To do this, need to
# 						# subtract the end point from starting point to find the difference, then use atan(y_length/x_length)
# 						#pri is primary (first), sec is secondary (concurrently planned)
# 						pri_sac_start_pos = array([]);						
# 						pri_sac_end_pos = array([]);
# 						pri_sac_start_time = 0;
# 						pri_sac_end_time = 0;
# 						pri_sac_latency = 0;
# 						sec_sac_start_pos = array([]);						
# 						sec_sac_end_pos = array([]);
# 						sec_sac_start_time = 0;
# 						sec_sac_end_time = 0;
# 						sec_sac_latency = 0;
# 						
# 						saccade_counter = 0;
# 						for ii,xx,yy,issac in zip(range(len(t.sample_times)),
# 															 t.eyeX, t.eyeY, t.isSaccade):
# 							#if no saccade has been made yet, keep running through the isSaccade array
# 							# issac < 1 will be zero at all non-saccading time points, including the start
# 							if issac == 0:
# 								#if the previous sample was saccading and now it isn't, the first saccade is complete and we can grab the data
# 								if (t.isSaccade[ii-1]==True)&(ii>0):
# 									
# 									if saccade_counter==0: #this will be the case if this is the first saccade
# 										pri_sac_end_time = t.sample_times[ii];
# 										pri_sac_end_pos = array([xx,yy]);
# 										saccade_counter+=1;
# 
# 									else:   #this will occur if we already have a primary saccade
# 										
# 										#if saccade_counter==1:
# 											#this is the first time we have a second saccade
# 											# get the saccadic latency of the second saccade
# 											
# 										#now I don't think I need to do anything differently at this point for first and other saccades	
# 										sec_sac_end_time = t.sample_times[ii];
# 										sec_sac_end_pos = array([xx,yy]);
# 										sec_sac_latency = sec_sac_start_time - pri_sac_end_time;
# 										saccade_counter += 1;
# 											
# 										# elif saccade_counter > 1:
# 										# 	sec_sac_end_time = t.sample_times[ii];
# 										# 	sec_sac_end_pos = array([xx,yy]);
# 										# 	sec_sac_latency = sec_sac_start_time - pri_sac_end_time;											
# 										# 	saccade_counter += 1;
# 											
# 										#check if the latency is less than 125 ms
# 										if sec_sac_latency<125:
# 											#now, find the angle of primary saccade and second saccade
# 											pri_y_length = pri_sac_end_pos[1] - pri_sac_start_pos[1]; #find the length of the y dimension of the saccade
# 											pri_x_length = pri_sac_end_pos[0] - pri_sac_start_pos[0]; #find the length of the x dimension of the saccade
# 											#^ note that using end - start is important for the theta calculation below
# 											
# 											#calculate theta
# 											pri_theta = degrees(atan(pri_y_length/pri_x_length));
# 											#correct theta for 'being' in a Quadrant other than 1, i.e. having the corresponding x and y values
# 											# simplfied explanation here: (https://www.mathsisfun.com/polar-cartesian-coordinates.html)
# 											# if both x and y values are positivie (Q 1), no correction needed
# 											# if x is negative and y is positive (Q2) or x is negative and y is negative (Q3), add 180
# 											# if x is positive but y is negative (Q4), add 360
# 											if (sign(pri_x_length)==1)&(sign(pri_y_length)==1): #Q1
# 												pri_theta = pri_theta;
# 											elif (sign(pri_x_length)==-1)&(sign(pri_y_length)==1): #Q2
# 												pri_theta = pri_theta + 180;
# 											elif (sign(pri_x_length)==-1)&(sign(pri_y_length)==-1): #Q3
# 												pri_theta = pri_theta + 180;
# 											elif (sign(pri_x_length)==1)&(sign(pri_y_length)==-1):	#Q4
# 												pri_theta = pri_theta + 360;												
# 												
# 												
# 											#secondary saccade
# 											sec_y_length = sec_sac_end_pos[1] - sec_sac_start_pos[1]; #find the length of the y dimension of the saccade
# 											sec_x_length = sec_sac_end_pos[0] - sec_sac_start_pos[0]; #find the length of the x dimension of the saccade
# 											
# 											#calculate theta
# 											sec_theta = degrees(atan(sec_y_length/sec_x_length));
# 											if (sign(sec_x_length)==1)&(sign(sec_y_length)==1): #Q1
# 												sec_theta = sec_theta;
# 											elif (sign(sec_x_length)==-1)&(sign(sec_y_length)==1): #Q2
# 												sec_theta = sec_theta + 180;
# 											elif (sign(sec_x_length)==-1)&(sign(sec_y_length)==-1): #Q3
# 												sec_theta = sec_theta + 180;
# 											elif (sign(sec_x_length)==1)&(sign(sec_y_length)==-1):	#Q4
# 												sec_theta = sec_theta + 360;
# 																								
# 											#now find the diff betwen pri and sec	
# 											theta_diff = sec_theta - pri_theta;
# 											#^0 is the same angle, positive means more counterclockwise for second saccade,
# 											#negtive means more counterclockwise for primary saccade, +-180 = exact opposite
# 											#let's correct the negative ones to make everything positive:
# 											if theta_diff < 0:
# 											 	theta_diff = theta_diff + 360;
# 											#now, less than 180 = second saccade was more counterclockwise than first saccade
# 											# and greater than 180 means first saccade was more counterclockwise than second saccade
# 											thetas[subj_nr].append(theta_diff);
# 											amplitudes[subj_nr].append(sqrt((sec_x_length)**2+(sec_y_length)**2));
# 										
# 									
# 							elif issac == 1:
# 								#get the starting point for this saccade as well as the time
# 								#the first transition between 0 and 1 will be the first saccade start
# 								if (t.isSaccade[ii-1]==False)&(ii>0)&(saccade_counter==0):
# 									pri_sac_start_time = t.sample_times[ii];
# 									pri_sac_start_pos = array([xx,yy]);
# 									pri_sac_latency = pri_sac_start_time; #get the latency of the first saccade
# 									
# 								elif (t.isSaccade[ii-1]==False)&(ii>0)&(saccade_counter>0):
# 									if saccade_counter == 1:
# 										#first time we have a second saccade, fill up the secondary saccade data
# 										sec_sac_start_time = t.sample_times[ii];
# 										sec_sac_start_pos = array([xx,yy]);
# 									elif saccade_counter > 1:
# 										#we will already have a secondary saccade, hand off the secondary saccade stuff to the primary saccade
# 										pri_sac_start_time = sec_sac_start_time;
# 										pri_sac_start_position = sec_sac_start_pos;
# 										pri_sac_end_time = sec_sac_end_time;
# 										pri_sac_end_position = sec_sac_end_pos;
# 										pri_sac_latency = pri_sac_end_time  - pri_sac_start_time;
# 										sec_sac_start_time = t.sample_times[ii];
# 										sec_sac_start_pos = array([xx,yy]);
# 										
# 	#now calculate population stats for latency and amplitude, and plot
# 	all_thetas = [l for lat in thetas for l in lat];
# 	all_amps = [a for am in amplitudes for a in am];
# 	mew_amps = array([mean(lat) for lat in amplitudes]);
# 	amps_sems = compute_BS_SEM(mew_amps);
# 	
# 	#calculate the circular mean for angles
# 	#mew_thetas = array([mean(t) for t in thetas]);
# 	#thetas_sems = compute_BS_SEM(mew_thetas);
# 	
# 	#plot the angles
# 	fig = figure(figsize = (11,6.5)); ax=subplot(111, polar=True); #gca(); #grid(True);
# 	ax.set_ylim(0, 1.2); ax.set_yticks([]); 
# 	ax.set_xlabel('Saccade angle',size=16,labelpad=7); #ax.set_ylabel('Frequency',size=18);
# 	ax.plot(all_thetas, [r+(randn(1)*0.07) for r in ones(len(all_thetas))], 'ro', markersize = 10, fillstyle = 'none', alpha = 0.4); #the randn() adds jitter in y dimension
# 	#ax.spines['polar'].set_linewidth(2.0);  #couldn't get this to work
# 	ax.yaxis.set_ticks_position('left'); ax.xaxis.set_ticks_position('bottom');
# 	#ax.set_title('Population anticipatory saccade (<100 ms) angular direction', fontsize = 20);
# 	title('Population concurrently planned saccade (<125 ms) relative angular direction\n (2nd saccade angle - 1st saccade angle)', fontsize = 18);
# 
# 	#save the figure
# 	savefig(figurepath+ 'SaccadeKinematics/' + 'CONCURRENT_SACCADE_RELATIVETHETA_DISTRIBUTION_ALLSUBJECTS.png');
# 	
# 	1/0
	