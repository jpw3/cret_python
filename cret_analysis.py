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

distance_threshold = 3.0; #threshold for how far away eye position can be from the coordinates to be considered looking at that item

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

# # this subsequent function determines aspects of the eye tracking data set such as time until first saccade, dwell time on first saccade, etc.
# 
# def computeEarlyTrialData(blocks, eyed='agg'):
# 	
# 	# #import trial-specific data for all participants
# 	# hp_trial_data = pd.read_csv(savepath+'/stim_locked/high_pref_trialdata.csv');
# 	# hcla_trial_data = pd.read_csv(savepath+'/stim_locked/highC_lowA_trialdata.csv');
# 	# lcha_trial_data = pd.read_csv(savepath+'/stim_locked/lowC_highA_trialdata.csv');
# 	# lp_trial_data = pd.read_csv(savepath+'/stim_locked/lowC_lowA_trialdata.csv');
# 	# 
# 	# #collect all the data trial for the first participant (cret 03)
# 	# 
# 	# trial_data = pd.concat([hp_trial_data[hp_trial_data['subject_nr']==1], hcla_trial_data[hcla_trial_data['subject_nr']==1], lcha_trial_data[lcha_trial_data['subject_nr']==1], lp_trial_data[lp_trial_data['subject_nr']==1]]);
# 	#choices = [];
# 	
# 	trial_counter = 0;
# 	#create plot to show first saccades
# 	#first create circles indicating where I'm crediting item assignment
# 	circle1 = pyplot.Circle(left_pic_coors, 4, color='lightgrey');
# 	circle2 = pyplot.Circle(right_pic_coors, 4, color='lightgrey');
# 	circle3 = pyplot.Circle(up_pic_coors, 4, color='lightgrey');
# 
# 	fig = figure(figsize = (11,7.5)); ax = gca(); ax.set_xlim([-display_size[0]/2,display_size[0]/2]); ax.set_ylim([-display_size[1]/2,display_size[1]/2]); #display_size[1]/2,display_size[1]/2]); #figsize = (12.8,7.64)
# 	ax.set_ylabel('Y Position, Degrees of Visual Angle',size=18); ax.set_xlabel('X Position, Degrees of Visual Angle',size=18,labelpad=11); hold(True);
# 	#add the circles
# 	ax.add_artist(circle1);
# 	ax.add_artist(circle2);
# 	ax.add_artist(circle3);
# 	
# 	#ttFS = []; #time to first saccades, average for each participant. for use when doing this for all participants at the same time
# 	
# 	for b in blocks:
# 		trials = [tri for bee in b for tri in bee.trials];
# 		times = []; #to store the time to first saccades for this participant
# 		
# 		for t in trials:
# 			if ((t.dropped_sample == 0)&(t.didntLookAtAnyItems == 0)&(t.skip == 0)): #&(sqrt(t.eyeX[0]**2 + t.eyeY[0]**2) < 2)&(t.trial_type=='high_pref')):
# 				
# 				trial_counter+=1;
# 				
# 				#first plot the eye trace for this trial's first saccade
# 				saccade_counter = 0;
# 				
# 				while saccade_counter==0:
# 					for i,xx,yy,issac in zip(range(len(t.sample_times)),
# 														 t.eyeX, t.eyeY, t.isSaccade):
# 						#plot the eye trace in black if not saccading
# 						if issac == 0:
# 							#ax.plot(xx,yy, color = 'black', marker = 'o', ms = 4);
# 							#conditional to switch to the next saccade color
# 							#if the previous sample was saccading and now it isn't, the first saccade is complete and plotting can stop
# 							if (t.isSaccade[i-1]==True)&(i>0):
# 								ax.plot(xx, yy, marker = 'x', color = 'red', ms = 15);
# 								saccade_counter+=1;
# 							
# 							#if there s no saccade, this will trigger the stop I need to move out of the infinite loop	
# 							if (i == range(len(t.sample_times))[-1]):
# 								saccade_counter = 100;
# 						# else:
# 						# 	if ((t.isSaccade[i-1]==False)&(i>0))|(i==0):
# 						# 		ax.plot(xx, yy, marker = 'x', color = 'green', ms = 7);
# 						# 	else:	
# 						# 		ax.plot(xx, yy, color = 'black', marker = 'o', ms = 4);
# 					
# 				#timing of first saccade
# 				
# 				binaryList = list(t.isSaccade.astype(int));			
# 				firstIndex = binaryList.index(1) if (1 in binaryList) else -1; #get the first index of a '1' in the isSaccade vector, indicating this is when the first saccade occurre			
# 				timeToFirstSaccade = firstIndex + 1 if (firstIndex > 0) else -1; #get the time point in ms of the first saccade to this trial, -1 means no saccade occurred
# 	
# 				#add this time to the list if they made a saccade in this time window
# 				if (timeToFirstSaccade > 0):
# 					times.append(timeToFirstSaccade); #choices.append(t.preferred_category)			
# 					
# 	ax.spines['right'].set_visible(False); ax.spines['top'].set_visible(False);
# 	ax.spines['bottom'].set_linewidth(2.0); ax.spines['left'].set_linewidth(2.0);
# 	ax.yaxis.set_ticks_position('left'); ax.xaxis.set_ticks_position('bottom');
# 	#ax.legend(handles=[hand for hand in legend_lines],loc = 2,ncol=3,fontsize = 10); 
# 	title('First Saccade Endpoints\n Subject %s'%(t.sub_id), fontsize = 22);					
# 
# 	#histogram the time until first saccades
# 	ia = inset_axes(ax, width="15%", height="25%", loc=1); #set the inset axes as percentages of the original axis size
# 	hist(times);
# 	ia.set_ylabel('Frequency', fontsize = 14); ia.set_xlabel('Latency', fontsize = 14); title('First saccade latencies', fontsize = 14);			
# 	mew_latency = mean(times);
# 	
# 	#add text detailing the mean saccadic latency
# 	fig.text(0.8, 0.48, 'MEAN LATENCY:\n %s ms'%(round(mew_latency)),size=16,weight='bold');
# 	
# 	
# 	#save the figure
# 	savefig(figurepath+'ALLTRIALS_first_saccade_data_subj_%s.png'%(t.sub_id));	
# 	
# 	## #now create the figures for the second saccade data
# 	
# 	#first create circles indicating where I'm crediting item assignment
# 	circle1 = pyplot.Circle(left_pic_coors, 4, color='lightgrey');
# 	circle2 = pyplot.Circle(right_pic_coors, 4, color='lightgrey');
# 	circle3 = pyplot.Circle(up_pic_coors, 4, color='lightgrey');
# 	
# 	fig = figure(figsize = (11,7.5)); ax = gca(); ax.set_xlim([-display_size[0]/2,display_size[0]/2]); ax.set_ylim([-display_size[0]/2,display_size[0]/2]); #display_size[1]/2,display_size[1]/2]); #figsize = (12.8,7.64)
# 	ax.set_ylabel('Y Position, Degrees of Visual Angle',size=18); ax.set_xlabel('X Position, Degrees of Visual Angle',size=18,labelpad=11); hold(True);
# 	#add the circles
# 	ax.add_artist(circle1);
# 	ax.add_artist(circle2);
# 	ax.add_artist(circle3);	
# 	
# 	dwell_times = [];
# 	
# 	for b in blocks:
# 		trials = [tri for bee in b for tri in bee.trials];
# 		times = []; #to store the time to first saccades for this participant
# 		
# 		for t in trials:
# 			if ((t.dropped_sample == 0)&(t.didntLookAtAnyItems == 0)&(t.skip == 0)): # &(t.nr_saccades>1)):
# 				
# 				dt = 0; #dwell time for this participants
# 				
# 				#first plot the eye trace for this trial's first saccade
# 				saccade_counter = 0;
# 				
# 				while saccade_counter<2:
# 					for i,xx,yy,issac in zip(range(len(t.sample_times)),
# 														 t.eyeX, t.eyeY, t.isSaccade):
# 						#plot the eye trace in black if not saccading
# 						if issac == 0:
# 							if (saccade_counter==1)&(t.isSaccade[i-1]==False):
# 								dt+=1;							
# 							#if the previous sample was saccading and now it isn't, the first saccade is complete and plotting can stop
# 							if (t.isSaccade[i-1]==True)&(i>0):
# 								#conditional checks if it's the second saccade or not								
# 								if saccade_counter==1:
# 									ax.plot(xx, yy, marker = 'x', color = 'blue', ms = 15);
# 								saccade_counter+=1;
# 								
# 							#if there s no saccade, this will trigger the stop I need to move out of the infinite loop	
# 							if (i == range(len(t.sample_times))[-1]):
# 								saccade_counter = 100;								
# 								
# 				#add this time to the list if they made a saccade in this time window
# 				if (dt > 0):
# 					dwell_times.append(dt);				
# 					
# 	ax.spines['right'].set_visible(False); ax.spines['top'].set_visible(False);
# 	ax.spines['bottom'].set_linewidth(2.0); ax.spines['left'].set_linewidth(2.0);
# 	ax.yaxis.set_ticks_position('left'); ax.xaxis.set_ticks_position('bottom');
# 	#ax.legend(handles=[hand for hand in legend_lines],loc = 2,ncol=3,fontsize = 10); 
# 	title('Second Saccade Endpoints\n Subject %s'%(t.sub_id), fontsize = 22);					
# 
# 	#histogram the time until first saccades
# 	ia = inset_axes(ax, width="15%", height="25%", loc=1); #set the inset axes as percentages of the original axis size
# 	hist(dwell_times);
# 	ia.set_ylabel('Frequency', fontsize = 14); ia.set_xlabel('Latency', fontsize = 14); title('Second saccade latencies', fontsize = 14);			
# 	mew_latency = mean(dwell_times);
# 	
# 	#add text detailing the mean saccadic latency
# 	fig.text(0.8, 0.48, 'MEAN LATENCY:\n %s ms'%(round(mew_latency)),size=16,weight='bold');
# 	
# 	#save the figure
# 	savefig(figurepath+'ALLTRIALS_second_saccade_data_subj_%s.png'%(t.sub_id));
# 	
# 	1/0;	
# 		
# 			#incorporate a conditional to match the trial type
# 			
# 			
# ##the following function does the same thing as above, but only for trials where the first saccade started at the origin
# 
# def computeEarlyTrialDataOriginStartTrialsOnly(blocks, eyed='agg'):
# 	
# 	# #import trial-specific data for all participants
# 	# hp_trial_data = pd.read_csv(savepath+'/stim_locked/high_pref_trialdata.csv');
# 	# hcla_trial_data = pd.read_csv(savepath+'/stim_locked/highC_lowA_trialdata.csv');
# 	# lcha_trial_data = pd.read_csv(savepath+'/stim_locked/lowC_highA_trialdata.csv');
# 	# lp_trial_data = pd.read_csv(savepath+'/stim_locked/lowC_lowA_trialdata.csv');
# 	# 
# 	# #collect all the data trial for the first participant (cret 03)
# 	# 
# 	# trial_data = pd.concat([hp_trial_data[hp_trial_data['subject_nr']==1], hcla_trial_data[hcla_trial_data['subject_nr']==1], lcha_trial_data[lcha_trial_data['subject_nr']==1], lp_trial_data[lp_trial_data['subject_nr']==1]]);
# 	#choices = [];
# 	
# 	#create plot to show first saccades
# 	#first create circles indicating where I'm crediting item assignment
# 	circle1 = pyplot.Circle(left_pic_coors, 4, color='lightgrey');
# 	circle2 = pyplot.Circle(right_pic_coors, 4, color='lightgrey');
# 	circle3 = pyplot.Circle(up_pic_coors, 4, color='lightgrey');
# 
# 	fig = figure(figsize = (11,7.5)); ax = gca(); ax.set_xlim([-display_size[0]/2,display_size[0]/2]); ax.set_ylim([-display_size[0]/2,display_size[0]/2]); #display_size[1]/2,display_size[1]/2]); #figsize = (12.8,7.64)
# 	ax.set_ylabel('Y Position, Degrees of Visual Angle',size=18); ax.set_xlabel('X Position, Degrees of Visual Angle',size=18,labelpad=11); hold(True);
# 	#add the circles
# 	ax.add_artist(circle1);
# 	ax.add_artist(circle2);
# 	ax.add_artist(circle3);
# 	
# 	#ttFS = []; #time to first saccades, average for each participant. for use when doing this for all participants at the same time
# 	trial_counter = 0;
# 	for b in blocks:
# 		trials = [tri for bee in b for tri in bee.trials];
# 		times = []; #to store the time to first saccades for this participant
# 		
# 		for t in trials:
# 			if ((t.dropped_sample == 0)&(t.didntLookAtAnyItems == 0)&(t.skip == 0)&(sqrt(t.eyeX[0]**2 + t.eyeY[0]**2) < 2)): #&(t.trial_type==1)): #
# 				
# 				trial_counter+=1;
# 				#first plot the eye trace for this trial's first saccade
# 				saccade_counter = 0;
# 				
# 				while saccade_counter==0:
# 					for i,xx,yy,issac in zip(range(len(t.sample_times)),
# 														 t.eyeX, t.eyeY, t.isSaccade):
# 						#plot the eye trace in black if not saccading
# 						if issac == 0:
# 							#ax.plot(xx,yy, color = 'black', marker = 'o', ms = 4);
# 							#conditional to switch to the next saccade color
# 							#if the previous sample was saccading and now it isn't, the first saccade is complete and plotting can stop
# 							if (t.isSaccade[i-1]==True)&(i>0):
# 								ax.plot(xx, yy, marker = 'x', color = 'red', ms = 15);
# 								saccade_counter+=1;
# 							#if there s no saccade, this will trigger the stop I need to move out of the infinite loop	
# 							if (i == range(len(t.sample_times))[-1]):
# 								saccade_counter = 100;
# 					
# 				#timing of first saccade
# 				
# 				binaryList = list(t.isSaccade.astype(int));			
# 				firstIndex = binaryList.index(1) if (1 in binaryList) else -1; #get the first index of a '1' in the isSaccade vector, indicating this is when the first saccade occurre			
# 				timeToFirstSaccade = firstIndex + 1 if (firstIndex > 0) else -1; #get the time point in ms of the first saccade to this trial, -1 means no saccade occurred
# 	
# 				#add this time to the list if they made a saccade in this time window
# 				if (timeToFirstSaccade > 0):
# 					times.append(timeToFirstSaccade); #choices.append(t.preferred_category)			
# 					
# 	ax.spines['right'].set_visible(False); ax.spines['top'].set_visible(False);
# 	ax.spines['bottom'].set_linewidth(2.0); ax.spines['left'].set_linewidth(2.0);
# 	ax.yaxis.set_ticks_position('left'); ax.xaxis.set_ticks_position('bottom');
# 	#ax.legend(handles=[hand for hand in legend_lines],loc = 2,ncol=3,fontsize = 10); 
# 	title('First Saccade Endpoints\n Subject %s'%(t.sub_id), fontsize = 22);					
# 
# 	#histogram the time until first saccades
# 	ia = inset_axes(ax, width="15%", height="25%", loc=1); #set the inset axes as percentages of the original axis size
# 	hist(times);
# 	ia.set_ylabel('Frequency', fontsize = 14); ia.set_xlabel('Latency', fontsize = 14); title('First saccade latencies', fontsize = 14);			
# 	mew_latency = mean(times);
# 	
# 	#add text detailing the mean saccadic latency
# 	fig.text(0.8, 0.48, 'MEAN LATENCY:\n %s ms'%(round(mew_latency)),size=16,weight='bold');
# 	
# 	#save the figure
# 	savefig(figurepath+'ORIGINSTARTTRIALS_first_saccade_data_subj_%s.png'%(t.sub_id));	
# 	
# 	## #now create the figures for the second saccade data
# 	
# 	#first create circles indicating where I'm crediting item assignment
# 	circle1 = pyplot.Circle(left_pic_coors, 4, color='lightgrey');
# 	circle2 = pyplot.Circle(right_pic_coors, 4, color='lightgrey');
# 	circle3 = pyplot.Circle(up_pic_coors, 4, color='lightgrey');
# 	
# 	fig = figure(figsize = (11,7.5)); ax = gca(); ax.set_xlim([-display_size[0]/2,display_size[0]/2]); ax.set_ylim([-display_size[0]/2,display_size[0]/2]); #display_size[1]/2,display_size[1]/2]); #figsize = (12.8,7.64)
# 	ax.set_ylabel('Y Position, Degrees of Visual Angle',size=18); ax.set_xlabel('X Position, Degrees of Visual Angle',size=18,labelpad=11); hold(True);
# 	#add the circles
# 	ax.add_artist(circle1);
# 	ax.add_artist(circle2);
# 	ax.add_artist(circle3);	
# 	
# 	dwell_times = [];
# 	
# 	for b in blocks:
# 		trials = [tri for bee in b for tri in bee.trials];
# 		times = []; #to store the time to first saccades for this participant
# 		
# 		for t in trials:
# 			if ((t.dropped_sample == 0)&(t.didntLookAtAnyItems == 0)&(t.skip == 0)&(sqrt(t.eyeX[0]**2 + t.eyeY[0]**2) < 2)): # &(t.nr_saccades>1)):
# 				
# 				dt = 0; #dwell time for this participants
# 				
# 				#first plot the eye trace for this trial's first saccade
# 				saccade_counter = 0;
# 				
# 				while saccade_counter<2:
# 					for i,xx,yy,issac in zip(range(len(t.sample_times)),
# 														 t.eyeX, t.eyeY, t.isSaccade):
# 						#plot the eye trace in black if not saccading
# 						if issac == 0:
# 							if (saccade_counter==1)&(t.isSaccade[i-1]==False):
# 								dt+=1;							
# 							#if the previous sample was saccading and now it isn't, the first saccade is complete and plotting can stop
# 							if (t.isSaccade[i-1]==True)&(i>0):
# 								#conditional checks if it's the second saccade or not								
# 								if saccade_counter==1:
# 									ax.plot(xx, yy, marker = 'x', color = 'blue', ms = 15);
# 								saccade_counter+=1;
# 							#if there s no saccade, this will trigger the stop I need to move out of the infinite loop	
# 							if (i == range(len(t.sample_times))[-1]):
# 								saccade_counter = 100;
# 								
# 				#add this time to the list if they made a saccade in this time window
# 				if (dt > 0):
# 					dwell_times.append(dt);				
# 					
# 	ax.spines['right'].set_visible(False); ax.spines['top'].set_visible(False);
# 	ax.spines['bottom'].set_linewidth(2.0); ax.spines['left'].set_linewidth(2.0);
# 	ax.yaxis.set_ticks_position('left'); ax.xaxis.set_ticks_position('bottom');
# 	#ax.legend(handles=[hand for hand in legend_lines],loc = 2,ncol=3,fontsize = 10); 
# 	title('Second Saccade Endpoints\n Subject %s'%(t.sub_id), fontsize = 22);					
# 
# 	#histogram the time until first saccades
# 	ia = inset_axes(ax, width="15%", height="25%", loc=1); #set the inset axes as percentages of the original axis size
# 	hist(dwell_times);
# 	ia.set_ylabel('Frequency', fontsize = 14); ia.set_xlabel('Latency', fontsize = 14); title('Second saccade latencies', fontsize = 14);			
# 	mew_latency = mean(dwell_times);
# 	
# 	#add text detailing the mean saccadic latency
# 	fig.text(0.8, 0.48, 'MEAN LATENCY:\n %s ms'%(round(mew_latency)),size=16,weight='bold');
# 	
# 	#save the figure
# 	savefig(figurepath+'ORIGINSTARTTRIALS_second_saccade_data_subj_%s.png'%(t.sub_id));
# 	
# 	1/0;	
			


def collectTemporalGazeProfileTrialsRawTimecourse(blocks, ttype, eyed = 'agg'):
	#collects each participants' trial data where they didn't blink or look down
	#this collects trial with respect to the onset of the first saccade
    #this collects time points according to their raw time course, rather than normalized to 100 equally spaced time points
	
	#loop through and get all the trials for each subject
    trial_matrix = [[tee for b in bl for tee in b.trials if (tee.skip==0)] for bl in blocks];
	
	#collect which trial type to run this analysis for
	#ttype = int(raw_input('Which trial type? 1 = HighC/HighA, 2 = HighC/LowA, 3 = LowC/HighA, 4 = LowC/LowA: '));
	
    name = ['high_pref', 'highC_lowA','lowC_highA','lowC_lowA'][ttype-1];
	
    data = pd.DataFrame(columns = concatenate([['subject_nr', 'trial_type', 'selected_item','block_nr','trial_nr','first_sac_latency','first_sac_item','last_sac_item','nr_dwells','prev_trial_last_dwelled_loc','prev_trial_type','prev_choice'] \
        ,['t_%s'%(t) for t in linspace(1,10000,10000)]])); #add all participants together to the same dataFrame for simplicty
    #maximum length of trial across all participants is ~9.5 seconds, so adding up to 100000 data points to include all time points        
	#SCORING FOR ITEM (entry at t_XX): 0 = not looked at any item, 1 = looked at alcohol, 2 = looked at cigarette, 3 = looked at neutral, nan = timepoint didn't exist in the trial
    trial_index_counter = 0;
	
    for subj_nr,subj in zip(ids, trial_matrix):    #enumerate(trial_matrix):

        for i,t in enumerate(subj):
			#conditional to differentiate between trials that should be skipped for this trial type, etc.
            if((t.dropped_sample == 0)&(t.didntLookAtAnyItems == 0)&(t.trial_type == ttype)&(t.skip == 0)&(sqrt(t.eyeX[0]**2 + t.eyeY[0]**2) < 2.5)):
                
                if (t.nr_saccades > 0):  #this conditional is used to ensure that no trials without saccades sneak through
                
                    #0. first, get first saccade latency, first saccade item identity, nr of dwells on current trial
                    #need the first saccade latency before collecting the gaze data, otherwise I can't align the data according to the first saccade onset

                    #this code gets the first saccade latency
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
                                saccade_counter+=1;
                                break; #once I get the first saccade, end it here
                            

                                
                        elif issac == 1:
                            #get the starting point for this saccade as well as the time
                            #the first transition between 0 and 1 will be the first saccade start
                            if (t.isSaccade[ii-1]==False)&(ii>0)&(saccade_counter==0):
                                sac_start_time = t.sample_times[ii];
                                sac_start_pos = array([xx,yy]);       
                    
                    #calculate the first saccade latency
                    first_sac_onset_latency = sac_start_time; 

                    #get the first item looked at			
                    if t.firstCategoryLookedAt=='alcohol':
                        first_sac_item_identity = 1;
                    elif t.firstCategoryLookedAt=='cigarette':
                        first_sac_item_identity = 2;
                    elif t.firstCategoryLookedAt=='neutral':
                        first_sac_item_identity = 3;

                    #get the last item looked at
                    if t.lastCategoryLookedAt=='alcohol':
                        last_sac_item_identity = 1;
                    elif t.lastCategoryLookedAt=='cigarette':
                        last_sac_item_identity = 2;
                    elif t.lastCategoryLookedAt=='neutral':
                        last_sac_item_identity = 3;						

                    #now here collect the total number of dwells
                    rexp_pattern = re.compile(r'01'); #this regular expression pattern looks for strings with a 1 or anything continuous run of 1s
					#In the computation of the lookedAtXX arrays during trial pre-processing, I include NaNs at times when no itm
					#was looked at... e.g., when the participant was fixating the center of the screen.
					#In order to ensure that I capture the change from not looking at one item to looking at any item (like the first dwell),
					#I need to convert those NaNs to 0's for calculation using the string-based method below. However, I want the original
					#lookedAtXX arrays to maintain the Nan, 0, 1 coding scheme, so I'll create holder arrays for each trial to use for the nr of dwell
					#calculations here
					
                    looked_at_alcohol = array([r if ((r==0)|(r==1)) else 0 for r in t.lookedAtAlcohol]);
                    looked_at_cigarette = array([r if ((r==0)|(r==1)) else 0 for r in t.lookedAtCigarette]);
                    looked_at_neutral = array([r if ((r==0)|(r==1)) else 0 for r in t.lookedAtNeutral]);
					
                    total_holder = 0;
					
                    str_alc = ''.join(str(int(g)) for g in looked_at_alcohol if not(isnan(g))); #first get the array into a string
                    run_lengths_alc = [len(f) for f in rexp_pattern.findall(str_alc)];
					#line above, then use the regular expression pattern, looking for 1s, to parse an array of the continuous runs of 1s in the string from above and get length
                    nr_fixs = sum([1 for r in run_lengths_alc]);
					#check if the first item is a 1... if so, the array started with looking at the item and it wouldnt be caught by the regexp.
					#this will only be the case if they weren't looking at anything to start (e.g., there were nan's to start, then the first item was looked at)
					#notice that because I have included NaNs in the t.lookedAtXX arrays for when items are not being looked at, the subsequent str_alc array
					#represents sequences of 1s and 0 s corresponding runs of looking at items, squished into the array; This means str_alc does not include
					#any information about samples where the eye was not on an item, which means this method cannot be used to understand differences in time between
					#dwells when that time is not being spent on an item. This is important to keep in mind
                    if str_alc[0]=='1':
                        nr_fixs +=1;
				
                    total_holder+=nr_fixs; #add the nr of dwells from looking at alc to this holder variable
					
                    str_cig = ''.join(str(int(g)) for g in looked_at_cigarette if not(isnan(g))); #parse cigarette
                    run_lengths_cig = [len(f) for f in rexp_pattern.findall(str_cig)];
                    nr_fixs = sum([1 for r in run_lengths_cig]);
					#check if the first item is a 1... if so, the array started with looking at the item and it wouldnt be caught by the regexp. need to correcy
                    if str_cig[0]=='1':
                        nr_fixs +=1;

                    total_holder+=nr_fixs; #add the nr of dwells from looking at cig to this holder variable

                    str_neu = ''.join(str(int(g)) for g in looked_at_neutral if not(isnan(g))); #do the parsing for neutral..
                    run_lengths_neu = [len(f) for f in rexp_pattern.findall(str_neu)];
                    nr_fixs = sum([1 for r in run_lengths_neu]);
					#check if the first item is a 1... if so, the array started with looking at the item and it wouldnt be caught by the regexp. need to correcy
                    if str_neu[0]=='1':
                        nr_fixs +=1;

                    total_holder+=nr_fixs; #add the nr of dwells from looking at neu to this holder variable
					
                    total_nr_dwells = total_holder; #this is the variable for collecting total nr of dwells on this trial               
                    

                    #1. get the previous trial last dwelled location and previous trial type
                    #conditional here is to only compute these values if this was not the first trial in a block. If it was, add nan's to these values
                    
                    if t.trial_nr > 1:
                        #this code below finds the location of the last dwell on trial N-1 a
						prev_looked_at_up = array([r if ((r==0)|(r==1)) else 0 for r in subj[i-1].lookedUp]);
						prev_looked_at_left = array([r if ((r==0)|(r==1)) else 0 for r in subj[i-1].lookedLeft]);
						prev_looked_at_right = array([r if ((r==0)|(r==1)) else 0 for r in subj[i-1].lookedRight]);			
        
						str_up = ''.join(str(int(g)) for g in prev_looked_at_up if not(isnan(g))); #first get the array into a string
        
                        #get last instane of the '1' in this array. if never loooked at, will return a -1
						up_indices = str_up.rfind('1'); #rfind searches the string from right to left
                        
						if isinstance(up_indices, int):
							up_last_index_lookedat = up_indices;
						else:
							up_last_index_lookedat = up_indices[0];
                            
						str_left = ''.join(str(int(g)) for g in prev_looked_at_left if not(isnan(g))); #parse cigarette
						left_indices = str_left.rfind('1');		
						if isinstance(left_indices, int):
							left_last_index_lookedat = left_indices;
						else:
							left_last_index_lookedat = left_indices[0];
        
						str_right = ''.join(str(int(g)) for g in prev_looked_at_right if not(isnan(g))); #do the parsing for neutral..
						right_indices = str_right.rfind('1');		
						if isinstance(right_indices, int):
							right_last_index_lookedat = right_indices;
						else:
							right_last_index_lookedat = right_indices[0];
                        
						last_instances =  array([up_last_index_lookedat, left_last_index_lookedat, right_last_index_lookedat]); #always keep it up, left, right
						last_item_index = where(last_instances == max(last_instances))[0][0];		
        
                        #conditonal to find the last item that was looked at accoridng to the index corresponding to the item 
						if last_item_index==0:
							prev_last_dwelled_item = 'up';
						elif last_item_index==1:
							prev_last_dwelled_item = 'left';
						elif last_item_index== 2:
							prev_last_dwelled_item = 'right';
                            
						previous_trial_type = subj[i-1].trial_type; #get the previous trial type
						
						if subj[i-1].preferred_category=='alcohol':
							previous_choice = 1;
						elif subj[i-1].preferred_category=='cigarette':
							previous_choice = 2;
						elif subj[i-1].preferred_category=='neutral':
							previous_choice = 3;    						                       
                    else:
                        prev_last_dwelled_item = nan;
                        previous_trial_type = nan;
                        previous_choice = nan;

                    #2. now finally get the gaze position information, aligning trials to the offset of the first saccade
                    #keep the start of the array nans until the timepoint when the trial has data for it
                    gaze_data = [nan for ja in range(10000)]; #this will be length 5000 and include each item looked at at each time point (or 0/NaN otherwise); pre-allocate with nans                    
                    trial_end_index = len(t.lookedAtNeutral); #get the duration of the trial (e.g., how many samples, corresponding to how many milliseconds)
    
                    #trials longer than 5000 ms will be trimmed to 5000 ms
                    if trial_end_index > 10000:
                        trial_end_index = 10000;
                    
                    iterator = 0; first_sac_offset = sac_end_time; #here, use the saccade end time to ofset the iterator through the gaze data array
                    #now go through for the 5000 time points prior to decision and score whether the paricipants was looking at 
                    for j in (arange(10000)):
                        if ((j+first_sac_offset)>=trial_end_index):
                            continue;					
                        elif (isnan(t.lookedAtNeutral[j+first_sac_offset]) & isnan(t.lookedAtAlcohol[j+first_sac_offset]) & isnan(t.lookedAtCigarette[j+first_sac_offset])):
                            #at this point, there was a nan inserted because the participant did not look at each item
                            #when there are no items looked at, include a 0
                            gaze_data[iterator] = 0;
                        elif (t.lookedAtAlcohol[j+first_sac_offset]==1):
                            gaze_data[iterator] = 1;
                        elif (t.lookedAtCigarette[j+first_sac_offset]==1):						
                            gaze_data[iterator] = 2;						
                        elif (t.lookedAtNeutral[j+first_sac_offset]==1):	
                            gaze_data[iterator] = 3;
                        iterator+=1;
                        
                    #if t.sub_id == ids[-1]: #stop at the subject who had very long RTS   
                    #    1/0; #check the first saccade offset is working as expected, and check if the appropriate thing to do in the first confitional cheking for trial_end_index is appropriate to use the first_sac_offset
                        
                    #for ease of the regression computation, get the selected item into a numerical representation, same mapping as with item looked at
                    if t.preferred_category=='alcohol':
                        selected_item = 1;
                    elif t.preferred_category=='cigarette':
                        selected_item = 2;
                    elif t.preferred_category=='neutral':
                        selected_item = 3;                                  
                        
                    #at this point have collected data for gaze profile together
                    #get all data points together for ease of incorporating into the dataFrame
                    this_trials_data = concatenate([[subj_nr, ttype, selected_item, t.block_nr, t.trial_nr, first_sac_onset_latency, first_sac_item_identity, last_sac_item_identity, \
                                                     total_nr_dwells, prev_last_dwelled_item, previous_trial_type, previous_choice],gaze_data]); #each trial variable, then each timepoint data   int(subj_nr+1)

					
                    #now translate this to the dataframe for this participant
                    data.loc[trial_index_counter] = this_trials_data;
			
                    trial_index_counter += 1; #1/0; #index for next trial
					
				
	print "completed subject %s.. \n\n"%subj_nr	

	#save the database
    data.to_csv(savepath+'first_sac_locked/'+'%s_trialdata.csv'%name,index=False);
	#data.to_csv(savepath+'/stim_locked/'+'%s_trialdata.csv'%name,index=False); #previous iteration of this was to align to the onset of the stimulus
	# ends here


### These next 4 methods compute the 4 specific dependent measures required for the correlative analysis with cue-reactivity paradigm, per meeting with Rachel 6/14/18 ###

def computeFirstItemLookedAt(blocks, eyed='agg'):
	#this function computes the average proportion of trials that the first item that was looked at was the selected item
	db = subject_data;
	
	#loop through and get all the trials for each subject
	trial_matrix = [[tee for b in bl for tee in b.trials if (tee.skip==0)] for bl in blocks];

	#find each subjects' cue substance based on which item them chose more often during PAPC trials where they selected the alcohol or cigarette
	if eyed=='agg':		
		index_counter=0; #index counter for the DataFrame object	
		data = pd.DataFrame(columns = ['sub_id','trial_type','alc_prop_first_fixated','cig_prop_first_fixated','neu_prop_first_fixated',
									   'chose_alc_alc_prop_first_fixated','chose_alc_cig_prop_first_fixated','chose_alc_neu_prop_first_fixated',
									   'chose_cig_alc_prop_first_fixated','chose_cig_cig_prop_first_fixated','chose_cig_neu_prop_first_fixated',
									   'chose_neu_alc_prop_first_fixated','chose_neu_cig_prop_first_fixated','chose_neu_neu_prop_first_fixated']);

	#get the proportion of trials where the last fixated item was alcohol, cigarettes, and neutral items
	#get the aggregate breakdwon as well as when they chose each item
	for ttype, name in zip([1,2,3,4],['high_pref', 'highC_lowA','lowC_highA','lowC_lowA']):	

		alc_first_fixated = [];
		cig_first_fixated = [];
		neu_first_fixated = [];
		chose_alc_alc_first_fixated = [];
		chose_alc_cig_first_fixated = [];
		chose_alc_neu_first_fixated = [];	
		chose_cig_alc_first_fixated = [];
		chose_cig_cig_first_fixated = [];
		chose_cig_neu_first_fixated = [];	
		chose_neu_alc_first_fixated = [];
		chose_neu_cig_first_fixated = [];
		chose_neu_neu_first_fixated = [];	


		#first run the analysis for all trials of this trial type, not breaking it down by whether they chose alcohol, cigeratte, or neutral
		#loop through trials for each subject
		for subj,sub_id in zip(trial_matrix, ids):
			alc_subj = [];
			cig_subj = [];
			neu_subj = [];	
			for t in subj:
				if((t.dropped_sample == 0)&(t.didntLookAtAnyItems == 0)&(t.trial_type == ttype)&
					(t.skip == 0)&(sqrt(t.eyeX[0]**2 + t.eyeY[0]**2) < 2.5)):				
					#conditionally append a 1 or 0 based on which item was last looked at in this trial
					if (t.firstCategoryLookedAt == 'alcohol'):
						alc_subj.append(1);
						cig_subj.append(0);
						neu_subj.append(0);
					elif (t.firstCategoryLookedAt == 'cigarette'):
						alc_subj.append(0);
						cig_subj.append(1);
						neu_subj.append(0);						
					elif (t.firstCategoryLookedAt == 'neutral'):
						alc_subj.append(0);
						cig_subj.append(0);
						neu_subj.append(1);
			alc_first_fixated.append(sum(alc_subj)/float(len(alc_subj)));
			cig_first_fixated.append(sum(cig_subj)/float(len(cig_subj)));
			neu_first_fixated.append(sum(neu_subj)/float(len(neu_subj)));
			
		#below here append averages to the database 
		db['%s_%s_alc_mean_prop_first_fixated_item'%(eyed,name)] = nanmean(alc_first_fixated); db['%s_%s_alc_bs_sems_prop_first_fixated_item'%(eyed,name)] = compute_BS_SEM(alc_first_fixated);
		db['%s_%s_cig_mean_prop_first_fixated_item'%(eyed,name)] = nanmean(cig_first_fixated); db['%s_%s_cig_bs_sems_prop_first_fixated_item'%(eyed,name)] = compute_BS_SEM(cig_first_fixated);
		db['%s_%s_neu_mean_prop_first_fixated_item'%(eyed,name)] = nanmean(neu_first_fixated); db['%s_%s_neu_bs_sems_prop_first_fixated_item'%(eyed,name)] = compute_BS_SEM(neu_first_fixated);
		db.sync();
		
		#now break it down by which item was chosen
		for selected_item in ['alcohol','cigarette','neutral']:			
			#loop through trials for each subject
			for subj,sub_id in zip(trial_matrix, ids):
				
				chose_alc_alc_subj = [];
				chose_alc_cig_subj = [];
				chose_alc_neu_subj = [];			
				chose_cig_alc_subj = [];
				chose_cig_cig_subj = [];
				chose_cig_neu_subj = [];
				chose_neu_alc_subj = [];
				chose_neu_cig_subj = [];
				chose_neu_neu_subj = [];				

				for t in subj:
					if((t.dropped_sample == 0)&(t.didntLookAtAnyItems == 0)&(t.trial_type == ttype)&(t.preferred_category==selected_item)&
						(t.skip == 0)&(sqrt(t.eyeX[0]**2 + t.eyeY[0]**2) < 2.5)):        
				
						#conditional
						if selected_item=='alcohol':
							#conditionally append a 1 or 0 based on which item was last looked at in this trial
							if (t.firstCategoryLookedAt == 'alcohol'):
								chose_alc_alc_subj.append(1);
								chose_alc_cig_subj.append(0);
								chose_alc_neu_subj.append(0);
							elif (t.firstCategoryLookedAt == 'cigarette'):
								chose_alc_alc_subj.append(0);
								chose_alc_cig_subj.append(1);
								chose_alc_neu_subj.append(0);						
							elif (t.firstCategoryLookedAt == 'neutral'):
								chose_alc_alc_subj.append(0);
								chose_alc_cig_subj.append(0);
								chose_alc_neu_subj.append(1);										
						elif selected_item=='cigarette':				
							#conditionally append a 1 or 0 based on which item was last looked at in this trial
							if (t.firstCategoryLookedAt == 'alcohol'):
								chose_cig_alc_subj.append(1);
								chose_cig_cig_subj.append(0);
								chose_cig_neu_subj.append(0);
							elif (t.firstCategoryLookedAt == 'cigarette'):
								chose_cig_alc_subj.append(0);
								chose_cig_cig_subj.append(1);
								chose_cig_neu_subj.append(0);						
							elif (t.firstCategoryLookedAt == 'neutral'):
								chose_cig_alc_subj.append(0);
								chose_cig_cig_subj.append(0);
								chose_cig_neu_subj.append(1);															
						elif selected_item=='neutral':
							#conditionally append a 1 or 0 based on which item was last looked at in this trial
							if (t.firstCategoryLookedAt == 'alcohol'):
								chose_neu_alc_subj.append(1);
								chose_neu_cig_subj.append(0);
								chose_neu_neu_subj.append(0);
							elif (t.firstCategoryLookedAt == 'cigarette'):
								chose_neu_alc_subj.append(0);
								chose_neu_cig_subj.append(1);
								chose_neu_neu_subj.append(0);						
							elif (t.firstCategoryLookedAt == 'neutral'):
								chose_neu_alc_subj.append(0);
								chose_neu_cig_subj.append(0);
								chose_neu_neu_subj.append(1);
				#append data to the all subject holders
				if selected_item=='alcohol':
					chose_alc_alc_first_fixated.append(sum(chose_alc_alc_subj)/float(len(chose_alc_alc_subj)));
					chose_alc_cig_first_fixated.append(sum(chose_alc_cig_subj)/float(len(chose_alc_cig_subj)));
					chose_alc_neu_first_fixated.append(sum(chose_alc_neu_subj)/float(len(chose_alc_neu_subj)));
				elif selected_item=='cigarette':
					chose_cig_alc_first_fixated.append(sum(chose_cig_alc_subj)/float(len(chose_cig_alc_subj)));
					chose_cig_cig_first_fixated.append(sum(chose_cig_cig_subj)/float(len(chose_cig_cig_subj)));
					chose_cig_neu_first_fixated.append(sum(chose_cig_neu_subj)/float(len(chose_cig_neu_subj)));
				elif selected_item=='neutral':
					chose_neu_alc_first_fixated.append(sum(chose_neu_alc_subj)/float(len(chose_neu_alc_subj)));
					chose_neu_cig_first_fixated.append(sum(chose_neu_cig_subj)/float(len(chose_neu_cig_subj)));
					chose_neu_neu_first_fixated.append(sum(chose_neu_neu_subj)/float(len(chose_neu_neu_subj)));

		#below here append averages to the database
		db['%s_%s_chose_alc_alc_mean_prop_first_fixated_item'%(eyed,name)] = nanmean(chose_alc_alc_first_fixated); db['%s_%s_chose_alc_alc_bs_sems_prop_first_fixated_item'%(eyed,name)] = compute_BS_SEM(chose_alc_alc_first_fixated);
		db['%s_%s_chose_alc_cig_mean_prop_first_fixated_item'%(eyed,name)] = nanmean(chose_alc_cig_first_fixated); db['%s_%s_chose_alc_cig_bs_sems_prop_first_fixated_item'%(eyed,name)] = compute_BS_SEM(chose_alc_cig_first_fixated);
		db['%s_%s_chose_alc_neu_mean_prop_first_fixated_item'%(eyed,name)] = nanmean(chose_alc_neu_first_fixated); db['%s_%s_chose_alc_neu_bs_sems_prop_first_fixated_item'%(eyed,name)] = compute_BS_SEM(chose_alc_neu_first_fixated);				
		db['%s_%s_chose_cig_alc_mean_prop_first_fixated_item'%(eyed,name)] = nanmean(chose_cig_alc_first_fixated); db['%s_%s_chose_cig_alc_bs_sems_prop_first_fixated_item'%(eyed,name)] = compute_BS_SEM(chose_cig_alc_first_fixated);
		db['%s_%s_chose_cig_cig_mean_prop_first_fixated_item'%(eyed,name)] = nanmean(chose_cig_cig_first_fixated); db['%s_%s_chose_cig_cig_bs_sems_prop_first_fixated_item'%(eyed,name)] = compute_BS_SEM(chose_cig_cig_first_fixated);
		db['%s_%s_chose_cig_neu_mean_prop_first_fixated_item'%(eyed,name)] = nanmean(chose_cig_neu_first_fixated); db['%s_%s_chose_cig_neu_bs_sems_prop_first_fixated_item'%(eyed,name)] = compute_BS_SEM(chose_cig_neu_first_fixated);									
		db['%s_%s_chose_neu_alc_mean_prop_first_fixated_item'%(eyed,name)] = nanmean(chose_neu_alc_first_fixated); db['%s_%s_chose_neu_alc_bs_sems_prop_first_fixated_item'%(eyed,name)] = compute_BS_SEM(chose_neu_alc_first_fixated);
		db['%s_%s_chose_neu_cig_mean_prop_first_fixated_item'%(eyed,name)] = nanmean(chose_neu_cig_first_fixated); db['%s_%s_chose_neu_cig_bs_sems_prop_first_fixated_item'%(eyed,name)] = compute_BS_SEM(chose_neu_cig_first_fixated);
		db['%s_%s_chose_neu_neu_mean_prop_first_fixated_item'%(eyed,name)] = nanmean(chose_neu_neu_first_fixated); db['%s_%s_chose_neu_neu_bs_sems_prop_first_fixated_item'%(eyed,name)] = compute_BS_SEM(chose_neu_neu_first_fixated);	
		db.sync();
	
		
		#below here append all the data to the DataFrame and then save it as a .csv		
		for sub_id, alc, cig, neu, alc_alc, alc_cig, alc_neu, cig_alc, cig_cig, cig_neu, neu_alc, neu_cig, neu_neu \
			in zip(ids, alc_first_fixated, cig_first_fixated, neu_first_fixated, \
			chose_alc_alc_first_fixated, chose_alc_cig_first_fixated, chose_alc_neu_first_fixated, \
			chose_cig_alc_first_fixated, chose_cig_cig_first_fixated, chose_cig_neu_first_fixated, \
			chose_neu_alc_first_fixated, chose_neu_cig_first_fixated, chose_neu_neu_first_fixated):

			#confirm that alc, cig, neu, etc 
			
			data.loc[index_counter] = [sub_id, name, mean(alc), mean(cig), mean(neu), \
									   mean(alc_alc), mean(alc_cig), mean(alc_neu), \
									mean(cig_alc), mean(cig_cig), mean(cig_neu), \
									mean(neu_alc), mean(neu_cig), mean(neu_neu)];
			index_counter+=1;
	
	if eyed=='agg':
		data.to_csv(savepath+'avg_first_fixated_item.csv',index=False);		
		

def computeTotalTimeLookingatEachItem(blocks, eyed = 'agg'):
	#this will compute the average time spent look at each item in a given trial, raw total time, for each trial type, aggregated
	# across selected items and broken down by selected item
	db = subject_data;
	
	#loop through and get all the trials for each subject
	trial_matrix = [[tee for b in bl for tee in b.trials if (tee.skip==0)] for bl in blocks];

	#find each subjects' cue substance based on which item them chose more often during PAPC trials where they selected the alcohol or cigarette
	if eyed=='agg':
		index_counter=0; #index counter for the DataFrame object		
		data = pd.DataFrame(columns = ['sub_id','trial_type','alc_avg_total_time','cig_avg_total_time','neu_avg_total_time',
									   'chose_alc_alc_avg_total_time','chose_alc_cig_avg_total_time','chose_alc_neu_avg_total_time',
									   'chose_cig_alc_avg_total_time','chose_cig_cig_avg_total_time','chose_cig_neu_avg_total_time',
									   'chose_neu_alc_avg_total_time','chose_neu_cig_avg_total_time','chose_neu_neu_avg_total_time']);		

	#get the avg total time spent looking at each of the alcohol, cigarettes, and neutral items
	#get the aggregate breakdown as well as when they chose each item
	for ttype, name in zip([1,2,3,4],['high_pref', 'highC_lowA','lowC_highA','lowC_lowA']):
		
		alc_total_time = [];
		cig_total_time = [];
		neu_total_time = [];
		chose_alc_alc_total_time = [];
		chose_alc_cig_total_time = [];
		chose_alc_neu_total_time = [];	
		chose_cig_alc_total_time = [];
		chose_cig_cig_total_time = [];
		chose_cig_neu_total_time = [];	
		chose_neu_alc_total_time = [];
		chose_neu_cig_total_time = [];
		chose_neu_neu_total_time = [];
		
		#first run the analysis for all trials of this trial type, not breaking it down by whether they chose alcohol, cigeratte, or neutral
		#loop through trials for each subject
		for subj,sub_id in zip(trial_matrix, ids):
			alc_subj = [];
			cig_subj = [];
			neu_subj = [];			
			for t in subj:
				if((t.dropped_sample == 0)&(t.didntLookAtAnyItems == 0)&(t.trial_type == ttype)&
					(t.skip == 0)&(sqrt(t.eyeX[0]**2 + t.eyeY[0]**2) < 2.5)):				
					#append the amount of raw time looking at each item to the corresponding array
					alc_subj.append(t.timeLookingAtAlcohol);
					cig_subj.append(t.timeLookingAtCigarette);
					neu_subj.append(t.timeLookingAtNeutral);
			alc_total_time.append(mean(alc_subj));
			cig_total_time.append(mean(cig_subj));
			neu_total_time.append(mean(neu_subj));		
		
		#below here append averages to the database 
		db['%s_%s_alc_mean_total_time_fixating'%(eyed,name)] = nanmean(alc_total_time); db['%s_%s_alc_bs_sems_total_time_fixating'%(eyed,name)] = compute_BS_SEM(alc_total_time);
		db['%s_%s_cig_mean_total_time_fixating'%(eyed,name)] = nanmean(cig_total_time); db['%s_%s_cig_bs_sems_total_time_fixating'%(eyed,name)] = compute_BS_SEM(cig_total_time);
		db['%s_%s_neu_mean_total_time_fixating'%(eyed,name)] = nanmean(neu_total_time); db['%s_%s_neu_bs_sems_total_time_fixating'%(eyed,name)] = compute_BS_SEM(neu_total_time);
		db.sync();		
		
		#now break it down by which item was chosen
		for selected_item in ['alcohol','cigarette','neutral']:			
			#loop through trials for each subject
			for subj,sub_id in zip(trial_matrix, ids):
				
				chose_alc_alc_subj = [];
				chose_alc_cig_subj = [];
				chose_alc_neu_subj = [];			
				chose_cig_alc_subj = [];
				chose_cig_cig_subj = [];
				chose_cig_neu_subj = [];
				chose_neu_alc_subj = [];
				chose_neu_cig_subj = [];
				chose_neu_neu_subj = [];				

				for t in subj:
					if((t.dropped_sample == 0)&(t.didntLookAtAnyItems == 0)&(t.trial_type == ttype)&(t.preferred_category==selected_item)
						(t.skip == 0)&(sqrt(t.eyeX[0]**2 + t.eyeY[0]**2) < 2.5)):
						
						#conditional
						if selected_item=='alcohol':
							#append the amount of raw time looking at each item to the corresponding array
							chose_alc_alc_subj.append(t.timeLookingAtAlcohol);
							chose_alc_cig_subj.append(t.timeLookingAtCigarette);
							chose_alc_neu_subj.append(t.timeLookingAtNeutral);									
						elif selected_item=='cigarette':				
							chose_cig_alc_subj.append(t.timeLookingAtAlcohol);
							chose_cig_cig_subj.append(t.timeLookingAtCigarette);
							chose_cig_neu_subj.append(t.timeLookingAtNeutral);															
						elif selected_item=='neutral':
							chose_neu_alc_subj.append(t.timeLookingAtAlcohol);
							chose_neu_cig_subj.append(t.timeLookingAtCigarette);
							chose_neu_neu_subj.append(t.timeLookingAtNeutral);						
		
				#append data to the all subject holders
				if selected_item=='alcohol':
					chose_alc_alc_total_time.append(mean(chose_alc_alc_subj));
					chose_alc_cig_total_time.append(mean(chose_alc_cig_subj));
					chose_alc_neu_total_time.append(mean(chose_alc_neu_subj));
				elif selected_item=='cigarette':
					chose_cig_alc_total_time.append(mean(chose_cig_alc_subj));
					chose_cig_cig_total_time.append(mean(chose_cig_cig_subj));
					chose_cig_neu_total_time.append(mean(chose_cig_neu_subj));
				elif selected_item=='neutral':
					chose_neu_alc_total_time.append(mean(chose_neu_alc_subj));
					chose_neu_cig_total_time.append(mean(chose_neu_cig_subj));
					chose_neu_neu_total_time.append(mean(chose_neu_neu_subj));
					
		#below here append averages to the database
		db['%s_%s_chose_alc_alc_mean_total_time_fixated'%(eyed,name)] = nanmean(chose_alc_alc_total_time); db['%s_%s_chose_alc_alc_bs_sems_total_time_fixated'%(eyed,name)] = compute_BS_SEM(chose_alc_alc_total_time);
		db['%s_%s_chose_alc_cig_mean_total_time_fixated'%(eyed,name)] = nanmean(chose_alc_cig_total_time); db['%s_%s_chose_alc_cig_bs_sems_total_time_fixated'%(eyed,name)] = compute_BS_SEM(chose_alc_cig_total_time);
		db['%s_%s_chose_alc_neu_mean_total_time_fixated'%(eyed,name)] = nanmean(chose_alc_neu_total_time); db['%s_%s_chose_alc_neu_bs_sems_total_time_fixated'%(eyed,name)] = compute_BS_SEM(chose_alc_neu_total_time);				
		db['%s_%s_chose_cig_alc_mean_total_time_fixated'%(eyed,name)] = nanmean(chose_cig_alc_total_time); db['%s_%s_chose_cig_alc_bs_sems_total_time_fixated'%(eyed,name)] = compute_BS_SEM(chose_cig_alc_total_time);
		db['%s_%s_chose_cig_cig_mean_total_time_fixated'%(eyed,name)] = nanmean(chose_cig_cig_total_time); db['%s_%s_chose_cig_cig_bs_sems_total_time_fixated'%(eyed,name)] = compute_BS_SEM(chose_cig_cig_total_time);
		db['%s_%s_chose_cig_neu_mean_total_time_fixated'%(eyed,name)] = nanmean(chose_cig_neu_total_time); db['%s_%s_chose_cig_neu_bs_sems_total_time_fixated'%(eyed,name)] = compute_BS_SEM(chose_cig_neu_total_time);									
		db['%s_%s_chose_neu_alc_mean_total_time_fixated'%(eyed,name)] = nanmean(chose_neu_alc_total_time); db['%s_%s_chose_neu_alc_bs_sems_total_time_fixated'%(eyed,name)] = compute_BS_SEM(chose_neu_alc_total_time);
		db['%s_%s_chose_neu_cig_mean_total_time_fixated'%(eyed,name)] = nanmean(chose_neu_cig_total_time); db['%s_%s_chose_neu_cig_bs_sems_total_time_fixated'%(eyed,name)] = compute_BS_SEM(chose_neu_cig_total_time);
		db['%s_%s_chose_neu_neu_mean_total_time_fixated'%(eyed,name)] = nanmean(chose_neu_neu_total_time); db['%s_%s_chose_neu_neu_bs_sems_total_time_fixated'%(eyed,name)] = compute_BS_SEM(chose_neu_neu_total_time);	
		db.sync();					
					
		#below here append all the data to the DataFrame and then save it as a .csv		
		for sub_id, alc, cig, neu, alc_alc, alc_cig, alc_neu, cig_alc, cig_cig, cig_neu, neu_alc, neu_cig, neu_neu \
			in zip(ids, alc_total_time, cig_total_time, neu_total_time, \
			chose_alc_alc_total_time, chose_alc_cig_total_time, chose_alc_neu_total_time, \
			chose_cig_alc_total_time, chose_cig_cig_total_time, chose_cig_neu_total_time, \
			chose_neu_alc_total_time, chose_neu_cig_total_time, chose_neu_neu_total_time):

			#confirm that alc, cig, neu, etc 
			
			data.loc[index_counter] = [sub_id, name, mean(alc), mean(cig), mean(neu), \
									   mean(alc_alc), mean(alc_cig), mean(alc_neu), \
									mean(cig_alc), mean(cig_cig), mean(cig_neu), \
									mean(neu_alc), mean(neu_cig), mean(neu_neu)];
			index_counter+=1;					

	if eyed=='agg':
		data.to_csv(savepath+'avg_total_time_fixating_item.csv',index=False);	


def computeSustainedResponses(blocks, eyed = 'agg'):
	# determine the continuous amount of time fixated at each item in each trial (not necessarrilly the item with largest amount of time)
	#compute this for all trial types, and then do it for breakdown of which item was selected
	db = subject_data;
	
	rexp_pattern = re.compile(r'1+'); #this regular expression pattern looks for strings with a 1 or anything continuous run of 1s
	
	#loop through and get all the trials for each subject
	trial_matrix = [[tee for b in bl for tee in b.trials if (tee.skip==0)] for bl in blocks];

	#find each subjects' cue substance based on which item them chose more often during PAPC trials where they selected the alcohol or cigarette
	if eyed=='agg':
		index_counter=0; #index counter for the DataFrame object		
		data = pd.DataFrame(columns = ['sub_id','trial_type','alc_avg_sustained_response','cig_avg_sustained_response','neu_avg_sustained_response',
									   'chose_alc_alc_avg_sustained_response','chose_alc_cig_avg_sustained_response','chose_alc_neu_avg_tsustained_response',
									   'chose_cig_alc_avg_sustained_response','chose_cig_cig_avg_sustained_response','chose_cig_neu_avg_sustained_response',
									   'chose_neu_alc_avg_sustained_response','chose_neu_cig_avg_sustained_response','chose_neu_neu_avg_sustained_response']);		

	#get the avg sustained response at each of the alcohol, cigarettes, and neutral items
	#get the aggregate breakdown as well as when they chose each item
	for ttype, name in zip([1,2,3,4],['high_pref', 'highC_lowA','lowC_highA','lowC_lowA']):
		
		alc_sr = [];
		cig_sr = [];
		neu_sr = [];
		chose_alc_alc_sr = [];
		chose_alc_cig_sr = [];
		chose_alc_neu_sr = [];	
		chose_cig_alc_sr = [];
		chose_cig_cig_sr = [];
		chose_cig_neu_sr = [];	
		chose_neu_alc_sr = [];
		chose_neu_cig_sr = [];
		chose_neu_neu_sr = [];

		#first run the analysis for all trials of this trial type, not breaking it down by whether they chose alcohol, cigeratte, or neutral
		#loop through trials for each subject
		for subj,sub_id in zip(trial_matrix, ids):
			alc_subj = [];
			cig_subj = [];
			neu_subj = [];			
			for t in subj:
				if((t.dropped_sample == 0)&(t.didntLookAtAnyItems == 0)&(t.trial_type == ttype)&
					(t.skip == 0)&(sqrt(t.eyeX[0]**2 + t.eyeY[0]**2) < 2.5)):				
					#get the duration of longest continuous fixation ("sustained response") for each item per trial
					
					str_alc = ''.join(str(int(g)) for g in t.lookedAtAlcohol if not(isnan(g))); #first get the array into a string
					run_lengths_alc = [len(f) for f in rexp_pattern.findall(str_alc)];
					#line above, then use the regular expression pattern, looking for 1s, to parse an array of the continuous runs of 1s in the string from above and get length
					if not(run_lengths_alc): alc_subj.append(0);
					else: alc_subj.append(max(run_lengths_alc)); #append the max, if there is one
					
					str_cig = ''.join(str(int(g)) for g in t.lookedAtCigarette if not(isnan(g))); #parse cigarette
					run_lengths_cig = [len(f) for f in rexp_pattern.findall(str_cig)];
					if not(run_lengths_cig): cig_subj.append(0);
					else: cig_subj.append(max(run_lengths_cig)); 					

					str_neu = ''.join(str(int(g)) for g in t.lookedAtNeutral if not(isnan(g))); #do the parsing for neutral..
					run_lengths_neu = [len(f) for f in rexp_pattern.findall(str_neu)];
					if not(run_lengths_neu): neu_subj.append(0);
					else: neu_subj.append(max(run_lengths_neu));
					
			alc_sr.append(mean(alc_subj));
			cig_sr.append(mean(cig_subj));
			neu_sr.append(mean(neu_subj));
			
		#below here append averages to the database 
		db['%s_%s_alc_mean_sustained_resp'%(eyed,name)] = nanmean(alc_sr); db['%s_%s_alc_bs_sems_sustained_resp'%(eyed,name)] = compute_BS_SEM(alc_sr);
		db['%s_%s_cig_mean_sustained_resp'%(eyed,name)] = nanmean(cig_sr); db['%s_%s_cig_bs_sems_sustained_resp'%(eyed,name)] = compute_BS_SEM(cig_sr);
		db['%s_%s_neu_mean_sustained_resp'%(eyed,name)] = nanmean(neu_sr); db['%s_%s_neu_bs_sems_sustained_resp'%(eyed,name)] = compute_BS_SEM(neu_sr);
		db.sync();	

		#now break it down by which item was chosen
		for selected_item in ['alcohol','cigarette','neutral']:			
			#loop through trials for each subject
			for subj,sub_id in zip(trial_matrix, ids):
				
				chose_alc_alc_subj = [];
				chose_alc_cig_subj = [];
				chose_alc_neu_subj = [];			
				chose_cig_alc_subj = [];
				chose_cig_cig_subj = [];
				chose_cig_neu_subj = [];
				chose_neu_alc_subj = [];
				chose_neu_cig_subj = [];
				chose_neu_neu_subj = [];

				for t in subj:
					if((t.dropped_sample == 0)&(t.didntLookAtAnyItems == 0)&(t.trial_type == ttype)&(t.preferred_category==selected_item)&
						(t.skip == 0)&(sqrt(t.eyeX[0]**2 + t.eyeY[0]**2) < 2.5)):
						
						#conditional
						if selected_item=='alcohol':
							str_alc = ''.join(str(int(g)) for g in t.lookedAtAlcohol if not(isnan(g))); #first get the array into a string
							run_lengths_alc = [len(f) for f in rexp_pattern.findall(str_alc)];
							#line above, then use the regular expression pattern, looking for 1s, to parse an array of the continuous runs of 1s in the string from above and get length
							if not(run_lengths_alc): chose_alc_alc_subj.append(0);
							else: chose_alc_alc_subj.append(max(run_lengths_alc)); #append the max, if there is one
							
							str_cig = ''.join(str(int(g)) for g in t.lookedAtCigarette if not(isnan(g))); #parse cigarette
							run_lengths_cig = [len(f) for f in rexp_pattern.findall(str_cig)];
							if not(run_lengths_cig): chose_alc_cig_subj.append(0);
							else: chose_alc_cig_subj.append(max(run_lengths_cig)); 					
			
							str_neu = ''.join(str(int(g)) for g in t.lookedAtNeutral if not(isnan(g))); #do the parsing for neutral..
							run_lengths_neu = [len(f) for f in rexp_pattern.findall(str_neu)];
							if not(run_lengths_neu): chose_alc_neu_subj.append(0);
							else: chose_alc_neu_subj.append(max(run_lengths_neu));
									
						elif selected_item=='cigarette':				
							str_alc = ''.join(str(int(g)) for g in t.lookedAtAlcohol if not(isnan(g))); #first get the array into a string
							run_lengths_alc = [len(f) for f in rexp_pattern.findall(str_alc)];
							#line above, then use the regular expression pattern, looking for 1s, to parse an array of the continuous runs of 1s in the string from above and get length
							if not(run_lengths_alc): chose_cig_alc_subj.append(0);
							else: chose_cig_alc_subj.append(max(run_lengths_alc)); #append the max, if there is one
							
							str_cig = ''.join(str(int(g)) for g in t.lookedAtCigarette if not(isnan(g))); #parse cigarette
							run_lengths_cig = [len(f) for f in rexp_pattern.findall(str_cig)];
							if not(run_lengths_cig): chose_cig_cig_subj.append(0);
							else: chose_cig_cig_subj.append(max(run_lengths_cig)); 					
			
							str_neu = ''.join(str(int(g)) for g in t.lookedAtNeutral if not(isnan(g))); #do the parsing for neutral..
							run_lengths_neu = [len(f) for f in rexp_pattern.findall(str_neu)];
							if not(run_lengths_neu): chose_cig_neu_subj.append(0);
							else: chose_cig_neu_subj.append(max(run_lengths_neu));
							
						elif selected_item=='neutral':
							str_alc = ''.join(str(int(g)) for g in t.lookedAtAlcohol if not(isnan(g))); #first get the array into a string
							run_lengths_alc = [len(f) for f in rexp_pattern.findall(str_alc)];
							#line above, then use the regular expression pattern, looking for 1s, to parse an array of the continuous runs of 1s in the string from above and get length
							if not(run_lengths_alc): chose_neu_alc_subj.append(0);
							else: chose_neu_alc_subj.append(max(run_lengths_alc)); #append the max, if there is one
							
							str_cig = ''.join(str(int(g)) for g in t.lookedAtCigarette if not(isnan(g))); #parse cigarette
							run_lengths_cig = [len(f) for f in rexp_pattern.findall(str_cig)];
							if not(run_lengths_cig): chose_neu_cig_subj.append(0);
							else: chose_neu_cig_subj.append(max(run_lengths_cig)); 					
			
							str_neu = ''.join(str(int(g)) for g in t.lookedAtNeutral if not(isnan(g))); #do the parsing for neutral..
							run_lengths_neu = [len(f) for f in rexp_pattern.findall(str_neu)];
							if not(run_lengths_neu): chose_neu_neu_subj.append(0);
							else: chose_neu_neu_subj.append(max(run_lengths_neu));
							
				#append data to the all subject holders
				if selected_item=='alcohol':
					chose_alc_alc_sr.append(mean(chose_alc_alc_subj));
					chose_alc_cig_sr.append(mean(chose_alc_cig_subj));
					chose_alc_neu_sr.append(mean(chose_alc_neu_subj));
				elif selected_item=='cigarette':
					chose_cig_alc_sr.append(mean(chose_cig_alc_subj));
					chose_cig_cig_sr.append(mean(chose_cig_cig_subj));
					chose_cig_neu_sr.append(mean(chose_cig_neu_subj));
				elif selected_item=='neutral':
					chose_neu_alc_sr.append(mean(chose_neu_alc_subj));
					chose_neu_cig_sr.append(mean(chose_neu_cig_subj));
					chose_neu_neu_sr.append(mean(chose_neu_neu_subj));							
							
		#below here append averages to the database
		db['%s_%s_chose_alc_alc_mean_sustained_resp'%(eyed,name)] = nanmean(chose_alc_alc_sr); db['%s_%s_chose_alc_alc_bs_sems_sustained_resp'%(eyed,name)] = compute_BS_SEM(chose_alc_alc_sr);
		db['%s_%s_chose_alc_cig_mean_sustained_resp'%(eyed,name)] = nanmean(chose_alc_cig_sr); db['%s_%s_chose_alc_cig_bs_sems_sustained_resp'%(eyed,name)] = compute_BS_SEM(chose_alc_cig_sr);
		db['%s_%s_chose_alc_neu_mean_sustained_resp'%(eyed,name)] = nanmean(chose_alc_neu_sr); db['%s_%s_chose_alc_neu_bs_sems_sustained_resp'%(eyed,name)] = compute_BS_SEM(chose_alc_neu_sr);				
		db['%s_%s_chose_cig_alc_mean_sustained_resp'%(eyed,name)] = nanmean(chose_cig_alc_sr); db['%s_%s_chose_cig_alc_bs_sems_sustained_resp'%(eyed,name)] = compute_BS_SEM(chose_cig_alc_sr);
		db['%s_%s_chose_cig_cig_mean_sustained_resp'%(eyed,name)] = nanmean(chose_cig_cig_sr); db['%s_%s_chose_cig_cig_bs_sems_sustained_resp'%(eyed,name)] = compute_BS_SEM(chose_cig_cig_sr);
		db['%s_%s_chose_cig_neu_mean_sustained_resp'%(eyed,name)] = nanmean(chose_cig_neu_sr); db['%s_%s_chose_cig_neu_bs_sems_sustained_resp'%(eyed,name)] = compute_BS_SEM(chose_cig_neu_sr);									
		db['%s_%s_chose_neu_alc_mean_sustained_resp'%(eyed,name)] = nanmean(chose_neu_alc_sr); db['%s_%s_chose_neu_alc_bs_sems_sustained_resp'%(eyed,name)] = compute_BS_SEM(chose_neu_alc_sr);
		db['%s_%s_chose_neu_cig_mean_sustained_resp'%(eyed,name)] = nanmean(chose_neu_cig_sr); db['%s_%s_chose_neu_cig_bs_sems_sustained_resp'%(eyed,name)] = compute_BS_SEM(chose_neu_cig_sr);
		db['%s_%s_chose_neu_neu_mean_sustained_resp'%(eyed,name)] = nanmean(chose_neu_neu_sr); db['%s_%s_chose_neu_neu_bs_sems_sustained_resp'%(eyed,name)] = compute_BS_SEM(chose_neu_neu_sr);	
		db.sync();
		
		#below here append all the data to the DataFrame and then save it as a .csv		
		for sub_id, alc, cig, neu, alc_alc, alc_cig, alc_neu, cig_alc, cig_cig, cig_neu, neu_alc, neu_cig, neu_neu \
			in zip(ids, alc_sr, cig_sr, neu_sr, \
			chose_alc_alc_sr, chose_alc_cig_sr, chose_alc_neu_sr, \
			chose_cig_alc_sr, chose_cig_cig_sr, chose_cig_neu_sr, \
			chose_neu_alc_sr, chose_neu_cig_sr, chose_neu_neu_sr):

			#confirm that alc, cig, neu, etc 
			
			data.loc[index_counter] = [sub_id, name, mean(alc), mean(cig), mean(neu), \
									   mean(alc_alc), mean(alc_cig), mean(alc_neu), \
									mean(cig_alc), mean(cig_cig), mean(cig_neu), \
									mean(neu_alc), mean(neu_cig), mean(neu_neu)];
			index_counter+=1;					

	if eyed=='agg':
		data.to_csv(savepath+'avg_sustained_response_item.csv',index=False);
		
		
		
def computePreviousTrialData(blocks, eyed='agg'):
	#compute the effect that the previous trial's (N-1) choice as well as last dwelled (fixated) item has on the current trial (N)
	db = subject_data;
	
	#first, check out effect that previous trial response has on current trial response/first dwelled item
	#this is likely to be biased due to the biases in choice
	
	rexp_pattern = re.compile(r'01'); #this regular expression pattern looks for strings with a 1 or anything continuous run of 1s
	
	#loop through and get all the trials for each subject
	trial_matrix = [[tee for b in bl for tee in b.trials if (tee.skip==0)] for bl in blocks];	
		
	#HERE, RUN A LOCATION-BASED PREVIOUS TRIAL ANALYSIS	

	if eyed=='agg':
		index_counter=0; #index counter for the DataFrame object
		#here, create a dataframe object to save the subsequent data
		data = pd.DataFrame(columns = ['sub_id','trial_type','prev_lastdwellloc_cur_firstdwellloc_avg_prop','first_sac_latency']);		
		
	#get the aggregate breakdown as well as when they chose each item
	for ttype, name in zip([1,2,3,4],['high_pref', 'highC_lowA','lowC_highA','lowC_lowA']):			
		
		#this counter variable hold boolean (0 or 1) values corresponding to whether the previous trials last dwelled loc is the first dwelled loc on trial N
		prev_last_dwell_dwells_bools = [];
		lengs = [];
		latencies = [];
		
		for subj,sub_id in zip(trial_matrix, ids):		
			subj_prev_last_dwell_bools = [];
			subj_latencies = [];

			for i,t in enumerate(subj):
				if((t.dropped_sample == 0)&(t.didntLookAtAnyItems == 0)&(t.trial_type == ttype)&
					(t.skip == 0)&(sqrt(t.eyeX[0]**2 + t.eyeY[0]**2) < 2.5)):
					
					#can't do n-back calculation for the first trial in a block
					if t.trial_nr>0:
						
						#get the previous last dwelled location
		
						prev_looked_at_up = array([r if ((r==0)|(r==1)) else 0 for r in subj[i-1].lookedUp]);
						prev_looked_at_left = array([r if ((r==0)|(r==1)) else 0 for r in subj[i-1].lookedLeft]);
						prev_looked_at_right = array([r if ((r==0)|(r==1)) else 0 for r in subj[i-1].lookedRight]);			

						str_up = ''.join(str(int(g)) for g in prev_looked_at_up if not(isnan(g))); #first get the array into a string

						#get last instane of the '1' in this array. if never loooked at, will return a -1
						up_indices = str_up.rfind('1'); #rfind searches the string from right to left
						
						if isinstance(up_indices, int):
							up_last_index_lookedat = up_indices;
						else:
							up_last_index_lookedat = up_indices[0];
							
						str_left = ''.join(str(int(g)) for g in prev_looked_at_left if not(isnan(g))); #parse cigarette
						left_indices = str_left.rfind('1');		
						if isinstance(left_indices, int):
							left_last_index_lookedat = left_indices;
						else:
							left_last_index_lookedat = left_indices[0];
	
						str_right = ''.join(str(int(g)) for g in prev_looked_at_right if not(isnan(g))); #do the parsing for neutral..
						right_indices = str_right.rfind('1');		
						if isinstance(right_indices, int):
							right_last_index_lookedat = right_indices;
						else:
							right_last_index_lookedat = right_indices[0];
						
						last_instances =  array([up_last_index_lookedat, left_last_index_lookedat, right_last_index_lookedat]); #always keep it up, left, right
						last_item_index = where(last_instances == max(last_instances))[0][0];		
		
						#conditonal to find the last item that was looked at accoridng to the index corresponding to the item 
						if last_item_index==0:
							prev_last_dwelled_item = 'up';
						elif last_item_index==1:
							prev_last_dwelled_item = 'left';
						elif last_item_index== 2:
							prev_last_dwelled_item = 'right';		

					#and the first looked at item in this trial. It's the same thing as used above, but using string.find() rather than string.rfind()		

						#get the current first dwelled location
		
						curr_looked_at_up = array([r if ((r==0)|(r==1)) else 0 for r in t.lookedUp]);
						curr_looked_at_left = array([r if ((r==0)|(r==1)) else 0 for r in t.lookedLeft]);
						curr_looked_at_right = array([r if ((r==0)|(r==1)) else 0 for r in t.lookedRight]);			

						curr_str_up = ''.join(str(int(g)) for g in curr_looked_at_up if not(isnan(g))); #first get the array into a string

						#get last instane of the '1' in this array. if never loooked at, will return a -1
						curr_up_indices = curr_str_up.find('1'); #find searches the string from left to right
						
						if isinstance(curr_up_indices, int):
							curr_up_first_index_lookedat = curr_up_indices;
						else:
							curr_up_first_index_lookedat = curr_up_indices[0];
						if curr_up_first_index_lookedat==-1:
							curr_up_first_index_lookedat = 100*1000; #this ensures that instead of a -1 being input into the array, I input a massive nr (needed for minimum calculation)
							
						curr_str_left = ''.join(str(int(g)) for g in curr_looked_at_left if not(isnan(g))); #parse cigarette
						curr_left_indices = curr_str_left.find('1');		
						if isinstance(curr_left_indices, int):
							curr_left_first_index_lookedat = curr_left_indices;
						else:
							curr_left_first_index_lookedat = curr_left_indices[0];
						if curr_left_first_index_lookedat==-1:
							curr_left_first_index_lookedat = 100*1000; #this ensures that instead of a -1 being input into the array, I input a massive nr (needed for minimum calculation)
								
						curr_str_right = ''.join(str(int(g)) for g in curr_looked_at_right if not(isnan(g))); #do the parsing for neutral..
						curr_right_indices = curr_str_right.find('1');		
						if isinstance(curr_right_indices, int):
							curr_right_first_index_lookedat = curr_right_indices;
						else:
							curr_right_first_index_lookedat = curr_right_indices[0];
						if curr_right_first_index_lookedat==-1:
							curr_right_first_index_lookedat = 100*1000; #this ensures that instead of a -1 being input into the array, I input a massive nr (needed for minimum calculation)			
													
						curr_first_instances =  array([curr_up_first_index_lookedat, curr_left_first_index_lookedat, curr_right_first_index_lookedat]); #always keep it up, left, right
						curr_first_item_index = where(curr_first_instances == min(curr_first_instances))[0][0];				
		
						#conditonal to find the last item that was looked at accoridng to the index corresponding to the item 
						if curr_first_item_index==0:
							curr_first_dwelled_item = 'up';
						elif curr_first_item_index==1:
							curr_first_dwelled_item = 'left';
						elif curr_first_item_index== 2:
							curr_first_dwelled_item = 'right';
							
						#now below here, compare the current trial's response and first looked at item with the last trials response and last looked at item	
						subj_prev_last_dwell_bools.append(prev_last_dwelled_item==curr_first_dwelled_item);
						
						#now here find the latency of the first saccade on current trial (trial N)
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
						subj_latencies.append(sac_start_time);
						
						
			#here, append the aggregated proportion of trials these variables matched to the average holders for each subject
			prev_last_dwell_dwells_bools.append(sum(subj_prev_last_dwell_bools)/float(len(subj_prev_last_dwell_bools)));
			lengs.append(len(subj_prev_last_dwell_bools));
			latencies.append(mean(subj_latencies));
			
		#lengs = array([len(s) for s in prev_last_dwell_dwells_bools]);

		#here, find average and standard error or these variables, then print it to the interpreter
				
		print('\n\n TRIAL TYPE %s \n\n'%name)
		print('\n Average proportion of trials the last fixated location on trial N-1 was the first fixated location on trial N for %s subjects: %4.2f \n'%(len(blocks),nanmean(prev_last_dwell_dwells_bools)));
		print('\n Between-subjects standard error of the mean: %4.2f \n\n'%(compute_BS_SEM(prev_last_dwell_dwells_bools)));
		print('Mean nr of trials for each participant: %s \n\n'%mean(array(lengs)));
		print('Mean first saccade current trial latency for each participant: %4.2f \n\n'%nanmean(latencies));
		print('\n Between-subjects standard error of the mean: %4.2f \n\n'%(compute_BS_SEM(latencies)));


		#add data to the data frame object to save as a .csv
		if eyed=='agg':
			for subid,  pl_cf, fr in zip(ids, prev_last_dwell_dwells_bools, latencies):
				data.loc[index_counter] = [subid, name, pl_cf, fr];
				index_counter+=1;

	if eyed=='agg':
		data.to_csv(savepath+'prev_trial_location-based_data.csv',index=False);
		
	#BELOW HERE IS CODE TO RUN AN ITEM-BASED PREVIOUS TRIAL PRIMING ANALYSIS
		
	# if eyed=='agg':
	# 	index_counter=0; #index counter for the DataFrame object
	# 	#here, create a dataframe object to save the subsequent data
	# 	data = pd.DataFrame(columns = ['sub_id','trial_type','prev_resp_cur_resp_avg_prop','prev_resp_cur_firstdwell_avg_prop', \
	# 								   'prev_lastdwell_cur_resp_avg_prop','prev_lastdwell_cur_firstdwell_avg_prop']);
	# 	
	# #get the aggregate breakdown as well as when they chose each item
	# for ttype, name in zip([1,2,3,4],['high_pref', 'highC_lowA','lowC_highA','lowC_lowA']):			
	# 	
	# 	#this counter variables hold boolean (0 or 1) values corresponding to whether the previous trials response corresponded to the current trials response/first dwelled item
	# 	prev_resp_resps_bools = [];
	# 	prev_resp_dwells_bools = [];
	# 	prev_last_dwell_resps_bools = [];
	# 	prev_last_dwell_dwells_bools = [];		
	# 	
	# 	for subj,sub_id in zip(trial_matrix, ids):		
	# 		subj_prev_resp_resps_bools = [];
	# 		subj_prev_resp_dwells_bools = [];
	# 		subj_prev_last_resps_bools = []; #previous trial's last dwelled item's boolean match with the current response
	# 		subj_prev_last_dwell_bools = [];			
	# 
	# 		for i,t in enumerate(subj):
	# 			if((t.dropped_sample == 0)&(t.didntLookAtAnyItems == 0)&(t.trial_type == ttype)&
	# 				(t.skip == 0)&(sqrt(t.eyeX[0]**2 + t.eyeY[0]**2) < 2.5)):
	# 				
	# 				#can't do n-back calculation for the first trial in a block
	# 				if t.trial_nr>0:
	# 					
	# 					#get the previous trial response and last looked at item!
	# 					prev_response = subj[i-1].preferred_category;
	# 					
	# 					#get previous last dwelled item
	# 					prev_alc_subj = []; prev_cig_subj = []; prev_neu_subj = [];
	# 						
	# 					prev_looked_at_alcohol = array([r if ((r==0)|(r==1)) else 0 for r in subj[i-1].lookedAtAlcohol]);
	# 					prev_looked_at_cigarette = array([r if ((r==0)|(r==1)) else 0 for r in subj[i-1].lookedAtCigarette]);
	# 					prev_looked_at_neutral = array([r if ((r==0)|(r==1)) else 0 for r in subj[i-1].lookedAtNeutral]);					
	# 					
	# 					str_alc = ''.join(str(int(g)) for g in prev_looked_at_alcohol if not(isnan(g))); #first get the array into a string
	# 					
	# 					#get last instane of the '1' in this array. if never loooked at, will return a -1
	# 					alc_indices = str_alc.rfind('1'); #rfind searches the string from right to left
	# 					
	# 					if isinstance(alc_indices, int):
	# 						alc_last_index_lookedat = alc_indices;
	# 					else:
	# 						alc_last_index_lookedat = alc_indices[0];
	# 						
	# 					str_cig = ''.join(str(int(g)) for g in prev_looked_at_cigarette if not(isnan(g))); #parse cigarette
	# 					cig_indices = str_cig.rfind('1');		
	# 					if isinstance(cig_indices, int):
	# 						cig_last_index_lookedat = cig_indices;
	# 					else:
	# 						cig_last_index_lookedat = cig_indices[0];
	# 
	# 					str_neu = ''.join(str(int(g)) for g in prev_looked_at_neutral if not(isnan(g))); #do the parsing for neutral..
	# 					neu_indices = str_neu.rfind('1');		
	# 					if isinstance(neu_indices, int):
	# 						neu_last_index_lookedat = neu_indices;
	# 					else:
	# 						neu_last_index_lookedat = neu_indices[0];
	# 					
	# 					last_instances =  array([alc_last_index_lookedat, cig_last_index_lookedat, neu_last_index_lookedat]); #always keep it alcohol, cigarette, neutral
	# 					last_item_index = where(last_instances == max(last_instances))[0][0];
						# 
						# #conditonal to find the last item that was looked at accoridng to the index corresponding to the item 
						# if last_item_index==0:
						# 	prev_last_dwelled_item = 'alcohol';
						# elif last_item_index==1:
						# 	prev_last_dwelled_item = 'cigarette';
						# elif last_item_index== 2:
						# 	prev_last_dwelled_item = 'neutral';
						# 
						# #now get the current trial first looked at item and response
						# 
						# current_response = t.preferred_category;
						# 
						# #and the first looked at item in this trial. It's the same thing as used above, but using string.find() rather than string.rfind()
						# alc_subj = []; cig_subj = []; neu_subj = [];
						# 	
						# looked_at_alcohol = array([r if ((r==0)|(r==1)) else 0 for r in t.lookedAtAlcohol]);
						# looked_at_cigarette = array([r if ((r==0)|(r==1)) else 0 for r in t.lookedAtCigarette]);
						# looked_at_neutral = array([r if ((r==0)|(r==1)) else 0 for r in t.lookedAtNeutral]);										
			# 			
			# 			curr_str_alc = ''.join(str(int(g)) for g in looked_at_alcohol if not(isnan(g))); #first get the array into a string
			# 			
			# 			#get last instane of the '1' in this array. if never loooked at, will return a -1
			# 			curr_alc_indices = curr_str_alc.find('1'); #rfind searches the string from right to left
			# 			
			# 			if isinstance(curr_alc_indices, int):
			# 				curr_alc_last_index_lookedat = curr_alc_indices;
			# 			else:
			# 				curr_alc_last_index_lookedat = curr_alc_indices[0];
			# 			if curr_alc_last_index_lookedat==-1:
			# 				curr_alc_last_index_lookedat = 100*1000; #this ensures that instead of a -1 being input into the array, I input a massive nr (needed for minimum calculation)
			# 				
			# 			curr_str_cig = ''.join(str(int(g)) for g in looked_at_cigarette if not(isnan(g))); #parse cigarette
			# 			curr_cig_indices = curr_str_cig.find('1');		
			# 			if isinstance(curr_cig_indices, int):
			# 				curr_cig_last_index_lookedat = curr_cig_indices;
			# 			else:
			# 				curr_cig_last_index_lookedat = curr_cig_indices[0];
			# 			if curr_cig_last_index_lookedat==-1:
			# 				curr_cig_last_index_lookedat = 100*1000;
			# 				
			# 			curr_str_neu = ''.join(str(int(g)) for g in looked_at_neutral if not(isnan(g))); #do the parsing for neutral..
			# 			curr_neu_indices = curr_str_neu.find('1');		
			# 			if isinstance(curr_neu_indices, int):
			# 				curr_neu_last_index_lookedat = curr_neu_indices;
			# 			else:
			# 				curr_neu_last_index_lookedat = curr_neu_indices[0];
			# 			if curr_neu_last_index_lookedat==-1:
			# 				curr_neu_last_index_lookedat = 100*1000;
			# 
			# 			curr_first_instances =  array([curr_alc_last_index_lookedat, curr_cig_last_index_lookedat, curr_neu_last_index_lookedat]); #always keep it alcohol, cigarette, neutral
			# 			curr_first_item_index = where(curr_first_instances == min(curr_first_instances))[0][0];
			# 			
			# 			#conditonal to find the last item that was looked at accoridng to the index corresponding to the item 
			# 			if curr_first_item_index==0:
			# 				curr_first_dwelled_item = 'alcohol';
			# 			elif curr_first_item_index==1:
			# 				curr_first_dwelled_item = 'cigarette';
			# 			elif curr_first_item_index== 2:
			# 				curr_first_dwelled_item = 'neutral';
			# 				
			# 			#now below here, compare the current trial's response and first looked at item with the last trials response and last looked at item	
			# 			subj_prev_resp_resps_bools.append(prev_response==current_response);
			# 			subj_prev_resp_dwells_bools.append(prev_response==curr_first_dwelled_item);
			# 			subj_prev_last_resps_bools.append(prev_last_dwelled_item==current_response); #previous trial's last dwelled item's boolean match with the current response
			# 			subj_prev_last_dwell_bools.append(prev_last_dwelled_item==curr_first_dwelled_item);
			# 
			# #here, append the aggregated proportion of trials these variables matched to the average holders for each subject
			# prev_resp_resps_bools.append(sum(subj_prev_resp_resps_bools)/float(len(subj_prev_resp_resps_bools)));
			# prev_resp_dwells_bools.append(sum(subj_prev_resp_dwells_bools)/float(len(subj_prev_resp_dwells_bools)));
			# prev_last_dwell_resps_bools.append(sum(subj_prev_last_resps_bools)/float(len(subj_prev_last_resps_bools)));
			# prev_last_dwell_dwells_bools.append(sum(subj_prev_last_dwell_bools)/float(len(subj_prev_last_dwell_bools)));
		# 	
		# 
		# #here, find average and standard error or these variables, then print it to the interpreter
		# 		
		# print('\n\n TRIAL TYPE %s \n\n'%name)
		# print('\n Average proportion of trials the last-dwelled item on trial N-1 was the first dwelled item on trial N for %s subjects: %4.2f \n'%(len(blocks),nanmean(prev_last_dwell_dwells_bools)));
		# print('\n Between-subjects standard error of the mean: %4.2f \n\n'%(compute_BS_SEM(prev_last_dwell_dwells_bools)));
		# print('\n Average proportion of trials the last-dwelled item on trial N-1 was the selected item on trial N for %s subjects: %4.2f \n'%(len(blocks),nanmean(prev_last_dwell_resps_bools)));
		# print('\n Between-subjects standard error of the mean: %4.2f \n\n'%(compute_BS_SEM(prev_last_dwell_resps_bools)));
		# print('\n Average proportion of trials the selected item on trial N-1 was the first dwelled item on trial N for %s subjects: %4.2f \n'%(len(blocks),nanmean(prev_resp_dwells_bools)));
		# print('\n Between-subjects standard error of the mean: %4.2f \n\n'%(compute_BS_SEM(prev_resp_dwells_bools)));
		# print('\n Average proportion of trials the selected item on trial N-1 was the selected item on trial N for %s subjects: %4.2f \n'%(len(blocks),nanmean(prev_resp_resps_bools)));
		# print('\n Between-subjects standard error of the mean: %4.2f \n\n'%(compute_BS_SEM(prev_resp_resps_bools)));		
	# 
	# 	#add data to the data frame object to save as a .csv
	# 	if eyed=='agg':
	# 		for subid, pr_cr, pr_cf, pl_cr, pl_cf in zip(ids, prev_resp_resps_bools, prev_resp_dwells_bools, prev_last_dwell_resps_bools,prev_last_dwell_dwells_bools):
	# 			data.loc[index_counter] = [subid, name, pr_cr, pr_cf, pl_cr, pl_cf];
	# 			index_counter+=1;
	# 
	# 
	# if eyed=='agg':
	# 	data.to_csv(savepath+'prev_trial_data.csv',index=False);

	1/0
		
		
		
def computeOneDwellTrialData(blocks, eyed='agg'):
	#check out the data for the trials where one dwell occurred
	#Compute:
	#1. For each subject, compute number/proportion of single dwell trials
	#^(compare against the corrective saccade data to see if high percentage of corrective saccades correlated with nr of single dwell trials)
	#2. What are the latencies of single dwell trials?
	#3. Where are these one dwell trials going? (Heatmaps)
	#4. What is being selected on single dwell trials?
	
	#below here, use the code to compute the number of dwells from the function below
	db = subject_data;

	rexp_pattern = re.compile(r'01'); #this regular expression pattern looks for strings with a 1 or anything continuous run of 1s
	
	#loop through and get all the trials for each subject
	trial_matrix = [[tee for b in bl for tee in b.trials if (tee.skip==0)] for bl in blocks];

	#find each subjects' cue substance based on which item them chose more often during PAPC trials where they selected the alcohol or cigarette
	if eyed=='agg':
		index_counter=0; #index counter for the DataFrame object
		#here, create a dataframe object to save the subsequent data
		
	#find the number of dwells for each of the alcohol, cigarettes, and neutral items
	#get the aggregate breakdown as well as when they chose each item
	for ttype, name in zip([1,2,3,4],['high_pref', 'highC_lowA','lowC_highA','lowC_lowA']):		
		
		#proportion of trials the one dwells occurs on
		alc_prop_trials = []; cig_prop_trials = []; neu_prop_trials = []; total_prop_trials = [];
		chose_alc_alc_prop_trials= []; chose_alc_cig_prop_trials = []; chose_alc_neu_prop_trials = []; chose_alc_total_prop_trials = [];
		chose_cig_alc_prop_trials = []; chose_cig_cig_prop_trials = []; chose_cig_neu_prop_trials = []; chose_cig_total_prop_trials = [];
		chose_neu_alc_prop_trials = []; chose_neu_cig_prop_trials = []; chose_neu_neu_prop_trials = []; chose_neu_total_prop_trials = [];
		#latency for first saccade holders for the one dwells occurs
		alc_lats = []; cig_lats = [];neu_lats = []; total_lats = []; 
		chose_alc_alc_lats= []; chose_alc_cig_lats = []; chose_alc_neu_lats = []; chose_alc_total_lats = [];
		chose_cig_alc_lats = []; chose_cig_cig_lats = []; chose_cig_neu_lats = []; chose_cig_total_lats = [];
		chose_neu_alc_lats = []; chose_neu_cig_lats = []; chose_neu_neu_lats = []; chose_neu_total_lats = [];
		#end points of the first saccade
		alc_endpoints = []; cig_endpoints = [];neu_endpoints = []; total_endpoints= []; 
		chose_alc_alc_endpoints= []; chose_alc_cig_endpoints = []; chose_alc_neu_endpoints = []; chose_alc_total_endpoints = [];
		chose_cig_alc_endpoints = []; chose_cig_cig_endpoints = []; chose_cig_neu_endpoints = []; chose_cig_total_endpoints = [];
		chose_neu_alc_endpoints = []; chose_neu_cig_endpoints = []; chose_neu_neu_endpoints = []; chose_neu_total_endpoints = [];		
		#which object the one dwells looked at
		alc_dwelled_items = []; cig_dwelled_items = []; neu_dwelled_items = []; total_dwelled_items = []; 
		chose_alc_alc_dwelled_items= []; chose_alc_cig_dwelled_items = []; chose_alc_neu_dwelled_items = [];chose_alc_total_dwelled_items = [];
		chose_cig_alc_dwelled_items = []; chose_cig_cig_dwelled_items = []; chose_cig_neu_dwelled_items = []; chose_cig_total_dwelled_items = [];
		chose_neu_alc_dwelled_items = []; chose_neu_cig_dwelled_items = []; chose_neu_neu_dwelled_items = []; chose_neu_total_dwelled_items = [];
		
		#first run the analysis for all trials of this trial type, not breaking it down by whether they chose alcohol, cigeratte, or neutral
		#loop through trials for each subject
		for subj,sub_id in zip(trial_matrix, ids):
			alc_subj = []; cig_subj = []; neu_subj = []; tot_subj = [];
			alc_subj_lats  = []; cig_subj_lats  = []; neu_subj_lats  = []; tot_subj_lats  = [];
			alc_subj_endpoints = []; cig_subj_endpoints = []; neu_subj_endpoints = []; tot_subj_endpoints = [];
			alc_subj_dwelled_items = []; cig_subj_dwelled_items = []; neu_subj_dwelled_items = []; tot_subj_dwelled_items = [];
			
			for t in subj:
				if((t.dropped_sample == 0)&(t.didntLookAtAnyItems == 0)&(t.trial_type == ttype)&
					(t.skip == 0)&(sqrt(t.eyeX[0]**2 + t.eyeY[0]**2) < 2.5)):
					
					#In the computation of the lookedAtXX arrays during trial pre-processing, I include NaNs at times when no itm
					#was looked at... e.g., when the participant was fixating the center of the screen.
					#In order to ensure that I capture the change from not looking at one item to looking at any item (like the first dwell),
					#I need to convert those NaNs to 0's for calculation using the string-based method below. However, I want the original
					#lookedAtXX arrays to maintain the Nan, 0, 1 coding scheme, so I'll create holder arrays for each trial to use for the nr of dwell
					#calculations here
					
					looked_at_alcohol = array([r if ((r==0)|(r==1)) else 0 for r in t.lookedAtAlcohol]);
					looked_at_cigarette = array([r if ((r==0)|(r==1)) else 0 for r in t.lookedAtCigarette]);
					looked_at_neutral = array([r if ((r==0)|(r==1)) else 0 for r in t.lookedAtNeutral]);
					
					total_holder = 0; #this determines how many items are dwelled on
					
					str_alc = ''.join(str(int(g)) for g in looked_at_alcohol if not(isnan(g))); #first get the array into a string
					run_lengths_alc = [len(f) for f in rexp_pattern.findall(str_alc)];
					#line above, then use the regular expression pattern, looking for 1s, to parse an array of the continuous runs of 1s in the string from above and get length
					nr_fixs = sum([1 for r in run_lengths_alc]);
					#Nuances of this code are below
					if str_alc[0]=='1':
						nr_fixs +=1;
					total_holder+=nr_fixs; #add the nr of dwells from looking at alc to this holder variable
					
					str_cig = ''.join(str(int(g)) for g in looked_at_cigarette if not(isnan(g))); #parse cigarette
					run_lengths_cig = [len(f) for f in rexp_pattern.findall(str_cig)];
					nr_fixs = sum([1 for r in run_lengths_cig]);
					#check if the first item is a 1... if so, the array started with looking at the item and it wouldnt be caught by the regexp. need to correcy
					if str_cig[0]=='1':
						nr_fixs +=1;
					total_holder+=nr_fixs; #add the nr of dwells from looking at cig to this holder variable

					str_neu = ''.join(str(int(g)) for g in looked_at_neutral if not(isnan(g))); #do the parsing for neutral..
					run_lengths_neu = [len(f) for f in rexp_pattern.findall(str_neu)];
					nr_fixs = sum([1 for r in run_lengths_neu]);
					#check if the first item is a 1... if so, the array started with looking at the item and it wouldnt be caught by the regexp. need to correcy
					if str_neu[0]=='1':
						nr_fixs +=1;
					total_holder+=nr_fixs; #add the nr of dwells from looking at neu to this holder variable
					
					#conditional to determine if the number of dwells was one or not
					#below here append the behavioral information to the holder variables
					if total_holder==1:
						
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
						
						#calculate the latency and endpoint, then save to the subject's array
						total_subj_lats.append(sac_start_time);
						total_subj_endpoints.append(sac_end_pos);
						
						#add prop times and dwelled items
		
		
		
		
		
		
def computeNrDwells(blocks, eyed='agg'):		
	# determine the number of unique fixations to each item in a trial
	#compute this for all trial types, and then do it for breakdown of which item was selected
	db = subject_data;
	
	rexp_pattern = re.compile(r'01'); #this regular expression pattern looks for strings with a 1 or anything continuous run of 1s
	
	#loop through and get all the trials for each subject
	trial_matrix = [[tee for b in bl for tee in b.trials if (tee.skip==0)] for bl in blocks];

	#find each subjects' cue substance based on which item them chose more often during PAPC trials where they selected the alcohol or cigarette
	if eyed=='agg':
		index_counter=0; #index counter for the DataFrame object		
		data = pd.DataFrame(columns = ['sub_id','trial_type','alc_avg_nr_fixations','cig_avg_nr_fixations','neu_avg_nr_fixations',
									   'chose_alc_alc_avg_nr_fixations','chose_alc_cig_avg_nr_fixations','chose_alc_neu_avg_nr_fixations',
									   'chose_cig_alc_avg_nr_fixations','chose_cig_cig_avg_nr_fixations','chose_cig_neu_avg_nr_fixations',
									   'chose_neu_alc_avg_nr_fixations','chose_neu_cig_avg_nr_fixations','chose_neu_neu_avg_nr_fixations',
									   'total_avg_nr_fixations','chose_alc_total_avg_nr_fixations','chose_cig_total_avg_nr_fixations',
									   'chose_neu_total_avg_nr_fixations']);		

	#get the avg sustained response at each of the alcohol, cigarettes, and neutral items
	#get the aggregate breakdown as well as when they chose each item
	for ttype, name in zip([1,2,3,4],['high_pref', 'highC_lowA','lowC_highA','lowC_lowA']):
		
		alc_nr_fix = [];
		cig_nr_fix = [];
		neu_nr_fix = [];
		total_nr_fix = []; #a holder to determine the total nr of dwells across items
		chose_alc_alc_nr_fix = [];
		chose_alc_cig_nr_fix = [];
		chose_alc_neu_nr_fix = [];
		chose_alc_total_nr_fix = [];
		chose_cig_alc_nr_fix = [];
		chose_cig_cig_nr_fix = [];
		chose_cig_neu_nr_fix = [];
		chose_cig_total_nr_fix = [];
		chose_neu_alc_nr_fix = [];
		chose_neu_cig_nr_fix = [];
		chose_neu_neu_nr_fix = [];
		chose_neu_total_nr_fix = [];

		#first run the analysis for all trials of this trial type, not breaking it down by whether they chose alcohol, cigeratte, or neutral
		#loop through trials for each subject
		for subj,sub_id in zip(trial_matrix, ids):
			alc_subj = [];
			cig_subj = [];
			neu_subj = [];
			tot_subj = [];
			
			for t in subj:
				if((t.dropped_sample == 0)&(t.didntLookAtAnyItems == 0)&(t.trial_type == ttype)&
					(t.skip == 0)&(sqrt(t.eyeX[0]**2 + t.eyeY[0]**2) < 2.5)):

					#In the computation of the lookedAtXX arrays during trial pre-processing, I include NaNs at times when no itm
					#was looked at... e.g., when the participant was fixating the center of the screen.
					#In order to ensure that I capture the change from not looking at one item to looking at any item (like the first dwell),
					#I need to convert those NaNs to 0's for calculation using the string-based method below. However, I want the original
					#lookedAtXX arrays to maintain the Nan, 0, 1 coding scheme, so I'll create holder arrays for each trial to use for the nr of dwell
					#calculations here
					
					looked_at_alcohol = array([r if ((r==0)|(r==1)) else 0 for r in t.lookedAtAlcohol]);
					looked_at_cigarette = array([r if ((r==0)|(r==1)) else 0 for r in t.lookedAtCigarette]);
					looked_at_neutral = array([r if ((r==0)|(r==1)) else 0 for r in t.lookedAtNeutral]);
					
					total_holder = 0;
					
					str_alc = ''.join(str(int(g)) for g in looked_at_alcohol if not(isnan(g))); #first get the array into a string
					run_lengths_alc = [len(f) for f in rexp_pattern.findall(str_alc)];
					#line above, then use the regular expression pattern, looking for 1s, to parse an array of the continuous runs of 1s in the string from above and get length
					nr_fixs = sum([1 for r in run_lengths_alc]);
					#check if the first item is a 1... if so, the array started with looking at the item and it wouldnt be caught by the regexp.
					#this will only be the case if they weren't looking at anything to start (e.g., there were nan's to start, then the first item was looked at)
					#notice that because I have included NaNs in the t.lookedAtXX arrays for when items are not being looked at, the subsequent str_alc array
					#represents sequences of 1s and 0 s corresponding runs of looking at items, squished into the array; This means str_alc does not include
					#any information about samples where the eye was not on an item, which means this method cannot be used to understand differences in time between
					#dwells when that time is not being spent on an item. This is important to keep in mind
					if str_alc[0]=='1':
						nr_fixs +=1;
					if (nr_fixs==0): alc_subj.append(0);
					else: alc_subj.append(nr_fixs); #append nr of fixations
					
					total_holder+=nr_fixs; #add the nr of dwells from looking at alc to this holder variable
					
					str_cig = ''.join(str(int(g)) for g in looked_at_cigarette if not(isnan(g))); #parse cigarette
					run_lengths_cig = [len(f) for f in rexp_pattern.findall(str_cig)];
					nr_fixs = sum([1 for r in run_lengths_cig]);
					#check if the first item is a 1... if so, the array started with looking at the item and it wouldnt be caught by the regexp. need to correcy
					if str_cig[0]=='1':
						nr_fixs +=1;
					if (nr_fixs==0): cig_subj.append(0);
					else: cig_subj.append(nr_fixs);
					total_holder+=nr_fixs; #add the nr of dwells from looking at cig to this holder variable


					str_neu = ''.join(str(int(g)) for g in looked_at_neutral if not(isnan(g))); #do the parsing for neutral..
					run_lengths_neu = [len(f) for f in rexp_pattern.findall(str_neu)];
					nr_fixs = sum([1 for r in run_lengths_neu]);
					#check if the first item is a 1... if so, the array started with looking at the item and it wouldnt be caught by the regexp. need to correcy
					if str_neu[0]=='1':
						nr_fixs +=1;
					if (nr_fixs==0): neu_subj.append(0);
					else: neu_subj.append(nr_fixs);
					total_holder+=nr_fixs; #add the nr of dwells from looking at neu to this holder variable
					
					tot_subj.append(total_holder); #append the total nr of dwells for this trial
					
					# #used to plot eye trace and confirm the dwell calculation is correct
					# if t.trial_nr > 16:
						# # 
						# plotSingleTrialEyeGaze(t,'Nr of dwells: %s'%(sum(array([alc_subj[-1],cig_subj[-1],neu_subj[-1]]))));	#now plot the trial's data to see if the dwell calculation is correct
						# show();
						# 1/0
					# 	
					# 	close('all');
									
			#below here need to make sure I am getting the information I want (mean nr of dwells on each item, for each subject)
			
			alc_nr_fix.append(mean(alc_subj));
			cig_nr_fix.append(mean(cig_subj));
			neu_nr_fix.append(mean(neu_subj));
			total_nr_fix.append(mean(tot_subj));
			
		#below here append averages to the database 
		db['%s_%s_alc_mean_nr_fix'%(eyed,name)] = nanmean(alc_nr_fix); db['%s_%s_alc_bs_sems_nr_fix'%(eyed,name)] = compute_BS_SEM(alc_nr_fix);
		db['%s_%s_cig_mean_nr_fix'%(eyed,name)] = nanmean(cig_nr_fix); db['%s_%s_cig_bs_sems_nr_fix'%(eyed,name)] = compute_BS_SEM(cig_nr_fix);
		db['%s_%s_neu_mean_nr_fix'%(eyed,name)] = nanmean(neu_nr_fix); db['%s_%s_neu_bs_sems_nr_fix'%(eyed,name)] = compute_BS_SEM(neu_nr_fix);
		db['%s_%s_tot_mean_nr_fix'%(eyed,name)] = nanmean(total_nr_fix); db['%s_%s_tot_bs_sems_nr_fix'%(eyed,name)] = compute_BS_SEM(total_nr_fix);
		db.sync();		


		#now break it down by which item was chosen
		for selected_item in ['alcohol','cigarette','neutral']:			
			#loop through trials for each subject
			for subj,sub_id in zip(trial_matrix, ids):
				
				chose_alc_alc_subj = [];
				chose_alc_cig_subj = [];
				chose_alc_neu_subj = [];
				chose_alc_tot_subj = []; #total holder
				chose_cig_alc_subj = [];
				chose_cig_cig_subj = [];
				chose_cig_neu_subj = [];
				chose_cig_tot_subj = []; #total holder
				chose_neu_alc_subj = [];
				chose_neu_cig_subj = [];
				chose_neu_neu_subj = [];
				chose_neu_tot_subj = []; #total holder

				for t in subj:
					if((t.dropped_sample == 0)&(t.didntLookAtAnyItems == 0)&(t.trial_type == ttype)&(t.preferred_category==selected_item)):
	
						looked_at_alcohol = array([r if ((r==0)|(r==1)) else 0 for r in t.lookedAtAlcohol]);
						looked_at_cigarette = array([r if ((r==0)|(r==1)) else 0 for r in t.lookedAtCigarette]);
						looked_at_neutral = array([r if ((r==0)|(r==1)) else 0 for r in t.lookedAtNeutral]);
						
						total_holder = 0;
						
						#conditional
						if selected_item=='alcohol':
							str_alc = ''.join(str(int(g)) for g in looked_at_alcohol if not(isnan(g))); #first get the array into a string
							run_lengths_alc = [len(f) for f in rexp_pattern.findall(str_alc)];
							#line above, then use the regular expression pattern, looking for 1s, to parse an array of the continuous runs of 1s in the string from above and get length
							nr_fixs = sum([1 for r in run_lengths_alc]);
							#check if the first item is a 1... if so, the array started with looking at the item and it wouldnt be caught by the regexp. need to correcy
							if str_alc[0]=='1':
								nr_fixs +=1;
							if (nr_fixs==0): chose_alc_alc_subj.append(0);
							else: chose_alc_alc_subj.append(nr_fixs); #append nr of fixations
							total_holder+=nr_fixs; #add the nr of dwells from looking at neu to this holder variable
							chose_alc_tot_subj.append(total_holder); #append the total nr of dwells for this trial
							
							str_cig = ''.join(str(int(g)) for g in looked_at_cigarette if not(isnan(g))); #parse cigarette
							run_lengths_cig = [len(f) for f in rexp_pattern.findall(str_cig)];
							nr_fixs = sum([1 for r in run_lengths_cig]);
							#check if the first item is a 1... if so, the array started with looking at the item and it wouldnt be caught by the regexp. need to correcy
							if str_cig[0]=='1':
								nr_fixs +=1;
							if (nr_fixs==0): chose_alc_cig_subj.append(0);
							else: chose_alc_cig_subj.append(nr_fixs);				
							total_holder+=nr_fixs; #add the nr of dwells from looking at neu to this holder variable
							chose_alc_tot_subj.append(total_holder); #append the total nr of dwells for this trial
							
							str_neu = ''.join(str(int(g)) for g in looked_at_neutral if not(isnan(g))); #do the parsing for neutral..
							run_lengths_neu = [len(f) for f in rexp_pattern.findall(str_neu)];
							nr_fixs = sum([1 for r in run_lengths_neu]);
							#check if the first item is a 1... if so, the array started with looking at the item and it wouldnt be caught by the regexp. need to correcy
							if str_neu[0]=='1':
								nr_fixs +=1;
							if (nr_fixs==0): chose_alc_neu_subj.append(0);
							else: chose_alc_neu_subj.append(nr_fixs);			
							total_holder+=nr_fixs; #add the nr of dwells from looking at neu to this holder variable
							chose_alc_tot_subj.append(total_holder); #append the total nr of dwells for this trial
							
						elif selected_item=='cigarette':				
							str_alc = ''.join(str(int(g)) for g in looked_at_alcohol if not(isnan(g))); #first get the array into a string
							run_lengths_alc = [len(f) for f in rexp_pattern.findall(str_alc)];
							#line above, then use the regular expression pattern, looking for 1s, to parse an array of the continuous runs of 1s in the string from above and get length
							nr_fixs = sum([1 for r in run_lengths_alc]);
							#check if the first item is a 1... if so, the array started with looking at the item and it wouldnt be caught by the regexp. need to correcy
							if str_alc[0]=='1':
								nr_fixs +=1;
							if (nr_fixs==0): chose_cig_alc_subj.append(0);
							else: chose_cig_alc_subj.append(nr_fixs); #append the max, if there is one
							total_holder+=nr_fixs; #add the nr of dwells from looking at alc to this holder variable
							chose_cig_tot_subj.append(total_holder); #append the total nr of dwells for this trial
							
							str_cig = ''.join(str(int(g)) for g in looked_at_cigarette if not(isnan(g))); #parse cigarette
							run_lengths_cig = [len(f) for f in rexp_pattern.findall(str_cig)];
							nr_fixs = sum([1 for r in run_lengths_cig]);
							#check if the first item is a 1... if so, the array started with looking at the item and it wouldnt be caught by the regexp. need to correcy
							if str_cig[0]=='1':
								nr_fixs +=1;
							if (nr_fixs==0): chose_cig_cig_subj.append(0);
							else: chose_cig_cig_subj.append(nr_fixs);				
							total_holder+=nr_fixs; #add the nr of dwells from looking at cig to this holder variable
							chose_cig_tot_subj.append(total_holder); #append the total nr of dwells for this trial
							
							str_neu = ''.join(str(int(g)) for g in looked_at_neutral if not(isnan(g))); #do the parsing for neutral..
							run_lengths_neu = [len(f) for f in rexp_pattern.findall(str_neu)];
							nr_fixs = sum([1 for r in run_lengths_neu]);
							#check if the first item is a 1... if so, the array started with looking at the item and it wouldnt be caught by the regexp. need to correcy
							if str_neu[0]=='1':
								nr_fixs +=1;
							if (nr_fixs==0): chose_cig_neu_subj.append(0);
							else: chose_cig_neu_subj.append(nr_fixs);			
							total_holder+=nr_fixs; #add the nr of dwells from looking at neu to this holder variable
							chose_cig_tot_subj.append(total_holder); #append the total nr of dwells for this trial
							
						elif selected_item=='neutral':
							str_alc = ''.join(str(int(g)) for g in looked_at_alcohol if not(isnan(g))); #first get the array into a string
							run_lengths_alc = [len(f) for f in rexp_pattern.findall(str_alc)];
							#line above, then use the regular expression pattern, looking for 1s, to parse an array of the continuous runs of 1s in the string from above and get length
							nr_fixs = sum([1 for r in run_lengths_alc]);
							#check if the first item is a 1... if so, the array started with looking at the item and it wouldnt be caught by the regexp. need to correcy
							if str_alc[0]=='1':
								nr_fixs +=1;
							if (nr_fixs==0): chose_neu_alc_subj.append(0);
							else: chose_neu_alc_subj.append(nr_fixs); #append the max, if there is one
							total_holder+=nr_fixs; #add the nr of dwells from looking at alc to this holder variable
							chose_neu_tot_subj.append(total_holder); #append the total nr of dwells for this trial
							
							str_cig = ''.join(str(int(g)) for g in looked_at_cigarette if not(isnan(g))); #parse cigarette
							run_lengths_cig = [len(f) for f in rexp_pattern.findall(str_cig)];
							nr_fixs = sum([1 for r in run_lengths_cig]);
							#check if the first item is a 1... if so, the array started with looking at the item and it wouldnt be caught by the regexp. need to correcy
							if str_cig[0]=='1':
								nr_fixs +=1;
							if (nr_fixs==0): chose_neu_cig_subj.append(0);
							else: chose_neu_cig_subj.append(nr_fixs);				
							total_holder+=nr_fixs; #add the nr of dwells from looking at cig to this holder variable
							chose_neu_tot_subj.append(total_holder); #append the total nr of dwells for this trial
							
							str_neu = ''.join(str(int(g)) for g in looked_at_neutral if not(isnan(g))); #do the parsing for neutral..
							run_lengths_neu = [len(f) for f in rexp_pattern.findall(str_neu)];
							nr_fixs = sum([1 for r in run_lengths_neu]);
							#check if the first item is a 1... if so, the array started with looking at the item and it wouldnt be caught by the regexp. need to correcy
							if str_neu[0]=='1':
								nr_fixs +=1;
							if (nr_fixs==0): chose_neu_neu_subj.append(0);
							else: chose_neu_neu_subj.append(nr_fixs);			
							total_holder+=nr_fixs; #add the nr of dwells from looking at neu to this holder variable
							chose_neu_tot_subj.append(total_holder); #append the total nr of dwells for this trial
							
				#append data to the all subject holders
				if selected_item=='alcohol':
					chose_alc_alc_nr_fix.append(mean(chose_alc_alc_subj));
					chose_alc_cig_nr_fix.append(mean(chose_alc_cig_subj));
					chose_alc_neu_nr_fix.append(mean(chose_alc_neu_subj));
					chose_alc_total_nr_fix.append(mean(chose_alc_tot_subj));
				elif selected_item=='cigarette':
					chose_cig_alc_nr_fix.append(mean(chose_cig_alc_subj));
					chose_cig_cig_nr_fix.append(mean(chose_cig_cig_subj));
					chose_cig_neu_nr_fix.append(mean(chose_cig_neu_subj));
					chose_cig_total_nr_fix.append(mean(chose_cig_tot_subj));
				elif selected_item=='neutral':
					chose_neu_alc_nr_fix.append(mean(chose_neu_alc_subj));
					chose_neu_cig_nr_fix.append(mean(chose_neu_cig_subj));
					chose_neu_neu_nr_fix.append(mean(chose_neu_neu_subj));
					chose_neu_total_nr_fix.append(mean(chose_neu_tot_subj));
					
				# if (sub_id == ids[20]) & (selected_item == 'neutral'):
				# 	1/0 #check out why this person has an average of 15 dwells
					
		#1/0 #check the standard error of the choose neutral neutral condition...			
							
		#below here append averages to the database
		db['%s_%s_chose_alc_alc_mean_nr_fix'%(eyed,name)] = nanmean(chose_alc_alc_nr_fix); db['%s_%s_chose_alc_alc_bs_sems_nr_fix'%(eyed,name)] = compute_BS_SEM(chose_alc_alc_nr_fix);
		db['%s_%s_chose_alc_cig_mean_nr_fix'%(eyed,name)] = nanmean(chose_alc_cig_nr_fix); db['%s_%s_chose_alc_cig_bs_sems_nr_fix'%(eyed,name)] = compute_BS_SEM(chose_alc_cig_nr_fix);
		db['%s_%s_chose_alc_neu_mean_nr_fix'%(eyed,name)] = nanmean(chose_alc_neu_nr_fix); db['%s_%s_chose_alc_neu_bs_sems_nr_fix'%(eyed,name)] = compute_BS_SEM(chose_alc_neu_nr_fix);				
		db['%s_%s_chose_alc_tot_mean_nr_fix'%(eyed,name)] = nanmean(chose_alc_total_nr_fix); db['%s_%s_chose_alc_tot_bs_sems_nr_fix'%(eyed,name)] = compute_BS_SEM(chose_alc_total_nr_fix);
		#HP condition,25 participants, 5 didn't choose alvohol ever

		db['%s_%s_chose_cig_alc_mean_nr_fix'%(eyed,name)] = nanmean(chose_cig_alc_nr_fix); db['%s_%s_chose_cig_alc_bs_sems_nr_fix'%(eyed,name)] = compute_BS_SEM(chose_cig_alc_nr_fix);
		db['%s_%s_chose_cig_cig_mean_nr_fix'%(eyed,name)] = nanmean(chose_cig_cig_nr_fix); db['%s_%s_chose_cig_cig_bs_sems_nr_fix'%(eyed,name)] = compute_BS_SEM(chose_cig_cig_nr_fix);
		db['%s_%s_chose_cig_neu_mean_nr_fix'%(eyed,name)] = nanmean(chose_cig_neu_nr_fix); db['%s_%s_chose_cig_neu_bs_sems_nr_fix'%(eyed,name)] = compute_BS_SEM(chose_cig_neu_nr_fix);
		db['%s_%s_chose_cig_tot_mean_nr_fix'%(eyed,name)] = nanmean(chose_cig_total_nr_fix); db['%s_%s_chose_cig_tot_bs_sems_nr_fix'%(eyed,name)] = compute_BS_SEM(chose_cig_total_nr_fix);
		#HP condition,all 29 participants chose cigarette at some point, they are all included here		
				
		db['%s_%s_chose_neu_alc_mean_nr_fix'%(eyed,name)] = nanmean(chose_neu_alc_nr_fix); db['%s_%s_chose_neu_alc_bs_sems_nr_fix'%(eyed,name)] = compute_BS_SEM(chose_neu_alc_nr_fix);
		db['%s_%s_chose_neu_cig_mean_nr_fix'%(eyed,name)] = nanmean(chose_neu_cig_nr_fix); db['%s_%s_chose_neu_cig_bs_sems_nr_fix'%(eyed,name)] = compute_BS_SEM(chose_neu_cig_nr_fix);
		db['%s_%s_chose_neu_neu_mean_nr_fix'%(eyed,name)] = nanmean(chose_neu_neu_nr_fix); db['%s_%s_chose_neu_neu_bs_sems_nr_fix'%(eyed,name)] = compute_BS_SEM(chose_neu_neu_nr_fix);	
		db['%s_%s_chose_neu_tot_mean_nr_fix'%(eyed,name)] = nanmean(chose_neu_total_nr_fix); db['%s_%s_chose_neu_tot_bs_sems_nr_fix'%(eyed,name)] = compute_BS_SEM(chose_neu_total_nr_fix);
		#HP condition, for chose neutral trials: 20 participants only, 9 don't have any trials whre they chose neutral
		# subject cret27 (ids[20)]) only has only trial where they chose neutral, which leads to the large nr of mean dwells (15)
		db.sync();
	
		#below here append all the data to the DataFrame and then save it as a .csv		
		for sub_id, alc, cig, neu, alc_alc, alc_cig, alc_neu, cig_alc, cig_cig, cig_neu, neu_alc, neu_cig, neu_neu, tot_fix, ca_tot_fix, cc_tot_fix, cn_tot_fix \
			in zip(ids, alc_nr_fix, cig_nr_fix, neu_nr_fix, \
			chose_alc_alc_nr_fix, chose_alc_cig_nr_fix, chose_alc_neu_nr_fix, \
			chose_cig_alc_nr_fix, chose_cig_cig_nr_fix, chose_cig_neu_nr_fix, \
			chose_neu_alc_nr_fix, chose_neu_cig_nr_fix, chose_neu_neu_nr_fix, \
			total_nr_fix, chose_alc_total_nr_fix, chose_cig_total_nr_fix, chose_neu_total_nr_fix):

			#confirm that alc, cig, neu, etc 
			
			data.loc[index_counter] = [sub_id, name, mean(alc), mean(cig), mean(neu), \
									   mean(alc_alc), mean(alc_cig), mean(alc_neu), \
									mean(cig_alc), mean(cig_cig), mean(cig_neu), \
									mean(neu_alc), mean(neu_cig), mean(neu_neu), \
									mean(tot_fix), mean(ca_tot_fix), mean(cc_tot_fix), mean(cn_tot_fix)];
			index_counter+=1;					

	if eyed=='agg':
		data.to_csv(savepath+'avg_nr_dwells_item.csv',index=False);
		

def computeProportionSelect(blocks, eyed = 'agg'):
	db = subject_data;
	#loop through and get all the trials for each subject
	trial_matrix = [[tee for b in bl for tee in b.trials if (tee.skip==0)] for bl in blocks];
	
	for ttype, name in zip([1,2,3,4],['high_pref', 'highC_lowA','lowC_highA','lowC_lowA']):	
	
		#this formulation is for the non-preference breakdown. not_hp stands for 'all high preference trials, even those where neutral was selected'
		all_hp_all_substances = [[tee.preferred_category for tee in subject if ((tee.dropped_sample == 0)&(tee.didntLookAtAnyItems == 0)&(tee.trial_type == ttype)&
			(tee.skip == 0)&(sqrt(tee.eyeX[0]**2 + tee.eyeY[0]**2) < 2.5))]
			for subject in trial_matrix]; #first get all the selected categories
		all_hp_prop_chose_alc = [sum([val == 'alcohol' for val in subject])/float(len([val == 'alcohol' for val in subject])) for subject in all_hp_all_substances]; #now get proportion of time seleteced alcohol
		all_hp_prop_chose_cig = [sum([val == 'cigarette' for val in subject])/float(len([val == 'alcohol' for val in subject])) for subject in all_hp_all_substances];
		all_hp_prop_chose_neu = [sum([val == 'neutral' for val in subject])/float(len([val == 'alcohol' for val in subject])) for subject in all_hp_all_substances];
	
		#save them to the database
		db['%s_%s_all_hp_mean_chose_alc'%(eyed,name)] = nanmean(all_hp_prop_chose_alc); db['%s_%s_all_hp_bs_sems_chose_alc'%(eyed,name)] = compute_BS_SEM(all_hp_prop_chose_alc);	
		db['%s_%s_all_hp_mean_chose_cig'%(eyed,name)] = nanmean(all_hp_prop_chose_cig); db['%s_%s_all_hp_bs_sems_chose_cig'%(eyed,name)] = compute_BS_SEM(all_hp_prop_chose_cig);
		db['%s_%s_all_hp_mean_chose_neu'%(eyed,name)] = nanmean(all_hp_prop_chose_neu); db['%s_%s_all_hp_bs_sems_chose_neu'%(eyed,name)] = compute_BS_SEM(all_hp_prop_chose_neu);
	db.sync();
	



#define a method that computes, for each subject, the average percentage of time spent looking at each of the items, including the preferred item
#do this for all trials, and then for trials where their two stated preferred items (e.g., trial type 1)
#assign each subject's data to a .csv and save it, and then campute the averages and plot for my use.

def computeProportionLookingTimes(blocks, eyed = 'agg'):
	db = subject_data;
	#loop through and get all the trials for each subject
	trial_matrix = [[tee for b in bl for tee in b.trials if (tee.skip==0)] for bl in blocks];
	
	#find each subjects' cue substance based on which item them chose more often during PAPC trials where they selected the alcohol or cigarette
	if eyed=='subjective_resps':
		subject_cues = [info[1] for info in subjective_prefs];
	elif eyed=='agg':
		all_substances = [[tee.preferred_category for tee in subject if (((tee.preferred_category=='alcohol')|(tee.preferred_category=='cigarette'))&
			(tee.dropped_sample == 0)&(tee.didntLookAtAnyItems == 0)&(tee.trial_type == 1))] for subject in trial_matrix]; #first get all the selected categories
		prop_chose_alc = [sum([val == 'alcohol' for val in subject])/float(len([val == 'alcohol' for val in subject])) for subject in all_substances]; #now get proportion of time seleteced alcohol
		prop_chose_cig = [sum([val == 'cigarette' for val in subject])/float(len([val == 'alcohol' for val in subject])) for subject in all_substances]; #then proportion of times selecting cigarette
		#then find which proportion is greater and define whether that subject's cue is alcohol or cigarette
		subject_cues = ['alcohol' if (a>c) else 'cigarette' for a,c in zip(prop_chose_alc,prop_chose_cig)];

		index_counter=0;

		# ##Build an average database instance of each value for each subject for high vs low preferred trials and the subsets of high preferred trials
		# data_preference = pd.DataFrame(columns = ['sub_id','subject_cue','selected','neu_mean_time_looking_at_pref','neu_mean_percentage_looking_at_pref',
		# 						   'cue_mean_time_looking_at_pref','cue_mean_percentage_looking_at_pref','not_cue_mean_time_looking_at_pref',
		# 						   'not_cue_mean_percentage_looking_at_pref', 'mean_response_time']);
		#database for the mean proportion of looking time for alcoho and cigarette items 
		data = pd.DataFrame(columns = ['sub_id','trial_type','prop_trials_chose_alc','prop_trials_chose_cig','prop_trials_chose_neu','neu_avg_looking_time','neu_avg_prop_time','cig_avg_looking_time','cig_avg_prop_time','alc_avg_looking_time',
									   'alc_avg_prop_time','avg_rt','chose_alc_neu_avg_looking_time','chose_alc_neu_avg_prop_time','chose_alc_cig_avg_looking_time',
									   'chose_alc_cig_avg_prop_time','chose_alc_alc_avg_looking_time','chose_alc_alc_avg_prop_time','chose_alc_avg_rt',
									   'chose_cig_neu_avg_looking_time','chose_cig_neu_avg_prop_time','chose_cig_cig_avg_looking_time','chose_cig_cig_avg_prop_time','chose_cig_alc_avg_looking_time',
									   'chose_cig_alc_avg_prop_time','chose_cig_avg_rt','chose_neu_neu_avg_looking_time','chose_neu_neu_avg_prop_time','chose_neu_cig_avg_looking_time',
									   'chose_neu_cig_avg_prop_time','chose_neu_alc_avg_looking_time','chose_neu_alc_avg_prop_time','chose_neu_avg_rt']);


		#this formulation is for the non-preference breakdown. not_hp stands for 'all high preference trials, even those where neutral was selected'
		all_hp_all_substances = [[tee.preferred_category for tee in subject if ((tee.dropped_sample == 0)&(tee.didntLookAtAnyItems == 0)&(tee.trial_type == 1))]
			for subject in trial_matrix]; #first get all the selected categories
		all_hp_prop_chose_alc = [sum([val == 'alcohol' for val in subject])/float(len([val == 'alcohol' for val in subject])) for subject in all_hp_all_substances]; #now get proportion of time seleteced alcohol
		all_hp_prop_chose_cig = [sum([val == 'cigarette' for val in subject])/float(len([val == 'alcohol' for val in subject])) for subject in all_hp_all_substances];
		all_hp_prop_chose_neu = [sum([val == 'neutral' for val in subject])/float(len([val == 'alcohol' for val in subject])) for subject in all_hp_all_substances];


	#get the proportion of looking time data for alcohol, cigarettes, and neutral items
	#get the aggregate breakdwon as well as when they chose each item
	#for high_pref_trial,name in zip([0,1],['non_high_pref','high_pref']):
	for ttype, name in zip([1,2,3,4],['high_pref', 'highC_lowA','lowC_highA','lowC_lowA']):
		
		
		#this formulation is for the non-preference breakdown. not_hp stands for 'all high preference trials, even those where neutral was selected'
		all_substances = [[tee.preferred_category for tee in subject if ((tee.dropped_sample == 0)&(tee.didntLookAtAnyItems == 0)&(tee.trial_type == ttype)&
			(tee.skip == 0)&(sqrt(tee.eyeX[0]**2 + tee.eyeY[0]**2) < 2.5))]
			for subject in trial_matrix]; #first get all the selected categories
		all_prop_chose_alc = [sum([val == 'alcohol' for val in subject])/float(len([val == 'alcohol' for val in subject])) for subject in all_substances]; #now get proportion of time seleteced alcohol
		all_prop_chose_cig = [sum([val == 'cigarette' for val in subject])/float(len([val == 'alcohol' for val in subject])) for subject in all_substances];
		all_prop_chose_neu = [sum([val == 'neutral' for val in subject])/float(len([val == 'alcohol' for val in subject])) for subject in all_substances];
		
		
		#define holders for each breakdown of the data to store each subjects' respective data
		neu_subject_times = []; 
		neu_subject_percs = [];
		alc_subject_times = [];
		alc_subject_percs = [];
		cig_subject_times = [];
		cig_subject_percs = [];
		all_rts = [];		
		chose_alc_neu_subject_times = [];  
		chose_alc_neu_subject_percs = [];
		chose_alc_alc_subject_times = [];
		chose_alc_alc_subject_percs = [];
		chose_alc_cig_subject_times = [];
		chose_alc_cig_subject_percs = [];
		chose_alc_all_rts = [];
		chose_cig_neu_subject_times = []; 
		chose_cig_neu_subject_percs = [];
		chose_cig_alc_subject_times = [];
		chose_cig_alc_subject_percs = [];
		chose_cig_cig_subject_times = [];
		chose_cig_cig_subject_percs = [];
		chose_cig_all_rts = [];
		chose_neu_neu_subject_times = []; 
		chose_neu_neu_subject_percs = [];
		chose_neu_alc_subject_times = [];
		chose_neu_alc_subject_percs = [];
		chose_neu_cig_subject_times = [];
		chose_neu_cig_subject_percs = [];
		chose_neu_all_rts = [];			
		#first run the analysis for all high preference trials, not breaking it down by whether they chose alcohol, cigeratte, or neutral
		#loop through trials for each subject
		for subj,sub_id in zip(trial_matrix, ids):
			neu_time_at_pref = [];
			neu_perc_at_pref = [];
			alc_time_at_pref = [];
			alc_perc_at_pref = [];
			cig_time_at_pref = [];
			cig_perc_at_pref = [];
			rts = [];			
			for t in subj:
				if((t.dropped_sample == 0)&(t.didntLookAtAnyItems == 0)&(t.trial_type == ttype)):                     #==high_pref_trial)):					
					neu_time_at_pref.append(t.timeLookingAtNeutral);
					neu_perc_at_pref.append(t.percentageTimeLookingAtNeutral);	
					alc_time_at_pref.append(t.timeLookingAtAlcohol);
					alc_perc_at_pref.append(t.percentageTimeLookingAtAlcohol);		
					cig_time_at_pref.append(t.timeLookingAtCigarette);
					cig_perc_at_pref.append(t.percentageTimeLookingAtCigarette);
					rts.append(t.response_time);
			neu_subject_times.append(nanmean(neu_time_at_pref)); 
			neu_subject_percs.append(nanmean(neu_perc_at_pref));
			alc_subject_times.append(nanmean(alc_time_at_pref));
			alc_subject_percs.append(nanmean(alc_perc_at_pref));
			cig_subject_times.append(nanmean(cig_time_at_pref));
			cig_subject_percs.append(nanmean(cig_perc_at_pref));
			all_rts.append(nanmean(rts));				
			# #append the individual subject data to the database
			# db['%s_high_pref_all_hp_look_at_neutral_mean_time_at_pref'%(sub_id)] = nanmean(neu_time_at_pref); 
			# db['%s_high_pref_all_hp_look_at_neutral_mean_perc_time_at_pref'%(sub_id)] = nanmean(neu_perc_at_pref);
			# db['%s_high_pref_all_hp_look_at_alc_mean_time_at_pref'%(sub_id)] = nanmean(alc_time_at_pref); 
			# db['%s_high_pref_all_hp_look_at_alc_mean_perc_time_at_pref'%(sub_id)] = nanmean(alc_perc_at_pref);
			# db['%s_high_pref_all_hp_look_at_cig_mean_time_at_pref'%(sub_id)] = nanmean(cig_time_at_pref); 
			# db['%s_high_pref_all_hp_look_at_cig_mean_perc_time_at_pref'%(sub_id)] = nanmean(cig_perc_at_pref); 					
			# db['%s_high_pref_all_hp_mean_rt'%(sub_id)] = nanmean(rts);
			# db.sync();
			
		#get the aggregated data points for this, across all subjects
		db['%s_%s_all_hp_look_at_neutral_mean_time_at_pref'%(eyed,name)] = nanmean(neu_subject_times); db['%s_%s_all_hp_look_at_neutral_bs_sems_time_at_pref'%(eyed,name)] = compute_BS_SEM(neu_subject_times);
		db['%s_%s_all_hp_look_at_neutral_mean_perc_time_at_pref'%(eyed,name)] = nanmean(neu_subject_percs); db['%s_%s_all_hp_look_at_neutral_bs_sems_perc_time_at_pref'%(eyed,name)] = compute_BS_SEM(neu_subject_percs);
		db['%s_%s_all_hp_look_at_alc_mean_time_at_pref'%(eyed,name)] = nanmean(alc_subject_times); db['%s_%s_all_hp_look_at_alc_bs_sems_time_at_pref'%(eyed,name)] = compute_BS_SEM(alc_subject_times); 
		db['%s_%s_all_hp_look_at_alc_mean_perc_time_at_pref'%(eyed,name)] = nanmean(alc_subject_percs); db['%s_%s_all_hp_look_at_alc_bs_sems_perc_time_at_pref'%(eyed,name)] = compute_BS_SEM(alc_subject_percs);
		db['%s_%s_all_hp_look_at_cig_mean_time_at_pref'%(eyed,name)] = nanmean(cig_subject_times);  db['%s_%s_all_hp_look_at_cig_bs_sems_time_at_pref'%(eyed,name)] = compute_BS_SEM(cig_subject_times); 
		db['%s_%s_all_hp_look_at_cig_mean_perc_time_at_pref'%(eyed,name)] = nanmean(cig_subject_percs); db['%s_%s_all_hp_look_at_cig_bs_sems_perc_time_at_pref'%(eyed,name)] = compute_BS_SEM(cig_subject_percs); 					
		db['%s_%s_all_hp_mean_rt'%(eyed,name)] = nanmean(all_rts); db['%s_%s_all_hp_bs_sems_rt'%(eyed,name)] = compute_BS_SEM(all_rts);	
		db.sync();
		
		#now run the analysis conditioned on which item was chosen
		for selected_item in ['alcohol','cigarette','neutral']:
			#loop through trials for each subject
			for subj,chose_alc,chose_cig,chose_neu,sub_id in zip(trial_matrix, all_prop_chose_alc, all_prop_chose_cig, all_prop_chose_neu, ids):
				neu_time_at_pref = [];
				neu_perc_at_pref = [];
				alc_time_at_pref = [];
				alc_perc_at_pref = [];
				cig_time_at_pref = [];
				cig_perc_at_pref = [];
				rts = [];	
				for t in subj:
					if((t.dropped_sample == 0)&(t.didntLookAtAnyItems == 0)&(t.trial_type == ttype)&(tee.skip == 0)&(sqrt(tee.eyeX[0]**2 + tee.eyeY[0]**2) < 2.5)):                       #==high_pref_trial)):					
						if (t.preferred_category==selected_item):
							neu_time_at_pref.append(t.timeLookingAtNeutral);
							neu_perc_at_pref.append(t.percentageTimeLookingAtNeutral);	
							alc_time_at_pref.append(t.timeLookingAtAlcohol);
							alc_perc_at_pref.append(t.percentageTimeLookingAtAlcohol);		
							cig_time_at_pref.append(t.timeLookingAtCigarette);
							cig_perc_at_pref.append(t.percentageTimeLookingAtCigarette);
							rts.append(t.response_time);
				#append this subjects' data to the holder list and calculate the nanmeans to store in the database
				if selected_item=='neutral':
					chose_neu_neu_subject_times.append(nanmean(neu_time_at_pref)); 
					chose_neu_neu_subject_percs.append(nanmean(neu_perc_at_pref));
					chose_neu_alc_subject_times.append(nanmean(alc_time_at_pref));
					chose_neu_alc_subject_percs.append(nanmean(alc_perc_at_pref));
					chose_neu_cig_subject_times.append(nanmean(cig_time_at_pref));
					chose_neu_cig_subject_percs.append(nanmean(cig_perc_at_pref));
					chose_neu_all_rts.append(nanmean(rts));					
				elif selected_item=='alcohol':
					chose_alc_neu_subject_times.append(nanmean(neu_time_at_pref)); 
					chose_alc_neu_subject_percs.append(nanmean(neu_perc_at_pref));
					chose_alc_alc_subject_times.append(nanmean(alc_time_at_pref));
					chose_alc_alc_subject_percs.append(nanmean(alc_perc_at_pref));
					chose_alc_cig_subject_times.append(nanmean(cig_time_at_pref));
					chose_alc_cig_subject_percs.append(nanmean(cig_perc_at_pref));
					chose_alc_all_rts.append(nanmean(rts));								
				elif selected_item=='cigarette':
					chose_cig_neu_subject_times.append(nanmean(neu_time_at_pref)); 
					chose_cig_neu_subject_percs.append(nanmean(neu_perc_at_pref));
					chose_cig_alc_subject_times.append(nanmean(alc_time_at_pref));
					chose_cig_alc_subject_percs.append(nanmean(alc_perc_at_pref));
					chose_cig_cig_subject_times.append(nanmean(cig_time_at_pref));
					chose_cig_cig_subject_percs.append(nanmean(cig_perc_at_pref));
					chose_cig_all_rts.append(nanmean(rts));								
					
				# #append the individual subject data to the database
				# db['%s_high_pref_selected_%s_look_at_neutral_mean_time_at_pref'%(sub_id,selected_item)] = nanmean(neu_time_at_pref); 
				# db['%s_high_pref_selected_%s_look_at_neutral_mean_perc_time_at_pref'%(sub_id,selected_item)] = nanmean(neu_perc_at_pref);
				# db['%s_high_pref_selected_%s_look_at_alc_mean_time_at_pref'%(sub_id,selected_item)] = nanmean(alc_time_at_pref); 
				# db['%s_high_pref_selected_%s_look_at_alc_mean_perc_time_at_pref'%(sub_id,selected_item)] = nanmean(alc_perc_at_pref);
				# db['%s_high_pref_selected_%s_look_at_cig_mean_time_at_pref'%(sub_id,selected_item)] = nanmean(cig_time_at_pref); 
				# db['%s_high_pref_selected_%s_look_at_cig_mean_perc_time_at_pref'%(sub_id,selected_item)] = nanmean(cig_perc_at_pref); 					
				# db['%s_high_pref_selected_%s_mean_rt'%(sub_id,selected_item)] = nanmean(rts);
				# db.sync();

		#now here aggregate all the data together and append it to the database
		#neutral first...
		db['%s_%s_selected_neutral_look_at_neutral_mean_time_at_pref'%(eyed,name)] = nanmean(chose_neu_neu_subject_times); db['%s_%s_selected_neutral_look_at_neutral_bs_sems_time_at_pref'%(eyed,name)] = compute_BS_SEM(chose_neu_neu_subject_times);
		db['%s_%s_selected_neutral_look_at_neutral_mean_perc_time_at_pref'%(eyed,name)] = nanmean(chose_neu_neu_subject_percs); db['%s_%s_selected_neutral_look_at_neutral_bs_sems_perc_time_at_pref'%(eyed,name)] = compute_BS_SEM(chose_neu_neu_subject_percs);				
		db['%s_%s_selected_neutral_look_at_alc_mean_time_at_pref'%(eyed,name)] = nanmean(chose_neu_alc_subject_times); db['%s_%s_selected_neutral_look_at_alc_bs_sems_time_at_pref'%(eyed,name)] = compute_BS_SEM(chose_neu_alc_subject_times);
		db['%s_%s_selected_neutral_look_at_alc_mean_perc_time_at_pref'%(eyed,name)] = nanmean(chose_neu_alc_subject_percs); db['%s_%s_selected_neutral_look_at_alc_bs_sems_perc_time_at_pref'%(eyed,name)] = compute_BS_SEM(chose_neu_alc_subject_percs);			
		db['%s_%s_selected_neutral_look_at_cig_mean_time_at_pref'%(eyed,name)] = nanmean(chose_neu_cig_subject_times); db['%s_%s_selected_neutral_look_at_cig_bs_sems_time_at_pref'%(eyed,name)] = compute_BS_SEM(chose_neu_cig_subject_times);
		db['%s_%s_selected_neutral_look_at_cig_mean_perc_time_at_pref'%(eyed,name)] = nanmean(chose_neu_cig_subject_percs); db['%s_%s_selected_neutral_look_at_cig_bs_sems_perc_time_at_pref'%(eyed,name)] = compute_BS_SEM(chose_neu_cig_subject_percs);				
		db['%s_%s_selected_neutral_mean_rt'%(eyed,name)] = nanmean(chose_neu_all_rts); db['%s_%s_selected_neutral_bs_sems_rt'%(eyed,name)] = compute_BS_SEM(chose_neu_all_rts);	
		db.sync();
		
		#cigarettes
		db['%s_%s_selected_cig_look_at_neutral_mean_time_at_pref'%(eyed,name)] = nanmean(chose_cig_neu_subject_times); db['%s_%s_selected_cig_look_at_neutral_bs_sems_time_at_pref'%(eyed,name)] = compute_BS_SEM(chose_cig_neu_subject_times);
		db['%s_%s_selected_cig_look_at_neutral_mean_perc_time_at_pref'%(eyed,name)] = nanmean(chose_cig_neu_subject_percs); db['%s_%s_selected_cig_look_at_neutral_bs_sems_perc_time_at_pref'%(eyed,name)] = compute_BS_SEM(chose_cig_neu_subject_percs);				
		db['%s_%s_selected_cig_look_at_alc_mean_time_at_pref'%(eyed,name)] = nanmean(chose_cig_alc_subject_times); db['%s_%s_selected_cig_look_at_alc_bs_sems_time_at_pref'%(eyed,name)] = compute_BS_SEM(chose_cig_alc_subject_times);
		db['%s_%s_selected_cig_look_at_alc_mean_perc_time_at_pref'%(eyed,name)] = nanmean(chose_cig_alc_subject_percs); db['%s_%s_selected_cig_look_at_alc_bs_sems_perc_time_at_pref'%(eyed,name)] = compute_BS_SEM(chose_cig_alc_subject_percs);			
		db['%s_%s_selected_cig_look_at_cig_mean_time_at_pref'%(eyed,name)] = nanmean(chose_cig_cig_subject_times); db['%s_%s_selected_cig_look_at_cig_bs_sems_time_at_pref'%(eyed,name)] = compute_BS_SEM(chose_cig_cig_subject_times);
		db['%s_%s_selected_cig_look_at_cig_mean_perc_time_at_pref'%(eyed,name)] = nanmean(chose_cig_cig_subject_percs); db['%s_%s_selected_cig_look_at_cig_bs_sems_perc_time_at_pref'%(eyed,name)] = compute_BS_SEM(chose_cig_cig_subject_percs);				
		db['%s_%s_selected_cig_mean_rt'%(eyed,name)] = nanmean(chose_cig_all_rts); db['%s_%s_selected_cig_bs_sems_rt'%(eyed,name)] = compute_BS_SEM(chose_cig_all_rts);	
		db.sync();
		
		#alcohol
		db['%s_%s_selected_alc_look_at_neutral_mean_time_at_pref'%(eyed,name)] = nanmean(chose_alc_neu_subject_times); db['%s_%s_selected_alc_look_at_neutral_bs_sems_time_at_pref'%(eyed,name)] = compute_BS_SEM(chose_alc_neu_subject_times);
		db['%s_%s_selected_alc_look_at_neutral_mean_perc_time_at_pref'%(eyed,name)] = nanmean(chose_alc_neu_subject_percs); db['%s_%s_selected_alc_look_at_neutral_bs_sems_perc_time_at_pref'%(eyed,name)] = compute_BS_SEM(chose_alc_neu_subject_percs);				
		db['%s_%s_selected_alc_look_at_alc_mean_time_at_pref'%(eyed,name)] = nanmean(chose_alc_alc_subject_times); db['%s_%s_selected_alc_look_at_alc_bs_sems_time_at_pref'%(eyed,name)] = compute_BS_SEM(chose_alc_alc_subject_times);
		db['%s_%s_selected_alc_look_at_alc_mean_perc_time_at_pref'%(eyed,name)] = nanmean(chose_alc_alc_subject_percs); db['%s_%s_selected_alc_look_at_alc_bs_sems_perc_time_at_pref'%(eyed,name)] = compute_BS_SEM(chose_alc_alc_subject_percs);			
		db['%s_%s_selected_alc_look_at_cig_mean_time_at_pref'%(eyed,name)] = nanmean(chose_alc_cig_subject_times); db['%s_%s_selected_alc_look_at_cig_bs_sems_time_at_pref'%(eyed,name)] = compute_BS_SEM(chose_alc_cig_subject_times);
		db['%s_%s_selected_alc_look_at_cig_mean_perc_time_at_pref'%(eyed,name)] = nanmean(chose_alc_cig_subject_percs); db['%s_%s_selected_alc_look_at_cig_bs_sems_perc_time_at_pref'%(eyed,name)] = compute_BS_SEM(chose_alc_cig_subject_percs);				
		db['%s_%s_selected_alc_mean_rt'%(eyed,name)] = nanmean(chose_alc_all_rts); db['%s_%s_selected_alc_bs_sems_rt'%(eyed,name)] = compute_BS_SEM(chose_alc_all_rts);	
		db.sync();
		
		#finally aggregate all of the data for each subject and each breakdown together and store it in the DataFrame (and then turn it into the .csv)
		for sub_id, chose_alc, chose_cig, chose_neu, neu_time, neu_prop, cig_time, cig_prop, alc_time, alc_prop, agg_rts, \
		alc_neu_time, alc_neu_prop, alc_cig_time, alc_cig_prop, alc_alc_time, alc_alc_prop, alc_agg_rts, \
		cig_neu_time, cig_neu_prop, cig_cig_time, cig_cig_prop, cig_alc_time, cig_alc_prop, cig_agg_rts, \
		neu_neu_time, neu_neu_prop, neu_cig_time, neu_cig_prop, neu_alc_time, neu_alc_prop, neu_agg_rts \
		in zip(ids, all_prop_chose_alc, all_prop_chose_cig, all_prop_chose_neu, \
			   neu_subject_times, neu_subject_percs, alc_subject_times, alc_subject_percs, cig_subject_times, cig_subject_percs, all_rts,\
			   chose_alc_neu_subject_times, chose_alc_neu_subject_percs, chose_alc_cig_subject_times, chose_alc_cig_subject_percs, chose_alc_alc_subject_times, chose_alc_alc_subject_percs,  chose_alc_all_rts, \
			   chose_cig_neu_subject_times, chose_cig_neu_subject_percs, chose_cig_cig_subject_times, chose_cig_cig_subject_percs, chose_cig_alc_subject_times, chose_cig_alc_subject_percs, chose_cig_all_rts, \
			   chose_neu_neu_subject_times, chose_neu_neu_subject_percs, chose_neu_cig_subject_times, chose_neu_cig_subject_percs, chose_neu_alc_subject_times, chose_neu_alc_subject_percs,  chose_neu_all_rts):
		
			data.loc[index_counter] = [sub_id, name, chose_alc, chose_cig, chose_neu, \
						nanmean(neu_time), nanmean(neu_prop), nanmean(cig_time), nanmean(cig_prop), nanmean(alc_time), nanmean(alc_prop), nanmean(agg_rts), \
						nanmean(alc_neu_time), nanmean(alc_neu_prop), nanmean(alc_cig_time), nanmean(alc_cig_prop), nanmean(alc_alc_time), nanmean(alc_alc_prop), nanmean(alc_agg_rts), \
						nanmean(cig_neu_time), nanmean(cig_neu_prop), nanmean(cig_cig_time), nanmean(cig_cig_prop), nanmean(cig_alc_time), nanmean(cig_alc_prop), nanmean(cig_agg_rts), \
						nanmean(neu_neu_time), nanmean(neu_neu_prop), nanmean(neu_cig_time), nanmean(neu_cig_prop), nanmean(neu_alc_time), nanmean(neu_alc_prop), nanmean(neu_agg_rts)];
			index_counter+=1;
	
	if eyed=='agg':
		data.to_csv(savepath+'avg_prop_time_spent_looking.csv',index=False);

	# ## Here is the preference-based (cue or not cue) breakdown of this data	
	# for high_pref_trial,name in zip([0,1],['non_high_pref','high_pref']):
	# 	#for now, only run this analysis for the high preference (preferred alcohol, preferred cigarette) trials
	# 	if high_pref_trial==0:
	# 		continue;
	# 	#below here, run the proportion of looking time analysis for cue, not cue, and neutral for each subset of trials where they chose each type
	# 	counter = 0; #counter for indexing appended data into the Pandas DataFrame
	# 	for cue_or_not, selected_item in zip([1,0,0],['cue','not_cue','neutral']):
	# 		neu_subject_times = []; #these are holders for the mean times and proportions for each subject, given the subset of trials 
	# 		neu_subject_percs = [];
	# 		cue_subject_times = [];
	# 		cue_subject_percs = [];
	# 		not_cue_subject_times = [];
	# 		not_cue_subject_percs = [];
	# 		all_rts = [];
	# 		#loop through the cues and trials for each subject
	# 		for subj,cue,sub_id in zip(trial_matrix, subject_cues, ids):
	# 			neu_time_at_pref = [];
	# 			neu_perc_at_pref = [];
	# 			cue_time_at_pref = [];
	# 			cue_perc_at_pref = [];
	# 			not_cue_time_at_pref = [];
	# 			not_cue_perc_at_pref = [];
	# 			rts = [];
	# 			for t in subj:
	# 				#conditional to differentiate between not-cue trials when selecteing the non-cue or not
	# 				if ((selected_item=='cue')|(selected_item=='not_cue')):
	# 					if((t.dropped_sample == 0)&(t.skip==0)&(t.didntLookAtAnyItems == 0)&((t.trial_type == 1)==high_pref_trial)&((t.preferred_category == cue)==cue_or_not)&((t.preferred_category == 'alcohol')|(t.preferred_category == 'cigarette'))):
	# 						neu_time_at_pref.append(t.timeLookingAtNeutral);
	# 						neu_perc_at_pref.append(t.percentageTimeLookingAtNeutral);
	# 						rts.append(t.response_time);
	# 						if (cue=='alcohol'):
	# 							cue_time_at_pref.append(t.timeLookingAtAlcohol);
	# 							cue_perc_at_pref.append(t.percentageTimeLookingAtAlcohol);
	# 							not_cue_time_at_pref.append(t.timeLookingAtCigarette);
	# 							not_cue_perc_at_pref.append(t.percentageTimeLookingAtCigarette);							
	# 							rts.append(t.response_time);							
	# 						elif (cue=='cigarette'):
	# 							cue_time_at_pref.append(t.timeLookingAtCigarette);
	# 							cue_perc_at_pref.append(t.percentageTimeLookingAtCigarette);
	# 							not_cue_time_at_pref.append(t.timeLookingAtAlcohol);
	# 							not_cue_perc_at_pref.append(t.percentageTimeLookingAtAlcohol);							
	# 							rts.append(t.response_time);																				
	# 				#this second conditional include neutral trials that were preferred only
	# 				elif (selected_item=='neutral'):
	# 					if((t.dropped_sample == 0)&(t.skip==0)&(t.didntLookAtAnyItems == 0)&((t.trial_type == 1)==high_pref_trial)&((t.preferred_category == cue)==cue_or_not)&(t.preferred_category == 'neutral')):
	# 						neu_time_at_pref.append(t.timeLookingAtNeutral);
	# 						neu_perc_at_pref.append(t.percentageTimeLookingAtNeutral);
	# 						rts.append(t.response_time);
	# 						if (cue=='alcohol'):
	# 							cue_time_at_pref.append(t.timeLookingAtAlcohol);
	# 							cue_perc_at_pref.append(t.percentageTimeLookingAtAlcohol);
	# 							not_cue_time_at_pref.append(t.timeLookingAtCigarette);
	# 							not_cue_perc_at_pref.append(t.percentageTimeLookingAtCigarette);							
	# 							rts.append(t.response_time);						
	# 						elif (cue=='cigarette'):
	# 							cue_time_at_pref.append(t.timeLookingAtCigarette);
	# 							cue_perc_at_pref.append(t.percentageTimeLookingAtCigarette);
	# 							not_cue_time_at_pref.append(t.timeLookingAtAlcohol);
	# 							not_cue_perc_at_pref.append(t.percentageTimeLookingAtAlcohol);							
	# 							rts.append(t.response_time);													
	# 			#append this subjects' data to the holder list and calculate the nanmeans to store in the database
	# 			neu_subject_times.append(nanmean(neu_time_at_pref)); 
	# 			neu_subject_percs.append(nanmean(neu_perc_at_pref));
	# 			cue_subject_times.append(nanmean(cue_time_at_pref));
	# 			cue_subject_percs.append(nanmean(cue_perc_at_pref));
	# 			not_cue_subject_times.append(nanmean(not_cue_time_at_pref));
	# 			not_cue_subject_percs.append(nanmean(not_cue_perc_at_pref));
	# 			all_rts.append(nanmean(rts));		
	# 			db['%s_high_pref_selected_%s_look_at_neutral_mean_time_at_pref'%(sub_id,selected_item)] = nanmean(neu_time_at_pref); 
	# 			db['%s_high_pref_selected_%s_look_at_neutral_mean_perc_time_at_pref'%(sub_id,selected_item)] = nanmean(neu_perc_at_pref);
	# 			db['%s_high_pref_selected_%s_look_at_cue_mean_time_at_pref'%(sub_id,selected_item)] = nanmean(cue_time_at_pref); 
	# 			db['%s_high_pref_selected_%s_look_at_cue_mean_perc_time_at_pref'%(sub_id,selected_item)] = nanmean(cue_perc_at_pref);
	# 			db['%s_high_pref_selected_%s_look_at_not_cue_mean_time_at_pref'%(sub_id,selected_item)] = nanmean(not_cue_time_at_pref); 
	# 			db['%s_high_pref_selected_%s_look_at_not_cue_mean_perc_time_at_pref'%(sub_id,selected_item)] = nanmean(not_cue_perc_at_pref); 					
	# 			db['%s_high_pref_selected_%s_mean_rt'%(sub_id,selected_item)] = nanmean(rts);
	# 			#add this data to the DataFrame for use in .csv creation
	# 			data.loc[counter] = [sub_id,cue,selected_item,nanmean(neu_time_at_pref),nanmean(neu_perc_at_pref),nanmean(cue_time_at_pref),nanmean(cue_perc_at_pref),nanmean(not_cue_time_at_pref),nanmean(not_cue_perc_at_pref),nanmean(rts)];
	# 			counter+=1;
	# 		#now here aggregate all the data together and append it to the database
	# 		db['%s_high_pref_selected_%s_look_at_neutral_mean_time_at_pref'%(eyed,selected_item)] = nanmean(neu_subject_times); db['%s_high_pref_selected_%s_look_at_neutral_bs_sems_time_at_pref'%(eyed,selected_item)] = compute_BS_SEM(neu_subject_times);
	# 		db['%s_high_pref_selected_%s_look_at_neutral_mean_perc_time_at_pref'%(eyed,selected_item)] = nanmean(neu_subject_percs); db['%s_high_pref_selected_%s_look_at_neutral_bs_sems_perc_time_at_pref'%(eyed,selected_item)] = compute_BS_SEM(neu_subject_percs);				
	# 		db['%s_high_pref_selected_%s_look_at_cue_mean_time_at_pref'%(eyed,selected_item)] = nanmean(cue_subject_times); db['%s_high_pref_selected_%s_look_at_cue_bs_sems_time_at_pref'%(eyed,selected_item)] = compute_BS_SEM(cue_subject_times);
	# 		db['%s_high_pref_selected_%s_look_at_cue_mean_perc_time_at_pref'%(eyed,selected_item)] = nanmean(cue_subject_percs); db['%s_high_pref_selected_%s_look_at_cue_bs_sems_perc_time_at_pref'%(eyed,selected_item)] = compute_BS_SEM(cue_subject_percs);			
	# 		db['%s_high_pref_selected_%s_look_at_not_cue_mean_time_at_pref'%(eyed,selected_item)] = nanmean(not_cue_subject_times); db['%s_high_pref_selected_%s_look_at_not_cue_bs_sems_time_at_pref'%(eyed,selected_item)] = compute_BS_SEM(not_cue_subject_times);
	# 		db['%s_high_pref_selected_%s_look_at_not_cue_mean_perc_time_at_pref'%(eyed,selected_item)] = nanmean(not_cue_subject_percs); db['%s_high_pref_selected_%s_look_at_not_cue_bs_sems_perc_time_at_pref'%(eyed,selected_item)] = compute_BS_SEM(not_cue_subject_percs);				
	# 		db['%s_high_pref_selected_%s_mean_rt'%(eyed,selected_item)] = nanmean(all_rts); db['%s_high_pref_selected_%s_bs_sems_rt'%(eyed,selected_item)] = compute_BS_SEM(all_rts);		
	# #write the data to csv files
	#if eyed=='agg':
	# 	data_preference.to_csv(savepath+'perc_time_avg_subj_data.csv',index=False); 



#this function will compute the average proportion of trials data for each participant, aggregating across all trial types

def computeAllTrialTypesAggregatedProportionLookingTimes(blocks, eyed = 'agg'):
	db = subject_data;
	#loop through and get all the trials for each subject
	trial_matrix = [[tee for b in bl for tee in b.trials if (tee.skip==0)] for bl in blocks];
	
	#find each subjects' cue substance based on which item them chose more often during PAPC trials where they selected the alcohol or cigarette
	if eyed=='agg':
		all_substances = [[tee.preferred_category for tee in subject if (((tee.preferred_category=='alcohol')|(tee.preferred_category=='cigarette'))&
			(tee.dropped_sample == 0)&(tee.didntLookAtAnyItems == 0))] for subject in trial_matrix]; #first get all the selected categories
		prop_chose_alc = [sum([val == 'alcohol' for val in subject])/float(len([val == 'alcohol' for val in subject])) for subject in all_substances]; #now get proportion of time seleteced alcohol
		prop_chose_cig = [sum([val == 'cigarette' for val in subject])/float(len([val == 'alcohol' for val in subject])) for subject in all_substances]; #then proportion of times selecting cigarette
		#then find which proportion is greater and define whether that subject's cue is alcohol or cigarette
		subject_cues = ['alcohol' if (a>c) else 'cigarette' for a,c in zip(prop_chose_alc,prop_chose_cig)];

		index_counter=0;

		# ##Build an average database instance of each value for each subject for high vs low preferred trials and the subsets of high preferred trials
		# data_preference = pd.DataFrame(columns = ['sub_id','subject_cue','selected','neu_mean_time_looking_at_pref','neu_mean_percentage_looking_at_pref',
		# 						   'cue_mean_time_looking_at_pref','cue_mean_percentage_looking_at_pref','not_cue_mean_time_looking_at_pref',
		# 						   'not_cue_mean_percentage_looking_at_pref', 'mean_response_time']);
		#database for the mean proportion of looking time for alcoho and cigarette items 
		data = pd.DataFrame(columns = ['sub_id','trial_type','prop_trials_chose_alc','prop_trials_chose_cig','prop_trials_chose_neu','neu_avg_looking_time','neu_avg_prop_time','cig_avg_looking_time','cig_avg_prop_time','alc_avg_looking_time',
									   'alc_avg_prop_time','avg_rt','chose_alc_neu_avg_looking_time','chose_alc_neu_avg_prop_time','chose_alc_cig_avg_looking_time',
									   'chose_alc_cig_avg_prop_time','chose_alc_alc_avg_looking_time','chose_alc_alc_avg_prop_time','chose_alc_avg_rt',
									   'chose_cig_neu_avg_looking_time','chose_cig_neu_avg_prop_time','chose_cig_cig_avg_looking_time','chose_cig_cig_avg_prop_time','chose_cig_alc_avg_looking_time',
									   'chose_cig_alc_avg_prop_time','chose_cig_avg_rt','chose_neu_neu_avg_looking_time','chose_neu_neu_avg_prop_time','chose_neu_cig_avg_looking_time',
									   'chose_neu_cig_avg_prop_time','chose_neu_alc_avg_looking_time','chose_neu_alc_avg_prop_time','chose_neu_avg_rt']);


		#this formulation is for the non-preference breakdown. not_hp stands for 'all high preference trials, even those where neutral was selected'
		all_substances = [[tee.preferred_category for tee in subject if ((tee.dropped_sample == 0)&(tee.didntLookAtAnyItems == 0))]
			for subject in trial_matrix]; #first get all the selected categories
		all_prop_chose_alc = [sum([val == 'alcohol' for val in subject])/float(len([val == 'alcohol' for val in subject])) for subject in all_substances]; #now get proportion of time seleteced alcohol
		all_prop_chose_cig = [sum([val == 'cigarette' for val in subject])/float(len([val == 'alcohol' for val in subject])) for subject in all_substances];
		all_prop_chose_neu = [sum([val == 'neutral' for val in subject])/float(len([val == 'alcohol' for val in subject])) for subject in all_substances];


	#get the proportion of looking time data for alcohol, cigarettes, and neutral items
	#get the aggregate breakdwon as well as when they chose each item
	#define holders for each breakdown of the data to store each subjects' respective data
	
	neu_subject_times = []; 
	neu_subject_percs = [];
	alc_subject_times = [];
	alc_subject_percs = [];
	cig_subject_times = [];
	cig_subject_percs = [];
	all_rts = [];		
	chose_alc_neu_subject_times = [];  
	chose_alc_neu_subject_percs = [];
	chose_alc_alc_subject_times = [];
	chose_alc_alc_subject_percs = [];
	chose_alc_cig_subject_times = [];
	chose_alc_cig_subject_percs = [];
	chose_alc_all_rts = [];
	chose_cig_neu_subject_times = []; 
	chose_cig_neu_subject_percs = [];
	chose_cig_alc_subject_times = [];
	chose_cig_alc_subject_percs = [];
	chose_cig_cig_subject_times = [];
	chose_cig_cig_subject_percs = [];
	chose_cig_all_rts = [];
	chose_neu_neu_subject_times = []; 
	chose_neu_neu_subject_percs = [];
	chose_neu_alc_subject_times = [];
	chose_neu_alc_subject_percs = [];
	chose_neu_cig_subject_times = [];
	chose_neu_cig_subject_percs = [];
	chose_neu_all_rts = [];
	
	#first run the analysis for all trials, not breaking down by choice
	#loop through trials for each subject
	for subj,sub_id in zip(trial_matrix, ids):
		neu_time_at_pref = [];
		neu_perc_at_pref = [];
		alc_time_at_pref = [];
		alc_perc_at_pref = [];
		cig_time_at_pref = [];
		cig_perc_at_pref = [];
		rts = [];			
		for t in subj:
			if((t.dropped_sample == 0)&(t.didntLookAtAnyItems == 0)):   			
				neu_time_at_pref.append(t.timeLookingAtNeutral);
				neu_perc_at_pref.append(t.percentageTimeLookingAtNeutral);	
				alc_time_at_pref.append(t.timeLookingAtAlcohol);
				alc_perc_at_pref.append(t.percentageTimeLookingAtAlcohol);		
				cig_time_at_pref.append(t.timeLookingAtCigarette);
				cig_perc_at_pref.append(t.percentageTimeLookingAtCigarette);
				rts.append(t.response_time);
		neu_subject_times.append(nanmean(neu_time_at_pref)); 
		neu_subject_percs.append(nanmean(neu_perc_at_pref));
		alc_subject_times.append(nanmean(alc_time_at_pref));
		alc_subject_percs.append(nanmean(alc_perc_at_pref));
		cig_subject_times.append(nanmean(cig_time_at_pref));
		cig_subject_percs.append(nanmean(cig_perc_at_pref));
		all_rts.append(nanmean(rts));				
	
	#now run the analysis conditioned on which item was chosen
	for selected_item in ['alcohol','cigarette','neutral']:
		#loop through trials for each subject
		for subj,chose_alc,chose_cig,chose_neu,sub_id in zip(trial_matrix, all_prop_chose_alc, all_prop_chose_cig, all_prop_chose_neu, ids):
			neu_time_at_pref = [];
			neu_perc_at_pref = [];
			alc_time_at_pref = [];
			alc_perc_at_pref = [];
			cig_time_at_pref = [];
			cig_perc_at_pref = [];
			rts = [];	
			for t in subj:
				if((t.dropped_sample == 0)&(t.didntLookAtAnyItems == 0)):   			
					if (t.preferred_category==selected_item):
						neu_time_at_pref.append(t.timeLookingAtNeutral);
						neu_perc_at_pref.append(t.percentageTimeLookingAtNeutral);	
						alc_time_at_pref.append(t.timeLookingAtAlcohol);
						alc_perc_at_pref.append(t.percentageTimeLookingAtAlcohol);		
						cig_time_at_pref.append(t.timeLookingAtCigarette);
						cig_perc_at_pref.append(t.percentageTimeLookingAtCigarette);
						rts.append(t.response_time);
			#append this subjects' data to the holder list and calculate the nanmeans to store in the database
			if selected_item=='neutral':
				chose_neu_neu_subject_times.append(nanmean(neu_time_at_pref)); 
				chose_neu_neu_subject_percs.append(nanmean(neu_perc_at_pref));
				chose_neu_alc_subject_times.append(nanmean(alc_time_at_pref));
				chose_neu_alc_subject_percs.append(nanmean(alc_perc_at_pref));
				chose_neu_cig_subject_times.append(nanmean(cig_time_at_pref));
				chose_neu_cig_subject_percs.append(nanmean(cig_perc_at_pref));
				chose_neu_all_rts.append(nanmean(rts));					
			elif selected_item=='alcohol':
				chose_alc_neu_subject_times.append(nanmean(neu_time_at_pref)); 
				chose_alc_neu_subject_percs.append(nanmean(neu_perc_at_pref));
				chose_alc_alc_subject_times.append(nanmean(alc_time_at_pref));
				chose_alc_alc_subject_percs.append(nanmean(alc_perc_at_pref));
				chose_alc_cig_subject_times.append(nanmean(cig_time_at_pref));
				chose_alc_cig_subject_percs.append(nanmean(cig_perc_at_pref));
				chose_alc_all_rts.append(nanmean(rts));								
			elif selected_item=='cigarette':
				chose_cig_neu_subject_times.append(nanmean(neu_time_at_pref)); 
				chose_cig_neu_subject_percs.append(nanmean(neu_perc_at_pref));
				chose_cig_alc_subject_times.append(nanmean(alc_time_at_pref));
				chose_cig_alc_subject_percs.append(nanmean(alc_perc_at_pref));
				chose_cig_cig_subject_times.append(nanmean(cig_time_at_pref));
				chose_cig_cig_subject_percs.append(nanmean(cig_perc_at_pref));
				chose_cig_all_rts.append(nanmean(rts));								

		
		#finally aggregate all of the data for each subject and each breakdown together and store it in the DataFrame (and then turn it into the .csv)
		for sub_id, chose_alc, chose_cig, chose_neu, neu_time, neu_prop, cig_time, cig_prop, alc_time, alc_prop, agg_rts, \
		alc_neu_time, alc_neu_prop, alc_cig_time, alc_cig_prop, alc_alc_time, alc_alc_prop, alc_agg_rts, \
		cig_neu_time, cig_neu_prop, cig_cig_time, cig_cig_prop, cig_alc_time, cig_alc_prop, cig_agg_rts, \
		neu_neu_time, neu_neu_prop, neu_cig_time, neu_cig_prop, neu_alc_time, neu_alc_prop, neu_agg_rts \
		in zip(ids, all_prop_chose_alc, all_prop_chose_cig, all_prop_chose_neu, \
			   neu_subject_times, neu_subject_percs, alc_subject_times, alc_subject_percs, cig_subject_times, cig_subject_percs, all_rts,\
			   chose_alc_neu_subject_times, chose_alc_neu_subject_percs, chose_alc_cig_subject_times, chose_alc_cig_subject_percs, chose_alc_alc_subject_times, chose_alc_alc_subject_percs,  chose_alc_all_rts, \
			   chose_cig_neu_subject_times, chose_cig_neu_subject_percs, chose_cig_cig_subject_times, chose_cig_cig_subject_percs, chose_cig_alc_subject_times, chose_cig_alc_subject_percs, chose_cig_all_rts, \
			   chose_neu_neu_subject_times, chose_neu_neu_subject_percs, chose_neu_cig_subject_times, chose_neu_cig_subject_percs, chose_neu_alc_subject_times, chose_neu_alc_subject_percs,  chose_neu_all_rts):
		
			data.loc[index_counter] = [sub_id, 'agg_all_trials', chose_alc, chose_cig, chose_neu, \
						nanmean(neu_time), nanmean(neu_prop), nanmean(cig_time), nanmean(cig_prop), nanmean(alc_time), nanmean(alc_prop), nanmean(agg_rts), \
						nanmean(alc_neu_time), nanmean(alc_neu_prop), nanmean(alc_cig_time), nanmean(alc_cig_prop), nanmean(alc_alc_time), nanmean(alc_alc_prop), nanmean(alc_agg_rts), \
						nanmean(cig_neu_time), nanmean(cig_neu_prop), nanmean(cig_cig_time), nanmean(cig_cig_prop), nanmean(cig_alc_time), nanmean(cig_alc_prop), nanmean(cig_agg_rts), \
						nanmean(neu_neu_time), nanmean(neu_neu_prop), nanmean(neu_cig_time), nanmean(neu_cig_prop), nanmean(neu_alc_time), nanmean(neu_alc_prop), nanmean(neu_agg_rts)];
			index_counter+=1;
	
	if eyed=='agg':
		data.to_csv(savepath+'ALL_TRIALTYPES_AGGREGATED_avg_prop_time_spent_looking.csv',index=False);



def computeLastItemLookedAt(blocks, eyed = 'agg'):
	#this function computes the average proportion of trials that the last item that was looked at was the selected item
	db = subject_data;
	
	#loop through and get all the trials for each subject
	trial_matrix = [[tee for b in bl for tee in b.trials if (tee.skip==0)] for bl in blocks];

	#find each subjects' cue substance based on which item them chose more often during PAPC trials where they selected the alcohol or cigarette
	if eyed=='subjective_resps':
		subject_cues = [info[1] for info in subjective_prefs];
	else:	
		all_substances = [[tee.preferred_category for tee in subject if (((tee.preferred_category=='alcohol')|(tee.preferred_category=='cigarette'))&
			(tee.dropped_sample == 0)&(tee.skip==0)&(tee.didntLookAtAnyItems == 0)&(tee.trial_type == 1))] for subject in trial_matrix]; #first get all the selected categories
		prop_chose_alc = [sum([val == 'alcohol' for val in subject])/float(len([val == 'alcohol' for val in subject])) for subject in all_substances]; #now get proportion of time seleteced alcohol
		prop_chose_cig = [sum([val == 'cigarette' for val in subject])/float(len([val == 'alcohol' for val in subject])) for subject in all_substances]; #then proportion of times selecting cigarette
		#then find which proportion is greater and define whether that subject's cue is alcohol or cigarette
		subject_cues = ['alcohol' if (a>c) else 'cigarette' for a,c in zip(prop_chose_alc,prop_chose_cig)];
		
		index_counter=0;		
	
		data = pd.DataFrame(columns = ['sub_id','trial_type','alc_prop_last_fixated','cig_prop_last_fixated','neu_prop_last_fixated',
									   'chose_alc_alc_prop_last_fixated','chose_alc_cig_prop_last_fixated','chose_alc_neu_prop_last_fixated',
									   'chose_cig_alc_prop_last_fixated','chose_cig_cig_prop_last_fixated','chose_cig_neu_prop_last_fixated',
									   'chose_neu_alc_prop_last_fixated','chose_neu_cig_prop_last_fixated','chose_neu_neu_prop_last_fixated']);
	
	
		# high_vs_other_pref_data = pd.DataFrame(columns = ['sub_id','trial_type','percentage_last_fixated_item_was_selected', 'mean_response_time']);
		# high_pref_only_data = pd.DataFrame(columns = ['sub_id','preferred_pic','percentage_last_fixated_item_was_selected', 'mean_response_time']);
		# cue_vs_not_cue_data = pd.DataFrame(columns = ['sub_id','cue_type','percentage_last_fixated_item_was_selected', 'mean_response_time']);
	
	
	
	
	#get the proportion of trials where the last fixated item was alcohol, cigarettes, and neutral items
	#get the aggregate breakdwon as well as when they chose each item
	for ttype, name in zip([1,2,3,4],['high_pref', 'highC_lowA','lowC_highA','lowC_lowA']):	

		alc_last_fixated = [];
		cig_last_fixated = [];
		neu_last_fixated = [];
		chose_alc_alc_last_fixated = [];
		chose_alc_cig_last_fixated = [];
		chose_alc_neu_last_fixated = [];	
		chose_cig_alc_last_fixated = [];
		chose_cig_cig_last_fixated = [];
		chose_cig_neu_last_fixated = [];	
		chose_neu_alc_last_fixated = [];
		chose_neu_cig_last_fixated = [];
		chose_neu_neu_last_fixated = [];	
	
		# #first run the analysis for all high preference trials, not breaking it down by whether they chose alcohol, cigeratte, or neutral
		# #loop through trials for each subject
		# for subj,sub_id in zip(trial_matrix, ids):
		# 	alc_subj = [];
		# 	cig_subj = [];
		# 	neu_subj = [];	
		# 	for t in subj:
		# 		if((t.dropped_sample == 0)&(t.didntLookAtAnyItems == 0)&(t.trial_type == ttype)&(tee.skip == 0)&(sqrt(tee.eyeX[0]**2 + tee.eyeY[0]**2) < 2.5)):					#==high_pref_trial)):
		# 			#conditionally append a 1 or 0 based on which item was last looked at in this trial
		# 			if (t.lastCategoryLookedAt == 'alcohol'):
		# 				alc_subj.append(1);
		# 				cig_subj.append(0);
		# 				neu_subj.append(0);
		# 			elif (t.lastCategoryLookedAt == 'cigarette'):
		# 				alc_subj.append(0);
		# 				cig_subj.append(1);
		# 				neu_subj.append(0);						
		# 			elif (t.lastCategoryLookedAt == 'neutral'):
		# 				alc_subj.append(0);
		# 				cig_subj.append(0);
		# 				neu_subj.append(1);
		# 	alc_last_fixated.append(sum(alc_subj)/float(len(alc_subj)));
		# 	cig_last_fixated.append(sum(cig_subj)/float(len(cig_subj)));
		# 	neu_last_fixated.append(sum(neu_subj)/float(len(neu_subj)));
		# 	
		# #below here append averages to the database 
		# db['%s_%s_alc_mean_prop_last_fixated_item'%(eyed,name)] = nanmean(alc_last_fixated); db['%s_%s_alc_bs_sems_prop_last_fixated_item'%(eyed,name)] = compute_BS_SEM(alc_last_fixated);
		# db['%s_%s_cig_mean_prop_last_fixated_item'%(eyed,name)] = nanmean(cig_last_fixated); db['%s_%s_cig_bs_sems_prop_last_fixated_item'%(eyed,name)] = compute_BS_SEM(cig_last_fixated);
		# db['%s_%s_neu_mean_prop_last_fixated_item'%(eyed,name)] = nanmean(neu_last_fixated); db['%s_%s_neu_bs_sems_prop_last_fixated_item'%(eyed,name)] = compute_BS_SEM(neu_last_fixated);
		# db.sync();
	
		#now break it down by which item was chosen
		for selected_item in ['alcohol','cigarette','neutral']:			
			#loop through trials for each subject
			for subj,sub_id in zip(trial_matrix, ids):
				chose_alc_alc_subj = [];
				chose_alc_cig_subj = [];
				chose_alc_neu_subj = [];			
				chose_cig_alc_subj = [];
				chose_cig_cig_subj = [];
				chose_cig_neu_subj = [];
				chose_neu_alc_subj = [];
				chose_neu_cig_subj = [];
				chose_neu_neu_subj = [];

				for t in subj:
					if((t.dropped_sample == 0)&(t.didntLookAtAnyItems == 0)&(t.trial_type == ttype)&(t.preferred_category==selected_item)&
						(tee.skip == 0)&(sqrt(tee.eyeX[0]**2 + tee.eyeY[0]**2) < 2.5)):         #1)==high_pref_trial
				
						#conditional
						if selected_item=='alcohol':
							#conditionally append a 1 or 0 based on which item was last looked at in this trial
							if (t.lastCategoryLookedAt == 'alcohol'):
								chose_alc_alc_subj.append(1);
								chose_alc_cig_subj.append(0);
								chose_alc_neu_subj.append(0);
							elif (t.lastCategoryLookedAt == 'cigarette'):
								chose_alc_alc_subj.append(0);
								chose_alc_cig_subj.append(1);
								chose_alc_neu_subj.append(0);						
							elif (t.lastCategoryLookedAt == 'neutral'):
								chose_alc_alc_subj.append(0);
								chose_alc_cig_subj.append(0);
								chose_alc_neu_subj.append(1);										
						elif selected_item=='cigarette':				
							#conditionally append a 1 or 0 based on which item was last looked at in this trial
							if (t.lastCategoryLookedAt == 'alcohol'):
								chose_cig_alc_subj.append(1);
								chose_cig_cig_subj.append(0);
								chose_cig_neu_subj.append(0);
							elif (t.lastCategoryLookedAt == 'cigarette'):
								chose_cig_alc_subj.append(0);
								chose_cig_cig_subj.append(1);
								chose_cig_neu_subj.append(0);						
							elif (t.lastCategoryLookedAt == 'neutral'):
								chose_cig_alc_subj.append(0);
								chose_cig_cig_subj.append(0);
								chose_cig_neu_subj.append(1);															
						elif selected_item=='neutral':
							#conditionally append a 1 or 0 based on which item was last looked at in this trial
							if (t.lastCategoryLookedAt == 'alcohol'):
								chose_neu_alc_subj.append(1);
								chose_neu_cig_subj.append(0);
								chose_neu_neu_subj.append(0);
							elif (t.lastCategoryLookedAt == 'cigarette'):
								chose_neu_alc_subj.append(0);
								chose_neu_cig_subj.append(1);
								chose_neu_neu_subj.append(0);						
							elif (t.lastCategoryLookedAt == 'neutral'):
								chose_neu_alc_subj.append(0);
								chose_neu_cig_subj.append(0);
								chose_neu_neu_subj.append(1);
				#append data to the all subject holders
				if selected_item=='alcohol':
					chose_alc_alc_last_fixated.append(sum(chose_alc_alc_subj)/float(len(chose_alc_alc_subj)));
					chose_alc_cig_last_fixated.append(sum(chose_alc_cig_subj)/float(len(chose_alc_cig_subj)));
					chose_alc_neu_last_fixated.append(sum(chose_alc_neu_subj)/float(len(chose_alc_neu_subj)));
				elif selected_item=='cigarette':
					chose_cig_alc_last_fixated.append(sum(chose_cig_alc_subj)/float(len(chose_cig_alc_subj)));
					chose_cig_cig_last_fixated.append(sum(chose_cig_cig_subj)/float(len(chose_cig_cig_subj)));
					chose_cig_neu_last_fixated.append(sum(chose_cig_neu_subj)/float(len(chose_cig_neu_subj)));
				elif selected_item=='neutral':
					chose_neu_alc_last_fixated.append(sum(chose_neu_alc_subj)/float(len(chose_neu_alc_subj)));
					chose_neu_cig_last_fixated.append(sum(chose_neu_cig_subj)/float(len(chose_neu_cig_subj)));
					chose_neu_neu_last_fixated.append(sum(chose_neu_neu_subj)/float(len(chose_neu_neu_subj)));

		#below here append averages to the database
		db['%s_%s_chose_alc_alc_mean_prop_last_fixated_item'%(eyed,name)] = nanmean(chose_alc_alc_last_fixated); db['%s_%s_chose_alc_alc_bs_sems_prop_last_fixated_item'%(eyed,name)] = compute_BS_SEM(chose_alc_alc_last_fixated);
		db['%s_%s_chose_alc_cig_mean_prop_last_fixated_item'%(eyed,name)] = nanmean(chose_alc_cig_last_fixated); db['%s_%s_chose_alc_cig_bs_sems_prop_last_fixated_item'%(eyed,name)] = compute_BS_SEM(chose_alc_cig_last_fixated);
		db['%s_%s_chose_alc_neu_mean_prop_last_fixated_item'%(eyed,name)] = nanmean(chose_alc_neu_last_fixated); db['%s_%s_chose_alc_neu_bs_sems_prop_last_fixated_item'%(eyed,name)] = compute_BS_SEM(chose_alc_neu_last_fixated);				
		db['%s_%s_chose_cig_alc_mean_prop_last_fixated_item'%(eyed,name)] = nanmean(chose_cig_alc_last_fixated); db['%s_%s_chose_cig_alc_bs_sems_prop_last_fixated_item'%(eyed,name)] = compute_BS_SEM(chose_cig_alc_last_fixated);
		db['%s_%s_chose_cig_cig_mean_prop_last_fixated_item'%(eyed,name)] = nanmean(chose_cig_cig_last_fixated); db['%s_%s_chose_cig_cig_bs_sems_prop_last_fixated_item'%(eyed,name)] = compute_BS_SEM(chose_cig_cig_last_fixated);
		db['%s_%s_chose_cig_neu_mean_prop_last_fixated_item'%(eyed,name)] = nanmean(chose_cig_neu_last_fixated); db['%s_%s_chose_cig_neu_bs_sems_prop_last_fixated_item'%(eyed,name)] = compute_BS_SEM(chose_cig_neu_last_fixated);									
		db['%s_%s_chose_neu_alc_mean_prop_last_fixated_item'%(eyed,name)] = nanmean(chose_neu_alc_last_fixated); db['%s_%s_chose_neu_alc_bs_sems_prop_last_fixated_item'%(eyed,name)] = compute_BS_SEM(chose_neu_alc_last_fixated);
		db['%s_%s_chose_neu_cig_mean_prop_last_fixated_item'%(eyed,name)] = nanmean(chose_neu_cig_last_fixated); db['%s_%s_chose_neu_cig_bs_sems_prop_last_fixated_item'%(eyed,name)] = compute_BS_SEM(chose_neu_cig_last_fixated);
		db['%s_%s_chose_neu_neu_mean_prop_last_fixated_item'%(eyed,name)] = nanmean(chose_neu_neu_last_fixated); db['%s_%s_chose_neu_neu_bs_sems_prop_last_fixated_item'%(eyed,name)] = compute_BS_SEM(chose_neu_neu_last_fixated);	
		db.sync();
		
		#below here append all the data to the DataFrame and then save it as a .csv
	# 	for sub_id, alc, cig, neu, alc_alc, alc_cig, alc_neu, cig_alc, cig_cig, cig_neu, neu_alc, neu_cig, neu_neu \
	# 		in zip(ids, alc_last_fixated, cig_last_fixated, neu_last_fixated, \
	# 		chose_alc_alc_last_fixated, chose_alc_cig_last_fixated, chose_alc_neu_last_fixated, \
	# 		chose_cig_alc_last_fixated, chose_cig_cig_last_fixated, chose_cig_neu_last_fixated, \
	# 		chose_neu_alc_last_fixated, chose_neu_cig_last_fixated, chose_neu_neu_last_fixated):
	# 
	# 		#confirm that alc, cig, neu, etc 
	# 		
	# 		data.loc[index_counter] = [sub_id, name, mean(alc), mean(cig), mean(neu), \
	# 								   mean(alc_alc), mean(alc_cig), mean(alc_neu), \
	# 								mean(cig_alc), mean(cig_cig), mean(cig_neu), \
	# 								mean(neu_alc), mean(neu_cig), mean(neu_neu)];
	# 		index_counter+=1;
	# 
	# if eyed=='agg':
	# 	data.to_csv(savepath+'avg_last_fixated_item.csv',index=False);
	
	# #store all the trial data for each subject in a master DB
	# hl_index_counter = 0;
	# all_high_index_counter = 0;
	# cv_counter = 0;
	# for high_pref_trial,name in zip([0,1],['non_high_pref','high_pref']):	
	# 	raw_prop_last_fixated_item = [[(tee.lastItemLookedAt == tee.preferred_item) for tee in subj
	# 		if((tee.dropped_sample == 0)&(tee.skip==0)&(tee.didntLookAtAnyItems == 0)&((tee.trial_type == 1)==high_pref_trial))] for subj in trial_matrix];
	# 	rts = [mean([tee.response_time for tee in subj
	# 		if((tee.dropped_sample == 0)&(tee.skip==0)&(tee.didntLookAtAnyItems == 0)&((tee.trial_type == 1)==high_pref_trial))]) for subj in trial_matrix];
	# 	prop_last_fixated_item = [sum(subj)/float(len(subj)) for subj in raw_prop_last_fixated_item];
	# 	db['%s_%s_mean_prop_last_fixated_item'%(eyed,name)] = nanmean(prop_last_fixated_item); db['%s_%s_bs_sems_prop_last_fixated_item'%(eyed,name)] = compute_BS_SEM(prop_last_fixated_item);
	# 	db['%s_%s_mean_rt'%(eyed,name)] = nanmean(rts); db['%s_%s_bs_sems_rt'%(eyed,name)] = compute_BS_SEM(rts);		
	# 	for id,pp,rt in zip(ids, prop_last_fixated_item, rts):
	# 		#add the data to a pandas.DataFrame object to write it to a file for use in R to run the stats
	# 		high_vs_other_pref_data.loc[hl_index_counter] = [id,name,nanmean(pp),nanmean(rt)];
	# 		hl_index_counter+=1;		
	# 	
	# 	#cycle through the different types of high preference trials (where each one could be selected):
	# 	#1. all high-pref trials, 2. all not high pref trials, 3. alcohol high pref trials
	# 	#4. cigarette high pref trials, and 5. neutral high pref trials
	# 	if high_pref_trial==1:		
	# 		for pref_category in ['alcohol','cigarette','neutral']:
	# 			raw_prop_last_fixated_item = [[(tee.lastItemLookedAt == tee.preferred_item) for tee in subj
	# 				if((tee.dropped_sample == 0)&(tee.skip==0)&(tee.didntLookAtAnyItems == 0)&((tee.trial_type == 1)==high_pref_trial))&(tee.preferred_category == pref_category)] for subj in trial_matrix];
	# 			rts = [mean([tee.response_time for tee in subj
	# 				if((tee.dropped_sample == 0)&(tee.skip==0)&(tee.didntLookAtAnyItems == 0)&((tee.trial_type == 1)==high_pref_trial))&(tee.preferred_category == pref_category)]) for subj in trial_matrix];
	# 			prop_last_fixated_item = [sum(subj)/float(len(subj)) for subj in raw_prop_last_fixated_item];
	# 			db['%s_high_pref_%s_mean_prop_last_fixated_item'%(eyed,pref_category)] = nanmean(prop_last_fixated_item); db['%s_high_pref_%s_bs_sems_prop_last_fixated_item'%(eyed,pref_category)] = compute_BS_SEM(prop_last_fixated_item);
	# 			db['%s_high_pref_%s_mean_rt'%(eyed,pref_category)] = nanmean(rts); db['%s_high_pref_%s_bs_sems_rt'%(eyed,pref_category)] = compute_BS_SEM(rts);
	# 			for id,pp,rt in zip(ids, prop_last_fixated_item, rts):
	# 				#add the data to a pandas.DataFrame object to write it to a file for use in R to run the stats
	# 				high_pref_only_data.loc[all_high_index_counter] = [id,name,nanmean(pp),nanmean(rt)];
	# 				all_high_index_counter+=1;
	# 									
	# 		#now run this analysis for the trials where the subject selected the cue item, as defined above, vs the non cued item 
	# 				
	# 		for cue_or_not, cue_name in zip([1,0],['cue','not_cue']):	
	# 			raw_prop_last_fixated_item = [[(tee.lastItemLookedAt == tee.preferred_item) for tee in subj
	# 				if((tee.dropped_sample == 0)&(tee.skip==0)&(tee.didntLookAtAnyItems == 0)&((tee.trial_type == 1)==high_pref_trial))&((tee.preferred_category == cue)==cue_or_not)
	# 				&((tee.preferred_category == 'alcohol')|(tee.preferred_category == 'cigarette'))] for subj,cue in zip(trial_matrix,subject_cues)];
	# 			rts = [mean([tee.response_time for tee in subj
	# 				if((tee.dropped_sample == 0)&(tee.skip==0)&(tee.didntLookAtAnyItems == 0)&((tee.trial_type == 1)==high_pref_trial))&((tee.preferred_category == cue)==cue_or_not)
	# 				&((tee.preferred_category == 'alcohol')|(tee.preferred_category == 'cigarette'))]) for subj,cue in zip(trial_matrix,subject_cues)];
	# 			prop_last_fixated_item = [sum(subj)/float(len(subj)) for subj in raw_prop_last_fixated_item];
	# 			db['%s_high_pref_selected_%s_mean_prop_last_fixated_item'%(eyed,cue_name)] = nanmean(prop_last_fixated_item); db['%s_high_pref_selected_%s_bs_sems_prop_last_fixated_item'%(eyed,cue_name)] = compute_BS_SEM(prop_last_fixated_item);
	# 			db['%s_high_pref_selected_%s_mean_rt'%(eyed,cue_name)] = nanmean(rts); db['%s_high_pref_selected_%s_bs_sems_rt'%(eyed,cue_name)] = compute_BS_SEM(rts);				
	# 			for id,pp,rt in zip(ids, prop_last_fixated_item, rts):
	# 				#add the data to a pandas.DataFrame object to write it to a file for use in R to run the stats				
	# 				cue_vs_not_cue_data.loc[all_high_index_counter] = [id,cue_name,nanmean(pp),nanmean(rt)];
	# 				cv_counter+=1;
	# 			
	# #write the data to csv files
	# if eyed=='agg':
	# 	high_vs_other_pref_data.to_csv(savepath+'last_item_avg_high_vs_nothigh_pref_trial_data.csv',index=False); 
	# 	high_pref_only_data.to_csv(savepath+'last_item_avg_high_pref_only_trial_data.csv',index=False);
	# 	cue_vs_not_cue_data.to_csv(savepath+'last_item_cue_not_cue_high_pref_trial_data.csv',index=False);


def computeMedianSplitTemporalGAzeProfiles(blocks, ttype, eyed='agg'):
	#computes the long RESPONSE LOCKED temporal gaze profiles but with a median split
	
	db = subject_data;
	index_counter = 0; #for database calculation
	
	time_bin_spacing = 0.001;
	time_duration = 2.0;
	
	#loop through and get all the trials for each subject
	trial_matrix = [[tee for b in bl for tee in b.trials if (tee.skip==0)] for bl in blocks];
	
	#collect which trial type to run this analysis for
	#ttype = int(raw_input('Which trial type? 1 = HighC/HighA, 2 = HighC/LowA, 3 = LowC/HighA, 4 = LowC/LowA: '));
	
	name = ['high_pref', 'highC_lowA','lowC_highA','lowC_lowA'][ttype-1];

	#create 2000 dataframe objects that will correspond to each time point
	fast_data = [pd.DataFrame(columns = ['sub_id','fast_or_slow','med_rt','trial_type','selected_item','looked_at_item','timepoint','nr_trials','nr_trials_used_for_likelihood','mean_fix_likelihood']) for i in arange(2000)];
	slow_data = [pd.DataFrame(columns = ['sub_id','fast_or_slow','med_rt','trial_type','selected_item','looked_at_item','timepoint','nr_trials','nr_trials_used_for_likelihood','mean_fix_likelihood']) for i in arange(2000)];
	#nr of trials used is the total number of trials used for tht time point (a trial where at least one item was looked at)
	#nr_trials_used_for_likelihood is the nr of trials where that specific item was looked at, at the given timepoint

	for selected_item in ['alcohol','cigarette','neutral']:
		
		for split,data_frame in zip(['fast','slow'], [fast_data, slow_data]):
			# ^ use this to determine which dataframe to save to
		
			fig = figure(); ax1 = gca();
			ax1.set_ylim(0.0, 1.0); ax1.set_yticks(arange(0,1.01,0.1)); ax1.set_xlim([0,2000]);
			ax1.set_ylabel('Likelihood of fixating',size=18); ax1.set_xlabel('Time with respect to stimulus onset, ms',size=18,labelpad=11);
			ax1.set_xticks([0,500, 1000, 1500, 2000]);
			#ax1.set_xticklabels(['-2000', '-1500', '-1000', '-500', '0']);
			colors = ['red','blue', 'green']; alphas = [1.0, 1.0, 1.0]; legend_lines = [];		count = 0;	
		
			# #define arrays for the neutral, alcohol and cigarette items
			neu_gaze_array = zeros(time_duration/time_bin_spacing);
			neu_counts = zeros(shape(neu_gaze_array));
			neu_subject_means_array = [[] for i in range(2000)]; #use this to store each individual subjects' mean for each time point
			neu_subject_agg_counts = []; 
			alc_gaze_array = zeros(time_duration/time_bin_spacing);
			alc_counts = zeros(shape(alc_gaze_array));
			alc_subject_means_array = [[] for i in range(2000)];
			alc_subject_agg_counts = []; 
			cig_cue_gaze_array = zeros(time_duration/time_bin_spacing);
			cig_cue_counts = zeros(shape(cig_cue_gaze_array));
			cig_cue_subject_means_array = [[] for i in range(2000)];
			cig_subject_agg_counts = []; 	

			for subj_nr,subj in enumerate(trial_matrix):
				neu_individ_subject_sum = zeros(time_duration/time_bin_spacing);
				neu_individ_subject_counts = zeros(time_duration/time_bin_spacing);
				neu_individ_subject_nrusedtrials = zeros(time_duration/time_bin_spacing);
				alc_individ_subject_sum = zeros(time_duration/time_bin_spacing);
				alc_individ_subject_counts = zeros(time_duration/time_bin_spacing);
				alc_individ_subject_nrusedtrials = zeros(time_duration/time_bin_spacing);			
				cig_cue_individ_subject_sum = zeros(time_duration/time_bin_spacing);
				cig_cue_individ_subject_counts = zeros(time_duration/time_bin_spacing);
				cig_individ_subject_nrusedtrials = zeros(time_duration/time_bin_spacing);

				med_rt = median([p.response_time for p in subj if ((p.dropped_sample == 0)&(p.didntLookAtAnyItems == 0)&(p.trial_type == ttype)&(p.preferred_category == selected_item))]); #get median RT for this subject

				if (med_rt <= 0):
					1/0;

				for t in subj:				
					#conditional to differentiate between not-cue trials when selecteing the non-cue or not
					#the second conditional include nuetral trials that were preferred only
					if ((t.dropped_sample == 0)&(t.didntLookAtAnyItems == 0)&(t.trial_type == ttype)&(t.preferred_category == selected_item)):
						
						#conditional to determine if this trial's RT is less than or equal to the median RT					
						if (split=='fast'):
							if (t.response_time > med_rt):
								continue;
						elif (split=='slow'):
							if (t.response_time <= med_rt):
								continue;		

						#neutral is always the same...
						#cycle through each time point, going backward through the array (e.g., -1, -2..) and aggregating the data accordingly
						for i in (arange(2000)+1):
							if (i>len(t.lookedAtNeutral)):
								continue;
							elif (isnan(t.lookedAtNeutral[-i])):
								continue; #nan means they weren't looking at anything at this timepoint
							neu_gaze_array[-i] += t.lookedAtNeutral[-i];
							neu_counts[-i] += 1;
							#put the individual subject data together
							neu_individ_subject_sum[-i] += t.lookedAtNeutral[-i];
							neu_individ_subject_counts[-i] += 1;
							neu_individ_subject_nrusedtrials[-i] += t.lookedAtNeutral[-i];
						for i in (arange(2000)+1):
							if (i>len(t.lookedAtAlcohol)):
								continue;
							elif (isnan(t.lookedAtAlcohol[-i])):
								continue;
							#store the alcohol gaze patterns as the cue item
							alc_gaze_array[-i] += t.lookedAtAlcohol[-i];
							alc_counts[-i] += 1;
							#put the individual subject data together
							alc_individ_subject_sum[-i] += t.lookedAtAlcohol[-i];
							alc_individ_subject_counts[-i] += 1;
							alc_individ_subject_nrusedtrials[-i] += t.lookedAtAlcohol[-i]; 
						for i in (arange(2000)+1):
							if (i>len(t.lookedAtCigarette)):
								continue;
							elif (isnan(t.lookedAtCigarette[-i])):
								continue;							
							#store the cigarette items as the not_cue item
							cig_cue_gaze_array[-i] += t.lookedAtCigarette[-i];
							cig_cue_counts[-i] += 1;
							#put the individual subject data together
							cig_cue_individ_subject_sum[-i] += t.lookedAtCigarette[-i];
							cig_cue_individ_subject_counts[-i] += 1;
							cig_individ_subject_nrusedtrials[-i] += t.lookedAtCigarette[-i];

	
				neu_individ_subject_mean = neu_individ_subject_sum/neu_individ_subject_counts; #calculate the mean for this subject at each time point
				[neu_subject_means_array[index].append(ind_mew) for index,ind_mew in zip(arange(2000),neu_individ_subject_mean)]; #append this to the array for each subject
				[neu_subject_agg_counts.append(ct) for ct in neu_individ_subject_counts]; #store number of trials here		
				alc_individ_subject_mean = alc_individ_subject_sum/alc_individ_subject_counts; #calculate the mean for this subject at each time point
				[alc_subject_means_array[index].append(ind_mew) for index,ind_mew in zip(arange(2000),alc_individ_subject_mean)]; #append this to the array for each subject
				[alc_subject_agg_counts.append(ct) for ct in alc_individ_subject_counts];
				cig_cue_individ_subject_mean = cig_cue_individ_subject_sum/cig_cue_individ_subject_counts; #calculate the mean for this subject at each time point
				[cig_cue_subject_means_array[index].append(ind_mew) for index,ind_mew in zip(arange(2000),cig_cue_individ_subject_mean)]; #append this to the array for each subject
				[cig_subject_agg_counts.append(ct) for ct in cig_cue_individ_subject_counts];
				
				for index in arange(2000):
					#make sure to reverse the time point from index...
					data_frame[index].loc[index_counter] = [int(subj_nr+1),split,med_rt,int(ttype),selected_item,'alcohol', (1999-index), alc_individ_subject_counts[index], alc_individ_subject_nrusedtrials[index], alc_individ_subject_mean[index]];
					data_frame[index].loc[index_counter+1] = [int(subj_nr+1),split,med_rt,int(ttype),selected_item,'cigarette', (1999-index), cig_cue_individ_subject_counts[index], cig_individ_subject_nrusedtrials[index], cig_cue_individ_subject_mean[index]];
					data_frame[index].loc[index_counter+2] = [int(subj_nr+1),split,med_rt,int(ttype),selected_item,'neutral', (1999-index), neu_individ_subject_counts[index], neu_individ_subject_nrusedtrials[index], neu_individ_subject_mean[index]];
				index_counter+=3;
							
				print "completed subject %s.. \n\n"%subj_nr	

			#plot each likelihood looking at items				
			for  subj_ms, cue_name, c, a in zip([alc_subject_means_array, cig_cue_subject_means_array, neu_subject_means_array], ['alcohol','cigarette','neutral'], colors, alphas):							
				mews = array([nanmean(subj) for subj in subj_ms]); # gaze_array/counts
				sems = array([compute_BS_SEM(subj) for subj in subj_ms]);
				ax1.plot(linspace(0,2000,2000), mews, lw = 4.0, color = c, alpha = a);
				#plot the errorbars
				#for x,m,s in zip(linspace(0,1000,1000),mews,sems):
				ax1.fill_between(linspace(0,2000,2000), mews-sems, mews+sems, color = c, alpha = a*0.4);
				legend_lines.append(mlines.Line2D([],[],color=c,lw=6,alpha = a, label='likelihood(looking at %s) '%cue_name));
			#plot the sum of each for a sanity emasure to ensure they equate to one
			#agg = [(nanmean(a)+nanmean(b)+nanmean(c)) for a,b,c in zip(alc_subject_means_array, cig_cue_subject_means_array, neu_subject_means_array)];
			#ax1.plot(linspace(0,1000,1000),agg,color = 'gray', lw = 3.0);
			#legend_lines.append(mlines.Line2D([],[],color='gray',lw=4, alpha = 1.0, label='sum of all'));
			ax1.plot(linspace(0,2000,2000),linspace(0.33,0.333,2000),color = 'gray', lw = 3.0, ls='dashed');
			legend_lines.append(mlines.Line2D([],[],color='gray',lw=4, alpha = 1.0, ls = 'dashed', label='random'));	
			ax1.spines['right'].set_visible(False); ax1.spines['top'].set_visible(False);
			ax1.spines['bottom'].set_linewidth(2.0); ax1.spines['left'].set_linewidth(2.0);
			ax1.yaxis.set_ticks_position('left'); ax1.xaxis.set_ticks_position('bottom');
			ax1.legend(handles=[legend_lines[0],legend_lines[1], legend_lines[2], legend_lines[3]],loc = 2,ncol=1,fontsize = 11); # legend_lines[4]]
			title('%s %s Average Temporal Gaze Profile, \n Chose %s Trials'%(name, split, selected_item), fontsize = 22);

	#save the databases
	[d.to_csv(savepath+'%s_FAST_timepoint_%s_temporal_gaze_profile_LONG.csv'%(name, (1999-i)),index=False) for d,i in zip(fast_data, arange(2000))]; #data.to_csv(savepath+'%s_temporal_gaze_profile.csv'%name,index=False);
	[d.to_csv(savepath+'%s_SLOW_timepoint_%s_temporal_gaze_profile_LONG.csv'%(name, (1999-i)),index=False) for d,i in zip(slow_data, arange(2000))];
	# ends here


def computeMedianSplitLongStimulusLockedTemporalGazeProfiles(blocks, ttype, eyed = 'agg'):
	#performs the median split temporal gaze profile analysis for the STIMULUS-LOCKED data

	db = subject_data;
	index_counter = 0; #for database calculation
	
	time_bin_spacing = 0.001;
	time_duration = 2.0;
	
	#loop through and get all the trials for each subject
	trial_matrix = [[tee for b in bl for tee in b.trials if (tee.skip==0)] for bl in blocks];
	
	#collect which trial type to run this analysis for
	#ttype = int(raw_input('Which trial type? 1 = HighC/HighA, 2 = HighC/LowA, 3 = LowC/HighA, 4 = LowC/LowA: '));
	
	name = ['high_pref', 'highC_lowA','lowC_highA','lowC_lowA'][ttype-1];

	#create 2000 dataframe objects that will correspond to each time point
	fast_data = [pd.DataFrame(columns = ['sub_id','fast_or_slow','med_rt','trial_type','selected_item','looked_at_item','timepoint','nr_trials','nr_trials_used_for_likelihood','mean_fix_likelihood']) for i in arange(2000)];
	slow_data = [pd.DataFrame(columns = ['sub_id','fast_or_slow','med_rt','trial_type','selected_item','looked_at_item','timepoint','nr_trials','nr_trials_used_for_likelihood','mean_fix_likelihood']) for i in arange(2000)];
	#nr of trials used is the total number of trials used for tht time point (a trial where at least one item was looked at)
	#nr_trials_used_for_likelihood is the nr of trials where that specific item was looked at, at the given timepoint

	for selected_item in ['alcohol','cigarette','neutral']:
		
		for split,data_frame in zip(['fast','slow'], [fast_data, slow_data]):
			# ^ use this to determine which dataframe to save to

			fig = figure(); ax1 = gca();
			ax1.set_ylim(0.0, 1.0); ax1.set_yticks(arange(0,1.01,0.1)); ax1.set_xlim([0,2000]);
			ax1.set_ylabel('Likelihood of fixating',size=18); ax1.set_xlabel('Time with respect to stimulus onset, ms',size=18,labelpad=11);
			ax1.set_xticks([0,500, 1000, 1500, 2000]);
			#ax1.set_xticklabels(['-2000', '-1500', '-1000', '-500', '0']);
			colors = ['red','blue', 'green']; alphas = [1.0, 1.0, 1.0]; legend_lines = [];		count = 0;	
		
			# #define arrays for the neutral, alcohol and cigarette items
			neu_gaze_array = zeros(time_duration/time_bin_spacing);
			neu_counts = zeros(shape(neu_gaze_array));
			neu_subject_means_array = [[] for i in range(2000)]; #use this to store each individual subjects' mean for each time point
			neu_subject_agg_counts = []; 
			alc_gaze_array = zeros(time_duration/time_bin_spacing);
			alc_counts = zeros(shape(alc_gaze_array));
			alc_subject_means_array = [[] for i in range(2000)];
			alc_subject_agg_counts = []; 
			cig_cue_gaze_array = zeros(time_duration/time_bin_spacing);
			cig_cue_counts = zeros(shape(cig_cue_gaze_array));
			cig_cue_subject_means_array = [[] for i in range(2000)];
			cig_subject_agg_counts = []; 	

			for subj_nr,subj in enumerate(trial_matrix):
				neu_individ_subject_sum = zeros(time_duration/time_bin_spacing);
				neu_individ_subject_counts = zeros(time_duration/time_bin_spacing);
				neu_individ_subject_nrusedtrials = zeros(time_duration/time_bin_spacing);
				alc_individ_subject_sum = zeros(time_duration/time_bin_spacing);
				alc_individ_subject_counts = zeros(time_duration/time_bin_spacing);
				alc_individ_subject_nrusedtrials = zeros(time_duration/time_bin_spacing);			
				cig_cue_individ_subject_sum = zeros(time_duration/time_bin_spacing);
				cig_cue_individ_subject_counts = zeros(time_duration/time_bin_spacing);
				cig_individ_subject_nrusedtrials = zeros(time_duration/time_bin_spacing);

				med_rt = median([p.response_time for p in subj if ((p.dropped_sample == 0)&(p.didntLookAtAnyItems == 0)&(p.trial_type == ttype)&(p.preferred_category == selected_item))]); #get median RT for this subject

				if (med_rt <= 0):
					1/0;

				for t in subj:	
					if ((t.dropped_sample == 0)&(t.didntLookAtAnyItems == 0)&(t.trial_type == ttype)&(t.preferred_category == selected_item)):
						
						#conditional to determine if this trial's RT is less than or equal to the median RT					
						if (split=='fast'):
							if (t.response_time > med_rt):
								continue;
						elif (split=='slow'):
							if (t.response_time <= med_rt):
								continue;

						#cycle through each time point, aggregating the data accordingly
						
						for i in (arange(2000)):
							if (i>=len(t.lookedAtNeutral)):
								continue;
							elif (isnan(t.lookedAtNeutral[i])):
								continue; #nan means they weren't looking at anything at this timepoint
							neu_gaze_array[i] += t.lookedAtNeutral[i];
							neu_counts[i] += 1;
							#put the individual subject data together
							neu_individ_subject_sum[i] += t.lookedAtNeutral[i];
							neu_individ_subject_counts[i] += 1;
							neu_individ_subject_nrusedtrials[i] += t.lookedAtNeutral[i];
	
						for i in (arange(2000)):
							if (i>=len(t.lookedAtAlcohol)):
								continue;
							elif (isnan(t.lookedAtAlcohol[i])):
								continue;
							#store the alcohol gaze patterns as the cue item
							alc_gaze_array[i] += t.lookedAtAlcohol[i];
							alc_counts[i] += 1;
							#put the individual subject data together
							alc_individ_subject_sum[i] += t.lookedAtAlcohol[i];
							alc_individ_subject_counts[i] += 1;
							alc_individ_subject_nrusedtrials[i] += t.lookedAtAlcohol[i];
							
						for i in (arange(2000)):
							if (i>=len(t.lookedAtCigarette)):
								continue;
							elif (isnan(t.lookedAtCigarette[i])):
								continue;							
							#store the cigarette items as the not_cue item
							cig_cue_gaze_array[i] += t.lookedAtCigarette[i];
							cig_cue_counts[i] += 1;
							#put the individual subject data together
							cig_cue_individ_subject_sum[i] += t.lookedAtCigarette[i];
							cig_cue_individ_subject_counts[i] += 1;
							cig_individ_subject_nrusedtrials[i] += t.lookedAtCigarette[i];
							
				neu_individ_subject_mean = neu_individ_subject_sum/neu_individ_subject_counts; #calculate the mean for this subject at each time point
				[neu_subject_means_array[index].append(ind_mew) for index,ind_mew in zip(arange(2000),neu_individ_subject_mean)]; #append this to the array for each subject
				[neu_subject_agg_counts.append(ct) for ct in neu_individ_subject_counts]; #store number of trials here		
				alc_individ_subject_mean = alc_individ_subject_sum/alc_individ_subject_counts; #calculate the mean for this subject at each time point
				[alc_subject_means_array[index].append(ind_mew) for index,ind_mew in zip(arange(2000),alc_individ_subject_mean)]; #append this to the array for each subject
				[alc_subject_agg_counts.append(ct) for ct in alc_individ_subject_counts];
				cig_cue_individ_subject_mean = cig_cue_individ_subject_sum/cig_cue_individ_subject_counts; #calculate the mean for this subject at each time point
				[cig_cue_subject_means_array[index].append(ind_mew) for index,ind_mew in zip(arange(2000),cig_cue_individ_subject_mean)]; #append this to the array for each subject
				[cig_subject_agg_counts.append(ct) for ct in cig_cue_individ_subject_counts];	

				for index in arange(2000):
					#make sure to reverse the time point from index...
					data_frame[index].loc[index_counter] = [int(subj_nr+1),split,med_rt,int(ttype),selected_item,'alcohol', (index), alc_individ_subject_counts[index], alc_individ_subject_nrusedtrials[index], alc_individ_subject_mean[index]];
					data_frame[index].loc[index_counter+1] = [int(subj_nr+1),split,med_rt,int(ttype),selected_item,'cigarette', (index), cig_cue_individ_subject_counts[index], cig_individ_subject_nrusedtrials[index], cig_cue_individ_subject_mean[index]];
					data_frame[index].loc[index_counter+2] = [int(subj_nr+1),split,med_rt,int(ttype),selected_item,'neutral', (index), neu_individ_subject_counts[index], neu_individ_subject_nrusedtrials[index], neu_individ_subject_mean[index]];
				index_counter+=3;
							
				print "completed subject %s.. \n\n"%subj_nr	

			#plot each likelihood looking at items				
			for  subj_ms, cue_name, c, a in zip([alc_subject_means_array, cig_cue_subject_means_array, neu_subject_means_array], ['alcohol','cigarette','neutral'], colors, alphas):							
				mews = array([nanmean(subj) for subj in subj_ms]); # gaze_array/counts
				sems = array([compute_BS_SEM(subj) for subj in subj_ms]);
				ax1.plot(linspace(0,2000,2000), mews, lw = 4.0, color = c, alpha = a);
				#plot the errorbars
				#for x,m,s in zip(linspace(0,1000,1000),mews,sems):
				ax1.fill_between(linspace(0,2000,2000), mews-sems, mews+sems, color = c, alpha = a*0.4);
				legend_lines.append(mlines.Line2D([],[],color=c,lw=6,alpha = a, label='likelihood(looking at %s) '%cue_name));
			#plot the sum of each for a sanity emasure to ensure they equate to one
			#agg = [(nanmean(a)+nanmean(b)+nanmean(c)) for a,b,c in zip(alc_subject_means_array, cig_cue_subject_means_array, neu_subject_means_array)];
			#ax1.plot(linspace(0,1000,1000),agg,color = 'gray', lw = 3.0);
			#legend_lines.append(mlines.Line2D([],[],color='gray',lw=4, alpha = 1.0, label='sum of all'));
			ax1.plot(linspace(0,2000,2000),linspace(0.33,0.333,2000),color = 'gray', lw = 3.0, ls='dashed');
			legend_lines.append(mlines.Line2D([],[],color='gray',lw=4, alpha = 1.0, ls = 'dashed', label='random'));	
			ax1.spines['right'].set_visible(False); ax1.spines['top'].set_visible(False);
			ax1.spines['bottom'].set_linewidth(2.0); ax1.spines['left'].set_linewidth(2.0);
			ax1.yaxis.set_ticks_position('left'); ax1.xaxis.set_ticks_position('bottom');
			ax1.legend(handles=[legend_lines[0],legend_lines[1], legend_lines[2], legend_lines[3]],loc = 2,ncol=1,fontsize = 11); # legend_lines[4]]
			title('STIMULUS LOCKED %s %s Average Temporal Gaze Profile, \n Chose %s Trials'%(name, split, selected_item), fontsize = 22);
			
	#save the databases
	[d.to_csv(savepath+'%s_STIMLOCKED_FAST_timepoint_%s_temporal_gaze_profile_LONG.csv'%(name, (i)),index=False) for d,i in zip(fast_data, arange(2000))]; #data.to_csv(savepath+'%s_temporal_gaze_profile.csv'%name,index=False);
	[d.to_csv(savepath+'%s_STIMLOCKED_SLOW_timepoint_%s_temporal_gaze_profile_LONG.csv'%(name, (i)),index=False) for d,i in zip(slow_data, arange(2000))];
	# ends here			
			
			

def computeLongStimulusLockedTemporalGazeProfiles(blocks, ttype, eyed = 'agg'):
	#performs the temporal gaze profile analysis from function below, but does ot for the STIMULUS-LOCKED data
	#i.e. looks at the 2000 ms prior to decision

	db = subject_data;
	index_counter = 0; #for database calculation
	
	time_bin_spacing = 0.001;
	time_duration = 2.0;

	#loop through and get all the trials for each subject
	trial_matrix = [[tee for b in bl for tee in b.trials if (tee.skip==0)] for bl in blocks];
	
	#collect which trial type to run this analysis for
	#ttype = int(raw_input('Which trial type? 1 = HighC/HighA, 2 = HighC/LowA, 3 = LowC/HighA, 4 = LowC/LowA: '));
	
	name = ['high_pref', 'highC_lowA','lowC_highA','lowC_lowA'][ttype-1];
	
	#create 2000 dataframe objects that will correspond to each time point
	data = [pd.DataFrame(columns = ['sub_id','trial_type','selected_item','looked_at_item','timepoint','nr_trials','nr_trials_used_for_likelihood','mean_fix_likelihood']) for i in arange(2000)];
	#nr of trials used is the total number of trials used for tht time point (a trial where at least one item was looked at)
	#nr_trials_used_for_likelihood is the nr of trials where that specific item was looked at, at the given timepoint
	
	for selected_item in ['alcohol','cigarette','neutral']:
		
		fig = figure(); ax1 = gca();
		ax1.set_ylim(0.0, 1.0); ax1.set_yticks(arange(0,1.01,0.1)); ax1.set_xlim([0,2000]);
		ax1.set_ylabel('Likelihood of fixating',size=18); ax1.set_xlabel('Time with respect to stimulus onset, ms',size=18,labelpad=11);
		ax1.set_xticks([0,500, 1000, 1500, 2000]);
		#ax1.set_xticklabels(['-2000', '-1500', '-1000', '-500', '0']);
		colors = ['red','blue', 'green']; alphas = [1.0, 1.0, 1.0]; legend_lines = [];		count = 0;	
	
		# #define arrays for the neutral, alcohol and cigarette items
		neu_gaze_array = zeros(time_duration/time_bin_spacing);
		neu_counts = zeros(shape(neu_gaze_array));
		neu_subject_means_array = [[] for i in range(2000)]; #use this to store each individual subjects' mean for each time point
		neu_subject_agg_counts = []; 
		alc_gaze_array = zeros(time_duration/time_bin_spacing);
		alc_counts = zeros(shape(alc_gaze_array));
		alc_subject_means_array = [[] for i in range(2000)];
		alc_subject_agg_counts = []; 
		cig_cue_gaze_array = zeros(time_duration/time_bin_spacing);
		cig_cue_counts = zeros(shape(cig_cue_gaze_array));
		cig_cue_subject_means_array = [[] for i in range(2000)];
		cig_subject_agg_counts = []; 	
	
		for subj_nr,subj in enumerate(trial_matrix):
			neu_individ_subject_sum = zeros(time_duration/time_bin_spacing);
			neu_individ_subject_counts = zeros(time_duration/time_bin_spacing);
			neu_individ_subject_nrusedtrials = zeros(time_duration/time_bin_spacing);
			alc_individ_subject_sum = zeros(time_duration/time_bin_spacing);
			alc_individ_subject_counts = zeros(time_duration/time_bin_spacing);
			alc_individ_subject_nrusedtrials = zeros(time_duration/time_bin_spacing);			
			cig_cue_individ_subject_sum = zeros(time_duration/time_bin_spacing);
			cig_cue_individ_subject_counts = zeros(time_duration/time_bin_spacing);
			cig_individ_subject_nrusedtrials = zeros(time_duration/time_bin_spacing);	
	
			for t in subj:
				#conditional to differentiate between not-cue trials when selecteing the non-cue or not
				#the second conditional include nuetral trials that were preferred only
				if ((t.dropped_sample == 0)&(t.didntLookAtAnyItems == 0)&(t.trial_type == ttype)&(t.preferred_category == selected_item)):
					#cycle through each time point, aggregating the data accordingly
					
					for i in (arange(2000)):
						if (i>=len(t.lookedAtNeutral)):
							continue;
						elif (isnan(t.lookedAtNeutral[i])):
							continue; #nan means they weren't looking at anything at this timepoint
						neu_gaze_array[i] += t.lookedAtNeutral[i];
						neu_counts[i] += 1;
						#put the individual subject data together
						neu_individ_subject_sum[i] += t.lookedAtNeutral[i];
						neu_individ_subject_counts[i] += 1;
						neu_individ_subject_nrusedtrials[i] += t.lookedAtNeutral[i];

					for i in (arange(2000)):
						if (i>=len(t.lookedAtAlcohol)):
							continue;
						elif (isnan(t.lookedAtAlcohol[i])):
							continue;
						#store the alcohol gaze patterns as the cue item
						alc_gaze_array[i] += t.lookedAtAlcohol[i];
						alc_counts[i] += 1;
						#put the individual subject data together
						alc_individ_subject_sum[i] += t.lookedAtAlcohol[i];
						alc_individ_subject_counts[i] += 1;
						alc_individ_subject_nrusedtrials[i] += t.lookedAtAlcohol[i];
						
					for i in (arange(2000)):
						if (i>=len(t.lookedAtCigarette)):
							continue;
						elif (isnan(t.lookedAtCigarette[i])):
							continue;							
						#store the cigarette items as the not_cue item
						cig_cue_gaze_array[i] += t.lookedAtCigarette[i];
						cig_cue_counts[i] += 1;
						#put the individual subject data together
						cig_cue_individ_subject_sum[i] += t.lookedAtCigarette[i];
						cig_cue_individ_subject_counts[i] += 1;
						cig_individ_subject_nrusedtrials[i] += t.lookedAtCigarette[i];
						
			neu_individ_subject_mean = neu_individ_subject_sum/neu_individ_subject_counts; #calculate the mean for this subject at each time point
			[neu_subject_means_array[index].append(ind_mew) for index,ind_mew in zip(arange(2000),neu_individ_subject_mean)]; #append this to the array for each subject
			[neu_subject_agg_counts.append(ct) for ct in neu_individ_subject_counts]; #store number of trials here		
			alc_individ_subject_mean = alc_individ_subject_sum/alc_individ_subject_counts; #calculate the mean for this subject at each time point
			[alc_subject_means_array[index].append(ind_mew) for index,ind_mew in zip(arange(2000),alc_individ_subject_mean)]; #append this to the array for each subject
			[alc_subject_agg_counts.append(ct) for ct in alc_individ_subject_counts];
			cig_cue_individ_subject_mean = cig_cue_individ_subject_sum/cig_cue_individ_subject_counts; #calculate the mean for this subject at each time point
			[cig_cue_subject_means_array[index].append(ind_mew) for index,ind_mew in zip(arange(2000),cig_cue_individ_subject_mean)]; #append this to the array for each subject
			[cig_subject_agg_counts.append(ct) for ct in cig_cue_individ_subject_counts];						
						
			for index in arange(2000):
				#make sure to reverse the time point from index...
				data[index].loc[index_counter] = [int(subj_nr+1),int(ttype),selected_item,'alcohol', (index), alc_individ_subject_counts[index], alc_individ_subject_nrusedtrials[index], alc_individ_subject_mean[index]];
				data[index].loc[index_counter+1] = [int(subj_nr+1),int(ttype),selected_item,'cigarette', (index), cig_cue_individ_subject_counts[index], cig_individ_subject_nrusedtrials[index], cig_cue_individ_subject_mean[index]];
				data[index].loc[index_counter+2] = [int(subj_nr+1),int(ttype),selected_item,'neutral', (index), neu_individ_subject_counts[index], neu_individ_subject_nrusedtrials[index], neu_individ_subject_mean[index]];
			index_counter+=3;
						
			print "completed subject %s.. \n\n"%subj_nr							

		#plot each likelihood looking at items				
		for  subj_ms, cue_name, c, a in zip([alc_subject_means_array, cig_cue_subject_means_array, neu_subject_means_array], ['alcohol','cigarette','neutral'], colors, alphas):							
			mews = array([nanmean(subj) for subj in subj_ms]); # gaze_array/counts
			sems = array([compute_BS_SEM(subj) for subj in subj_ms]);
			ax1.plot(linspace(0,2000,2000), mews, lw = 4.0, color = c, alpha = a);
			#plot the errorbars
			#for x,m,s in zip(linspace(0,1000,1000),mews,sems):
			ax1.fill_between(linspace(0,2000,2000), mews-sems, mews+sems, color = c, alpha = a*0.4);
			legend_lines.append(mlines.Line2D([],[],color=c,lw=6,alpha = a, label='likelihood(looking at %s) '%cue_name));
		#plot the sum of each for a sanity emasure to ensure they equate to one
		#agg = [(nanmean(a)+nanmean(b)+nanmean(c)) for a,b,c in zip(alc_subject_means_array, cig_cue_subject_means_array, neu_subject_means_array)];
		#ax1.plot(linspace(0,1000,1000),agg,color = 'gray', lw = 3.0);
		#legend_lines.append(mlines.Line2D([],[],color='gray',lw=4, alpha = 1.0, label='sum of all'));
		ax1.plot(linspace(0,2000,2000),linspace(0.33,0.333,2000),color = 'gray', lw = 3.0, ls='dashed');
		legend_lines.append(mlines.Line2D([],[],color='gray',lw=4, alpha = 1.0, ls = 'dashed', label='random'));	
		ax1.spines['right'].set_visible(False); ax1.spines['top'].set_visible(False);
		ax1.spines['bottom'].set_linewidth(2.0); ax1.spines['left'].set_linewidth(2.0);
		ax1.yaxis.set_ticks_position('left'); ax1.xaxis.set_ticks_position('bottom');
		ax1.legend(handles=[legend_lines[0],legend_lines[1], legend_lines[2], legend_lines[3]],loc = 2,ncol=1,fontsize = 11); # legend_lines[4]]
		title('STIMULUS LOCKED %s Average Temporal Gaze Profile, \n Chose %s Trials'%(name, selected_item), fontsize = 22);

	#save the databases
	[d.to_csv(savepath+'STIMLOCKED_%s_timepoint_%s_temporal_gaze_profile_LONG.csv'%(name, (i)),index=False) for d,i in zip(data, arange(2000))]; #data.to_csv(savepath+'%s_temporal_gaze_profile.csv'%name,index=False);
	# ends here

	print "\n\ncompleted trial type %s.. \n\n\n\n"%name



def computeLongTemporalGazeProfiles(blocks, ttype, eyed = 'agg'):
	#performs the temporal gaze profile analysis from function below, but looks at a longer time frame
	#i.e. looks at the 2000 ms prior to decision
	#no plotting done here, will create in R later

	db = subject_data;
	index_counter = 0; #for database calculation
	
	time_bin_spacing = 0.001;
	time_duration = 2.0;
	
	#loop through and get all the trials for each subject
	trial_matrix = [[tee for b in bl for tee in b.trials if (tee.skip==0)] for bl in blocks];
	
	#collect which trial type to run this analysis for
	#ttype = int(raw_input('Which trial type? 1 = HighC/HighA, 2 = HighC/LowA, 3 = LowC/HighA, 4 = LowC/LowA: '));
	
	name = ['high_pref', 'highC_lowA','lowC_highA','lowC_lowA'][ttype-1];

	#create 2000 dataframe objects that will correspond to each time point
	data = [pd.DataFrame(columns = ['sub_id','trial_type','selected_item','looked_at_item','timepoint','nr_trials','nr_trials_used_for_likelihood','mean_fix_likelihood']) for i in arange(2000)];
	#nr of trials used is the total number of trials used for tht time point (a trial where at least one item was looked at)
	#nr_trials_used_for_likelihood is the nr of trials where that specific item was looked at, at the given timepoint
	
	for selected_item in ['cigarette','alcohol','neutral']:
		
		fig = figure(); ax1 = gca();
		ax1.set_ylim(0.0, 1.0); ax1.set_yticks(arange(0,1.01,0.1)); ax1.set_xlim([0,2000]);
		ax1.set_ylabel('Likelihood of fixating',size=18); ax1.set_xlabel('Time with respect to decision, ms',size=18,labelpad=11);
		ax1.set_xticks([0,500, 1000, 1500, 2000]);
		ax1.set_xticklabels(['-2000', '-1500', '-1000', '-500', '0']);
		colors = ['red','blue', 'green']; alphas = [1.0, 1.0, 1.0]; legend_lines = [];		count = 0;
		
		
		#define arrays for the neutral, alcohol and cigarette items
		neu_gaze_array = zeros(time_duration/time_bin_spacing);
		neu_counts = zeros(shape(neu_gaze_array));
		neu_subject_means_array = [[] for i in range(2000)]; #use this to store each individual subjects' mean for each time point
		neu_subject_agg_counts = []; 
		alc_gaze_array = zeros(time_duration/time_bin_spacing);
		alc_counts = zeros(shape(alc_gaze_array));
		alc_subject_means_array = [[] for i in range(2000)];
		alc_subject_agg_counts = []; 
		cig_cue_gaze_array = zeros(time_duration/time_bin_spacing);
		cig_cue_counts = zeros(shape(cig_cue_gaze_array));
		cig_cue_subject_means_array = [[] for i in range(2000)];
		cig_subject_agg_counts = []; 
	
		for subj_nr,subj in enumerate(trial_matrix):
			neu_individ_subject_sum = zeros(time_duration/time_bin_spacing);
			neu_individ_subject_counts = zeros(time_duration/time_bin_spacing);
			neu_individ_subject_nrusedtrials = zeros(time_duration/time_bin_spacing);
			alc_individ_subject_sum = zeros(time_duration/time_bin_spacing);
			alc_individ_subject_counts = zeros(time_duration/time_bin_spacing);
			alc_individ_subject_nrusedtrials = zeros(time_duration/time_bin_spacing);			
			cig_cue_individ_subject_sum = zeros(time_duration/time_bin_spacing);
			cig_cue_individ_subject_counts = zeros(time_duration/time_bin_spacing);
			cig_individ_subject_nrusedtrials = zeros(time_duration/time_bin_spacing);
			
			for t in subj:
				#conditional to differentiate between not-cue trials when selecteing the non-cue or not
				#the second conditional include nuetral trials that were preferred only
				if ((t.dropped_sample == 0)&(t.didntLookAtAnyItems == 0)&(t.trial_type == ttype)&(t.preferred_category == selected_item)):
					#neutral is always the same...
					#cycle through each time point, going backward through the array (e.g., -1, -2..) and aggregating the data accordingly
					for i in (arange(2000)+1):
						if (i>len(t.lookedAtNeutral)):
							continue;
						elif (isnan(t.lookedAtNeutral[-i])):
							continue; #nan means they weren't looking at anything at this timepoint
						neu_gaze_array[-i] += t.lookedAtNeutral[-i];
						neu_counts[-i] += 1;
						#put the individual subject data together
						neu_individ_subject_sum[-i] += t.lookedAtNeutral[-i];
						neu_individ_subject_counts[-i] += 1;
						neu_individ_subject_nrusedtrials[-i] += t.lookedAtNeutral[-i];
					for i in (arange(2000)+1):
						if (i>len(t.lookedAtAlcohol)):
							continue;
						elif (isnan(t.lookedAtAlcohol[-i])):
							continue;
						#store the alcohol gaze patterns as the cue item
						alc_gaze_array[-i] += t.lookedAtAlcohol[-i];
						alc_counts[-i] += 1;
						#put the individual subject data together
						alc_individ_subject_sum[-i] += t.lookedAtAlcohol[-i];
						alc_individ_subject_counts[-i] += 1;
						alc_individ_subject_nrusedtrials[-i] += t.lookedAtAlcohol[-i]; 
					for i in (arange(2000)+1):
						if (i>len(t.lookedAtCigarette)):
							continue;
						elif (isnan(t.lookedAtCigarette[-i])):
							continue;							
						#store the cigarette items as the not_cue item
						cig_cue_gaze_array[-i] += t.lookedAtCigarette[-i];
						cig_cue_counts[-i] += 1;
						#put the individual subject data together
						cig_cue_individ_subject_sum[-i] += t.lookedAtCigarette[-i];
						cig_cue_individ_subject_counts[-i] += 1;
						cig_individ_subject_nrusedtrials[-i] += t.lookedAtCigarette[-i];

			neu_individ_subject_mean = neu_individ_subject_sum/neu_individ_subject_counts; #calculate the mean for this subject at each time point
			[neu_subject_means_array[index].append(ind_mew) for index,ind_mew in zip(arange(2000),neu_individ_subject_mean)]; #append this to the array for each subject
			[neu_subject_agg_counts.append(ct) for ct in neu_individ_subject_counts]; #store number of trials here		
			alc_individ_subject_mean = alc_individ_subject_sum/alc_individ_subject_counts; #calculate the mean for this subject at each time point
			[alc_subject_means_array[index].append(ind_mew) for index,ind_mew in zip(arange(2000),alc_individ_subject_mean)]; #append this to the array for each subject
			[alc_subject_agg_counts.append(ct) for ct in alc_individ_subject_counts];
			cig_cue_individ_subject_mean = cig_cue_individ_subject_sum/cig_cue_individ_subject_counts; #calculate the mean for this subject at each time point
			[cig_cue_subject_means_array[index].append(ind_mew) for index,ind_mew in zip(arange(2000),cig_cue_individ_subject_mean)]; #append this to the array for each subject
			[cig_subject_agg_counts.append(ct) for ct in cig_cue_individ_subject_counts];
			
			for index in arange(2000):
				#make sure to reverse the time point from index...
				data[index].loc[index_counter] = [int(subj_nr+1),int(ttype),selected_item,'alcohol', (1999-index), alc_individ_subject_counts[index], alc_individ_subject_nrusedtrials[index], alc_individ_subject_mean[index]];
				data[index].loc[index_counter+1] = [int(subj_nr+1),int(ttype),selected_item,'cigarette', (1999-index), cig_cue_individ_subject_counts[index], cig_individ_subject_nrusedtrials[index], cig_cue_individ_subject_mean[index]];
				data[index].loc[index_counter+2] = [int(subj_nr+1),int(ttype),selected_item,'neutral', (1999-index), neu_individ_subject_counts[index], neu_individ_subject_nrusedtrials[index], neu_individ_subject_mean[index]];
			index_counter+=3;
						
			print "completed subject %s.. \n\n"%subj_nr	

		#plot each likelihood looking at items				
		for  subj_ms, cue_name, c, a in zip([alc_subject_means_array, cig_cue_subject_means_array, neu_subject_means_array], ['alcohol','cigarette','neutral'], colors, alphas):							
			mews = array([nanmean(subj) for subj in subj_ms]); # gaze_array/counts
			sems = array([compute_BS_SEM(subj) for subj in subj_ms]);
			ax1.plot(linspace(0,2000,2000), mews, lw = 4.0, color = c, alpha = a);
			#plot the errorbars
			#for x,m,s in zip(linspace(0,1000,1000),mews,sems):
			ax1.fill_between(linspace(0,2000,2000), mews-sems, mews+sems, color = c, alpha = a*0.4);
			legend_lines.append(mlines.Line2D([],[],color=c,lw=6,alpha = a, label='likelihood(looking at %s) '%cue_name));
		#plot the sum of each for a sanity emasure to ensure they equate to one
		#agg = [(nanmean(a)+nanmean(b)+nanmean(c)) for a,b,c in zip(alc_subject_means_array, cig_cue_subject_means_array, neu_subject_means_array)];
		#ax1.plot(linspace(0,1000,1000),agg,color = 'gray', lw = 3.0);
		#legend_lines.append(mlines.Line2D([],[],color='gray',lw=4, alpha = 1.0, label='sum of all'));
		ax1.plot(linspace(0,2000,2000),linspace(0.33,0.333,2000),color = 'gray', lw = 3.0, ls='dashed');
		legend_lines.append(mlines.Line2D([],[],color='gray',lw=4, alpha = 1.0, ls = 'dashed', label='random'));	
		ax1.spines['right'].set_visible(False); ax1.spines['top'].set_visible(False);
		ax1.spines['bottom'].set_linewidth(2.0); ax1.spines['left'].set_linewidth(2.0);
		ax1.yaxis.set_ticks_position('left'); ax1.xaxis.set_ticks_position('bottom');
		ax1.legend(handles=[legend_lines[0],legend_lines[1], legend_lines[2], legend_lines[3]],loc = 2,ncol=1,fontsize = 11); # legend_lines[4]]
		title('%s Average Temporal Gaze Profile, \n Chose %s Trials'%(name, selected_item), fontsize = 22);

	#save the databases
	[d.to_csv(savepath+'%s_timepoint_%s_temporal_gaze_profile_LONG.csv'%(name, (1999-i)),index=False) for d,i in zip(data, arange(2000))]; #data.to_csv(savepath+'%s_temporal_gaze_profile.csv'%name,index=False);
	# ends here
	
	
	
def collectTemporalGazeWRTFirstSaccade(blocks, ttype, eyed = 'agg'):
	#collects each participants' trial data where they didn't blink or look down
	#do this for the STIMULUS-LOCKED data
	#allign these to the offset of the first saccade
	
	#loop through and get all the trials for each subject
	trial_matrix = [[tee for b in bl for tee in b.trials if (tee.skip==0)] for bl in blocks];
	
	#collect which trial type to run this analysis for
	#ttype = int(raw_input('Which trial type? 1 = HighC/HighA, 2 = HighC/LowA, 3 = LowC/HighA, 4 = LowC/LowA: '));
	
	name = ['high_pref', 'highC_lowA','lowC_highA','lowC_lowA'][ttype-1];
	
	data = pd.DataFrame(columns = concatenate([['subject_nr', 'trial_type', 'selected_item'],['t_%s'%(t) for t in linspace(1,2000,2000)]])); #add all participants together to the same dataFrame for simplicty
	#SCORING FOR ITEM (entry at t_XX): 0 = not looked at any item, 1 = looked at alcohol, 2 = looked at cigarette, 3 = looked at neutral, nan = timepoint didn't exist in the trial
	trial_index_counter = 0;
	
	for subj_nr,subj in enumerate(trial_matrix):

		for t in subj:
			#conditional to differentiate between trials that should be skipped for this trial type, etc.
			if ((t.dropped_sample == 0)&(t.didntLookAtAnyItems == 0)&(t.trial_type == ttype)&(t.nr_saccades > 0)):
				gaze_data = [nan for i in range(2000)]; #this will be length 2000 and include each item looked at at each time point (or 0/NaN otherwise); pre-allocate with nans
				#keep the start of the array nans until the timepoint when the trial has data for it
				
				#get the indexes corresponding to the onset of the first saccade and the end of the trial
				trial_start_index = where(t.isSaccade)[0][0];
				trial_end_index = len(t.lookedAtNeutral);
	
				#trials longer than 2000 ms will be trimmed to 2000 ms
				if trial_end_index > (2000 + trial_start_index):
					trial_end_index = (2000 + trial_start_index);
				
				iterator = 0;
	
				#now go through for the 2000 time points prior to decision and score whether the paricipants was looking at 
				for i in (linspace(trial_start_index,(2000+trial_start_index), ((2000+trial_start_index)-trial_start_index)+1)):
					if (i>=trial_end_index):
						continue;
					elif (isnan(t.lookedAtNeutral[i]) & isnan(t.lookedAtAlcohol[i]) & isnan(t.lookedAtCigarette[i])):
					#at this point, there was a nan inserted because the participant did not look at each item
					#when there are no items looked at, include a 0
						gaze_data[iterator] = 0;
					elif (t.lookedAtAlcohol[i]==1):
						gaze_data[iterator] = 1;
					elif (t.lookedAtCigarette[i]==1):						
						gaze_data[iterator] = 2;						
					elif (t.lookedAtNeutral[i]==1):	
						gaze_data[iterator] = 3;
					iterator+=1;

				#for ease of the regression computation, get the selected item into a numerical representation, same mapping as with item looked at
				if t.preferred_category=='alcohol':
					selected_item = 1;
				elif t.preferred_category=='cigarette':
					selected_item = 2;
				elif t.preferred_category=='neutral':
					selected_item = 3;					
				#at this point have collected data for gaze profile together
				#get all data points together for ease of incorporating into the dataFrame
				this_trials_data = concatenate([[int(subj_nr+1), ttype, selected_item],gaze_data]); #subject nr, trial_type, selected_item, then each timepoint data
				
				#now translate this to the dataframe for this participant
				data.loc[trial_index_counter] = this_trials_data;
				trial_index_counter += 1; #index for next trial
				
		print "completed subject %s.. \n\n"%subj_nr		

	#save the database
	data.to_csv(savepath+'/stim_locked/'+'%s_WRTFirstSaccade_trialdata.csv'%name,index=False); 
	# ends here	
	
	
	
def computeTemporalGazeProfile(blocks, eyed = 'agg'):
	#this function compute the temporal gaze profile with respect to the preferred item
	#for each subject and each trial type, find the average proportion of time spent looking
	#at the perferred tem or not. This will be the 'likelihood' of fixating the preferred item
	#with respect to time to the decision
	
	db = subject_data;
	index_counter = 0; #for database calculation
	
	#loop through and get all the trials for each subject
	trial_matrix = [[tee for b in bl for tee in b.trials if (tee.skip==0)] for bl in blocks];
	
	# #at some point store this data into a database/csv
		
	#calculate the temporal gaze profiles for each subset of rials: selected the cue, selected the not cue, and selected the neutral
	#then for each of these subsets, find and plot the probability of looking at each item through the trial
	#for cue_or_not, selected_item in zip([1,0,0],['cue','not_cue','neutral']):
	
	#collect which trial type to run this analysis for
	ttype = int(raw_input('Which trial type? 1 = HighC/HighA, 2 = HighC/LowA, 3 = LowC/HighA, 4 = LowC/LowA: '));
	
	name = ['high_pref', 'highC_lowA','lowC_highA','lowC_lowA'][ttype-1];

	#create 1000 dataframe objects that will correspond to each time point
	data = [pd.DataFrame(columns = ['sub_id','trial_type','selected_item','looked_at_item','timepoint','mean_fix_likelihood']) for i in arange(1000)];
		
	for selected_item in ['cigarette','alcohol','neutral']:		
		
		
		fig = figure(); ax1 = gca();
		ax1.set_ylim(0.0, 1.0); ax1.set_yticks(arange(0,1.01,0.1)); ax1.set_xlim([0,1000]);
		ax1.set_ylabel('Likelihood of fixating',size=18); ax1.set_xlabel('Time with respect to decision, ms',size=18,labelpad=11);
		ax1.set_xticks([0,200,400,600,800,1000]);
		ax1.set_xticklabels(['-1000','-800','-600','-400','-200','0']);
		colors = ['red','blue', 'green']; alphas = [1.0, 1.0, 1.0]; legend_lines = [];		count = 0;

		#define arrays for the neutral, alcohol and cigarette items
		neu_gaze_array = zeros(time_duration/time_bin_spacing);
		neu_counts = zeros(shape(neu_gaze_array));
		neu_subject_means_array = [[] for i in range(1000)]; #use this to store each individual subjects' mean for each time point			
		alc_gaze_array = zeros(time_duration/time_bin_spacing);
		alc_counts = zeros(shape(alc_gaze_array));
		alc_subject_means_array = [[] for i in range(1000)]; 		
		cig_cue_gaze_array = zeros(time_duration/time_bin_spacing);
		cig_cue_counts = zeros(shape(cig_cue_gaze_array));
		cig_cue_subject_means_array = [[] for i in range(1000)];
		
		for subj_nr,subj in enumerate(trial_matrix):
			neu_individ_subject_sum = zeros(time_duration/time_bin_spacing);
			neu_individ_subject_counts = zeros(time_duration/time_bin_spacing);
			alc_individ_subject_sum = zeros(time_duration/time_bin_spacing);
			alc_individ_subject_counts = zeros(time_duration/time_bin_spacing);
			cig_cue_individ_subject_sum = zeros(time_duration/time_bin_spacing);
			cig_cue_individ_subject_counts = zeros(time_duration/time_bin_spacing);
			
			for t in subj:
				#conditional to differentiate between not-cue trials when selecteing the non-cue or not
				#the second conditional include nuetral trials that were preferred only
				if ((t.dropped_sample == 0)&(t.didntLookAtAnyItems == 0)&(t.trial_type == ttype)&((t.preferred_category == selected_item))):
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
					for i in (arange(1000)+1):
						if (i>len(t.lookedAtAlcohol)):
							continue;
						elif (isnan(t.lookedAtAlcohol[-i])):
							continue;
						#store the alcohol gaze patterns as the cue item
						alc_gaze_array[-i] += t.lookedAtAlcohol[-i];
						alc_counts[-i] += 1;
						#put the individual subject data together
						alc_individ_subject_sum[-i] += t.lookedAtAlcohol[-i];
						alc_individ_subject_counts[-i] += 1;				
					for i in (arange(1000)+1):
						if (i>len(t.lookedAtCigarette)):
							continue;
						elif (isnan(t.lookedAtCigarette[-i])):
							continue;							
						#store the cigarette items as the not_cue item
						cig_cue_gaze_array[-i] += t.lookedAtCigarette[-i];
						cig_cue_counts[-i] += 1;
						#put the individual subject data together
						cig_cue_individ_subject_sum[-i] += t.lookedAtCigarette[-i];
						cig_cue_individ_subject_counts[-i] += 1;												
							
			neu_individ_subject_mean = neu_individ_subject_sum/neu_individ_subject_counts; #calculate the mean for this subject at each time point
			[neu_subject_means_array[index].append(ind_mew) for index,ind_mew in zip(arange(1000),neu_individ_subject_mean)]; #append this to the array for each subject   			
			alc_individ_subject_mean = alc_individ_subject_sum/alc_individ_subject_counts; #calculate the mean for this subject at each time point
			[alc_subject_means_array[index].append(ind_mew) for index,ind_mew in zip(arange(1000),alc_individ_subject_mean)]; #append this to the array for each subject
			cig_cue_individ_subject_mean = cig_cue_individ_subject_sum/cig_cue_individ_subject_counts; #calculate the mean for this subject at each time point
			[cig_cue_subject_means_array[index].append(ind_mew) for index,ind_mew in zip(arange(1000),cig_cue_individ_subject_mean)]; #append this to the array for each subject
			
			for index in arange(1000):
				#make sure to reverse the time point from index...
				data[index].loc[index_counter] = [int(subj_nr+1),int(ttype),selected_item,'alcohol', (999-index), alc_individ_subject_mean[index]];
				data[index].loc[index_counter+1] = [int(subj_nr+1),int(ttype),selected_item,'cigarette', (999-index), cig_cue_individ_subject_mean[index]];
				data[index].loc[index_counter+2] = [int(subj_nr+1),int(ttype),selected_item,'neutral', (999-index), neu_individ_subject_mean[index]];
			index_counter+=3;
			
			print "completed subject %s.. \n\n"%subj_nr	
		
		#plot each likelihood looking at items				
		for  subj_ms, cue_name, c, a in zip([alc_subject_means_array, cig_cue_subject_means_array, neu_subject_means_array], ['alcohol','cigarette','neutral'], colors, alphas):							
			mews = array([nanmean(subj) for subj in subj_ms]); # gaze_array/counts
			sems = array([compute_BS_SEM(subj) for subj in subj_ms]);
			ax1.plot(linspace(0,1000,1000), mews, lw = 4.0, color = c, alpha = a);
			#plot the errorbars
			#for x,m,s in zip(linspace(0,1000,1000),mews,sems):
			ax1.fill_between(linspace(0,1000,1000), mews-sems, mews+sems, color = c, alpha = a*0.4);
			legend_lines.append(mlines.Line2D([],[],color=c,lw=6,alpha = a, label='likelihood(looking at %s) '%cue_name));
		#plot the sum of each for a sanity emasure to ensure they equate to one
		#agg = [(nanmean(a)+nanmean(b)+nanmean(c)) for a,b,c in zip(alc_subject_means_array, cig_cue_subject_means_array, neu_subject_means_array)];
		#ax1.plot(linspace(0,1000,1000),agg,color = 'gray', lw = 3.0);
		#legend_lines.append(mlines.Line2D([],[],color='gray',lw=4, alpha = 1.0, label='sum of all'));
		ax1.plot(linspace(0,1000,1000),linspace(0.33,0.333,1000),color = 'gray', lw = 3.0, ls='dashed');
		legend_lines.append(mlines.Line2D([],[],color='gray',lw=4, alpha = 1.0, ls = 'dashed', label='random'));	
		ax1.spines['right'].set_visible(False); ax1.spines['top'].set_visible(False);
		ax1.spines['bottom'].set_linewidth(2.0); ax1.spines['left'].set_linewidth(2.0);
		ax1.yaxis.set_ticks_position('left'); ax1.xaxis.set_ticks_position('bottom');
		ax1.legend(handles=[legend_lines[0],legend_lines[1], legend_lines[2], legend_lines[3]],loc = 2,ncol=1,fontsize = 11); # legend_lines[4]]
		title('%s Average Temporal Gaze Profile, \n Chose %s Trials'%(name, selected_item), fontsize = 22);
		# savefig(savepath+'temporal_gaze_profile_selected_%s.png'%selected_item,dpi=400); #save as .png
		# #then strip axes and save as an .eps object
		# ax1.legend_.remove(); # legend_lines[4]]
		# title('');
		# ax1.set_ylabel(''); ax1.set_xlabel('');
		# ax1.set_xticklabels(['','','','','','']);
		# ax1.set_yticklabels(['','','','','','','','','','','','','','']);
		# savefig(savepath+'temporal_gaze_profile_selected_%s.eps'%selected_item,dpi=400); #save as .png
		
		1/0
	
	#save the databases
	[d.to_csv(savepath+'%s_timepoint_%s_temporal_gaze_profile.csv'%(name, (999-i)),index=False) for d,i in zip(data, arange(1000))]; #data.to_csv(savepath+'%s_temporal_gaze_profile.csv'%name,index=False);		
	show();
	
	
def compute_heatmaps(block_matrix, id):
	#determine and normalize all eye traces to assign alcohol to left, cigarette to top, and neutral to right
	
	ttype = int(raw_input('Which trial type? 1 = HighC/HighA, 2 = HighC/LowA, 3 = LowC/HighA, 4 = LowC/LowA: '));
	
	name = ['high_pref', 'highC_lowA','lowC_highA','lowC_lowA'][ttype-1];
		
	start_time = time.time();
		
	for selected_item in ['alcohol','cigarette','neutral']:		 #	
		
		#first, get the individual eye traces for each item for each trial where the selected_item was chosen
		# store each item's eye traces (adding a +1 for the trace being in that location at any time point in the trial) by creating little windows
		# e.g., a 4-degree by 4-degree square around each picture
		#compare against reference X,Y coordinates and place the values into each matrrix accordingly
		#aggregate this for each participant into a combined map
			
		#these are holder arrays for each participant, for each item. Each list holds a 500 by 500 matrix that will hold the aggregated 1's associated with an eye trace at that location according to it's distance wrt the reference array
		alc_subj_arrays = [zeros((20,20)) for su in block_matrix];
		cig_subj_arrays = [zeros((20,20)) for su in block_matrix];
		neu_subj_arrays = [zeros((20,20)) for su in block_matrix];
		
		#these are arrays for the aggregated data
		agg_alc_array = zeros((20,20));
		agg_cig_array = zeros((20,20));
		agg_neu_array = zeros((20,20));

		for subj_nr, blocks in enumerate(block_matrix):
			for b in blocks:
				for i in arange(0,len(b.trials)):
					if (b.trials[i].dropped_sample>0):
						continue; #skip trials with blinks or eye movements away from the screen
					elif (b.trials[i].didntLookAtAnyItems>0):
						continue;
					if (b.trials[i].trial_type!=ttype):
						continue; #skip trials where this isn't the right trial type
					
					if b.trials[i].preferred_category==selected_item: 
						
						#here, figure out where the alcohol, cigarette, and neutral items were located on each trial
						if b.trials[i].alcohol_loc == 'up':
							alc_center_xy = array([0.0,6.0]);
						elif b.trials[i].alcohol_loc == 'right':
							alc_center_xy = array([5.20,-3.0]);
						elif b.trials[i].alcohol_loc == 'left':	
							alc_center_xy = array([-5.20,-3.0]);
						else:
							1/0;
							
						if b.trials[i].cigarette_loc == 'up':
							cig_center_xy = array([0.0,6.0]);
						elif b.trials[i].cigarette_loc == 'right':
							cig_center_xy = array([5.20,-3.0]);
						elif b.trials[i].cigarette_loc == 'left':	
							cig_center_xy = array([-5.20,-3.0]);
						else:
							1/0;
							
						if b.trials[i].neutral_loc == 'up':
							neu_center_xy = array([0.0,6.0]);
						elif b.trials[i].neutral_loc == 'right':
							neu_center_xy = array([5.20,-3.0]);
						elif b.trials[i].neutral_loc == 'left':	
							neu_center_xy = array([-5.20,-3.0]);
						else:
							1/0;							
						
						#distance_threshold = 6.0;	
						#get reference arrays for each substance item for this trial, reference X, Y coordinates for a spatial array correpsonding to 4 by 4 degree square around the picture	
						alc_xx = linspace(alc_center_xy[0]-distance_threshold,alc_center_xy[0]+distance_threshold,20);
						alc_yy = linspace(alc_center_xy[1]+distance_threshold,alc_center_xy[1]-distance_threshold,20); 
						cig_xx = linspace(cig_center_xy[0]-distance_threshold,cig_center_xy[0]+distance_threshold,20);
						cig_yy = linspace(cig_center_xy[1]+distance_threshold,cig_center_xy[1]-distance_threshold,20);
						neu_xx = linspace(neu_center_xy[0]-distance_threshold,neu_center_xy[0]+distance_threshold,20);
						neu_yy = linspace(neu_center_xy[1]+distance_threshold,neu_center_xy[1]-distance_threshold,20);
											
						#just test to make sure the rfrence coordinates for each item don't overlap
						if (sum((alc_center_xy == cig_center_xy)) + sum((alc_center_xy == neu_center_xy)) + sum((neu_center_xy == cig_center_xy))) > 1:
							#the comparison is against 1 because the y coordinates of the left and right picture are the same (-3) and they would sum to 1
							1/0;
						
						#at this point, go through the eye traces and for each point determine if it's within the alcohol, cigarette, or neutral 6 by 6 window using the center coordinates for reference
						# if it is, compare it's (adjusted, zero-centered coordinates) against the reference array X and Y values (XX and YY) and allocate a 1 to that corresponding location in this subject's alc, cig, or neu combined locations
						# if there is no data to add (e.g., no looking at that item for that participants, it will still just be a zero)
						
						# #plot to draw the boundaries of alcohol limits for this trial (sanity check)											
						# fig = figure(); ax = gca();
						# ax.set_xlim(-display_size[0]/2,display_size[0]/2); ax.set_ylim(-display_size[1]/2,display_size[1]/2);
						# xx,yy = meshgrid(alc_xx,alc_yy);
						# for ex, why in zip(xx,yy):
						# 	ax.plot(ex, why, color='gray', marker='o', alpha = 0.1);
						# xx,yy = meshgrid(cig_xx,cig_yy);
						# for ex, why in zip(xx,yy):
						# 	ax.plot(ex, why, color='gray', marker='o',alpha=0.1);
						# xx,yy = meshgrid(neu_xx,neu_yy);
						# for ex, why in zip(xx,yy):
						# 	ax.plot(ex, why, color='gray', marker='o',alpha=0.1);
						# 	
						# theta = linspace(0,2*pi, 20);
						# alc_circle_x = alc_center_xy[0] + distance_threshold*cos(theta);
						# alc_circle_y = alc_center_xy[1] + distance_threshold*sin(theta);					
						# for t,g in zip(alc_circle_x, alc_circle_y):
						# 	ax.plot(t,g, color='black', marker='o',);
						# cig_circle_x = cig_center_xy[0] + distance_threshold*cos(theta);
						# cig_circle_y = cig_center_xy[1] + distance_threshold*sin(theta);					
						# for t,g in zip(cig_circle_x, cig_circle_y):
						# 	ax.plot(t,g, color='black', marker='o',);						
						# neu_circle_x = neu_center_xy[0] + distance_threshold*cos(theta);
						# neu_circle_y = neu_center_xy[1] + distance_threshold*sin(theta);					
						# for t,g in zip(neu_circle_x, neu_circle_y):
						# 	ax.plot(t,g, color='black', marker='o',);						
									
						for data_i,data in enumerate(zip(b.trials[i].eyeX, b.trials[i].eyeY)):					
							x = data[0]; y = data[1];
							#check if the X and Y position is within the boundaries for alcohol; boundaries are the endpoints of the X and Y coordinates
							if sqrt((x-alc_center_xy[0])**2 + (y-alc_center_xy[1])**2)<distance_threshold:
								#confirm that this was a lookedAtAlcohol instance
								if b.trials[i].lookedAtAlcohol[data_i]!=1:
									1/0;
								#now check where in the alcohol array is the closest distane to the X,Y position of this data point
								#this will be the minimum of the distance between each alc_xx point and alc_yy point
								x_x, y_y = meshgrid(alc_xx, alc_yy);
								minimum = 10000; coors = array([nan,nan]);
								for xx,yy in zip(flatten(x_x),flatten(y_y)):
									comparison = sqrt((x-xx)**2 + (y-yy)**2);
									if comparison < minimum:
										minimum = comparison;
										coors[0] = xx; coors[1] = yy;
										
								#after this, add a 1 to the appropriate location in this subjects' aggregated alcohol 'map'
								x_loc = where(coors[0]==alc_xx)[0][0]; #x coordinate
								y_loc = where(coors[1]==alc_yy)[0][0]; #y coordinate
								alc_subj_arrays[subj_nr][y_loc,x_loc] += 1; #add the 1 to the location in the corresponding map. NOTE the yloc, xloc coordinate system for indexing with this array. 
								
								# ax.plot(b.trials[i].eyeX[data_i], b.trials[i].eyeY[data_i], color='red', marker='o'); #for plotting/debugging 

							elif sqrt((x-cig_center_xy[0])**2 + (y-cig_center_xy[1])**2)<distance_threshold:	
								#confirm that this was a lookedAtAlcohol instance
								if b.trials[i].lookedAtCigarette[data_i]!=1:
									1/0;
								#now check where in the cigarette array is the closest distane to the X,Y position of this data point
								#this will be the minimum of the distance between each cig_xx point and cig_yy point
								x_x, y_y = meshgrid(cig_xx, cig_yy);
								minimum = 10000; coors = array([nan,nan]);
								for xx,yy in zip(flatten(x_x),flatten(y_y)):
									comparison = sqrt((x-xx)**2 + (y-yy)**2);
									if comparison < minimum:
										minimum = comparison;
										coors[0] = xx; coors[1] = yy;
										
								#after this, add a 1 to the appropriate location in this subjects' aggregated alcohol 'map'
								x_loc = where(coors[0]==cig_xx)[0][0]; #x coordinate
								y_loc = where(coors[1]==cig_yy)[0][0]; #y coordinate
								cig_subj_arrays[subj_nr][y_loc,x_loc] += 1; #add the 1 to the location in the corresponding map. NOTE the yloc, xloc coordinate system for indexing with this array.
								
							elif sqrt((x-neu_center_xy[0])**2 + (y-neu_center_xy[1])**2)<distance_threshold:
								#confirm that this was a lookedAtAlcohol instance
								if b.trials[i].lookedAtNeutral[data_i]!=1:
									1/0;
								#now check where in the neutral array is the closest distane to the X,Y position of this data point
								#this will be the minimum of the distance between each neu_xx point and neu_yy point
								x_x, y_y = meshgrid(neu_xx, neu_yy);
								minimum = 10000; coors = array([nan,nan]);
								for xx,yy in zip(flatten(x_x),flatten(y_y)):
									comparison = sqrt((x-xx)**2 + (y-yy)**2);
									if comparison < minimum:
										minimum = comparison;
										coors[0] = xx; coors[1] = yy;
										
								#after this, add a 1 to the appropriate location in this subjects' aggregated alcohol 'map'
								x_loc = where(coors[0]==neu_xx)[0][0]; #x coordinate
								y_loc = where(coors[1]==neu_yy)[0][0]; #y coordinate
								neu_subj_arrays[subj_nr][y_loc,x_loc] += 1; #add the 1 to the location in the corresponding map. NOTE the yloc, xloc coordinate system for indexing with this array.
					end_time = time.time();
					print 'Aggregated total time = %4.2f minutes, completed trial nr %s'%((end_time-start_time)/60.0, b.trials[i].trial_nr);
				print '\n completed subject %s block nr %s '%(subj_nr, b.block_nr)  # trial nr %sb.trials[i].trial_nr)
				end_time = time.time();
				print 'Aggregated total time = %4.2f minutes \n'%((end_time-start_time)/60.0);
				if b.block_nr==len(blocks):
					# #first save the 'raw' heat maps
					# figure(); imshow(alc_subj_arrays[subj_nr], cmap='hot'); title('%s_selected_%s_raw_ALC_heatmap_subj_%s'%(name, selected_item, subj_nr));
					# savefig(figurepath+'heatmaps/'+'%s_selected_%s_raw_ALC_heatmap_subj_%s.png'%(name, selected_item, subj_nr));
					# figure(); imshow(cig_subj_arrays[subj_nr], cmap='hot'); title('%s_selected_%s_raw_CIG_heatmap_subj_%s'%(name, selected_item, subj_nr));
					# savefig(figurepath+'heatmaps/'+'%s_selected_%s_raw_CIG_heatmap_subj_%s.png'%(name, selected_item, subj_nr));
					# figure(); imshow(neu_subj_arrays[subj_nr], cmap='hot'); title('%s_selected_%s_raw_NEU_heatmap_subj_%s'%(name, selected_item, subj_nr));
					# savefig(figurepath+'heatmaps/'+'%s_selected_%s_raw_NEU_heatmap_subj_%s.png'%(name, selected_item, subj_nr));
									
					#then standardize the values (e.g., make them proportions) wrt to the maximum values in this subjct's alcohol, cigarette, or neutral maps (is this right?)
					#first find the maximum overall for this subject across alc, cig and neu maps
					alc_max = amax(alc_subj_arrays[subj_nr]); #[amax(alc_subj_arrays[subj_nr]) if (isnan()) else -2];
					cig_max = amax(cig_subj_arrays[subj_nr]);
					neu_max = amax(neu_subj_arrays[subj_nr]);
					subject_max = max(alc_max,cig_max,neu_max); #max for this subject across all maps
					
					#if there is a maximum more than 0, divide by that maximum. Otherwise, do nothing to keep the maps as all zeros (otherwise would be nans...)
					if subject_max > 0:
						#then, divide this subjects' maps by this value
						alc_subj_arrays[subj_nr] = alc_subj_arrays[subj_nr]/float(subject_max);
						cig_subj_arrays[subj_nr] = cig_subj_arrays[subj_nr]/float(subject_max);
						neu_subj_arrays[subj_nr] = neu_subj_arrays[subj_nr]/float(subject_max);
					
					#now save this subjects' maps again with the standardized values
					figure(); imshow(alc_subj_arrays[subj_nr], cmap='hot', vmin = 0.0, vmax = 1.0); title('%s_selected_%s_standardized_ALC_heatmap_subj_%s'%(name, selected_item, subj_nr));
					savefig(figurepath+'heatmaps/'+name+'/'+'%s_selected_%s_standardized_ALC_heatmap_subj_%s.png'%(name, selected_item, subj_nr));
					figure(); imshow(cig_subj_arrays[subj_nr], cmap='hot', vmin = 0.0, vmax = 1.0); title('%s_selected_%s_standardized_CIG_heatmap_subj_%s'%(name, selected_item, subj_nr));
					savefig(figurepath+'heatmaps/'+name+'/'+'%s_selected_%s_standardized_CIG_heatmap_subj_%s.png'%(name, selected_item, subj_nr));
					figure(); imshow(neu_subj_arrays[subj_nr], cmap='hot', vmin = 0.0, vmax = 1.0); title('%s_selected_%s_standardized_NEU_heatmap_subj_%s'%(name, selected_item, subj_nr));
					savefig(figurepath+'heatmaps/'+name+'/'+'%s_selected_%s_standardized_NEU_heatmap_subj_%s.png'%(name, selected_item, subj_nr));					
					
					close('all');
					
				#after all subjects' have been run through, we want to aggregate them all together by averaging
				
		for sualc, sucig, suneu in zip(alc_subj_arrays,cig_subj_arrays,neu_subj_arrays):
			agg_alc_array += sualc; #add each subjects' heat maps together
			agg_cig_array += sucig; 
			agg_neu_array += suneu;
		
		agg_alc_array = agg_alc_array/29.0; #to get the average
		agg_cig_array = agg_cig_array/29.0; #to get the average
		agg_neu_array = agg_neu_array/29.0; #to get the average

		figure(); imshow(agg_alc_array, cmap='hot', vmin = 0.0, vmax = 1.0); title('%s_selected_%s_averaged_ALC_heatmap_subj_%s'%(name, selected_item, id));
		savefig(figurepath+'heatmaps/'+name+'/'+'%s_selected_%s_averaged_ALC_heatmap_subj_%s.png'%(name, selected_item, id));
		savefig(figurepath+'heatmaps/'+name+'/'+'%s_selected_%s_averaged_ALC_heatmap_subj_%s.eps'%(name, selected_item, id));			
		figure(); imshow(agg_cig_array , cmap='hot', vmin = 0.0, vmax = 1.0); title('%s_selected_%s_averaged_CIG_heatmap_subj_%s'%(name, selected_item, id));
		savefig(figurepath+'heatmaps/'+name+'/'+'%s_selected_%s_averaged_CIG_heatmap_subj_%s.png'%(name, selected_item, id));
		savefig(figurepath+'heatmaps/'+name+'/'+'%s_selected_%s_averaged_CIG_heatmap_subj_%s.eps'%(name, selected_item, id));
		figure(); imshow(agg_neu_array, cmap='hot', vmin = 0.0, vmax = 1.0); title('%s_selected_%s_averaged_NEU_heatmap_subj_%s'%(name, selected_item, id));
		savefig(figurepath+'heatmaps/'+name+'/'+'%s_selected_%s_averaged_NEU_heatmap_subj_%s.png'%(name, selected_item, id));
		savefig(figurepath+'heatmaps/'+name+'/'+'%s_selected_%s_averaged_NEU_heatmap_subj_%s.eps'%(name, selected_item, id));
		show();


def compute_aggregated_heatmaps(block_matrix, id, ttype):
	#determine and normalize all eye traces to assign alcohol to left, cigarette to top, and neutral to right
	
	#ttype = int(raw_input('Which trial type? 1 = HighC/HighA, 2 = HighC/LowA, 3 = LowC/HighA, 4 = LowC/LowA: '));
	
	name = ['high_pref', 'highC_lowA','lowC_highA','lowC_lowA'][ttype-1];
		
	start_time = time.time();
		
	#first, get the individual eye traces for each item for each trial where the selected_item was chosen
	# store each item's eye traces (adding a +1 for the trace being in that location at any time point in the trial) by creating little windows
	# e.g., a 4-degree by 4-degree square around each picture
	#compare against reference X,Y coordinates and place the values into each matrrix accordingly
	#aggregate this for each participant into a combined map
		
	#these are holder arrays for each participant, for each item. Each list holds a 500 by 500 matrix that will hold the aggregated 1's associated with an eye trace at that location according to it's distance wrt the reference array
	alc_subj_arrays = [zeros((20,20)) for su in block_matrix];
	cig_subj_arrays = [zeros((20,20)) for su in block_matrix];
	neu_subj_arrays = [zeros((20,20)) for su in block_matrix];
	
	#these are arrays for the aggregated data
	agg_alc_array = zeros((20,20));
	agg_cig_array = zeros((20,20));
	agg_neu_array = zeros((20,20));

	for subj_nr, blocks in enumerate(block_matrix):
		for b in blocks:
			for i in arange(0,len(b.trials)):
				if (b.trials[i].dropped_sample>0):
					continue; #skip trials with blinks or eye movements away from the screen
				elif (b.trials[i].didntLookAtAnyItems>0):
					continue;
				if (b.trials[i].trial_type!=ttype):
					continue; #skip trials where this isn't the right trial type

				#here, figure out where the alcohol, cigarette, and neutral items were located on each trial
				if b.trials[i].alcohol_loc == 'up':
					alc_center_xy = array([0.0,6.0]);
				elif b.trials[i].alcohol_loc == 'right':
					alc_center_xy = array([5.20,-3.0]);
				elif b.trials[i].alcohol_loc == 'left':	
					alc_center_xy = array([-5.20,-3.0]);
				else:
					1/0;
					
				if b.trials[i].cigarette_loc == 'up':
					cig_center_xy = array([0.0,6.0]);
				elif b.trials[i].cigarette_loc == 'right':
					cig_center_xy = array([5.20,-3.0]);
				elif b.trials[i].cigarette_loc == 'left':	
					cig_center_xy = array([-5.20,-3.0]);
				else:
					1/0;
					
				if b.trials[i].neutral_loc == 'up':
					neu_center_xy = array([0.0,6.0]);
				elif b.trials[i].neutral_loc == 'right':
					neu_center_xy = array([5.20,-3.0]);
				elif b.trials[i].neutral_loc == 'left':	
					neu_center_xy = array([-5.20,-3.0]);
				else:
					1/0;							
				
				#distance_threshold = 6.0;	
				#get reference arrays for each substance item for this trial, reference X, Y coordinates for a spatial array correpsonding to 4 by 4 degree square around the picture	
				alc_xx = linspace(alc_center_xy[0]-distance_threshold,alc_center_xy[0]+distance_threshold,20);
				alc_yy = linspace(alc_center_xy[1]+distance_threshold,alc_center_xy[1]-distance_threshold,20); 
				cig_xx = linspace(cig_center_xy[0]-distance_threshold,cig_center_xy[0]+distance_threshold,20);
				cig_yy = linspace(cig_center_xy[1]+distance_threshold,cig_center_xy[1]-distance_threshold,20);
				neu_xx = linspace(neu_center_xy[0]-distance_threshold,neu_center_xy[0]+distance_threshold,20);
				neu_yy = linspace(neu_center_xy[1]+distance_threshold,neu_center_xy[1]-distance_threshold,20);
									
				#just test to make sure the rfrence coordinates for each item don't overlap
				if (sum((alc_center_xy == cig_center_xy)) + sum((alc_center_xy == neu_center_xy)) + sum((neu_center_xy == cig_center_xy))) > 1:
					#the comparison is against 1 because the y coordinates of the left and right picture are the same (-3) and they would sum to 1
					1/0;
				
				#at this point, go through the eye traces and for each point determine if it's within the alcohol, cigarette, or neutral 6 by 6 window using the center coordinates for reference
				# if it is, compare it's (adjusted, zero-centered coordinates) against the reference array X and Y values (XX and YY) and allocate a 1 to that corresponding location in this subject's alc, cig, or neu combined locations
				# if there is no data to add (e.g., no looking at that item for that participants, it will still just be a zero)					
							
				for data_i,data in enumerate(zip(b.trials[i].eyeX, b.trials[i].eyeY)):					
					x = data[0]; y = data[1];
					#check if the X and Y position is within the boundaries for alcohol; boundaries are the endpoints of the X and Y coordinates
					if sqrt((x-alc_center_xy[0])**2 + (y-alc_center_xy[1])**2)<distance_threshold:
						#confirm that this was a lookedAtAlcohol instance
						if b.trials[i].lookedAtAlcohol[data_i]!=1:
							1/0;
						#now check where in the alcohol array is the closest distane to the X,Y position of this data point
						#this will be the minimum of the distance between each alc_xx point and alc_yy point
						x_x, y_y = meshgrid(alc_xx, alc_yy);
						minimum = 10000; coors = array([nan,nan]);
						for xx,yy in zip(flatten(x_x),flatten(y_y)):
							comparison = sqrt((x-xx)**2 + (y-yy)**2);
							if comparison < minimum:
								minimum = comparison;
								coors[0] = xx; coors[1] = yy;
								
						#after this, add a 1 to the appropriate location in this subjects' aggregated alcohol 'map'
						x_loc = where(coors[0]==alc_xx)[0][0]; #x coordinate
						y_loc = where(coors[1]==alc_yy)[0][0]; #y coordinate
						alc_subj_arrays[subj_nr][y_loc,x_loc] += 1; #add the 1 to the location in the corresponding map. NOTE the yloc, xloc coordinate system for indexing with this array. 
						
						# ax.plot(b.trials[i].eyeX[data_i], b.trials[i].eyeY[data_i], color='red', marker='o'); #for plotting/debugging 

					elif sqrt((x-cig_center_xy[0])**2 + (y-cig_center_xy[1])**2)<distance_threshold:	
						#confirm that this was a lookedAtAlcohol instance
						if b.trials[i].lookedAtCigarette[data_i]!=1:
							1/0;
						#now check where in the cigarette array is the closest distane to the X,Y position of this data point
						#this will be the minimum of the distance between each cig_xx point and cig_yy point
						x_x, y_y = meshgrid(cig_xx, cig_yy);
						minimum = 10000; coors = array([nan,nan]);
						for xx,yy in zip(flatten(x_x),flatten(y_y)):
							comparison = sqrt((x-xx)**2 + (y-yy)**2);
							if comparison < minimum:
								minimum = comparison;
								coors[0] = xx; coors[1] = yy;
								
						#after this, add a 1 to the appropriate location in this subjects' aggregated alcohol 'map'
						x_loc = where(coors[0]==cig_xx)[0][0]; #x coordinate
						y_loc = where(coors[1]==cig_yy)[0][0]; #y coordinate
						cig_subj_arrays[subj_nr][y_loc,x_loc] += 1; #add the 1 to the location in the corresponding map. NOTE the yloc, xloc coordinate system for indexing with this array.
						
					elif sqrt((x-neu_center_xy[0])**2 + (y-neu_center_xy[1])**2)<distance_threshold:
						#confirm that this was a lookedAtAlcohol instance
						if b.trials[i].lookedAtNeutral[data_i]!=1:
							1/0;
						#now check where in the neutral array is the closest distane to the X,Y position of this data point
						#this will be the minimum of the distance between each neu_xx point and neu_yy point
						x_x, y_y = meshgrid(neu_xx, neu_yy);
						minimum = 10000; coors = array([nan,nan]);
						for xx,yy in zip(flatten(x_x),flatten(y_y)):
							comparison = sqrt((x-xx)**2 + (y-yy)**2);
							if comparison < minimum:
								minimum = comparison;
								coors[0] = xx; coors[1] = yy;
								
						#after this, add a 1 to the appropriate location in this subjects' aggregated alcohol 'map'
						x_loc = where(coors[0]==neu_xx)[0][0]; #x coordinate
						y_loc = where(coors[1]==neu_yy)[0][0]; #y coordinate
						neu_subj_arrays[subj_nr][y_loc,x_loc] += 1; #add the 1 to the location in the corresponding map. NOTE the yloc, xloc coordinate system for indexing with this array.
				end_time = time.time();
				print 'Aggregated total time = %4.2f minutes, completed trial nr %s'%((end_time-start_time)/60.0, b.trials[i].trial_nr);
			print '\n completed subject %s block nr %s '%(subj_nr, b.block_nr)  # trial nr %sb.trials[i].trial_nr)
			end_time = time.time();
			print 'Aggregated total time = %4.2f minutes \n'%((end_time-start_time)/60.0);
			if b.block_nr==len(blocks):
				# #first save the 'raw' heat maps
				# figure(); imshow(alc_subj_arrays[subj_nr], cmap='hot'); title('%s_selected_%s_raw_ALC_heatmap_subj_%s'%(name, selected_item, subj_nr));
				# savefig(figurepath+'heatmaps/'+'%s_selected_%s_raw_ALC_heatmap_subj_%s.png'%(name, selected_item, subj_nr));
				# figure(); imshow(cig_subj_arrays[subj_nr], cmap='hot'); title('%s_selected_%s_raw_CIG_heatmap_subj_%s'%(name, selected_item, subj_nr));
				# savefig(figurepath+'heatmaps/'+'%s_selected_%s_raw_CIG_heatmap_subj_%s.png'%(name, selected_item, subj_nr));
				# figure(); imshow(neu_subj_arrays[subj_nr], cmap='hot'); title('%s_selected_%s_raw_NEU_heatmap_subj_%s'%(name, selected_item, subj_nr));
				# savefig(figurepath+'heatmaps/'+'%s_selected_%s_raw_NEU_heatmap_subj_%s.png'%(name, selected_item, subj_nr));
								
				#then standardize the values (e.g., make them proportions) wrt to the maximum values in this subjct's alcohol, cigarette, or neutral maps (is this right?)
				#first find the maximum overall for this subject across alc, cig and neu maps
				alc_max = amax(alc_subj_arrays[subj_nr]); #[amax(alc_subj_arrays[subj_nr]) if (isnan()) else -2];
				cig_max = amax(cig_subj_arrays[subj_nr]);
				neu_max = amax(neu_subj_arrays[subj_nr]);
				subject_max = max(alc_max,cig_max,neu_max); #max for this subject across all maps
				
				#if there is a maximum more than 0, divide by that maximum. Otherwise, do nothing to keep the maps as all zeros (otherwise would be nans...)
				if subject_max > 0:
					#then, divide this subjects' maps by this value
					alc_subj_arrays[subj_nr] = alc_subj_arrays[subj_nr]/float(subject_max);
					cig_subj_arrays[subj_nr] = cig_subj_arrays[subj_nr]/float(subject_max);
					neu_subj_arrays[subj_nr] = neu_subj_arrays[subj_nr]/float(subject_max);
				
				#now save this subjects' maps again with the standardized values
				figure(); imshow(alc_subj_arrays[subj_nr], cmap='hot', vmin = 0.0, vmax = 1.0); title('%s_aggregatedacrosschoices_standardized_ALC_heatmap_subj_%s'%(name,  subj_nr));
				savefig(figurepath+'heatmaps/'+name+'/'+'%s_aggregatedacrosschoices_standardized_ALC_heatmap_subj_%s.png'%(name,  subj_nr));
				figure(); imshow(cig_subj_arrays[subj_nr], cmap='hot', vmin = 0.0, vmax = 1.0); title('%s_aggregatedacrosschoices_standardized_CIG_heatmap_subj_%s'%(name,  subj_nr));
				savefig(figurepath+'heatmaps/'+name+'/'+'%s_aggregatedacrosschoices_standardized_CIG_heatmap_subj_%s.png'%(name,  subj_nr));
				figure(); imshow(neu_subj_arrays[subj_nr], cmap='hot', vmin = 0.0, vmax = 1.0); title('%s_aggregatedacrosschoices_standardized_NEU_heatmap_subj_%s'%(name, subj_nr));
				savefig(figurepath+'heatmaps/'+name+'/'+'%s_aggregatedacrosschoices_standardized_NEU_heatmap_subj_%s.png'%(name,  subj_nr));					
				
				close('all');
				
			#after all subjects' have been run through, we want to aggregate them all together by averaging
				
	for sualc, sucig, suneu in zip(alc_subj_arrays,cig_subj_arrays,neu_subj_arrays):
		agg_alc_array += sualc; #add each subjects' heat maps together
		agg_cig_array += sucig; 
		agg_neu_array += suneu;
	
	agg_alc_array = agg_alc_array/29.0; #to get the average
	agg_cig_array = agg_cig_array/29.0; #to get the average
	agg_neu_array = agg_neu_array/29.0; #to get the average

	figure(); imshow(agg_alc_array, cmap='hot', vmin = 0.0, vmax = 1.0); title('%s_aggregatedacrosschoices_averaged_ALC_heatmap_subj_%s'%(name,  id));
	savefig(figurepath+'heatmaps/'+name+'/'+'%s_aggregatedacrosschoices_averaged_ALC_heatmap_subj_%s.png'%(name,  id));
	savefig(figurepath+'heatmaps/'+name+'/'+'%s_aggregatedacrosschoices_averaged_ALC_heatmap_subj_%s.eps'%(name,  id));			
	figure(); imshow(agg_cig_array , cmap='hot', vmin = 0.0, vmax = 1.0); title('%s_aggregatedacrosschoices_averaged_CIG_heatmap_subj_%s'%(name,  id));
	savefig(figurepath+'heatmaps/'+name+'/'+'%s_aggregatedacrosschoices_averaged_CIG_heatmap_subj_%s.png'%(name,  id));
	savefig(figurepath+'heatmaps/'+name+'/'+'%s_aggregatedacrosschoices_averaged_CIG_heatmap_subj_%s.eps'%(name, id));
	figure(); imshow(agg_neu_array, cmap='hot', vmin = 0.0, vmax = 1.0); title('%s_aggregatedacrosschoices_averaged_NEU_heatmap_subj_%s'%(name,  id));
	savefig(figurepath+'heatmaps/'+name+'/'+'%s_aggregatedacrosschoices_averaged_NEU_heatmap_subj_%s.png'%(name, id));
	savefig(figurepath+'heatmaps/'+name+'/'+'%s_aggregatedacrosschoices_averaged_NEU_heatmap_subj_%s.eps'%(name,  id));
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

def plotSingleTrialEyeGaze(trial, string_for_display = ''):
	
	#string for display is a string that will be displayed on the plot (e.g., this trial has this many dwells)	
	circle1 = pyplot.Circle(left_pic_coors, distance_threshold, color='lightgrey');
	circle2 = pyplot.Circle(right_pic_coors, distance_threshold, color='lightgrey');
	circle3 = pyplot.Circle(up_pic_coors, distance_threshold, color='lightgrey');

	isSaccade = trial.isSaccade; #get the isSaccade data from the previously calculated criterion
	# # #plot the different saccades for the given trial for use in debugging	
	fig = figure(figsize = (11,7.5)); ax = gca(); ax.set_xlim([-display_size[0]/2,display_size[0]/2]); ax.set_ylim([-display_size[1]/2,display_size[1]/2]); #figsize = (12.8,7.64)
	ax.set_ylabel('Y Position, Degrees of Visual Angle',size=18); ax.set_xlabel('X Position, Degrees of Visual Angle',size=18,labelpad=11); hold(True);
	legend_lines = []; colors = ['red','green','blue','purple','orange','brown','grey','crimson','deepskyblue','lime','salmon','deeppink','lightsteelblue','palevioletred','azure','gold','yellowgreen',
								 'paleturquoise','darkorange', 'orchid', 'chocolate', 'yellow', 'lavender','indianred','bisque','olivedrab','seagreen','darkcyan','cadetblue',
								 'palevioletred','navy','blanchedalmond','tomato','saddlebrown','honeydew',
								 'indigo','lightpink','peru','slateblue', 'red','green','blue','purple','orange','brown','grey','crimson','deepskyblue','lime','salmon','deeppink','lightsteelblue','palevioletred','azure','gold','yellowgreen',
								 'paleturquoise','darkorange', 'orchid', 'chocolate', 'yellow', 'lavender','indianred','bisque','olivedrab','seagreen','darkcyan','cadetblue',
								 'palevioletred','navy','blanchedalmond','tomato','saddlebrown','honeydew',
								 'indigo','lightpink','peru','slateblue','red','green','blue','purple','orange','brown','grey','crimson','deepskyblue','lime','salmon','deeppink','lightsteelblue','palevioletred','azure','gold','yellowgreen',
								 'paleturquoise','darkorange', 'orchid', 'chocolate', 'yellow', 'lavender','indianred','bisque','olivedrab','seagreen','darkcyan','cadetblue',
								 'palevioletred','navy','blanchedalmond','tomato','saddlebrown','honeydew',
								 'indigo','lightpink','peru','slateblue'];
	#add the circles
	ax.add_artist(circle1);
	ax.add_artist(circle2);
	ax.add_artist(circle3);
	
	#first plot the eye traces with respect to the velocity data
	#if the eye is in movements, use the color array above. otheriwse use black to denote fixation
	saccade_counter = 0; nr_saccades = 0;
	for i,xx,yy,issac in zip(range(len(trial.sample_times)),
										 trial.eyeX, trial.eyeY, isSaccade):
		#plot the eye trace in black if not saccading
		if issac == 0:
			ax.plot(xx,yy, color = 'black', marker = 'o', ms = 4);
			#conditional to switch to the next saccade color
			#if the previous sample was saccading and now it isn't time for a swtch (add a number to saccades, switch the color for next time)
			if (isSaccade[i-1]==True)&(i>0):  					
				saccade_counter+=1;
				if saccade_counter > len(colors):
					saccade_counter=0;					
		else:
			ax.plot(xx, yy, color = colors[saccade_counter], marker = 'o', ms = 4);
			if (isSaccade[i-1]==False)&(i>0):  
				nr_saccades+=1;
				legend_lines.append(mlines.Line2D([],[],color=colors[saccade_counter],lw=6,alpha = 1.0, label='saccade  %s'%(nr_saccades)));
			
	ax.spines['right'].set_visible(False); ax.spines['top'].set_visible(False);
	ax.spines['bottom'].set_linewidth(2.0); ax.spines['left'].set_linewidth(2.0);
	ax.yaxis.set_ticks_position('left'); ax.xaxis.set_ticks_position('bottom');
	ax.legend(handles=[hand for hand in legend_lines],loc = 2,ncol=3,fontsize = 10); 
	title('Eye Trace and Position Velocity \nSubject %s, Block %s, Trial %s'%(trial.sub_id, trial.block_nr, trial.trial_nr), fontsize = 22);
	
	#now plot the velocity data in an inset plot	
	ia = inset_axes(ax, width="30%", height="30%", loc=1); #set the inset axes as percentages of the original axis size
	saccade_counter = 0; nr_saccades = 0;
	for i,filt_vel,orig_vel,issac in zip(range(len(trial.sample_times)),
										 trial.filtered_velocities, trial.velocities, isSaccade):
		#plot the eye trace in black if not saccading
		plot(i, orig_vel, color = 'gray', marker = '*', ms = 1.0, alpha = 0.5),
		if issac == 0:
			plot(i, filt_vel, color = 'black', marker = '*', ms = 1.5);  #
			#conditional to switch to the next saccade color
			#if the previous sample was saccading and now it isn't time for a swtch (add a number to saccades, switch the color for next time)
			if (isSaccade[i-1]==True)&(i>0):			
				saccade_counter+=1;
				if saccade_counter > len(colors):
					saccade_counter=0;
		else:
			plot(i, filt_vel, color = colors[saccade_counter], marker = '*', ms = 1.5); #filt_vel
			if (isSaccade[i-1]==False)&(i>0):  
				nr_saccades+=1;
	#plot the velocity trheshold and set labels
	plot(linspace(0,len(trial.sample_times),len(trial.sample_times)), linspace(trial.saccadeCriterion,trial.saccadeCriterion+0.01,len(trial.sample_times)), color = 'red', ls = 'dashed', lw = 1.0);
	ia.set_ylabel('Velocity', fontsize = 14); ia.set_xlabel('Time', fontsize = 14); title('Velocity Profile', fontsize = 14);
	
	fig.text(0.7, 0.4, string_for_display,size=16,weight='bold');

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

#this gets the subject blocks for a specified subset of subjects
#'indexes' should be an array or list that specifies which indices
#should be used to correspondingly import the data from the 'ids' structures
def getSubsetSubjectBlocks(indexes):
	indexes = array(indexes); #cast the variables so that the index vector is an array
	# id_indexes = range(len(ids)); #get the full list of indexes
	# bool_arr = [True if (idx in indexes) else False for idx in id_indexes];
	# #^create a boolean array of truth values corresponding to subjects I care about 
	blocks = [[] for i in range(len(ids))]; #create a list of empty lists to append the individual blocks to
	for i, sub_id in zip(indexes, ids[0:indexes[-1]]):    #bool_arr
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
		
		if os.path.isfile(shelvepath+'/velocity_thresholds/'+'subject_%s_block%s_velthresholds.csv'%(self.sub_id, self.block_nr)):
			block_data = pd.read_csv(shelvepath+'/velocity_thresholds/'+'subject_%s_block%s_velthresholds.csv'%(self.sub_id, self.block_nr),index_col=0);
			print('\n Loaded existing data for subject %s , block %s \n'%(self.sub_id, self.block_nr));

		else:
			l = len(matStructure.trial_data);
			block_data = pd.DataFrame(columns = ['sub_id', 'block_nr', 'trial_number','completed','endingVelCrit','skip_trial'],
									  index = range(1,l+1));
			block_data['sub_id'] = self.sub_id; block_data['block_nr'] = self.block_nr;
			block_data['completed'] = 0;
		
		self.trials = [trial(trialData, block_data) for trialData in matStructure.trial_data];

		#save the velocity threshold criterion data
		block_data.to_csv(shelvepath+'/velocity_thresholds/'+'subject_%s_block%s_velthresholds.csv'%(self.sub_id, self.block_nr));

#define a Trial object that will hold the individual trial data 
class trial(object):
	#object being passed into this Trial instance should be a dictionary corresponding to the trial data for this given trial
	def __init__(self, trialData, df):
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
		self.preferred_category = nan; #will change later in the loop below
		#finally, eye position and pupil size information
		self.drift_shift = trialData.drift_shift;

		self.skip = 0;
		self.didntLookAtAnyItems = nan; #predfine this, will change it in self.getETData for valid trials

		#get eye trace information for all trials here
		#loop through to get only unique samples, e.g. sampling at 1000 Hz
		if isinstance(trialData.sampleTimes, int):
			#this is only triggered if there was only one sample in sample times, which means it can't be accessed via trialDate.sampleTimes[0]
			all_sample_times = trialData.sampleTimes;
			#get the data together	
			self.sample_times = array([all_sample_times]); #[::sampStep];
			self.eyeX = array([trialData.eyeX]); #[::sampStep];
			self.eyeY = array([trialData.eyeY]); #[::sampStep];
			self.p_size = array([trialData.pSize]); #[::sampStep];
		else:
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
					if (abs(x_pos)>(0.5*display_size[0]))|(abs(y_pos)>(0.5*display_size[1])):
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
		
		#here, could standardize the eye trace information (e.g., from sample 1 to sample 100)
		#			
		
		#get the velocity threshold, skip trial, and completed values from the block_data
		df['trial_number'].iloc[self.trial_nr-1] = self.trial_nr;
		sk = df['skip_trial'].iloc[self.trial_nr-1];
		completed = df['completed'].iloc[self.trial_nr-1];
		velCrit = df['endingVelCrit'].iloc[self.trial_nr-1];
		
		#in the extreme case of there only being one sample, just skip the trial because it's a pain in the ass and I won't be able to use it anyway...
		if type(trialData.sampleTimes)==int:
			self.trial_type = -1;
			self.dropped_sample = 1;
			self.skip = 1;
			self.preferred_category = -1;
			self.isSaccade = [-1];
			#save these values to the DataFrame
			df['skip_trial'].iloc[self.trial_nr-1] = 1;
			df['completed'].iloc[self.trial_nr-1] = 1;
			df['endingVelCrit'].iloc[self.trial_nr-1] = -1;
			
		else:
			#find when the subject was saccading in each trial
			#use a differentiation method to define the velocity (eye position change/time change) for each time point in the trial
			#for each trial for each subject, go through and manually adjust the criterion for velocity as needed
			# because of how I'm doing this, I want to save each trial after I've been through it so I don't have to do this each time...
			#to do so, I will save completed trials' saccade velocity criterion to a .csv that I will import
			#if I've already done the trial, I will use the velocity criertion that was already saved
			
			timeChange = 0.001; #diff(self.sample_times); #difference in time, in seconds 
			xChange = -diff(self.eyeX);
			yChange = -diff(self.eyeY);
			totalChange = sqrt(xChange**2+yChange**2);
			temp = totalChange/timeChange; #calculate the velocity for each time point
			self.velocities = insert(temp,0,0); #insert a 0 at the beginning of the array for the first time point
			
			#create a failsafe for very fast trials, where there is not enough samples to use the butterworth filter
			if len(self.velocities)>=9:

				#Next filter the velocities.
				#get params for a butterworth filter and bandpass it at 20 Hz
				trialTime = self.sample_times[-1]-self.sample_times[0]; #get total time for the trial
				samplingRate = 1000.0; #round(len(self.sample_times)/float(trialTime)); #get the downsampled sampling rate
				halfSRate = samplingRate/2;
				
				freqCut =  100; #20; #Christie used a frequency cut off of 20 for the filter, but 'it should be 100' 
		
				butterwindow = freqCut/halfSRate; nthOrder = 2; #defining parameters for the butterworth filter
				[b,a] = ssignal.butter(nthOrder,butterwindow); #fit the butterworth filter			
				y = ssignal.filtfilt(b,a,self.velocities,padtype='odd'); #get the filtered velocity data		
				self.filtered_velocities = y; #append the filtered velocities to this trial instance
				
				#if there is a NaN in the filtered velocities data, it means we lost samples of data from this trial (they looked down, etc.)
				#we want to skip this trial, so I'll set self. skip to 1
				
				if isnan(self.filtered_velocities).any():
					self.skip = 1;
					self.isSaccade = [-1];
					#save these values to the DataFrame
					df['skip_trial'].iloc[self.trial_nr-1] = 1;
					df['completed'].iloc[self.trial_nr-1] = 1;
					df['endingVelCrit'].iloc[self.trial_nr-1] = -1;
				else:
					#check if this subject has been completed. if so, find the corresponding trial velocity threshold and skip trial
					if isnan(velCrit):
						#now determine where the eye was in motion by using an (arbitrary) criterion for saccade velocity

						startingVelCrit = 100; #80; #55; #christie used a velocity threshold of 100 degrees/second

					else:
						startingVelCrit = velCrit;
						self.skip = sk;
						
					# #plot this for looks
					# new_crit = 60;
					# 
					# isSaccade = self.filtered_velocities > new_crit;
					# #now plot the velocity data in an inset plot	
					# figure();ia = gca(); #ia = inset_axes(ax, width="30%", height="30%", loc=1); #set the inset axes as percentages of the original axis size
					# saccade_counter = 0; nr_saccades = 0;
					# for i,filt_vel,orig_vel,issac in zip(range(len(self.sample_times)),
					# 									 self.filtered_velocities, self.velocities, isSaccade):
					# 	#plot the eye trace
					# 	plot(i, orig_vel, color = 'gray', marker = '*', ms = 2.0, alpha = 0.5);
					# 	plot(i, filt_vel, color = 'red', marker = '*', ms = 2.0);  #
					# 
					# #plot the velocity trheshold and set labels
					# plot(linspace(0,len(self.sample_times),len(self.sample_times)), linspace(new_crit,new_crit+0.01,len(self.sample_times)), color = 'black', ls = 'dashed', lw = 1.0);
					# ia.set_ylabel('Velocity', fontsize = 14); ia.set_xlabel('Time', fontsize = 14); title('Velocity Profile', fontsize = 14);
					# 	
					# 1/0;	
					
					########## Here, plotting of eye traces occurs ############
					
					[endingVelCrit, nr_saccades] = self.plotSaccadeGetVelocity(startingVelCrit, completed);
					
					#save these values to the DataFrame
					df['skip_trial'].iloc[self.trial_nr-1] = self.skip;
					df['completed'].iloc[self.trial_nr-1] = 1;
					df['endingVelCrit'].iloc[self.trial_nr-1] = endingVelCrit;			
					
					#save the velocity threshold and the isSaccade truth vector to the array
					self.saccadeCriterion = endingVelCrit; #degrees/sec
					if self.saccadeCriterion == -1:
						self.isSaccade = [-1];
					self.nr_saccades = nr_saccades;
				
				############ End plotting of eye traces #################
				
				self.get_ET_data();
				self.get_picture_organzation();
				
				#print '\nDidnt look at any items: %s \n'%self.didntLookAtAnyItems;
				
			else:
				self.filtered_velocities = -1;
				self.skip = 1;
				self.isSaccade = [-1];
				self.saccadeCriterion = -1;
				self.nr_saccades = -1;
				#save these values to the DataFrame
				df['skip_trial'].iloc[self.trial_nr-1] = 1;
				df['completed'].iloc[self.trial_nr-1] = 1;
				df['endingVelCrit'].iloc[self.trial_nr-1] = -1;
	
	def get_picture_organzation(self):
		#standardized_eyetraces
		#determine and normalize all eye traces to assign alcohol to left, cigarette to top, and neutral to right
		#apply transformation to eye traces and then save it to the trial instance
		# Location coordinates:
		# Top (stim loc 1): 0, 6
		# Bottom right (stim loc 2): 5.1962, -3
		# Bottom left (stim loc 3): -5.1962, -3
		# radians difference: 2.0944 (120 degrees), 4.1889 (240 degrees)
		# what I want: alcohol = 'left', cigarette = 'top', neutral = 'right'
		# What I might have:
		# 1. alcohol = 'left', cigarette = 'top', neutral = 'right'
		# 2. alcohol = 'top', cigarette = 'left', neutral = 'right'
		# 3. alcohol = 'right', cigarette = 'top', neutral = 'left'
		# 4. alcohol = 'right', cigarette = 'left', neutral = 'top'
		# 5. alcohol = 'top', cigarette = 'right', neutral = 'left'
		# 6. alcohol = 'left', cigarette = 'right', neutral = 'top'
		
		#break it down by which location trial type it was and transform the eye traces accordingly
		# will need to rotate by 120 (alcohol in top) or 240 degrees (alcohol in right), by using the following:
		# xprime = x cos(theta) + y sin(theta) ; yprime = -x sin(theta) + y cos(theta), using radians

		
		if (self.alcohol_loc=='left')&(self.cigarette_loc=='up')&(self.neutral_loc=='right'):
			#trial type 1
			self.pre_transformed_picture_organiztion = 1;
			#self.post_transformed_picture_organiztion = 1;
			#self.transformedX = self.eyeX; self.transformedY = self.eyeY;
		elif (self.alcohol_loc=='up')&(self.cigarette_loc=='left')&(self.neutral_loc=='right'):		
			self.pre_transformed_picture_organiztion = 2;
		elif (self.alcohol_loc=='right')&(self.cigarette_loc=='up')&(self.neutral_loc=='left'):		
			self.pre_transformed_picture_organiztion = 3;
		elif (self.alcohol_loc=='right')&(self.cigarette_loc=='left')&(self.neutral_loc=='up'):		
			self.pre_transformed_picture_organiztion = 4;
		elif (self.alcohol_loc=='up')&(self.cigarette_loc=='right')&(self.neutral_loc=='left'):		
			self.pre_transformed_picture_organiztion = 5;
		elif (self.alcohol_loc=='left')&(self.cigarette_loc=='right')&(self.neutral_loc=='up'):		
			self.pre_transformed_picture_organiztion = 6;
		


	#define a function that takes a trial object and determines the proportion of time was looking at each item
	#this should find arrays of length(trial time) for each item/location, marking a 0 if not looking at that loc
	#and a 1 if it is. also should aggregate this together in a succint manner (e.g., proportion of trial spent looking at each item)
	#will call this in the Trial definition function			

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
			
		#and then assign the original arrays of direction
		self.lookedUp = lookedUp;
		self.lookedLeft = lookedLeft;
		self.lookedRight = lookedRight;
			
		#1.1 find the timepoints where the subject wasn't looking at any item and replace it with nan
		
		notLookingAtAnyItem = where((self.lookedAtAlcohol==0)&(self.lookedAtCigarette==0)&(self.lookedAtNeutral==0))[0]; #this is an array of indices where the overlap between arrays exists
		self.lookedAtAlcohol[notLookingAtAnyItem] = nan;
		self.lookedAtCigarette[notLookingAtAnyItem] = nan;
		self.lookedAtNeutral[notLookingAtAnyItem] = nan;
			
		#2. compute the amount and percentage of time spent looking at each item in each trial
		#THIS RESULTS IN EACH ARRAY HERE ONLY CORRESPONDING TO THE RELATIVE PROPORTION OF TIME SPENT LOOKING AT EACH ITEM WRT ALL TIME LOOKING AT AN ITEM
		
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
		
		# 5. Using the same (adjusted) analysis as above for the last item looked at, determine the FIRST item looked at within each trial
		if nansum(self.lookedAtAlcohol) == 0:
			earliestAlc = inf;
		else:
			earliestAlc = min(where(self.lookedAtAlcohol > 0)[0]);	
		if nansum(self.lookedAtCigarette) == 0:
			earliestCig = inf;
		else:
			earliestCig = min(where(self.lookedAtCigarette > 0)[0]);
		if nansum(self.lookedAtNeutral) == 0:	
			earliestNeu = inf;
		else:
			earliestNeu = min(where(self.lookedAtNeutral > 0)[0]);
			
		#get the ranking of the values. The first rank (1) will be the smallest value, and correspond to first item. 'max' ensures a tie will be 3, won't be picked up below
		ranks = stats.rankdata(array([earliestAlc, earliestCig, earliestNeu]), method = 'max');
				
		#conditional to determine which item had the lowest rank and thus latest time in the trial it was looked at
		if ranks[0] == 1:
			self.firstCategoryLookedAt = 'alcohol';
			self.firstItemLookedAt = self.presented_pics[where([name in alcohol_filenames for name in self.presented_pics])[0][0]];
			self.timeFirstItemLookedAt = self.sample_times[earliestAlc];
		elif ranks[1] == 1:
			self.firstCategoryLookedAt = 'cigarette';
			self.firstItemLookedAt = self.presented_pics[where([name in cigarette_filenames for name in self.presented_pics])[0][0]];
			self.timeFirstItemLookedAt = self.sample_times[earliestCig];
		elif ranks[2] == 1:
			self.firstCategoryLookedAt = 'neutral';
			self.firstItemLookedAt = self.presented_pics[where([name in neutral_filenames for name in self.presented_pics])[0][0]];
			self.timeFirstItemLookedAt = self.sample_times[earliestNeu];
		else:
			self.firstCategoryLookedAt = 'none';
			self.firstItemLookedAt = 'none';
			self.timeFirstItemLookedAt = -1;
			
		# if (self.sub_id=='cret03')&(self.block_nr==1)&(self.trial_nr == 10):	
		# 	1/0;			

	def plotSaccadeGetVelocity(self, startingVelCrit, completed=0):
		
		#completed is a boolean which determines if this trial had been completed previously. if so, then startingVelCrit will be the (already accepted) threshold
		
		## December 4 2018 - currently not plotting of setting velocity threshold for ech trial, instead sticking with 100 degrees / second threshold for all trials
		#plotting code is commented out
		# 
		# print; print "'a' = accept this trial, 'c' = crash, 's' = skip this trial"; print;
		# print ; print "To adjust threshold, just type new threshold: " ; print ;
		
		#must make this iterative to that I can adjust the velocity threshold until it is appropriate for this trial	
		new_crit = startingVelCrit;
		resp = 0; skip_trial = 0;
		
		while resp!=('a'):
			
			isSaccade = self.filtered_velocities > new_crit; #identify where a saccade was based on the velocity criterion     filtered
			if new_crit == -1:
				self.isSaccade = [-1]; #assign the isSaccade vector to be a -1 if there were no saccades made
			self.isSaccade = isSaccade; #append the isSaccade vector to the trial object
			
			#determine if I did this trial/block before. If so, need need to re-plot (takes too much time)
			if completed == 0:
				# # #plot the different saccades for the given trial for use in debugging	
				fig = figure(figsize = (11,7.5)); ax = gca(); ax.set_xlim([-display_size[0]/2,display_size[0]/2]); ax.set_ylim([-display_size[1]/2,display_size[1]/2]); #figsize = (12.8,7.64)
				ax.set_ylabel('Y Position, Degrees of Visual Angle',size=18); ax.set_xlabel('X Position, Degrees of Visual Angle',size=18,labelpad=11); hold(True);
				legend_lines = []; colors = ['red','green','blue','purple','orange','brown','grey','crimson','deepskyblue','lime','salmon','deeppink','lightsteelblue','palevioletred','azure','gold','yellowgreen',
											 'paleturquoise','darkorange', 'orchid', 'chocolate', 'yellow', 'lavender','indianred','bisque','olivedrab','seagreen','darkcyan','cadetblue',
											 'palevioletred','navy','blanchedalmond','tomato','saddlebrown','honeydew',
											 'indigo','lightpink','peru','slateblue', 'red','green','blue','purple','orange','brown','grey','crimson','deepskyblue','lime','salmon','deeppink','lightsteelblue','palevioletred','azure','gold','yellowgreen',
											 'paleturquoise','darkorange', 'orchid', 'chocolate', 'yellow', 'lavender','indianred','bisque','olivedrab','seagreen','darkcyan','cadetblue',
											 'palevioletred','navy','blanchedalmond','tomato','saddlebrown','honeydew',
											 'indigo','lightpink','peru','slateblue','red','green','blue','purple','orange','brown','grey','crimson','deepskyblue','lime','salmon','deeppink','lightsteelblue','palevioletred','azure','gold','yellowgreen',
											 'paleturquoise','darkorange', 'orchid', 'chocolate', 'yellow', 'lavender','indianred','bisque','olivedrab','seagreen','darkcyan','cadetblue',
											 'palevioletred','navy','blanchedalmond','tomato','saddlebrown','honeydew',
											 'indigo','lightpink','peru','slateblue'];
				#first plot the eye traces with respect to the velocity data
				#if the eye is in movements, use the color array above. otheriwse use black to denote fixation
				saccade_counter = 0; nr_saccades = 0;
				for i,xx,yy,issac in zip(range(len(self.sample_times)),
													 self.eyeX, self.eyeY, isSaccade):
					#plot the eye trace in black if not saccading
					if issac == 0:
						ax.plot(xx,yy, color = 'black', marker = 'o', ms = 4);
						#conditional to switch to the next saccade color
						#if the previous sample was saccading and now it isn't time for a swtch (add a number to saccades, switch the color for next time)
						if (isSaccade[i-1]==True)&(i>0):  					
							saccade_counter+=1;
							if saccade_counter > len(colors):
								saccade_counter=0;					
					else:
						ax.plot(xx, yy, color = colors[saccade_counter], marker = 'o', ms = 4);
						if (isSaccade[i-1]==False)&(i>0):  
							nr_saccades+=1;
							legend_lines.append(mlines.Line2D([],[],color=colors[saccade_counter],lw=6,alpha = 1.0, label='saccade  %s'%(nr_saccades)));
						
				ax.spines['right'].set_visible(False); ax.spines['top'].set_visible(False);
				ax.spines['bottom'].set_linewidth(2.0); ax.spines['left'].set_linewidth(2.0);
				ax.yaxis.set_ticks_position('left'); ax.xaxis.set_ticks_position('bottom');
				ax.legend(handles=[hand for hand in legend_lines],loc = 2,ncol=3,fontsize = 10); 
				title('Eye Trace and Position Velocity \nSubject %s, Block %s, Trial %s'%(self.sub_id, self.block_nr, self.trial_nr), fontsize = 22);
				
				#now plot the velocity data in an inset plot	
				ia = inset_axes(ax, width="30%", height="30%", loc=1); #set the inset axes as percentages of the original axis size
				saccade_counter = 0; nr_saccades = 0;
				for i,filt_vel,orig_vel,issac in zip(range(len(self.sample_times)),
													 self.filtered_velocities, self.velocities, isSaccade):
					#plot the eye trace in black if not saccading
					plot(i, orig_vel, color = 'gray', marker = '*', ms = 1.0, alpha = 0.5),
					if issac == 0:
						plot(i, filt_vel, color = 'black', marker = '*', ms = 1.5);  #
						#conditional to switch to the next saccade color
						#if the previous sample was saccading and now it isn't time for a swtch (add a number to saccades, switch the color for next time)
						if (isSaccade[i-1]==True)&(i>0):			
							saccade_counter+=1;
							if saccade_counter > len(colors):
								saccade_counter=0;
					else:
						plot(i, filt_vel, color = colors[saccade_counter], marker = '*', ms = 1.5); #filt_vel
						if (isSaccade[i-1]==False)&(i>0):  
							nr_saccades+=1;
				#plot the velocity trheshold and set labels
				plot(linspace(0,len(self.sample_times),len(self.sample_times)), linspace(new_crit,new_crit+0.01,len(self.sample_times)), color = 'red', ls = 'dashed', lw = 1.0);
				ia.set_ylabel('Velocity', fontsize = 14); ia.set_xlabel('Time', fontsize = 14); title('Velocity Profile', fontsize = 14);
				
				fig.text(0.7, 0.4, 'CURRENT VELOCITY \n THRESHOLD: %s deg/s'%(new_crit),size=16,weight='bold');
				
				resp = raw_input();	#wait for the button press to move to next trial				
				
			elif completed == 1:

				# no need to plot here, just slows everything down. RUn through and determine the nr of saccades
				saccade_counter = 0; nr_saccades = 0;
				for i,xx,yy,issac in zip(range(len(self.sample_times)),
													 self.eyeX, self.eyeY, isSaccade):
					#plot the eye trace in black if not saccading
					if issac == 0:
						foo = 'bar';			
					else:
						if (isSaccade[i-1]==False)&(i>0):  
							nr_saccades+=1;
		
				resp = 'a'; #move on if this trial was already completed
		
		# below here dictates what to do depending on the saccade threshold variable
		
			if resp.isdigit(): #adjust the threshold here
				new_crit = float(resp);
			elif resp == 'c':
				1/0;
			elif resp == 'a':
				endingVelCrit = new_crit;
			elif resp == 's':
				endingVelCrit = -1; #this is a flag for skipping this trial
				nr_saccades = -1;
				self.skip = 1;
				resp = 'a';
			else:
				new_crit = new_crit;
			
			close('all');
			
			#####endingVelCrit = startingVelCrit;
		return [endingVelCrit, nr_saccades];

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
	
	# #find each subjects' cue substance based on which item them chose more often during PAPC trials where they selected the alcohol or cigarette
	# if eyed=='subjective_resps':
	# 	subject_cues = [info[1] for info in subjective_prefs];
	# else:	
	# 	all_substances = [[tee.preferred_category for tee in subject if (((tee.preferred_category=='alcohol')|(tee.preferred_category=='cigarette'))&
	# 		(tee.dropped_sample == 0)&(tee.didntLookAtAnyItems == 0)&(tee.trial_type == 1))] for subject in trial_matrix]; #first get all the selected categories
	# 	prop_chose_alc = [sum([val == 'alcohol' for val in subject])/float(len([val == 'alcohol' for val in subject])) for subject in all_substances]; #now get proportion of time seleteced alcohol
	# 	prop_chose_cig = [sum([val == 'cigarette' for val in subject])/float(len([val == 'alcohol' for val in subject])) for subject in all_substances]; #then proportion of times selecting cigarette
	# 	#then find which proportion is greater and define whether that subject's cue is alcohol or cigarette
	# 	subject_cues = ['alcohol' if (a>c) else 'cigarette' for a,c in zip(prop_chose_alc,prop_chose_cig)];		
	# 
	# # #at some point store this data into a database/csv
	# 	
	# #calculate the temporal gaze profiles for each subset of rials: selected the cue, selected the not cue, and selected the neutral
	# #then for each of these subsets, find and plot the probability of looking at each item through the trial
	# for cue_or_not, selected_item in zip([1,0,0],['cue','not_cue','neutral']):
	# 	fig = figure(); ax1 = gca();
	# 	ax1.set_ylim(0.0, 1.0); ax1.set_yticks(arange(0,1.01,0.1)); ax1.set_xlim([0,1000]);
	# 	ax1.set_ylabel('Likelihood of fixating',size=18); ax1.set_xlabel('Time with respect to decision, ms',size=18,labelpad=11);
	# 	ax1.set_xticks([0,200,400,600,800,1000]);
	# 	ax1.set_xticklabels(['-1000','-800','-600','-400','-200','0']);
	# 	colors = ['red','blue', 'green']; alphas = [1.0, 1.0, 1.0]; legend_lines = [];		count = 0;
	# 	#define arrays for the neutral, cue, and not_cue items
	# 	neu_gaze_array = zeros(time_duration/time_bin_spacing);
	# 	neu_counts = zeros(shape(neu_gaze_array));
	# 	neu_subject_means_array = [[] for i in range(1000)]; #use this to store each individual subjects' mean for each time point			
	# 	cue_gaze_array = zeros(time_duration/time_bin_spacing);
	# 	cue_counts = zeros(shape(cue_gaze_array));
	# 	cue_subject_means_array = [[] for i in range(1000)]; 		
	# 	not_cue_gaze_array = zeros(time_duration/time_bin_spacing);
	# 	not_cue_counts = zeros(shape(not_cue_gaze_array));
	# 	not_cue_subject_means_array = [[] for i in range(1000)]; 		
	# 	for subj,cue in zip(trial_matrix, subject_cues):
	# 		neu_individ_subject_sum = zeros(time_duration/time_bin_spacing);
	# 		neu_individ_subject_counts = zeros(time_duration/time_bin_spacing);
	# 		cue_individ_subject_sum = zeros(time_duration/time_bin_spacing);
	# 		cue_individ_subject_counts = zeros(time_duration/time_bin_spacing);
	# 		not_cue_individ_subject_sum = zeros(time_duration/time_bin_spacing);
	# 		not_cue_individ_subject_counts = zeros(time_duration/time_bin_spacing);	
	# 		for t in subj:
	# 			#conditional to differentiate between not-cue trials when selecteing the non-cue or not
	# 			#the second conditional include nuetral trials that were preferred only
	# 			if ((selected_item=='cue')|(selected_item=='not_cue')):
	# 				if ((t.dropped_sample == 0)&(t.didntLookAtAnyItems == 0)&((t.trial_type == 1)==1)&((t.preferred_category == cue)==cue_or_not)&((t.preferred_category == 'alcohol')|(t.preferred_category == 'cigarette'))):
	# 					#neutral is always the same...
	# 					#cycle through each time point, going backward through the array (e.g., -1, -2..) and aggregating the data accordingly
	# 					for i in (arange(1000)+1):
	# 						if (i>len(t.lookedAtNeutral)):
	# 							continue;
	# 						elif (isnan(t.lookedAtNeutral[-i])):
	# 							continue;
	# 						neu_gaze_array[-i] += t.lookedAtNeutral[-i];
	# 						neu_counts[-i] += 1;
	# 						#put the individual subject data together
	# 						neu_individ_subject_sum[-i] += t.lookedAtNeutral[-i];
	# 						neu_individ_subject_counts[-i] += 1;
	# 					if cue=='alcohol':
	# 						for i in (arange(1000)+1):
	# 							if (i>len(t.lookedAtAlcohol)):
	# 								continue;
	# 							elif (isnan(t.lookedAtAlcohol[-i])):
	# 								continue;
	# 							#store the alcohol gaze patterns as the cue item
	# 							cue_gaze_array[-i] += t.lookedAtAlcohol[-i];
	# 							cue_counts[-i] += 1;
	# 							#put the individual subject data together
	# 							cue_individ_subject_sum[-i] += t.lookedAtAlcohol[-i];
	# 							cue_individ_subject_counts[-i] += 1;
	# 							
	# 							#and store the cigarette items as the not_cue item
	# 							not_cue_gaze_array[-i] += t.lookedAtCigarette[-i];
	# 							not_cue_counts[-i] += 1;
	# 							#put the individual subject data together
	# 							not_cue_individ_subject_sum[-i] += t.lookedAtCigarette[-i];
	# 							not_cue_individ_subject_counts[-i] += 1;
	# 						
	# 					elif cue=='cigarette':
	# 						for i in (arange(1000)+1):
	# 							if (i>len(t.lookedAtAlcohol)):
	# 								continue;
	# 							elif (isnan(t.lookedAtAlcohol[-i])):
	# 								continue;							
	# 							#store the cigarette items as the not_cue item
	# 							cue_gaze_array[-i] += t.lookedAtCigarette[-i];
	# 							cue_counts[-i] += 1;
	# 							#put the individual subject data together
	# 							cue_individ_subject_sum[-i] += t.lookedAtCigarette[-i];
	# 							cue_individ_subject_counts[-i] += 1;							
	# 
	# 							#and store the alcohol gaze patterns as the cue item
	# 							not_cue_gaze_array[-i] += t.lookedAtAlcohol[-i];
	# 							not_cue_counts[-i] += 1;
	# 							#put the individual subject data together
	# 							not_cue_individ_subject_sum[-i] += t.lookedAtAlcohol[-i];
	# 							not_cue_individ_subject_counts[-i] += 1;
	# 							
	# 			if (selected_item=='neutral'):
	# 				if ((t.dropped_sample == 0)&(t.didntLookAtAnyItems == 0)&((t.trial_type == 1)==1)&((t.preferred_category == cue)==cue_or_not)&(t.preferred_category == 'neutral')):
	# 					#neutral is always the same...
	# 					#cycle through each time point, going backward through the array (e.g., -1, -2..) and aggregating the data accordingly
	# 					for i in (arange(1000)+1):
	# 						if (i>len(t.lookedAtNeutral)):
	# 							continue;
	# 						elif (isnan(t.lookedAtNeutral[-i])):
	# 							continue;
	# 						neu_gaze_array[-i] += t.lookedAtNeutral[-i];
	# 						neu_counts[-i] += 1;
	# 						#put the individual subject data together
	# 						neu_individ_subject_sum[-i] += t.lookedAtNeutral[-i];
	# 						neu_individ_subject_counts[-i] += 1;
	# 					if cue=='alcohol':
	# 						for i in (arange(1000)+1):
	# 							if (i>len(t.lookedAtAlcohol)):
	# 								continue;
	# 							elif (isnan(t.lookedAtAlcohol[-i])):
	# 								continue;
	# 							#store the alcohol gaze patterns as the cue item
	# 							cue_gaze_array[-i] += t.lookedAtAlcohol[-i];
	# 							cue_counts[-i] += 1;
	# 							#put the individual subject data together
	# 							cue_individ_subject_sum[-i] += t.lookedAtAlcohol[-i];
	# 							cue_individ_subject_counts[-i] += 1;
	# 							
	# 							#and store the cigarette items as the not_cue item
	# 							not_cue_gaze_array[-i] += t.lookedAtCigarette[-i];
	# 							not_cue_counts[-i] += 1;
	# 							#put the individual subject data together
	# 							not_cue_individ_subject_sum[-i] += t.lookedAtCigarette[-i];
	# 							not_cue_individ_subject_counts[-i] += 1;
	# 						
	# 					elif cue=='cigarette':
	# 						for i in (arange(1000)+1):
	# 							if (i>len(t.lookedAtAlcohol)):
	# 								continue;
	# 							elif (isnan(t.lookedAtAlcohol[-i])):
	# 								continue;							
	# 							#store the cigarette items as the not_cue item
	# 							cue_gaze_array[-i] += t.lookedAtCigarette[-i];
	# 							cue_counts[-i] += 1;
	# 							#put the individual subject data together
	# 							cue_individ_subject_sum[-i] += t.lookedAtCigarette[-i];
	# 							cue_individ_subject_counts[-i] += 1;							
	# 
	# 							#and store the alcohol gaze patterns as the cue item
	# 							not_cue_gaze_array[-i] += t.lookedAtAlcohol[-i];
	# 							not_cue_counts[-i] += 1;
	# 							#put the individual subject data together
	# 							not_cue_individ_subject_sum[-i] += t.lookedAtAlcohol[-i];
	# 							not_cue_individ_subject_counts[-i] += 1;								
	# 							
	# 						
	# 		neu_individ_subject_mean = neu_individ_subject_sum/neu_individ_subject_counts; #calculate the mean for this subject at each time point
	# 		[neu_subject_means_array[index].append(ind_mew) for index,ind_mew in zip(arange(1000),neu_individ_subject_mean)]; #append this to the array for each subject   			
	# 		cue_individ_subject_mean = cue_individ_subject_sum/cue_individ_subject_counts; #calculate the mean for this subject at each time point
	# 		[cue_subject_means_array[index].append(ind_mew) for index,ind_mew in zip(arange(1000),cue_individ_subject_mean)]; #append this to the array for each subject
	# 		not_cue_individ_subject_mean = not_cue_individ_subject_sum/not_cue_individ_subject_counts; #calculate the mean for this subject at each time point
	# 		[not_cue_subject_means_array[index].append(ind_mew) for index,ind_mew in zip(arange(1000),not_cue_individ_subject_mean)]; #append this to the array for each subject   					
	# 						
	# 	#plot each likelihood looking at items				
	# 	for  subj_ms, cue_name, c, a in zip([cue_subject_means_array, not_cue_subject_means_array, neu_subject_means_array], ['cue','not_cue','neutral'], colors, alphas):							
	# 		mews = array([nanmean(subj) for subj in subj_ms]); # gaze_array/counts
	# 		sems = array([compute_BS_SEM(subj) for subj in subj_ms]);
	# 		ax1.plot(linspace(0,1000,1000), mews, lw = 4.0, color = c, alpha = a);
	# 		#plot the errorbars
	# 		#for x,m,s in zip(linspace(0,1000,1000),mews,sems):
	# 		ax1.fill_between(linspace(0,1000,1000), mews-sems, mews+sems, color = c, alpha = a*0.4);
	# 		legend_lines.append(mlines.Line2D([],[],color=c,lw=6,alpha = a, label='likelihood(looking at %s) '%cue_name));
	# 	#plot the sum of each fora sanity emasure to ensure they equate to one
	# 	agg = [(nanmean(a)+nanmean(b)+nanmean(c)) for a,b,c in zip(cue_subject_means_array, not_cue_subject_means_array, neu_subject_means_array)];
	# 	ax1.plot(linspace(0,1000,1000),agg,color = 'gray', lw = 3.0);
	# 	legend_lines.append(mlines.Line2D([],[],color='gray',lw=4, alpha = 1.0, label='sum of all'));
	# 	ax1.plot(linspace(0,1000,1000),linspace(0.33,0.333,1000),color = 'gray', lw = 3.0, ls='dashed');
	# 	legend_lines.append(mlines.Line2D([],[],color='gray',lw=4, alpha = 1.0, ls = 'dashed', label='random'));	
	# 	ax1.spines['right'].set_visible(False); ax1.spines['top'].set_visible(False);
	# 	ax1.spines['bottom'].set_linewidth(2.0); ax1.spines['left'].set_linewidth(2.0);
	# 	ax1.yaxis.set_ticks_position('left'); ax1.xaxis.set_ticks_position('bottom');
	# 	ax1.legend(handles=[legend_lines[0],legend_lines[1], legend_lines[2], legend_lines[3], legend_lines[4]],loc = 2,ncol=1,fontsize = 11); #, legend_lines[2]
	# 	title('Average Temporal Gaze Profile, \n Chose %s Trials'%(selected_item), fontsize = 22);
	# show();
	# 
	
## Commetns about transformations for displays to try and aggregate eye positions all together (heat maps)	
	#apply transformation to eye traces and then save it to the trial instance
	# Location coordinates:
	# Top (stim loc 1): 0, 6
	# Bottom right (stim loc 2): 5.1962, -3
	# Bottom left (stim loc 3): -5.1962, -3
	# radians difference: 2.0944 (120 degrees), 4.1889 (240 degrees)
	# what I want: alcohol = 'left', cigarette = 'top', neutral = 'right'
	# What I might have:
	# 1. alcohol = 'left', cigarette = 'top', neutral = 'right'
	# 2. alcohol = 'top', cigarette = 'left', neutral = 'right'
	# 3. alcohol = 'right', cigarette = 'top', neutral = 'left'
	# 4. alcohol = 'right', cigarette = 'left', neutral = 'top'
	# 5. alcohol = 'top', cigarette = 'right', neutral = 'left'
	# 6. alcohol = 'left', cigarette = 'right', neutral = 'top'
	
	#break it down by which location trial type it was and transform the eye traces accordingly
	# will need to rotate by 120 (alcohol in top) or 240 degrees (alcohol in right), by using the following:
	# xprime = x cos(theta) + y sin(theta) ; yprime = -x sin(theta) + y cos(theta), using radians	