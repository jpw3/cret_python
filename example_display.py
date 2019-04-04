#Designed to create an example eye trace display with pictures of the items and the the eye trace overlaid
#need to have already imported the data with the use of cret_analysis.py
#Check to see if the trial type is high_pref or not.. I won't be upset if using a differnt one, just want to know

#import the matplotlib image reading packagae
from pylab import *
import matplotlib.image as mpimg


#Specify the paths of the pictures
picpath = '/Users/jameswilmott/Documents/MATLAB/CRET/pictures'; #Then it's /alcohol, /cigarettes, /neutral... /completed/ %name%_grayscaled_resized.png
figurepath = '/Users/jameswilmott/Documents/Python/CRET/figures/';

#specify display related information
display_size = array([22.80, 17.10]); #width, height of the screen used to present the images in degrees of visual angle
image_size = array([6,6]); #width, and height of the presented images in degress of visual angle
left_pic_coors = array([-5.20,-3.0]); #in dva
right_pic_coors = array([5.20,-3]);
up_pic_coors = array([0,6]);

#Using subject cret18, block 1, trial 6 (trial type = highc higha)

#Take the trial (denoted as t), which should have already been partitioned out
#get the relevant data

presented_up = t.presented_up; #alcohol
presented_right = t.presented_right; #neutral
presented_left = t.presented_left; #cigarette

eyeX = t.eyeX;
eyeY = t.eyeY;

#import the pictures
up = mpimg.imread(picpath +'/alcohol/completed/' + presented_up + '_grayscaled_resized.png');
right = mpimg.imread(picpath +'/neutral/completed/' + presented_right + '_grayscaled_resized.png');
left = mpimg.imread(picpath +'/cigarettes/completed/' + presented_left + '_grayscaled_resized.png');

# Create the figure
fig = figure(figsize = (11,7.5)); ax = gca(); ax.set_xlim([-display_size[0]/2,display_size[0]/2]); ax.set_ylim([-display_size[1]/2,display_size[1]/2]);
#make the whole background of figure gray
ax.set_facecolor('lightgrey');
ax.plot(eyeX, eyeY, color = 'red', lw = 5);

savefig(figurepath+'ORIGINSTARTTRIALS_second_saccade_data_subj_%s.png'%(t.sub_id))

1/0

## Now incorporating the pictures of items offline in adobe illustrator

#add up picture first
fig.figimage(up, xo = up_pic_coors[0], yo = up_pic_coors[1], zorder = 3); #, cmap = 'Greys'