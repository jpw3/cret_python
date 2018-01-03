#Data anlaysis code for CRET study collaboration with CAAS
#Author: James Wilmott, Fall/Winter 2017-18

from pylab import *
from scipy.io import loadmat #used to load .mat files in as dictionaries
from scipy import stats
from glob import glob #for use in searching for/ finding data files
import random #general purpose
import pandas as pd
import math

############################################
## Specify some universal parameters ##
############################################

datapath = '/Users/jameswilmott/Documents/MATLAB/data/CRET/'; #'/Users/james/Documents/MATLAB/data/CRET/'; #
savepath =  '/Users/jameswilmott/Documents/Python/CRET/data/';  #'/Users/james/Documents/Python/CRET/data/'; # 

ids=['cret01','cret03','cret04','cret05','cret06','cret07','cret08','cret09','cret10','cret11'];

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

############################################
## Data Analysis ##
############################################













############################################
## Data Importing Methods ##
############################################

#define a function to import individual .mat data files
def loadBlock(subid,block_type,block_nr):
	#returns a single Block object corresponding to the block number and subject id
	#block type should be a string corresponding to the task type(e.g. 'Discrim')
	filename = glob(datapath+'%s'%subid+'/'+'*_%s_%d.mat'%(subid,block_nr)); #Not sure if this regex will work here, must check
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
		
		self.get_ET_data(); #call this method... see if it works
		
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
			
		#2. compute the amount and percentage of time spent looking at each item in each trial
		
		self.timeLookingAtAlcohol = sum(self.lookedAtAlcohol);
		self.percentageTimeLookingAtAlcohol = sum(self.lookedAtAlcohol)/float(len(self.lookedAtAlcohol));		
		self.timeLookingAtCigarette = sum(self.lookedAtCigarette);
		self.percentageTimeLookingAtCigarette = sum(self.lookedAtCigarette)/float(len(self.lookedAtCigarette));
		self.timeLookingAtNeutral = sum(self.lookedAtNeutral);
		self.percentageTimeLookingAtNeutral = sum(self.lookedAtNeutral)/float(len(self.lookedAtNeutral));
		
		#3. assign the array and stats that corresponded to the chosen item to a unique array	
			
		if self.preferred_item in alcohol_filenames:
			self.lookedAtPreferred = self.lookedAtAlcohol;
			self.timeLookingAtPreferred = self.timeLookingAtAlcohol;
			self.percentageTimeLookingAtPreferred = self.percentageTimeLookingAtAlcohol;
		elif self.preferred_item in cigarette_filenames:
			self.lookedAtPreferred = self.lookedAtCigarette;
			self.timeLookingAtPreferred = self.timeLookingAtCigarette;
			self.percentageTimeLookingAtPreferred = self.percentageTimeLookingAtCigarette;
		elif self.preferred_item in neutral_filenames:
			self.lookedAtPreferred = self.lookedAtNeutral;			
			self.timeLookingAtPreferred = self.timeLookingAtNeutral;
			self.percentageTimeLookingAtPreferred = self.percentageTimeLookingAtNeutral;
			
		#4. Determine which item was looked at last (alcohol, neutral, or cigarette)
			
			
			
