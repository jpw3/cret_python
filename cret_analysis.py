#Data anlaysis code for CRET study collaboration with CAAS
#Author: James Wilmott, Winter 2017

from pylab import *
from scipy.io import loadmat #used to load .mat files in as dictionaries
from scipy import stats
from glob import glob #for use in searching for/ finding data files
import random #general purpose
import pandas as pd

datapath = '/Users/james/Documents/MATLAB/data/CRET/'; #
savepath =  '/Users/james/Documents/Python/CRET/data/';

ids=['cret01','cret03','cret04','cret05'];

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
def getAllSubjectBlocks(ids):
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
		self.trials = [trial(trialData,self.block_type,self.sub_id) for trialData in  matStructure.trial_data];

#define a Trial object that will hold the individual trial data 
class trial(object):
	#object being passed into this Trial instance should be a dictionary corresponding to the trial data for this given trial
	def __init__(self, trialData, block_type, sub_id):
		self.sub_id = saved_id;
		self.block_nr = trialData.block_nr;
		self.trial_nr = trialData.trial_nr;
		self.trial_type = trialData.trial_type; #determines the pictures that were presented
		self.response_time = trialData.trial_times.response_time*1000; #put reaction time into seconds
		self.alcohol_pref = trialData.alcohol_pref;
		self.cigarette_pref = trialData.cigarette_pref;
		self.presented_pics = trialData.corresponding_names;
		self.picture_order = trialData.picture_ordering;
		self.presented_up = trialData.presented_up;
		self.presented_left = trialData.presented_left;
		self.presented_right = trialData.presented_right;		
		#response and results
		self.reponse = str(trialData.response); #letter corresponding to presented
		self.selected_type = trialData.selected_type; 
		self.preferred_item = trialData.preferred_item;
		#finally, eye position and pupil size information
		self.eyeX = trialData.eyeX;
		self.eyeY = trialData.eyeY;
		self.p_size = trialData.pSize;
		self.sample_times = trialData.sampleTimes;
		self.drift_shift = trialData.drift_shift;