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

datapath = '/Users/jameswilmott/Documents/MATLAB/data/CRET/'; #
savepath =  '/Users/jameswilmott/Documents/Python/CRET/data/';  # #/'/Users/james/Documents/Python/CRET/data/';  # 
shelvepath =  '/Users/jameswilmott/Documents/Python/CRET/data/'; # # #  #'/Users/james/Documents/Python/CRET/data/'; # 
figurepath = '/Users/jameswilmott/Documents/Python/CRET/figures/'; # #'/Users/james/Documents/Python/CRET/figures/'; #


# datapath = '/Volumes/WORK_HD/data/CRET/'; #'/Users/jameswilmott/Documents/MATLAB/data/CRET/'; #
# savepath =  '/Volumes/WORK_HD/code/Python/CRET/data/'; #'/Users/jameswilmott/Documents/Python/CRET/data/';  # #/'/Users/james/Documents/Python/CRET/data/';  # 
# shelvepath =  '/Volumes/WORK_HD/code/Python/CRET/data/'; #'/Users/jameswilmott/Documents/Python/CRET/data/'; # # #  #'/Users/james/Documents/Python/CRET/data/'; # 
# figurepath = '/Volumes/WORK_HD/code/Python/CRET/figures/'; #'/Users/jameswilmott/Documents/Python/CRET/figures/'; # #'/Users/james/Documents/Python/CRET/figures/'; #

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
## Data Analysis Methods ##
############################################