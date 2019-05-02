#This script is to hold additional code that is no longer being used in the cret_analysis.py script
#This code may be helpful or useful in the future, but I am not currently using it and so I'm de-cluttering the analysis file


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

# def collectTemporalGazeProfileTrialsRawTimecourseStimOnsetAligned(blocks, ttype, eyed = 'agg'):
# 	#collects each participants' trial data where they didn't blink or look down
# 	#this collects trial with respect to the onset of the stimulus display
#     #this collects time points according to their raw time course, rather than normalized to 100 equally spaced time points
# 	#loop through and get all the trials for each subject
#     trial_matrix = [[tee for b in bl for tee in b.trials if (tee.skip==0)] for bl in blocks];
# 	
# 	#collect which trial type to run this analysis for
# 	#ttype = int(raw_input('Which trial type? 1 = HighC/HighA, 2 = HighC/LowA, 3 = LowC/HighA, 4 = LowC/LowA: '));
# 	
#     name = ['high_pref', 'highC_lowA','lowC_highA','lowC_lowA'][ttype-1];
# 	
#     data = pd.DataFrame(columns = concatenate([['subject_nr', 'trial_type', 'selected_item','block_nr','trial_nr','first_sac_latency','first_sac_item','last_sac_item','nr_dwells','prev_trial_last_dwelled_loc','prev_trial_type','prev_choice'] \
#         ,['t_%s'%(t) for t in linspace(1,10000,10000)]])); #add all participants together to the same dataFrame for simplicty
#     #maximum length of trial across all participants is ~9.5 seconds, so adding up to 100000 data points to include all time points        
# 	#SCORING FOR ITEM (entry at t_XX): 0 = not looked at any item, 1 = looked at alcohol, 2 = looked at cigarette, 3 = looked at neutral, nan = timepoint didn't exist in the trial
#     trial_index_counter = 0;
# 
#     for subj_nr,subj in zip(ids, trial_matrix):    #enumerate(trial_matrix):
# 
#         for i,t in enumerate(subj):
# 			#conditional to differentiate between trials that should be skipped for this trial type, etc.
#             if((t.dropped_sample == 0)&(t.didntLookAtAnyItems == 0)&(t.trial_type == ttype)&(t.skip == 0)&(sqrt(t.eyeX[0]**2 + t.eyeY[0]**2) < 2.5)):
#                 
#                 if (t.nr_saccades > 0):  #this conditional is used to ensure that no trials without saccades sneak through
#                 
#                     #0. first, get first saccade latency, first saccade item identity, nr of dwells on current trial
#                     #need the first saccade latency before collecting the gaze data, otherwise I can't align the data according to the first saccade onset
# 
#                     #this code gets the first saccade latency
#                     sac_start_time = 0;
#                     sac_start_pos = array([]);						
#                     sac_end_time = 0;
#                     sac_end_pos = array([]);
#                     
#                     #Below here goes through each trial and pulls out the first saccde
#                     # the while loop below runs through until a saccade is found (saccade_counter = 1) or
#                     # we get to the end of the trial
#                     
#                     saccade_counter = 0;
#                     
#                     for ii,xx,yy,issac in zip(range(len(t.sample_times)),
#                                                          t.eyeX, t.eyeY, t.isSaccade):
#                         #if no saccade has been made yet, keep running through the isSaccade array
#                         # issac < 1 will be zero at all non-saccading time points, including the start
#                         if issac == 0:
#                             #if the previous sample was saccading and now it isn't, the first saccade is complete and we can grab the data
#                             if (t.isSaccade[ii-1]==True)&(ii>0):
#                                 sac_end_time = t.sample_times[ii];
#                                 sac_end_pos = array([xx,yy]);
#                                 saccade_counter+=1;
#                                 break; #once I get the first saccade, end it here
#                             
# 
#                                 
#                         elif issac == 1:
#                             #get the starting point for this saccade as well as the time
#                             #the first transition between 0 and 1 will be the first saccade start
#                             if (t.isSaccade[ii-1]==False)&(ii>0)&(saccade_counter==0):
#                                 sac_start_time = t.sample_times[ii];
#                                 sac_start_pos = array([xx,yy]);       
#                     
#                     #calculate the first saccade latency
#                     first_sac_onset_latency = sac_start_time; 
# 
#                     #get the first item looked at			
#                     if t.firstCategoryLookedAt=='alcohol':
#                         first_sac_item_identity = 1;
#                     elif t.firstCategoryLookedAt=='cigarette':
#                         first_sac_item_identity = 2;
#                     elif t.firstCategoryLookedAt=='neutral':
#                         first_sac_item_identity = 3;
# 
#                     #get the last item looked at
#                     if t.lastCategoryLookedAt=='alcohol':
#                         last_sac_item_identity = 1;
#                     elif t.lastCategoryLookedAt=='cigarette':
#                         last_sac_item_identity = 2;
#                     elif t.lastCategoryLookedAt=='neutral':
#                         last_sac_item_identity = 3;						
# 
#                     #now here collect the total number of dwells
#                     rexp_pattern = re.compile(r'01'); #this regular expression pattern looks for strings with a 1 or anything continuous run of 1s
# 					#In the computation of the lookedAtXX arrays during trial pre-processing, I include NaNs at times when no itm
# 					#was looked at... e.g., when the participant was fixating the center of the screen.
# 					#In order to ensure that I capture the change from not looking at one item to looking at any item (like the first dwell),
# 					#I need to convert those NaNs to 0's for calculation using the string-based method below. However, I want the original
# 					#lookedAtXX arrays to maintain the Nan, 0, 1 coding scheme, so I'll create holder arrays for each trial to use for the nr of dwell
# 					#calculations here
# 					
#                     looked_at_alcohol = array([r if ((r==0)|(r==1)) else 0 for r in t.lookedAtAlcohol]);
#                     looked_at_cigarette = array([r if ((r==0)|(r==1)) else 0 for r in t.lookedAtCigarette]);
#                     looked_at_neutral = array([r if ((r==0)|(r==1)) else 0 for r in t.lookedAtNeutral]);
# 					
#                     total_holder = 0;
# 					
#                     str_alc = ''.join(str(int(g)) for g in looked_at_alcohol if not(isnan(g))); #first get the array into a string
#                     run_lengths_alc = [len(f) for f in rexp_pattern.findall(str_alc)];
# 					#line above, then use the regular expression pattern, looking for 1s, to parse an array of the continuous runs of 1s in the string from above and get length
#                     nr_fixs = sum([1 for r in run_lengths_alc]);
# 					#check if the first item is a 1... if so, the array started with looking at the item and it wouldnt be caught by the regexp.
# 					#this will only be the case if they weren't looking at anything to start (e.g., there were nan's to start, then the first item was looked at)
# 					#notice that because I have included NaNs in the t.lookedAtXX arrays for when items are not being looked at, the subsequent str_alc array
# 					#represents sequences of 1s and 0 s corresponding runs of looking at items, squished into the array; This means str_alc does not include
# 					#any information about samples where the eye was not on an item, which means this method cannot be used to understand differences in time between
# 					#dwells when that time is not being spent on an item. This is important to keep in mind
#                     if str_alc[0]=='1':
#                         nr_fixs +=1;
# 				
#                     total_holder+=nr_fixs; #add the nr of dwells from looking at alc to this holder variable
# 					
#                     str_cig = ''.join(str(int(g)) for g in looked_at_cigarette if not(isnan(g))); #parse cigarette
#                     run_lengths_cig = [len(f) for f in rexp_pattern.findall(str_cig)];
#                     nr_fixs = sum([1 for r in run_lengths_cig]);
# 					#check if the first item is a 1... if so, the array started with looking at the item and it wouldnt be caught by the regexp. need to correcy
#                     if str_cig[0]=='1':
#                         nr_fixs +=1;
# 
#                     total_holder+=nr_fixs; #add the nr of dwells from looking at cig to this holder variable
# 
#                     str_neu = ''.join(str(int(g)) for g in looked_at_neutral if not(isnan(g))); #do the parsing for neutral..
#                     run_lengths_neu = [len(f) for f in rexp_pattern.findall(str_neu)];
#                     nr_fixs = sum([1 for r in run_lengths_neu]);
# 					#check if the first item is a 1... if so, the array started with looking at the item and it wouldnt be caught by the regexp. need to correcy
#                     if str_neu[0]=='1':
#                         nr_fixs +=1;
# 
#                     total_holder+=nr_fixs; #add the nr of dwells from looking at neu to this holder variable
# 					
#                     total_nr_dwells = total_holder; #this is the variable for collecting total nr of dwells on this trial               
#                     
# 
#                     #1. get the previous trial last dwelled location and previous trial type
#                     #conditional here is to only compute these values if this was not the first trial in a block. If it was, add nan's to these values
#                     
#                     if t.trial_nr > 1:
#                         #this code below finds the location of the last dwell on trial N-1 a
# 						prev_looked_at_up = array([r if ((r==0)|(r==1)) else 0 for r in subj[i-1].lookedUp]);
# 						prev_looked_at_left = array([r if ((r==0)|(r==1)) else 0 for r in subj[i-1].lookedLeft]);
# 						prev_looked_at_right = array([r if ((r==0)|(r==1)) else 0 for r in subj[i-1].lookedRight]);			
#         
# 						str_up = ''.join(str(int(g)) for g in prev_looked_at_up if not(isnan(g))); #first get the array into a string
#         
#                         #get last instane of the '1' in this array. if never loooked at, will return a -1
# 						up_indices = str_up.rfind('1'); #rfind searches the string from right to left
#                         
# 						if isinstance(up_indices, int):
# 							up_last_index_lookedat = up_indices;
# 						else:
# 							up_last_index_lookedat = up_indices[0];
#                             
# 						str_left = ''.join(str(int(g)) for g in prev_looked_at_left if not(isnan(g))); #parse cigarette
# 						left_indices = str_left.rfind('1');		
# 						if isinstance(left_indices, int):
# 							left_last_index_lookedat = left_indices;
# 						else:
# 							left_last_index_lookedat = left_indices[0];
#         
# 						str_right = ''.join(str(int(g)) for g in prev_looked_at_right if not(isnan(g))); #do the parsing for neutral..
# 						right_indices = str_right.rfind('1');		
# 						if isinstance(right_indices, int):
# 							right_last_index_lookedat = right_indices;
# 						else:
# 							right_last_index_lookedat = right_indices[0];
#                         
# 						last_instances =  array([up_last_index_lookedat, left_last_index_lookedat, right_last_index_lookedat]); #always keep it up, left, right
# 						last_item_index = where(last_instances == max(last_instances))[0][0];		
#         
#                         #conditonal to find the last item that was looked at accoridng to the index corresponding to the item 
# 						if last_item_index==0:
# 							prev_last_dwelled_item = 'up';
# 						elif last_item_index==1:
# 							prev_last_dwelled_item = 'left';
# 						elif last_item_index== 2:
# 							prev_last_dwelled_item = 'right';
#                             
# 						previous_trial_type = subj[i-1].trial_type; #get the previous trial type
# 						
# 						if subj[i-1].preferred_category=='alcohol':
# 							previous_choice = 1;
# 						elif subj[i-1].preferred_category=='cigarette':
# 							previous_choice = 2;
# 						elif subj[i-1].preferred_category=='neutral':
# 							previous_choice = 3;    						                       
#                     else:
#                         prev_last_dwelled_item = nan;
#                         previous_trial_type = nan;
#                         previous_choice = nan;
# 
#                     #2. now finally get the gaze position information, aligning trials to the onset of the stimulus
#                     #keep the start of the array nans until the timepoint when the trial has data for it
#                     gaze_data = [nan for ja in range(10000)]; #this will be length 10000 and include each item looked at at each time point (or 0/NaN otherwise); pre-allocate with nans                    
#                     trial_end_index = len(t.lookedAtNeutral); #get the duration of the trial (e.g., how many samples, corresponding to how many milliseconds)
#     
#                     #trials longer than 10000 ms will be trimmed to 10000 ms
#                     if trial_end_index > 10000:
#                         trial_end_index = 10000;
#                     
#                     iterator = 0; 
#                     #now go through for the 10000 time points prior to decision and score whether the paricipants was looking at 
#                     for j in (arange(10000)):
#                         if ((j)>=trial_end_index):
#                             continue;					
#                         elif (isnan(t.lookedAtNeutral[j]) & isnan(t.lookedAtAlcohol[j]) & isnan(t.lookedAtCigarette[j])):
#                             #at this point, there was a nan inserted because the participant did not look at each item
#                             #when there are no items looked at, include a 0
#                             gaze_data[iterator] = 0;
#                         elif (t.lookedAtAlcohol[j]==1):
#                             gaze_data[iterator] = 1;
#                         elif (t.lookedAtCigarette[j]==1):						
#                             gaze_data[iterator] = 2;						
#                         elif (t.lookedAtNeutral[j]==1):	
#                             gaze_data[iterator] = 3;
#                         iterator+=1;
#                         
#                     #for ease of the regression computation, get the selected item into a numerical representation, same mapping as with item looked at
#                     if t.preferred_category=='alcohol':
#                         selected_item = 1;
#                     elif t.preferred_category=='cigarette':
#                         selected_item = 2;
#                     elif t.preferred_category=='neutral':
#                         selected_item = 3;                                  
#                         
#                     #at this point have collected data for gaze profile together
#                     #get all data points together for ease of incorporating into the dataFrame
#                     this_trials_data = concatenate([[subj_nr, ttype, selected_item, t.block_nr, t.trial_nr, first_sac_onset_latency, first_sac_item_identity, last_sac_item_identity, \
#                                                      total_nr_dwells, prev_last_dwelled_item, previous_trial_type, previous_choice],gaze_data]); #each trial variable, then each timepoint data   int(subj_nr+1)
# 
# 					
#                     #now translate this to the dataframe for this participant
#                     data.loc[trial_index_counter] = this_trials_data;
# 			
#                     trial_index_counter += 1; #1/0; #index for next trial
#                     
# 	print "completed subject %s.. \n\n"%subj_nr	
# 
# 	#save the database
#     data.to_csv(savepath+'/stim_locked/'+'%s_trialdata_STIMLOCKED.csv'%name,index=False); 
# 	#data.to_csv(savepath+'/stim_locked/'+'%s_trialdata.csv'%name,index=False); #previous iteration of this was to align to the onset of the stimulus
# 	# ends here                    
#                     
# 
# 
# def collectTemporalGazeProfileTrialsRawTimecourse(blocks, ttype, eyed = 'agg'):
# 	#collects each participants' trial data where they didn't blink or look down
# 	#this collects trial with respect to the onset of the first saccade
#     #this collects time points according to their raw time course, rather than normalized to 100 equally spaced time points
# 	
# 	#loop through and get all the trials for each subject
#     trial_matrix = [[tee for b in bl for tee in b.trials if (tee.skip==0)] for bl in blocks];
# 	
# 	#collect which trial type to run this analysis for
# 	#ttype = int(raw_input('Which trial type? 1 = HighC/HighA, 2 = HighC/LowA, 3 = LowC/HighA, 4 = LowC/LowA: '));
# 	
#     name = ['high_pref', 'highC_lowA','lowC_highA','lowC_lowA'][ttype-1];
# 	
#     data = pd.DataFrame(columns = concatenate([['subject_nr', 'trial_type', 'selected_item','block_nr','trial_nr','first_sac_latency','first_sac_item','last_sac_item','nr_dwells','prev_trial_last_dwelled_loc','prev_trial_type','prev_choice'] \
#         ,['t_%s'%(t) for t in linspace(1,10000,10000)]])); #add all participants together to the same dataFrame for simplicty
#     #maximum length of trial across all participants is ~9.5 seconds, so adding up to 100000 data points to include all time points        
# 	#SCORING FOR ITEM (entry at t_XX): 0 = not looked at any item, 1 = looked at alcohol, 2 = looked at cigarette, 3 = looked at neutral, nan = timepoint didn't exist in the trial
#     trial_index_counter = 0;
# 	
#     for subj_nr,subj in zip(ids, trial_matrix):    #enumerate(trial_matrix):
# 
#         for i,t in enumerate(subj):
# 			#conditional to differentiate between trials that should be skipped for this trial type, etc.
#             if((t.dropped_sample == 0)&(t.didntLookAtAnyItems == 0)&(t.trial_type == ttype)&(t.skip == 0)&(sqrt(t.eyeX[0]**2 + t.eyeY[0]**2) < 2.5)):
#                 
#                 if (t.nr_saccades > 0):  #this conditional is used to ensure that no trials without saccades sneak through
#                 
#                     #0. first, get first saccade latency, first saccade item identity, nr of dwells on current trial
#                     #need the first saccade latency before collecting the gaze data, otherwise I can't align the data according to the first saccade onset
# 
#                     #this code gets the first saccade latency
#                     sac_start_time = 0;
#                     sac_start_pos = array([]);						
#                     sac_end_time = 0;
#                     sac_end_pos = array([]);
#                     
#                     #Below here goes through each trial and pulls out the first saccde
#                     # the while loop below runs through until a saccade is found (saccade_counter = 1) or
#                     # we get to the end of the trial
#                     
#                     saccade_counter = 0;
#                     
#                     for ii,xx,yy,issac in zip(range(len(t.sample_times)),
#                                                          t.eyeX, t.eyeY, t.isSaccade):
#                         #if no saccade has been made yet, keep running through the isSaccade array
#                         # issac < 1 will be zero at all non-saccading time points, including the start
#                         if issac == 0:
#                             #if the previous sample was saccading and now it isn't, the first saccade is complete and we can grab the data
#                             if (t.isSaccade[ii-1]==True)&(ii>0):
#                                 sac_end_time = t.sample_times[ii];
#                                 sac_end_pos = array([xx,yy]);
#                                 saccade_counter+=1;
#                                 break; #once I get the first saccade, end it here
#                             
# 
#                                 
#                         elif issac == 1:
#                             #get the starting point for this saccade as well as the time
#                             #the first transition between 0 and 1 will be the first saccade start
#                             if (t.isSaccade[ii-1]==False)&(ii>0)&(saccade_counter==0):
#                                 sac_start_time = t.sample_times[ii];
#                                 sac_start_pos = array([xx,yy]);       
#                     
#                     #calculate the first saccade latency
#                     first_sac_onset_latency = sac_start_time; 
# 
#                     #get the first item looked at			
#                     if t.firstCategoryLookedAt=='alcohol':
#                         first_sac_item_identity = 1;
#                     elif t.firstCategoryLookedAt=='cigarette':
#                         first_sac_item_identity = 2;
#                     elif t.firstCategoryLookedAt=='neutral':
#                         first_sac_item_identity = 3;
# 
#                     #get the last item looked at
#                     if t.lastCategoryLookedAt=='alcohol':
#                         last_sac_item_identity = 1;
#                     elif t.lastCategoryLookedAt=='cigarette':
#                         last_sac_item_identity = 2;
#                     elif t.lastCategoryLookedAt=='neutral':
#                         last_sac_item_identity = 3;						
# 
#                     #now here collect the total number of dwells
#                     rexp_pattern = re.compile(r'01'); #this regular expression pattern looks for strings with a 1 or anything continuous run of 1s
# 					#In the computation of the lookedAtXX arrays during trial pre-processing, I include NaNs at times when no itm
# 					#was looked at... e.g., when the participant was fixating the center of the screen.
# 					#In order to ensure that I capture the change from not looking at one item to looking at any item (like the first dwell),
# 					#I need to convert those NaNs to 0's for calculation using the string-based method below. However, I want the original
# 					#lookedAtXX arrays to maintain the Nan, 0, 1 coding scheme, so I'll create holder arrays for each trial to use for the nr of dwell
# 					#calculations here
# 					
#                     looked_at_alcohol = array([r if ((r==0)|(r==1)) else 0 for r in t.lookedAtAlcohol]);
#                     looked_at_cigarette = array([r if ((r==0)|(r==1)) else 0 for r in t.lookedAtCigarette]);
#                     looked_at_neutral = array([r if ((r==0)|(r==1)) else 0 for r in t.lookedAtNeutral]);
# 					
#                     total_holder = 0;
# 					
#                     str_alc = ''.join(str(int(g)) for g in looked_at_alcohol if not(isnan(g))); #first get the array into a string
#                     run_lengths_alc = [len(f) for f in rexp_pattern.findall(str_alc)];
# 					#line above, then use the regular expression pattern, looking for 1s, to parse an array of the continuous runs of 1s in the string from above and get length
#                     nr_fixs = sum([1 for r in run_lengths_alc]);
# 					#check if the first item is a 1... if so, the array started with looking at the item and it wouldnt be caught by the regexp.
# 					#this will only be the case if they weren't looking at anything to start (e.g., there were nan's to start, then the first item was looked at)
# 					#notice that because I have included NaNs in the t.lookedAtXX arrays for when items are not being looked at, the subsequent str_alc array
# 					#represents sequences of 1s and 0 s corresponding runs of looking at items, squished into the array; This means str_alc does not include
# 					#any information about samples where the eye was not on an item, which means this method cannot be used to understand differences in time between
# 					#dwells when that time is not being spent on an item. This is important to keep in mind
#                     if str_alc[0]=='1':
#                         nr_fixs +=1;
# 				
#                     total_holder+=nr_fixs; #add the nr of dwells from looking at alc to this holder variable
# 					
#                     str_cig = ''.join(str(int(g)) for g in looked_at_cigarette if not(isnan(g))); #parse cigarette
#                     run_lengths_cig = [len(f) for f in rexp_pattern.findall(str_cig)];
#                     nr_fixs = sum([1 for r in run_lengths_cig]);
# 					#check if the first item is a 1... if so, the array started with looking at the item and it wouldnt be caught by the regexp. need to correcy
#                     if str_cig[0]=='1':
#                         nr_fixs +=1;
# 
#                     total_holder+=nr_fixs; #add the nr of dwells from looking at cig to this holder variable
# 
#                     str_neu = ''.join(str(int(g)) for g in looked_at_neutral if not(isnan(g))); #do the parsing for neutral..
#                     run_lengths_neu = [len(f) for f in rexp_pattern.findall(str_neu)];
#                     nr_fixs = sum([1 for r in run_lengths_neu]);
# 					#check if the first item is a 1... if so, the array started with looking at the item and it wouldnt be caught by the regexp. need to correcy
#                     if str_neu[0]=='1':
#                         nr_fixs +=1;
# 
#                     total_holder+=nr_fixs; #add the nr of dwells from looking at neu to this holder variable
# 					
#                     total_nr_dwells = total_holder; #this is the variable for collecting total nr of dwells on this trial               
#                     
# 
#                     #1. get the previous trial last dwelled location and previous trial type
#                     #conditional here is to only compute these values if this was not the first trial in a block. If it was, add nan's to these values
#                     
#                     if t.trial_nr > 1:
#                         #this code below finds the location of the last dwell on trial N-1 a
# 						prev_looked_at_up = array([r if ((r==0)|(r==1)) else 0 for r in subj[i-1].lookedUp]);
# 						prev_looked_at_left = array([r if ((r==0)|(r==1)) else 0 for r in subj[i-1].lookedLeft]);
# 						prev_looked_at_right = array([r if ((r==0)|(r==1)) else 0 for r in subj[i-1].lookedRight]);			
#         
# 						str_up = ''.join(str(int(g)) for g in prev_looked_at_up if not(isnan(g))); #first get the array into a string
#         
#                         #get last instane of the '1' in this array. if never loooked at, will return a -1
# 						up_indices = str_up.rfind('1'); #rfind searches the string from right to left
#                         
# 						if isinstance(up_indices, int):
# 							up_last_index_lookedat = up_indices;
# 						else:
# 							up_last_index_lookedat = up_indices[0];
#                             
# 						str_left = ''.join(str(int(g)) for g in prev_looked_at_left if not(isnan(g))); #parse cigarette
# 						left_indices = str_left.rfind('1');		
# 						if isinstance(left_indices, int):
# 							left_last_index_lookedat = left_indices;
# 						else:
# 							left_last_index_lookedat = left_indices[0];
#         
# 						str_right = ''.join(str(int(g)) for g in prev_looked_at_right if not(isnan(g))); #do the parsing for neutral..
# 						right_indices = str_right.rfind('1');		
# 						if isinstance(right_indices, int):
# 							right_last_index_lookedat = right_indices;
# 						else:
# 							right_last_index_lookedat = right_indices[0];
#                         
# 						last_instances =  array([up_last_index_lookedat, left_last_index_lookedat, right_last_index_lookedat]); #always keep it up, left, right
# 						last_item_index = where(last_instances == max(last_instances))[0][0];		
#         
#                         #conditonal to find the last item that was looked at accoridng to the index corresponding to the item 
# 						if last_item_index==0:
# 							prev_last_dwelled_item = 'up';
# 						elif last_item_index==1:
# 							prev_last_dwelled_item = 'left';
# 						elif last_item_index== 2:
# 							prev_last_dwelled_item = 'right';
#                             
# 						previous_trial_type = subj[i-1].trial_type; #get the previous trial type
# 						
# 						if subj[i-1].preferred_category=='alcohol':
# 							previous_choice = 1;
# 						elif subj[i-1].preferred_category=='cigarette':
# 							previous_choice = 2;
# 						elif subj[i-1].preferred_category=='neutral':
# 							previous_choice = 3;    						                       
#                     else:
#                         prev_last_dwelled_item = nan;
#                         previous_trial_type = nan;
#                         previous_choice = nan;
# 
#                     #2. now finally get the gaze position information, aligning trials to the offset of the first saccade
#                     #keep the start of the array nans until the timepoint when the trial has data for it
#                     gaze_data = [nan for ja in range(10000)]; #this will be length 5000 and include each item looked at at each time point (or 0/NaN otherwise); pre-allocate with nans                    
#                     trial_end_index = len(t.lookedAtNeutral); #get the duration of the trial (e.g., how many samples, corresponding to how many milliseconds)
#     
#                     #trials longer than 5000 ms will be trimmed to 5000 ms
#                     if trial_end_index > 10000:
#                         trial_end_index = 10000;
#                     
#                     iterator = 0; first_sac_offset = sac_end_time; #here, use the saccade end time to ofset the iterator through the gaze data array
#                     #now go through for the 5000 time points prior to decision and score whether the paricipants was looking at 
#                     for j in (arange(10000)):
#                         if ((j+first_sac_offset)>=trial_end_index):
#                             continue;					
#                         elif (isnan(t.lookedAtNeutral[j+first_sac_offset]) & isnan(t.lookedAtAlcohol[j+first_sac_offset]) & isnan(t.lookedAtCigarette[j+first_sac_offset])):
#                             #at this point, there was a nan inserted because the participant did not look at each item
#                             #when there are no items looked at, include a 0
#                             gaze_data[iterator] = 0;
#                         elif (t.lookedAtAlcohol[j+first_sac_offset]==1):
#                             gaze_data[iterator] = 1;
#                         elif (t.lookedAtCigarette[j+first_sac_offset]==1):						
#                             gaze_data[iterator] = 2;						
#                         elif (t.lookedAtNeutral[j+first_sac_offset]==1):	
#                             gaze_data[iterator] = 3;
#                         iterator+=1;
#                         
#                     #if t.sub_id == ids[-1]: #stop at the subject who had very long RTS   
#                     #    1/0; #check the first saccade offset is working as expected, and check if the appropriate thing to do in the first confitional cheking for trial_end_index is appropriate to use the first_sac_offset
#                         
#                     #for ease of the regression computation, get the selected item into a numerical representation, same mapping as with item looked at
#                     if t.preferred_category=='alcohol':
#                         selected_item = 1;
#                     elif t.preferred_category=='cigarette':
#                         selected_item = 2;
#                     elif t.preferred_category=='neutral':
#                         selected_item = 3;                                  
#                         
#                     #at this point have collected data for gaze profile together
#                     #get all data points together for ease of incorporating into the dataFrame
#                     this_trials_data = concatenate([[subj_nr, ttype, selected_item, t.block_nr, t.trial_nr, first_sac_onset_latency, first_sac_item_identity, last_sac_item_identity, \
#                                                      total_nr_dwells, prev_last_dwelled_item, previous_trial_type, previous_choice],gaze_data]); #each trial variable, then each timepoint data   int(subj_nr+1)
# 
# 					
#                     #now translate this to the dataframe for this participant
#                     data.loc[trial_index_counter] = this_trials_data;
# 			
#                     trial_index_counter += 1; #1/0; #index for next trial
# 					
# 				
# 	print "completed subject %s.. \n\n"%subj_nr	
# 
# 	#save the database
#     data.to_csv(savepath+'%s_trialdata.csv'%name,index=False); #+'first_sac_locked/'
# 	#data.to_csv(savepath+'/stim_locked/'+'%s_trialdata.csv'%name,index=False); #previous iteration of this was to align to the onset of the stimulus
# 	# ends here
##################################################################################################################################################################

# def computePreviousTrialData(blocks, eyed='agg'):
# 	#compute the effect that the previous trial's (N-1) choice as well as last dwelled (fixated) item has on the current trial (N)
# 	db = subject_data;
# 	
# 	#first, check out effect that previous trial response has on current trial response/first dwelled item
# 	#this is likely to be biased due to the biases in choice
# 	
# 	rexp_pattern = re.compile(r'01'); #this regular expression pattern looks for strings with a 1 or anything continuous run of 1s
# 	
# 	#loop through and get all the trials for each subject
# 	trial_matrix = [[tee for b in bl for tee in b.trials if (tee.skip==0)] for bl in blocks];	
# 		
# 	#HERE, RUN A LOCATION-BASED PREVIOUS TRIAL ANALYSIS	
# 
# 	if eyed=='agg':
# 		index_counter=0; #index counter for the DataFrame object
# 		#here, create a dataframe object to save the subsequent data
# 		data = pd.DataFrame(columns = ['sub_id','trial_type','prev_lastdwellloc_cur_firstdwellloc_avg_prop','first_sac_latency']);		
# 		
# 	#get the aggregate breakdown as well as when they chose each item
# 	for ttype, name in zip([1,2,3,4],['high_pref', 'highC_lowA','lowC_highA','lowC_lowA']):			
# 		
# 		#this counter variable hold boolean (0 or 1) values corresponding to whether the previous trials last dwelled loc is the first dwelled loc on trial N
# 		prev_last_dwell_dwells_bools = [];
# 		lengs = [];
# 		latencies = [];
# 		
# 		for subj,sub_id in zip(trial_matrix, ids):		
# 			subj_prev_last_dwell_bools = [];
# 			subj_latencies = [];
# 
# 			for i,t in enumerate(subj):
# 				if((t.dropped_sample == 0)&(t.didntLookAtAnyItems == 0)&(t.trial_type == ttype)&
# 					(t.skip == 0)&(sqrt(t.eyeX[0]**2 + t.eyeY[0]**2) < 2.5)):
# 					
# 					#can't do n-back calculation for the first trial in a block
# 					if t.trial_nr>0:
# 						
# 						#get the previous last dwelled location
# 		
# 						prev_looked_at_up = array([r if ((r==0)|(r==1)) else 0 for r in subj[i-1].lookedUp]);
# 						prev_looked_at_left = array([r if ((r==0)|(r==1)) else 0 for r in subj[i-1].lookedLeft]);
# 						prev_looked_at_right = array([r if ((r==0)|(r==1)) else 0 for r in subj[i-1].lookedRight]);			
# 
# 						str_up = ''.join(str(int(g)) for g in prev_looked_at_up if not(isnan(g))); #first get the array into a string
# 
# 						#get last instane of the '1' in this array. if never loooked at, will return a -1
# 						up_indices = str_up.rfind('1'); #rfind searches the string from right to left
# 						
# 						if isinstance(up_indices, int):
# 							up_last_index_lookedat = up_indices;
# 						else:
# 							up_last_index_lookedat = up_indices[0];
# 							
# 						str_left = ''.join(str(int(g)) for g in prev_looked_at_left if not(isnan(g))); #parse cigarette
# 						left_indices = str_left.rfind('1');		
# 						if isinstance(left_indices, int):
# 							left_last_index_lookedat = left_indices;
# 						else:
# 							left_last_index_lookedat = left_indices[0];
# 	
# 						str_right = ''.join(str(int(g)) for g in prev_looked_at_right if not(isnan(g))); #do the parsing for neutral..
# 						right_indices = str_right.rfind('1');		
# 						if isinstance(right_indices, int):
# 							right_last_index_lookedat = right_indices;
# 						else:
# 							right_last_index_lookedat = right_indices[0];
# 						
# 						last_instances =  array([up_last_index_lookedat, left_last_index_lookedat, right_last_index_lookedat]); #always keep it up, left, right
# 						last_item_index = where(last_instances == max(last_instances))[0][0];		
# 		
# 						#conditonal to find the last item that was looked at accoridng to the index corresponding to the item 
# 						if last_item_index==0:
# 							prev_last_dwelled_item = 'up';
# 						elif last_item_index==1:
# 							prev_last_dwelled_item = 'left';
# 						elif last_item_index== 2:
# 							prev_last_dwelled_item = 'right';		
# 
# 					#and the first looked at item in this trial. It's the same thing as used above, but using string.find() rather than string.rfind()		
# 
# 						#get the current first dwelled location
# 		
# 						curr_looked_at_up = array([r if ((r==0)|(r==1)) else 0 for r in t.lookedUp]);
# 						curr_looked_at_left = array([r if ((r==0)|(r==1)) else 0 for r in t.lookedLeft]);
# 						curr_looked_at_right = array([r if ((r==0)|(r==1)) else 0 for r in t.lookedRight]);			
# 
# 						curr_str_up = ''.join(str(int(g)) for g in curr_looked_at_up if not(isnan(g))); #first get the array into a string
# 
# 						#get last instane of the '1' in this array. if never loooked at, will return a -1
# 						curr_up_indices = curr_str_up.find('1'); #find searches the string from left to right
# 						
# 						if isinstance(curr_up_indices, int):
# 							curr_up_first_index_lookedat = curr_up_indices;
# 						else:
# 							curr_up_first_index_lookedat = curr_up_indices[0];
# 						if curr_up_first_index_lookedat==-1:
# 							curr_up_first_index_lookedat = 100*1000; #this ensures that instead of a -1 being input into the array, I input a massive nr (needed for minimum calculation)
# 							
# 						curr_str_left = ''.join(str(int(g)) for g in curr_looked_at_left if not(isnan(g))); #parse cigarette
# 						curr_left_indices = curr_str_left.find('1');		
# 						if isinstance(curr_left_indices, int):
# 							curr_left_first_index_lookedat = curr_left_indices;
# 						else:
# 							curr_left_first_index_lookedat = curr_left_indices[0];
# 						if curr_left_first_index_lookedat==-1:
# 							curr_left_first_index_lookedat = 100*1000; #this ensures that instead of a -1 being input into the array, I input a massive nr (needed for minimum calculation)
# 								
# 						curr_str_right = ''.join(str(int(g)) for g in curr_looked_at_right if not(isnan(g))); #do the parsing for neutral..
# 						curr_right_indices = curr_str_right.find('1');		
# 						if isinstance(curr_right_indices, int):
# 							curr_right_first_index_lookedat = curr_right_indices;
# 						else:
# 							curr_right_first_index_lookedat = curr_right_indices[0];
# 						if curr_right_first_index_lookedat==-1:
# 							curr_right_first_index_lookedat = 100*1000; #this ensures that instead of a -1 being input into the array, I input a massive nr (needed for minimum calculation)			
# 													
# 						curr_first_instances =  array([curr_up_first_index_lookedat, curr_left_first_index_lookedat, curr_right_first_index_lookedat]); #always keep it up, left, right
# 						curr_first_item_index = where(curr_first_instances == min(curr_first_instances))[0][0];				
# 		
# 						#conditonal to find the last item that was looked at accoridng to the index corresponding to the item 
# 						if curr_first_item_index==0:
# 							curr_first_dwelled_item = 'up';
# 						elif curr_first_item_index==1:
# 							curr_first_dwelled_item = 'left';
# 						elif curr_first_item_index== 2:
# 							curr_first_dwelled_item = 'right';
# 							
# 						#now below here, compare the current trial's response and first looked at item with the last trials response and last looked at item	
# 						subj_prev_last_dwell_bools.append(prev_last_dwelled_item==curr_first_dwelled_item);
# 						
# 						#now here find the latency of the first saccade on current trial (trial N)
# 						sac_start_time = 0;
# 						sac_start_pos = array([]);						
# 						sac_end_time = 0;
# 						sac_end_pos = array([]);
# 						
# 						#Below here goes through each trial and pulls out the first saccde
# 						# the while loop below runs through until a saccade is found (saccade_counter = 1) or
# 						# we get to the end of the trial
# 						
# 						saccade_counter = 0;
# 						while saccade_counter==0:
# 							for ii,xx,yy,issac in zip(range(len(t.sample_times)),
# 																 t.eyeX, t.eyeY, t.isSaccade):
# 								#if no saccade has been made yet, keep running through the isSaccade array
# 								# issac < 1 will be zero at all non-saccading time points, including the start
# 								if issac == 0:
# 									#if the previous sample was saccading and now it isn't, the first saccade is complete and we can grab the data
# 									if (t.isSaccade[ii-1]==True)&(ii>0):
# 										sac_end_time = t.sample_times[ii];
# 										sac_end_pos = array([xx,yy]);
# 										saccade_counter+=1;
# 									
# 									#if there is no saccade, this will trigger the stop I need to move out of the infinite loop	
# 									if (ii == range(len(t.sample_times))[-1]):
# 										saccade_counter = 100;
# 										
# 								elif issac == 1:
# 									#get the starting point for this saccade as well as the time
# 									#the first transition between 0 and 1 will be the first saccade start
# 									if (t.isSaccade[ii-1]==False)&(ii>0)&(saccade_counter==0):
# 										sac_start_time = t.sample_times[ii];
# 										sac_start_pos = array([xx,yy]);
# 						
# 						#calculate the latency and amplitude, then save to the subject's array
# 						subj_latencies.append(sac_start_time);
# 						
# 						
# 			#here, append the aggregated proportion of trials these variables matched to the average holders for each subject
# 			prev_last_dwell_dwells_bools.append(sum(subj_prev_last_dwell_bools)/float(len(subj_prev_last_dwell_bools)));
# 			lengs.append(len(subj_prev_last_dwell_bools));
# 			latencies.append(mean(subj_latencies));
# 			
# 		#lengs = array([len(s) for s in prev_last_dwell_dwells_bools]);
# 
# 		#here, find average and standard error or these variables, then print it to the interpreter
# 				
# 		print('\n\n TRIAL TYPE %s \n\n'%name)
# 		print('\n Average proportion of trials the last fixated location on trial N-1 was the first fixated location on trial N for %s subjects: %4.2f \n'%(len(blocks),nanmean(prev_last_dwell_dwells_bools)));
# 		print('\n Between-subjects standard error of the mean: %4.2f \n\n'%(compute_BS_SEM(prev_last_dwell_dwells_bools)));
# 		print('Mean nr of trials for each participant: %s \n\n'%mean(array(lengs)));
# 		print('Mean first saccade current trial latency for each participant: %4.2f \n\n'%nanmean(latencies));
# 		print('\n Between-subjects standard error of the mean: %4.2f \n\n'%(compute_BS_SEM(latencies)));
# 
# 
# 		#add data to the data frame object to save as a .csv
# 		if eyed=='agg':
# 			for subid,  pl_cf, fr in zip(ids, prev_last_dwell_dwells_bools, latencies):
# 				data.loc[index_counter] = [subid, name, pl_cf, fr];
# 				index_counter+=1;
# 
# 	if eyed=='agg':
# 		data.to_csv(savepath+'prev_trial_location-based_data.csv',index=False);
# 		
# 	#BELOW HERE IS CODE TO RUN AN ITEM-BASED PREVIOUS TRIAL PRIMING ANALYSIS
# 		
# 	# if eyed=='agg':
# 	# 	index_counter=0; #index counter for the DataFrame object
# 	# 	#here, create a dataframe object to save the subsequent data
# 	# 	data = pd.DataFrame(columns = ['sub_id','trial_type','prev_resp_cur_resp_avg_prop','prev_resp_cur_firstdwell_avg_prop', \
# 	# 								   'prev_lastdwell_cur_resp_avg_prop','prev_lastdwell_cur_firstdwell_avg_prop']);
# 	# 	
# 	# #get the aggregate breakdown as well as when they chose each item
# 	# for ttype, name in zip([1,2,3,4],['high_pref', 'highC_lowA','lowC_highA','lowC_lowA']):			
# 	# 	
# 	# 	#this counter variables hold boolean (0 or 1) values corresponding to whether the previous trials response corresponded to the current trials response/first dwelled item
# 	# 	prev_resp_resps_bools = [];
# 	# 	prev_resp_dwells_bools = [];
# 	# 	prev_last_dwell_resps_bools = [];
# 	# 	prev_last_dwell_dwells_bools = [];		
# 	# 	
# 	# 	for subj,sub_id in zip(trial_matrix, ids):		
# 	# 		subj_prev_resp_resps_bools = [];
# 	# 		subj_prev_resp_dwells_bools = [];
# 	# 		subj_prev_last_resps_bools = []; #previous trial's last dwelled item's boolean match with the current response
# 	# 		subj_prev_last_dwell_bools = [];			
# 	# 
# 	# 		for i,t in enumerate(subj):
# 	# 			if((t.dropped_sample == 0)&(t.didntLookAtAnyItems == 0)&(t.trial_type == ttype)&
# 	# 				(t.skip == 0)&(sqrt(t.eyeX[0]**2 + t.eyeY[0]**2) < 2.5)):
# 	# 				
# 	# 				#can't do n-back calculation for the first trial in a block
# 	# 				if t.trial_nr>0:
# 	# 					
# 	# 					#get the previous trial response and last looked at item!
# 	# 					prev_response = subj[i-1].preferred_category;
# 	# 					
# 	# 					#get previous last dwelled item
# 	# 					prev_alc_subj = []; prev_cig_subj = []; prev_neu_subj = [];
# 	# 						
# 	# 					prev_looked_at_alcohol = array([r if ((r==0)|(r==1)) else 0 for r in subj[i-1].lookedAtAlcohol]);
# 	# 					prev_looked_at_cigarette = array([r if ((r==0)|(r==1)) else 0 for r in subj[i-1].lookedAtCigarette]);
# 	# 					prev_looked_at_neutral = array([r if ((r==0)|(r==1)) else 0 for r in subj[i-1].lookedAtNeutral]);					
# 	# 					
# 	# 					str_alc = ''.join(str(int(g)) for g in prev_looked_at_alcohol if not(isnan(g))); #first get the array into a string
# 	# 					
# 	# 					#get last instane of the '1' in this array. if never loooked at, will return a -1
# 	# 					alc_indices = str_alc.rfind('1'); #rfind searches the string from right to left
# 	# 					
# 	# 					if isinstance(alc_indices, int):
# 	# 						alc_last_index_lookedat = alc_indices;
# 	# 					else:
# 	# 						alc_last_index_lookedat = alc_indices[0];
# 	# 						
# 	# 					str_cig = ''.join(str(int(g)) for g in prev_looked_at_cigarette if not(isnan(g))); #parse cigarette
# 	# 					cig_indices = str_cig.rfind('1');		
# 	# 					if isinstance(cig_indices, int):
# 	# 						cig_last_index_lookedat = cig_indices;
# 	# 					else:
# 	# 						cig_last_index_lookedat = cig_indices[0];
# 	# 
# 	# 					str_neu = ''.join(str(int(g)) for g in prev_looked_at_neutral if not(isnan(g))); #do the parsing for neutral..
# 	# 					neu_indices = str_neu.rfind('1');		
# 	# 					if isinstance(neu_indices, int):
# 	# 						neu_last_index_lookedat = neu_indices;
# 	# 					else:
# 	# 						neu_last_index_lookedat = neu_indices[0];
# 	# 					
# 	# 					last_instances =  array([alc_last_index_lookedat, cig_last_index_lookedat, neu_last_index_lookedat]); #always keep it alcohol, cigarette, neutral
# 	# 					last_item_index = where(last_instances == max(last_instances))[0][0];
# 						# 
# 						# #conditonal to find the last item that was looked at accoridng to the index corresponding to the item 
# 						# if last_item_index==0:
# 						# 	prev_last_dwelled_item = 'alcohol';
# 						# elif last_item_index==1:
# 						# 	prev_last_dwelled_item = 'cigarette';
# 						# elif last_item_index== 2:
# 						# 	prev_last_dwelled_item = 'neutral';
# 						# 
# 						# #now get the current trial first looked at item and response
# 						# 
# 						# current_response = t.preferred_category;
# 						# 
# 						# #and the first looked at item in this trial. It's the same thing as used above, but using string.find() rather than string.rfind()
# 						# alc_subj = []; cig_subj = []; neu_subj = [];
# 						# 	
# 						# looked_at_alcohol = array([r if ((r==0)|(r==1)) else 0 for r in t.lookedAtAlcohol]);
# 						# looked_at_cigarette = array([r if ((r==0)|(r==1)) else 0 for r in t.lookedAtCigarette]);
# 						# looked_at_neutral = array([r if ((r==0)|(r==1)) else 0 for r in t.lookedAtNeutral]);										
# 			# 			
# 			# 			curr_str_alc = ''.join(str(int(g)) for g in looked_at_alcohol if not(isnan(g))); #first get the array into a string
# 			# 			
# 			# 			#get last instane of the '1' in this array. if never loooked at, will return a -1
# 			# 			curr_alc_indices = curr_str_alc.find('1'); #rfind searches the string from right to left
# 			# 			
# 			# 			if isinstance(curr_alc_indices, int):
# 			# 				curr_alc_last_index_lookedat = curr_alc_indices;
# 			# 			else:
# 			# 				curr_alc_last_index_lookedat = curr_alc_indices[0];
# 			# 			if curr_alc_last_index_lookedat==-1:
# 			# 				curr_alc_last_index_lookedat = 100*1000; #this ensures that instead of a -1 being input into the array, I input a massive nr (needed for minimum calculation)
# 			# 				
# 			# 			curr_str_cig = ''.join(str(int(g)) for g in looked_at_cigarette if not(isnan(g))); #parse cigarette
# 			# 			curr_cig_indices = curr_str_cig.find('1');		
# 			# 			if isinstance(curr_cig_indices, int):
# 			# 				curr_cig_last_index_lookedat = curr_cig_indices;
# 			# 			else:
# 			# 				curr_cig_last_index_lookedat = curr_cig_indices[0];
# 			# 			if curr_cig_last_index_lookedat==-1:
# 			# 				curr_cig_last_index_lookedat = 100*1000;
# 			# 				
# 			# 			curr_str_neu = ''.join(str(int(g)) for g in looked_at_neutral if not(isnan(g))); #do the parsing for neutral..
# 			# 			curr_neu_indices = curr_str_neu.find('1');		
# 			# 			if isinstance(curr_neu_indices, int):
# 			# 				curr_neu_last_index_lookedat = curr_neu_indices;
# 			# 			else:
# 			# 				curr_neu_last_index_lookedat = curr_neu_indices[0];
# 			# 			if curr_neu_last_index_lookedat==-1:
# 			# 				curr_neu_last_index_lookedat = 100*1000;
# 			# 
# 			# 			curr_first_instances =  array([curr_alc_last_index_lookedat, curr_cig_last_index_lookedat, curr_neu_last_index_lookedat]); #always keep it alcohol, cigarette, neutral
# 			# 			curr_first_item_index = where(curr_first_instances == min(curr_first_instances))[0][0];
# 			# 			
# 			# 			#conditonal to find the last item that was looked at accoridng to the index corresponding to the item 
# 			# 			if curr_first_item_index==0:
# 			# 				curr_first_dwelled_item = 'alcohol';
# 			# 			elif curr_first_item_index==1:
# 			# 				curr_first_dwelled_item = 'cigarette';
# 			# 			elif curr_first_item_index== 2:
# 			# 				curr_first_dwelled_item = 'neutral';
# 			# 				
# 			# 			#now below here, compare the current trial's response and first looked at item with the last trials response and last looked at item	
# 			# 			subj_prev_resp_resps_bools.append(prev_response==current_response);
# 			# 			subj_prev_resp_dwells_bools.append(prev_response==curr_first_dwelled_item);
# 			# 			subj_prev_last_resps_bools.append(prev_last_dwelled_item==current_response); #previous trial's last dwelled item's boolean match with the current response
# 			# 			subj_prev_last_dwell_bools.append(prev_last_dwelled_item==curr_first_dwelled_item);
# 			# 
# 			# #here, append the aggregated proportion of trials these variables matched to the average holders for each subject
# 			# prev_resp_resps_bools.append(sum(subj_prev_resp_resps_bools)/float(len(subj_prev_resp_resps_bools)));
# 			# prev_resp_dwells_bools.append(sum(subj_prev_resp_dwells_bools)/float(len(subj_prev_resp_dwells_bools)));
# 			# prev_last_dwell_resps_bools.append(sum(subj_prev_last_resps_bools)/float(len(subj_prev_last_resps_bools)));
# 			# prev_last_dwell_dwells_bools.append(sum(subj_prev_last_dwell_bools)/float(len(subj_prev_last_dwell_bools)));
# 		# 	
# 		# 
# 		# #here, find average and standard error or these variables, then print it to the interpreter
# 		# 		
# 		# print('\n\n TRIAL TYPE %s \n\n'%name)
# 		# print('\n Average proportion of trials the last-dwelled item on trial N-1 was the first dwelled item on trial N for %s subjects: %4.2f \n'%(len(blocks),nanmean(prev_last_dwell_dwells_bools)));
# 		# print('\n Between-subjects standard error of the mean: %4.2f \n\n'%(compute_BS_SEM(prev_last_dwell_dwells_bools)));
# 		# print('\n Average proportion of trials the last-dwelled item on trial N-1 was the selected item on trial N for %s subjects: %4.2f \n'%(len(blocks),nanmean(prev_last_dwell_resps_bools)));
# 		# print('\n Between-subjects standard error of the mean: %4.2f \n\n'%(compute_BS_SEM(prev_last_dwell_resps_bools)));
# 		# print('\n Average proportion of trials the selected item on trial N-1 was the first dwelled item on trial N for %s subjects: %4.2f \n'%(len(blocks),nanmean(prev_resp_dwells_bools)));
# 		# print('\n Between-subjects standard error of the mean: %4.2f \n\n'%(compute_BS_SEM(prev_resp_dwells_bools)));
# 		# print('\n Average proportion of trials the selected item on trial N-1 was the selected item on trial N for %s subjects: %4.2f \n'%(len(blocks),nanmean(prev_resp_resps_bools)));
# 		# print('\n Between-subjects standard error of the mean: %4.2f \n\n'%(compute_BS_SEM(prev_resp_resps_bools)));		
# 	# 
# 	# 	#add data to the data frame object to save as a .csv
# 	# 	if eyed=='agg':
# 	# 		for subid, pr_cr, pr_cf, pl_cr, pl_cf in zip(ids, prev_resp_resps_bools, prev_resp_dwells_bools, prev_last_dwell_resps_bools,prev_last_dwell_dwells_bools):
# 	# 			data.loc[index_counter] = [subid, name, pr_cr, pr_cf, pl_cr, pl_cf];
# 	# 			index_counter+=1;
# 	# 
# 	# 
# 	# if eyed=='agg':
# 	# 	data.to_csv(savepath+'prev_trial_data.csv',index=False);
# 
# 	1/0
##################################################################################################################################################################

# def computeOneDwellTrialData(blocks, eyed='agg'):
# 	#check out the data for the trials where one dwell occurred
# 	#Compute:
# 	#1. For each subject, compute number/proportion of single dwell trials
# 	#^(compare against the corrective saccade data to see if high percentage of corrective saccades correlated with nr of single dwell trials)
# 	#2. What are the latencies of single dwell trials?
# 	#3. Where are these one dwell trials going? (Heatmaps)
# 	#4. What is being selected on single dwell trials?
# 	
# 	#below here, use the code to compute the number of dwells from the function below
# 	db = subject_data;
# 
# 	rexp_pattern = re.compile(r'01'); #this regular expression pattern looks for strings with a 1 or anything continuous run of 1s
# 	
# 	#loop through and get all the trials for each subject
# 	trial_matrix = [[tee for b in bl for tee in b.trials if (tee.skip==0)] for bl in blocks];
# 
# 	#find each subjects' cue substance based on which item them chose more often during PAPC trials where they selected the alcohol or cigarette
# 	if eyed=='agg':
# 		index_counter=0; #index counter for the DataFrame object
# 		#here, create a dataframe object to save the subsequent data
# 		
# 	#find the number of dwells for each of the alcohol, cigarettes, and neutral items
# 	#get the aggregate breakdown as well as when they chose each item
# 	for ttype, name in zip([1,2,3,4],['high_pref', 'highC_lowA','lowC_highA','lowC_lowA']):		
# 		
# 		#proportion of trials the one dwells occurs on
# 		alc_prop_trials = []; cig_prop_trials = []; neu_prop_trials = []; total_prop_trials = [];
# 		chose_alc_alc_prop_trials= []; chose_alc_cig_prop_trials = []; chose_alc_neu_prop_trials = []; chose_alc_total_prop_trials = [];
# 		chose_cig_alc_prop_trials = []; chose_cig_cig_prop_trials = []; chose_cig_neu_prop_trials = []; chose_cig_total_prop_trials = [];
# 		chose_neu_alc_prop_trials = []; chose_neu_cig_prop_trials = []; chose_neu_neu_prop_trials = []; chose_neu_total_prop_trials = [];
# 		#latency for first saccade holders for the one dwells occurs
# 		alc_lats = []; cig_lats = [];neu_lats = []; total_lats = []; 
# 		chose_alc_alc_lats= []; chose_alc_cig_lats = []; chose_alc_neu_lats = []; chose_alc_total_lats = [];
# 		chose_cig_alc_lats = []; chose_cig_cig_lats = []; chose_cig_neu_lats = []; chose_cig_total_lats = [];
# 		chose_neu_alc_lats = []; chose_neu_cig_lats = []; chose_neu_neu_lats = []; chose_neu_total_lats = [];
# 		#end points of the first saccade
# 		alc_endpoints = []; cig_endpoints = [];neu_endpoints = []; total_endpoints= []; 
# 		chose_alc_alc_endpoints= []; chose_alc_cig_endpoints = []; chose_alc_neu_endpoints = []; chose_alc_total_endpoints = [];
# 		chose_cig_alc_endpoints = []; chose_cig_cig_endpoints = []; chose_cig_neu_endpoints = []; chose_cig_total_endpoints = [];
# 		chose_neu_alc_endpoints = []; chose_neu_cig_endpoints = []; chose_neu_neu_endpoints = []; chose_neu_total_endpoints = [];		
# 		#which object the one dwells looked at
# 		alc_dwelled_items = []; cig_dwelled_items = []; neu_dwelled_items = []; total_dwelled_items = []; 
# 		chose_alc_alc_dwelled_items= []; chose_alc_cig_dwelled_items = []; chose_alc_neu_dwelled_items = [];chose_alc_total_dwelled_items = [];
# 		chose_cig_alc_dwelled_items = []; chose_cig_cig_dwelled_items = []; chose_cig_neu_dwelled_items = []; chose_cig_total_dwelled_items = [];
# 		chose_neu_alc_dwelled_items = []; chose_neu_cig_dwelled_items = []; chose_neu_neu_dwelled_items = []; chose_neu_total_dwelled_items = [];
# 		
# 		#first run the analysis for all trials of this trial type, not breaking it down by whether they chose alcohol, cigeratte, or neutral
# 		#loop through trials for each subject
# 		for subj,sub_id in zip(trial_matrix, ids):
# 			alc_subj = []; cig_subj = []; neu_subj = []; tot_subj = [];
# 			alc_subj_lats  = []; cig_subj_lats  = []; neu_subj_lats  = []; tot_subj_lats  = [];
# 			alc_subj_endpoints = []; cig_subj_endpoints = []; neu_subj_endpoints = []; tot_subj_endpoints = [];
# 			alc_subj_dwelled_items = []; cig_subj_dwelled_items = []; neu_subj_dwelled_items = []; tot_subj_dwelled_items = [];
# 			
# 			for t in subj:
# 				if((t.dropped_sample == 0)&(t.didntLookAtAnyItems == 0)&(t.trial_type == ttype)&
# 					(t.skip == 0)&(sqrt(t.eyeX[0]**2 + t.eyeY[0]**2) < 2.5)):
# 					
# 					#In the computation of the lookedAtXX arrays during trial pre-processing, I include NaNs at times when no itm
# 					#was looked at... e.g., when the participant was fixating the center of the screen.
# 					#In order to ensure that I capture the change from not looking at one item to looking at any item (like the first dwell),
# 					#I need to convert those NaNs to 0's for calculation using the string-based method below. However, I want the original
# 					#lookedAtXX arrays to maintain the Nan, 0, 1 coding scheme, so I'll create holder arrays for each trial to use for the nr of dwell
# 					#calculations here
# 					
# 					looked_at_alcohol = array([r if ((r==0)|(r==1)) else 0 for r in t.lookedAtAlcohol]);
# 					looked_at_cigarette = array([r if ((r==0)|(r==1)) else 0 for r in t.lookedAtCigarette]);
# 					looked_at_neutral = array([r if ((r==0)|(r==1)) else 0 for r in t.lookedAtNeutral]);
# 					
# 					total_holder = 0; #this determines how many items are dwelled on
# 					
# 					str_alc = ''.join(str(int(g)) for g in looked_at_alcohol if not(isnan(g))); #first get the array into a string
# 					run_lengths_alc = [len(f) for f in rexp_pattern.findall(str_alc)];
# 					#line above, then use the regular expression pattern, looking for 1s, to parse an array of the continuous runs of 1s in the string from above and get length
# 					nr_fixs = sum([1 for r in run_lengths_alc]);
# 					#Nuances of this code are below
# 					if str_alc[0]=='1':
# 						nr_fixs +=1;
# 					total_holder+=nr_fixs; #add the nr of dwells from looking at alc to this holder variable
# 					
# 					str_cig = ''.join(str(int(g)) for g in looked_at_cigarette if not(isnan(g))); #parse cigarette
# 					run_lengths_cig = [len(f) for f in rexp_pattern.findall(str_cig)];
# 					nr_fixs = sum([1 for r in run_lengths_cig]);
# 					#check if the first item is a 1... if so, the array started with looking at the item and it wouldnt be caught by the regexp. need to correcy
# 					if str_cig[0]=='1':
# 						nr_fixs +=1;
# 					total_holder+=nr_fixs; #add the nr of dwells from looking at cig to this holder variable
# 
# 					str_neu = ''.join(str(int(g)) for g in looked_at_neutral if not(isnan(g))); #do the parsing for neutral..
# 					run_lengths_neu = [len(f) for f in rexp_pattern.findall(str_neu)];
# 					nr_fixs = sum([1 for r in run_lengths_neu]);
# 					#check if the first item is a 1... if so, the array started with looking at the item and it wouldnt be caught by the regexp. need to correcy
# 					if str_neu[0]=='1':
# 						nr_fixs +=1;
# 					total_holder+=nr_fixs; #add the nr of dwells from looking at neu to this holder variable
# 					
# 					#conditional to determine if the number of dwells was one or not
# 					#below here append the behavioral information to the holder variables
# 					if total_holder==1:
# 						
# 						sac_start_time = 0;
# 						sac_start_pos = array([]);						
# 						sac_end_time = 0;
# 						sac_end_pos = array([]);
# 						
# 						#Below here goes through each trial and pulls out the first saccde
# 						# the while loop below runs through until a saccade is found (saccade_counter = 1) or
# 						# we get to the end of the trial
# 						
# 						saccade_counter = 0;
# 						while saccade_counter==0:
# 							for ii,xx,yy,issac in zip(range(len(t.sample_times)),
# 																 t.eyeX, t.eyeY, t.isSaccade):
# 								#if no saccade has been made yet, keep running through the isSaccade array
# 								# issac < 1 will be zero at all non-saccading time points, including the start
# 								if issac == 0:
# 									#if the previous sample was saccading and now it isn't, the first saccade is complete and we can grab the data
# 									if (t.isSaccade[ii-1]==True)&(ii>0):
# 										sac_end_time = t.sample_times[ii];
# 										sac_end_pos = array([xx,yy]);
# 										saccade_counter+=1;
# 									
# 									#if there is no saccade, this will trigger the stop I need to move out of the infinite loop	
# 									if (ii == range(len(t.sample_times))[-1]):
# 										saccade_counter = 100;
# 										
# 								elif issac == 1:
# 									#get the starting point for this saccade as well as the time
# 									#the first transition between 0 and 1 will be the first saccade start
# 									if (t.isSaccade[ii-1]==False)&(ii>0)&(saccade_counter==0):
# 										sac_start_time = t.sample_times[ii];
# 										sac_start_pos = array([xx,yy]);
# 						
# 						#calculate the latency and endpoint, then save to the subject's array
# 						total_subj_lats.append(sac_start_time);
# 						total_subj_endpoints.append(sac_end_pos);
# 						
# 						#add prop times and dwelled items
##################################################################################################################################################################

# def computeMedianSplitTemporalGAzeProfiles(blocks, ttype, eyed='agg'):
# 	#computes the long RESPONSE LOCKED temporal gaze profiles but with a median split
# 	
# 	db = subject_data;
# 	index_counter = 0; #for database calculation
# 	
# 	time_bin_spacing = 0.001;
# 	time_duration = 2.0;
# 	
# 	#loop through and get all the trials for each subject
# 	trial_matrix = [[tee for b in bl for tee in b.trials if (tee.skip==0)] for bl in blocks];
# 	
# 	#collect which trial type to run this analysis for
# 	#ttype = int(raw_input('Which trial type? 1 = HighC/HighA, 2 = HighC/LowA, 3 = LowC/HighA, 4 = LowC/LowA: '));
# 	
# 	name = ['high_pref', 'highC_lowA','lowC_highA','lowC_lowA'][ttype-1];
# 
# 	#create 2000 dataframe objects that will correspond to each time point
# 	fast_data = [pd.DataFrame(columns = ['sub_id','fast_or_slow','med_rt','trial_type','selected_item','looked_at_item','timepoint','nr_trials','nr_trials_used_for_likelihood','mean_fix_likelihood']) for i in arange(2000)];
# 	slow_data = [pd.DataFrame(columns = ['sub_id','fast_or_slow','med_rt','trial_type','selected_item','looked_at_item','timepoint','nr_trials','nr_trials_used_for_likelihood','mean_fix_likelihood']) for i in arange(2000)];
# 	#nr of trials used is the total number of trials used for tht time point (a trial where at least one item was looked at)
# 	#nr_trials_used_for_likelihood is the nr of trials where that specific item was looked at, at the given timepoint
# 
# 	for selected_item in ['alcohol','cigarette','neutral']:
# 		
# 		for split,data_frame in zip(['fast','slow'], [fast_data, slow_data]):
# 			# ^ use this to determine which dataframe to save to
# 		
# 			fig = figure(); ax1 = gca();
# 			ax1.set_ylim(0.0, 1.0); ax1.set_yticks(arange(0,1.01,0.1)); ax1.set_xlim([0,2000]);
# 			ax1.set_ylabel('Likelihood of fixating',size=18); ax1.set_xlabel('Time with respect to stimulus onset, ms',size=18,labelpad=11);
# 			ax1.set_xticks([0,500, 1000, 1500, 2000]);
# 			#ax1.set_xticklabels(['-2000', '-1500', '-1000', '-500', '0']);
# 			colors = ['red','blue', 'green']; alphas = [1.0, 1.0, 1.0]; legend_lines = [];		count = 0;	
# 		
# 			# #define arrays for the neutral, alcohol and cigarette items
# 			neu_gaze_array = zeros(time_duration/time_bin_spacing);
# 			neu_counts = zeros(shape(neu_gaze_array));
# 			neu_subject_means_array = [[] for i in range(2000)]; #use this to store each individual subjects' mean for each time point
# 			neu_subject_agg_counts = []; 
# 			alc_gaze_array = zeros(time_duration/time_bin_spacing);
# 			alc_counts = zeros(shape(alc_gaze_array));
# 			alc_subject_means_array = [[] for i in range(2000)];
# 			alc_subject_agg_counts = []; 
# 			cig_cue_gaze_array = zeros(time_duration/time_bin_spacing);
# 			cig_cue_counts = zeros(shape(cig_cue_gaze_array));
# 			cig_cue_subject_means_array = [[] for i in range(2000)];
# 			cig_subject_agg_counts = []; 	
# 
# 			for subj_nr,subj in enumerate(trial_matrix):
# 				neu_individ_subject_sum = zeros(time_duration/time_bin_spacing);
# 				neu_individ_subject_counts = zeros(time_duration/time_bin_spacing);
# 				neu_individ_subject_nrusedtrials = zeros(time_duration/time_bin_spacing);
# 				alc_individ_subject_sum = zeros(time_duration/time_bin_spacing);
# 				alc_individ_subject_counts = zeros(time_duration/time_bin_spacing);
# 				alc_individ_subject_nrusedtrials = zeros(time_duration/time_bin_spacing);			
# 				cig_cue_individ_subject_sum = zeros(time_duration/time_bin_spacing);
# 				cig_cue_individ_subject_counts = zeros(time_duration/time_bin_spacing);
# 				cig_individ_subject_nrusedtrials = zeros(time_duration/time_bin_spacing);
# 
# 				med_rt = median([p.response_time for p in subj if ((p.dropped_sample == 0)&(p.didntLookAtAnyItems == 0)&(p.trial_type == ttype)&(p.preferred_category == selected_item))]); #get median RT for this subject
# 
# 				if (med_rt <= 0):
# 					1/0;
# 
# 				for t in subj:				
# 					#conditional to differentiate between not-cue trials when selecteing the non-cue or not
# 					#the second conditional include nuetral trials that were preferred only
# 					if ((t.dropped_sample == 0)&(t.didntLookAtAnyItems == 0)&(t.trial_type == ttype)&(t.preferred_category == selected_item)):
# 						
# 						#conditional to determine if this trial's RT is less than or equal to the median RT					
# 						if (split=='fast'):
# 							if (t.response_time > med_rt):
# 								continue;
# 						elif (split=='slow'):
# 							if (t.response_time <= med_rt):
# 								continue;		
# 
# 						#neutral is always the same...
# 						#cycle through each time point, going backward through the array (e.g., -1, -2..) and aggregating the data accordingly
# 						for i in (arange(2000)+1):
# 							if (i>len(t.lookedAtNeutral)):
# 								continue;
# 							elif (isnan(t.lookedAtNeutral[-i])):
# 								continue; #nan means they weren't looking at anything at this timepoint
# 							neu_gaze_array[-i] += t.lookedAtNeutral[-i];
# 							neu_counts[-i] += 1;
# 							#put the individual subject data together
# 							neu_individ_subject_sum[-i] += t.lookedAtNeutral[-i];
# 							neu_individ_subject_counts[-i] += 1;
# 							neu_individ_subject_nrusedtrials[-i] += t.lookedAtNeutral[-i];
# 						for i in (arange(2000)+1):
# 							if (i>len(t.lookedAtAlcohol)):
# 								continue;
# 							elif (isnan(t.lookedAtAlcohol[-i])):
# 								continue;
# 							#store the alcohol gaze patterns as the cue item
# 							alc_gaze_array[-i] += t.lookedAtAlcohol[-i];
# 							alc_counts[-i] += 1;
# 							#put the individual subject data together
# 							alc_individ_subject_sum[-i] += t.lookedAtAlcohol[-i];
# 							alc_individ_subject_counts[-i] += 1;
# 							alc_individ_subject_nrusedtrials[-i] += t.lookedAtAlcohol[-i]; 
# 						for i in (arange(2000)+1):
# 							if (i>len(t.lookedAtCigarette)):
# 								continue;
# 							elif (isnan(t.lookedAtCigarette[-i])):
# 								continue;							
# 							#store the cigarette items as the not_cue item
# 							cig_cue_gaze_array[-i] += t.lookedAtCigarette[-i];
# 							cig_cue_counts[-i] += 1;
# 							#put the individual subject data together
# 							cig_cue_individ_subject_sum[-i] += t.lookedAtCigarette[-i];
# 							cig_cue_individ_subject_counts[-i] += 1;
# 							cig_individ_subject_nrusedtrials[-i] += t.lookedAtCigarette[-i];
# 
# 	
# 				neu_individ_subject_mean = neu_individ_subject_sum/neu_individ_subject_counts; #calculate the mean for this subject at each time point
# 				[neu_subject_means_array[index].append(ind_mew) for index,ind_mew in zip(arange(2000),neu_individ_subject_mean)]; #append this to the array for each subject
# 				[neu_subject_agg_counts.append(ct) for ct in neu_individ_subject_counts]; #store number of trials here		
# 				alc_individ_subject_mean = alc_individ_subject_sum/alc_individ_subject_counts; #calculate the mean for this subject at each time point
# 				[alc_subject_means_array[index].append(ind_mew) for index,ind_mew in zip(arange(2000),alc_individ_subject_mean)]; #append this to the array for each subject
# 				[alc_subject_agg_counts.append(ct) for ct in alc_individ_subject_counts];
# 				cig_cue_individ_subject_mean = cig_cue_individ_subject_sum/cig_cue_individ_subject_counts; #calculate the mean for this subject at each time point
# 				[cig_cue_subject_means_array[index].append(ind_mew) for index,ind_mew in zip(arange(2000),cig_cue_individ_subject_mean)]; #append this to the array for each subject
# 				[cig_subject_agg_counts.append(ct) for ct in cig_cue_individ_subject_counts];
# 				
# 				for index in arange(2000):
# 					#make sure to reverse the time point from index...
# 					data_frame[index].loc[index_counter] = [int(subj_nr+1),split,med_rt,int(ttype),selected_item,'alcohol', (1999-index), alc_individ_subject_counts[index], alc_individ_subject_nrusedtrials[index], alc_individ_subject_mean[index]];
# 					data_frame[index].loc[index_counter+1] = [int(subj_nr+1),split,med_rt,int(ttype),selected_item,'cigarette', (1999-index), cig_cue_individ_subject_counts[index], cig_individ_subject_nrusedtrials[index], cig_cue_individ_subject_mean[index]];
# 					data_frame[index].loc[index_counter+2] = [int(subj_nr+1),split,med_rt,int(ttype),selected_item,'neutral', (1999-index), neu_individ_subject_counts[index], neu_individ_subject_nrusedtrials[index], neu_individ_subject_mean[index]];
# 				index_counter+=3;
# 							
# 				print "completed subject %s.. \n\n"%subj_nr	
# 
# 			#plot each likelihood looking at items				
# 			for  subj_ms, cue_name, c, a in zip([alc_subject_means_array, cig_cue_subject_means_array, neu_subject_means_array], ['alcohol','cigarette','neutral'], colors, alphas):							
# 				mews = array([nanmean(subj) for subj in subj_ms]); # gaze_array/counts
# 				sems = array([compute_BS_SEM(subj) for subj in subj_ms]);
# 				ax1.plot(linspace(0,2000,2000), mews, lw = 4.0, color = c, alpha = a);
# 				#plot the errorbars
# 				#for x,m,s in zip(linspace(0,1000,1000),mews,sems):
# 				ax1.fill_between(linspace(0,2000,2000), mews-sems, mews+sems, color = c, alpha = a*0.4);
# 				legend_lines.append(mlines.Line2D([],[],color=c,lw=6,alpha = a, label='likelihood(looking at %s) '%cue_name));
# 			#plot the sum of each for a sanity emasure to ensure they equate to one
# 			#agg = [(nanmean(a)+nanmean(b)+nanmean(c)) for a,b,c in zip(alc_subject_means_array, cig_cue_subject_means_array, neu_subject_means_array)];
# 			#ax1.plot(linspace(0,1000,1000),agg,color = 'gray', lw = 3.0);
# 			#legend_lines.append(mlines.Line2D([],[],color='gray',lw=4, alpha = 1.0, label='sum of all'));
# 			ax1.plot(linspace(0,2000,2000),linspace(0.33,0.333,2000),color = 'gray', lw = 3.0, ls='dashed');
# 			legend_lines.append(mlines.Line2D([],[],color='gray',lw=4, alpha = 1.0, ls = 'dashed', label='random'));	
# 			ax1.spines['right'].set_visible(False); ax1.spines['top'].set_visible(False);
# 			ax1.spines['bottom'].set_linewidth(2.0); ax1.spines['left'].set_linewidth(2.0);
# 			ax1.yaxis.set_ticks_position('left'); ax1.xaxis.set_ticks_position('bottom');
# 			ax1.legend(handles=[legend_lines[0],legend_lines[1], legend_lines[2], legend_lines[3]],loc = 2,ncol=1,fontsize = 11); # legend_lines[4]]
# 			title('%s %s Average Temporal Gaze Profile, \n Chose %s Trials'%(name, split, selected_item), fontsize = 22);
# 
# 	#save the databases
# 	[d.to_csv(savepath+'%s_FAST_timepoint_%s_temporal_gaze_profile_LONG.csv'%(name, (1999-i)),index=False) for d,i in zip(fast_data, arange(2000))]; #data.to_csv(savepath+'%s_temporal_gaze_profile.csv'%name,index=False);
# 	[d.to_csv(savepath+'%s_SLOW_timepoint_%s_temporal_gaze_profile_LONG.csv'%(name, (1999-i)),index=False) for d,i in zip(slow_data, arange(2000))];
# 	# ends here
##################################################################################################################################################################
# 
# def computeMedianSplitLongStimulusLockedTemporalGazeProfiles(blocks, ttype, eyed = 'agg'):
# 	#performs the median split temporal gaze profile analysis for the STIMULUS-LOCKED data
# 
# 	db = subject_data;
# 	index_counter = 0; #for database calculation
# 	
# 	time_bin_spacing = 0.001;
# 	time_duration = 2.0;
# 	
# 	#loop through and get all the trials for each subject
# 	trial_matrix = [[tee for b in bl for tee in b.trials if (tee.skip==0)] for bl in blocks];
# 	
# 	#collect which trial type to run this analysis for
# 	#ttype = int(raw_input('Which trial type? 1 = HighC/HighA, 2 = HighC/LowA, 3 = LowC/HighA, 4 = LowC/LowA: '));
# 	
# 	name = ['high_pref', 'highC_lowA','lowC_highA','lowC_lowA'][ttype-1];
# 
# 	#create 2000 dataframe objects that will correspond to each time point
# 	fast_data = [pd.DataFrame(columns = ['sub_id','fast_or_slow','med_rt','trial_type','selected_item','looked_at_item','timepoint','nr_trials','nr_trials_used_for_likelihood','mean_fix_likelihood']) for i in arange(2000)];
# 	slow_data = [pd.DataFrame(columns = ['sub_id','fast_or_slow','med_rt','trial_type','selected_item','looked_at_item','timepoint','nr_trials','nr_trials_used_for_likelihood','mean_fix_likelihood']) for i in arange(2000)];
# 	#nr of trials used is the total number of trials used for tht time point (a trial where at least one item was looked at)
# 	#nr_trials_used_for_likelihood is the nr of trials where that specific item was looked at, at the given timepoint
# 
# 	for selected_item in ['alcohol','cigarette','neutral']:
# 		
# 		for split,data_frame in zip(['fast','slow'], [fast_data, slow_data]):
# 			# ^ use this to determine which dataframe to save to
# 
# 			fig = figure(); ax1 = gca();
# 			ax1.set_ylim(0.0, 1.0); ax1.set_yticks(arange(0,1.01,0.1)); ax1.set_xlim([0,2000]);
# 			ax1.set_ylabel('Likelihood of fixating',size=18); ax1.set_xlabel('Time with respect to stimulus onset, ms',size=18,labelpad=11);
# 			ax1.set_xticks([0,500, 1000, 1500, 2000]);
# 			#ax1.set_xticklabels(['-2000', '-1500', '-1000', '-500', '0']);
# 			colors = ['red','blue', 'green']; alphas = [1.0, 1.0, 1.0]; legend_lines = [];		count = 0;	
# 		
# 			# #define arrays for the neutral, alcohol and cigarette items
# 			neu_gaze_array = zeros(time_duration/time_bin_spacing);
# 			neu_counts = zeros(shape(neu_gaze_array));
# 			neu_subject_means_array = [[] for i in range(2000)]; #use this to store each individual subjects' mean for each time point
# 			neu_subject_agg_counts = []; 
# 			alc_gaze_array = zeros(time_duration/time_bin_spacing);
# 			alc_counts = zeros(shape(alc_gaze_array));
# 			alc_subject_means_array = [[] for i in range(2000)];
# 			alc_subject_agg_counts = []; 
# 			cig_cue_gaze_array = zeros(time_duration/time_bin_spacing);
# 			cig_cue_counts = zeros(shape(cig_cue_gaze_array));
# 			cig_cue_subject_means_array = [[] for i in range(2000)];
# 			cig_subject_agg_counts = []; 	
# 
# 			for subj_nr,subj in enumerate(trial_matrix):
# 				neu_individ_subject_sum = zeros(time_duration/time_bin_spacing);
# 				neu_individ_subject_counts = zeros(time_duration/time_bin_spacing);
# 				neu_individ_subject_nrusedtrials = zeros(time_duration/time_bin_spacing);
# 				alc_individ_subject_sum = zeros(time_duration/time_bin_spacing);
# 				alc_individ_subject_counts = zeros(time_duration/time_bin_spacing);
# 				alc_individ_subject_nrusedtrials = zeros(time_duration/time_bin_spacing);			
# 				cig_cue_individ_subject_sum = zeros(time_duration/time_bin_spacing);
# 				cig_cue_individ_subject_counts = zeros(time_duration/time_bin_spacing);
# 				cig_individ_subject_nrusedtrials = zeros(time_duration/time_bin_spacing);
# 
# 				med_rt = median([p.response_time for p in subj if ((p.dropped_sample == 0)&(p.didntLookAtAnyItems == 0)&(p.trial_type == ttype)&(p.preferred_category == selected_item))]); #get median RT for this subject
# 
# 				if (med_rt <= 0):
# 					1/0;
# 
# 				for t in subj:	
# 					if ((t.dropped_sample == 0)&(t.didntLookAtAnyItems == 0)&(t.trial_type == ttype)&(t.preferred_category == selected_item)):
# 						
# 						#conditional to determine if this trial's RT is less than or equal to the median RT					
# 						if (split=='fast'):
# 							if (t.response_time > med_rt):
# 								continue;
# 						elif (split=='slow'):
# 							if (t.response_time <= med_rt):
# 								continue;
# 
# 						#cycle through each time point, aggregating the data accordingly
# 						
# 						for i in (arange(2000)):
# 							if (i>=len(t.lookedAtNeutral)):
# 								continue;
# 							elif (isnan(t.lookedAtNeutral[i])):
# 								continue; #nan means they weren't looking at anything at this timepoint
# 							neu_gaze_array[i] += t.lookedAtNeutral[i];
# 							neu_counts[i] += 1;
# 							#put the individual subject data together
# 							neu_individ_subject_sum[i] += t.lookedAtNeutral[i];
# 							neu_individ_subject_counts[i] += 1;
# 							neu_individ_subject_nrusedtrials[i] += t.lookedAtNeutral[i];
# 	
# 						for i in (arange(2000)):
# 							if (i>=len(t.lookedAtAlcohol)):
# 								continue;
# 							elif (isnan(t.lookedAtAlcohol[i])):
# 								continue;
# 							#store the alcohol gaze patterns as the cue item
# 							alc_gaze_array[i] += t.lookedAtAlcohol[i];
# 							alc_counts[i] += 1;
# 							#put the individual subject data together
# 							alc_individ_subject_sum[i] += t.lookedAtAlcohol[i];
# 							alc_individ_subject_counts[i] += 1;
# 							alc_individ_subject_nrusedtrials[i] += t.lookedAtAlcohol[i];
# 							
# 						for i in (arange(2000)):
# 							if (i>=len(t.lookedAtCigarette)):
# 								continue;
# 							elif (isnan(t.lookedAtCigarette[i])):
# 								continue;							
# 							#store the cigarette items as the not_cue item
# 							cig_cue_gaze_array[i] += t.lookedAtCigarette[i];
# 							cig_cue_counts[i] += 1;
# 							#put the individual subject data together
# 							cig_cue_individ_subject_sum[i] += t.lookedAtCigarette[i];
# 							cig_cue_individ_subject_counts[i] += 1;
# 							cig_individ_subject_nrusedtrials[i] += t.lookedAtCigarette[i];
# 							
# 				neu_individ_subject_mean = neu_individ_subject_sum/neu_individ_subject_counts; #calculate the mean for this subject at each time point
# 				[neu_subject_means_array[index].append(ind_mew) for index,ind_mew in zip(arange(2000),neu_individ_subject_mean)]; #append this to the array for each subject
# 				[neu_subject_agg_counts.append(ct) for ct in neu_individ_subject_counts]; #store number of trials here		
# 				alc_individ_subject_mean = alc_individ_subject_sum/alc_individ_subject_counts; #calculate the mean for this subject at each time point
# 				[alc_subject_means_array[index].append(ind_mew) for index,ind_mew in zip(arange(2000),alc_individ_subject_mean)]; #append this to the array for each subject
# 				[alc_subject_agg_counts.append(ct) for ct in alc_individ_subject_counts];
# 				cig_cue_individ_subject_mean = cig_cue_individ_subject_sum/cig_cue_individ_subject_counts; #calculate the mean for this subject at each time point
# 				[cig_cue_subject_means_array[index].append(ind_mew) for index,ind_mew in zip(arange(2000),cig_cue_individ_subject_mean)]; #append this to the array for each subject
# 				[cig_subject_agg_counts.append(ct) for ct in cig_cue_individ_subject_counts];	
# 
# 				for index in arange(2000):
# 					#make sure to reverse the time point from index...
# 					data_frame[index].loc[index_counter] = [int(subj_nr+1),split,med_rt,int(ttype),selected_item,'alcohol', (index), alc_individ_subject_counts[index], alc_individ_subject_nrusedtrials[index], alc_individ_subject_mean[index]];
# 					data_frame[index].loc[index_counter+1] = [int(subj_nr+1),split,med_rt,int(ttype),selected_item,'cigarette', (index), cig_cue_individ_subject_counts[index], cig_individ_subject_nrusedtrials[index], cig_cue_individ_subject_mean[index]];
# 					data_frame[index].loc[index_counter+2] = [int(subj_nr+1),split,med_rt,int(ttype),selected_item,'neutral', (index), neu_individ_subject_counts[index], neu_individ_subject_nrusedtrials[index], neu_individ_subject_mean[index]];
# 				index_counter+=3;
# 							
# 				print "completed subject %s.. \n\n"%subj_nr	
# 
# 			#plot each likelihood looking at items				
# 			for  subj_ms, cue_name, c, a in zip([alc_subject_means_array, cig_cue_subject_means_array, neu_subject_means_array], ['alcohol','cigarette','neutral'], colors, alphas):							
# 				mews = array([nanmean(subj) for subj in subj_ms]); # gaze_array/counts
# 				sems = array([compute_BS_SEM(subj) for subj in subj_ms]);
# 				ax1.plot(linspace(0,2000,2000), mews, lw = 4.0, color = c, alpha = a);
# 				#plot the errorbars
# 				#for x,m,s in zip(linspace(0,1000,1000),mews,sems):
# 				ax1.fill_between(linspace(0,2000,2000), mews-sems, mews+sems, color = c, alpha = a*0.4);
# 				legend_lines.append(mlines.Line2D([],[],color=c,lw=6,alpha = a, label='likelihood(looking at %s) '%cue_name));
# 			#plot the sum of each for a sanity emasure to ensure they equate to one
# 			#agg = [(nanmean(a)+nanmean(b)+nanmean(c)) for a,b,c in zip(alc_subject_means_array, cig_cue_subject_means_array, neu_subject_means_array)];
# 			#ax1.plot(linspace(0,1000,1000),agg,color = 'gray', lw = 3.0);
# 			#legend_lines.append(mlines.Line2D([],[],color='gray',lw=4, alpha = 1.0, label='sum of all'));
# 			ax1.plot(linspace(0,2000,2000),linspace(0.33,0.333,2000),color = 'gray', lw = 3.0, ls='dashed');
# 			legend_lines.append(mlines.Line2D([],[],color='gray',lw=4, alpha = 1.0, ls = 'dashed', label='random'));	
# 			ax1.spines['right'].set_visible(False); ax1.spines['top'].set_visible(False);
# 			ax1.spines['bottom'].set_linewidth(2.0); ax1.spines['left'].set_linewidth(2.0);
# 			ax1.yaxis.set_ticks_position('left'); ax1.xaxis.set_ticks_position('bottom');
# 			ax1.legend(handles=[legend_lines[0],legend_lines[1], legend_lines[2], legend_lines[3]],loc = 2,ncol=1,fontsize = 11); # legend_lines[4]]
# 			title('STIMULUS LOCKED %s %s Average Temporal Gaze Profile, \n Chose %s Trials'%(name, split, selected_item), fontsize = 22);
# 			
# 	#save the databases
# 	[d.to_csv(savepath+'%s_STIMLOCKED_FAST_timepoint_%s_temporal_gaze_profile_LONG.csv'%(name, (i)),index=False) for d,i in zip(fast_data, arange(2000))]; #data.to_csv(savepath+'%s_temporal_gaze_profile.csv'%name,index=False);
# 	[d.to_csv(savepath+'%s_STIMLOCKED_SLOW_timepoint_%s_temporal_gaze_profile_LONG.csv'%(name, (i)),index=False) for d,i in zip(slow_data, arange(2000))];
# 	# ends here			
##################################################################################################################################################################
# 
# def computeLongStimulusLockedTemporalGazeProfilesRTCUTOFF(blocks, ttype, eyed = 'agg'):
# 	#performs the temporal gaze profile analysis from for the STIMULUS-LOCKED data but cuts out trials that are too early/slow on a subject by subject level
# 	#i.e. looks at the 2000 ms after stimulus onset
# 
# 	db = subject_data;
# 	index_counter = 0; #for database calculation
# 	
# 	time_bin_spacing = 0.001;
# 	time_duration = 2.0;
# 
# 	#loop through and get all the trials for each subject
# 	trial_matrix = [[tee for b in bl for tee in b.trials if (tee.skip==0)] for bl in blocks];
# 	
# 	#collect which trial type to run this analysis for
# 	#ttype = int(raw_input('Which trial type? 1 = HighC/HighA, 2 = HighC/LowA, 3 = LowC/HighA, 4 = LowC/LowA: '));
# 	
# 	name = ['high_pref', 'highC_lowA','lowC_highA','lowC_lowA'][ttype-1];
# 	
# 	#create 2000 dataframe objects that will correspond to each time point
# 	data = [pd.DataFrame(columns = ['sub_id','trial_type','selected_item','looked_at_item','timepoint','nr_trials','nr_trials_used_for_likelihood','mean_fix_likelihood']) for i in arange(2000)];
# 	#nr of trials used is the total number of trials used for tht time point (a trial where at least one item was looked at)
# 	#nr_trials_used_for_likelihood is the nr of trials where that specific item was looked at, at the given timepoint
# 	
# 	for selected_item in ['alcohol','cigarette','neutral']:
# 		
# 		fig = figure(); ax1 = gca();
# 		ax1.set_ylim(0.0, 1.0); ax1.set_yticks(arange(0,1.01,0.1)); ax1.set_xlim([0,2000]);
# 		ax1.set_ylabel('Likelihood of fixating',size=18); ax1.set_xlabel('Time with respect to stimulus onset, ms',size=18,labelpad=11);
# 		ax1.set_xticks([0,500, 1000, 1500, 2000]);
# 		#ax1.set_xticklabels(['-2000', '-1500', '-1000', '-500', '0']);
# 		colors = ['red','blue', 'green']; alphas = [1.0, 1.0, 1.0]; legend_lines = [];		count = 0;	
# 	
# 		# #define arrays for the neutral, alcohol and cigarette items
# 		neu_gaze_array = zeros(time_duration/time_bin_spacing);
# 		neu_counts = zeros(shape(neu_gaze_array));
# 		neu_subject_means_array = [[] for i in range(2000)]; #use this to store each individual subjects' mean for each time point
# 		neu_subject_agg_counts = []; 
# 		alc_gaze_array = zeros(time_duration/time_bin_spacing);
# 		alc_counts = zeros(shape(alc_gaze_array));
# 		alc_subject_means_array = [[] for i in range(2000)];
# 		alc_subject_agg_counts = []; 
# 		cig_cue_gaze_array = zeros(time_duration/time_bin_spacing);
# 		cig_cue_counts = zeros(shape(cig_cue_gaze_array));
# 		cig_cue_subject_means_array = [[] for i in range(2000)];
# 		cig_subject_agg_counts = []; 	
# 	
# 		for subj_nr,subj in enumerate(trial_matrix):
# 			neu_individ_subject_sum = zeros(time_duration/time_bin_spacing);
# 			neu_individ_subject_counts = zeros(time_duration/time_bin_spacing);
# 			neu_individ_subject_nrusedtrials = zeros(time_duration/time_bin_spacing);
# 			alc_individ_subject_sum = zeros(time_duration/time_bin_spacing);
# 			alc_individ_subject_counts = zeros(time_duration/time_bin_spacing);
# 			alc_individ_subject_nrusedtrials = zeros(time_duration/time_bin_spacing);			
# 			cig_cue_individ_subject_sum = zeros(time_duration/time_bin_spacing);
# 			cig_cue_individ_subject_counts = zeros(time_duration/time_bin_spacing);
# 			cig_individ_subject_nrusedtrials = zeros(time_duration/time_bin_spacing);	
# 	
# 	
# 			#first, get this subjects' average RT information (mean and standard deviations) by collecting all valid RTs in a holder
# 			all_rts = [];
# 			for t in subj:
# 				if ((t.dropped_sample == 0)&(t.didntLookAtAnyItems == 0)&(t.skip == 0)&(sqrt(t.eyeX[0]**2 + t.eyeY[0]**2) < 2.5) \
#                     &(t.trial_type == ttype)&(t.preferred_category == selected_item)):
# 					#cycle through each time point, aggregating the data accordingly
# 					all_rts.append(t.response_time);
# 			mew_rt = mean(all_rts);
# 			sd_rt = std(all_rts);
# 			#get the lower and upper bounds
# 			low_bound = mew_rt - 2*sd_rt;
# 			up_bound = mew_rt + 2*sd_rt;
# 	
# 			for t in subj:
# 				#conditional to differentiate between not-cue trials when selecteing the non-cue or not
# 				#the second conditional include nuetral trials that were preferred only
# 				#notice the last conditional term is determing if the RT is within the bounds
# 				if ((t.dropped_sample == 0)&(t.didntLookAtAnyItems == 0)&(t.skip == 0)&(sqrt(t.eyeX[0]**2 + t.eyeY[0]**2) < 2.5) \
#                     &(t.trial_type == ttype)&(t.preferred_category == selected_item)&((t.response_time >= low_bound)&(t.response_time <= up_bound))):
# 					
# 					1/0
# 					
# 					#cycle through each time point, aggregating the data accordingly
# 					
# 					for i in (arange(2000)):
# 						if (i>=len(t.lookedAtNeutral)):
# 							continue;
# 						elif (isnan(t.lookedAtNeutral[i])):
# 							continue; #nan means they weren't looking at anything at this timepoint
# 						neu_gaze_array[i] += t.lookedAtNeutral[i];
# 						neu_counts[i] += 1;
# 						#put the individual subject data together
# 						neu_individ_subject_sum[i] += t.lookedAtNeutral[i];
# 						neu_individ_subject_counts[i] += 1;
# 						neu_individ_subject_nrusedtrials[i] += t.lookedAtNeutral[i];
# 
# 					for i in (arange(2000)):
# 						if (i>=len(t.lookedAtAlcohol)):
# 							continue;
# 						elif (isnan(t.lookedAtAlcohol[i])):
# 							continue;
# 						#store the alcohol gaze patterns as the cue item
# 						alc_gaze_array[i] += t.lookedAtAlcohol[i];
# 						alc_counts[i] += 1;
# 						#put the individual subject data together
# 						alc_individ_subject_sum[i] += t.lookedAtAlcohol[i];
# 						alc_individ_subject_counts[i] += 1;
# 						alc_individ_subject_nrusedtrials[i] += t.lookedAtAlcohol[i];
# 						
# 					for i in (arange(2000)):
# 						if (i>=len(t.lookedAtCigarette)):
# 							continue;
# 						elif (isnan(t.lookedAtCigarette[i])):
# 							continue;							
# 						#store the cigarette items as the not_cue item
# 						cig_cue_gaze_array[i] += t.lookedAtCigarette[i];
# 						cig_cue_counts[i] += 1;
# 						#put the individual subject data together
# 						cig_cue_individ_subject_sum[i] += t.lookedAtCigarette[i];
# 						cig_cue_individ_subject_counts[i] += 1;
# 						cig_individ_subject_nrusedtrials[i] += t.lookedAtCigarette[i];
# 						
# 			neu_individ_subject_mean = neu_individ_subject_sum/neu_individ_subject_counts; #calculate the mean for this subject at each time point
# 			[neu_subject_means_array[index].append(ind_mew) for index,ind_mew in zip(arange(2000),neu_individ_subject_mean)]; #append this to the array for each subject
# 			[neu_subject_agg_counts.append(ct) for ct in neu_individ_subject_counts]; #store number of trials here		
# 			alc_individ_subject_mean = alc_individ_subject_sum/alc_individ_subject_counts; #calculate the mean for this subject at each time point
# 			[alc_subject_means_array[index].append(ind_mew) for index,ind_mew in zip(arange(2000),alc_individ_subject_mean)]; #append this to the array for each subject
# 			[alc_subject_agg_counts.append(ct) for ct in alc_individ_subject_counts];
# 			cig_cue_individ_subject_mean = cig_cue_individ_subject_sum/cig_cue_individ_subject_counts; #calculate the mean for this subject at each time point
# 			[cig_cue_subject_means_array[index].append(ind_mew) for index,ind_mew in zip(arange(2000),cig_cue_individ_subject_mean)]; #append this to the array for each subject
# 			[cig_subject_agg_counts.append(ct) for ct in cig_cue_individ_subject_counts];						
# 						
# 			for index in arange(2000):
# 				#make sure to reverse the time point from index...
# 				data[index].loc[index_counter] = [int(subj_nr+1),int(ttype),selected_item,'alcohol', (index), alc_individ_subject_counts[index], alc_individ_subject_nrusedtrials[index], alc_individ_subject_mean[index]];
# 				data[index].loc[index_counter+1] = [int(subj_nr+1),int(ttype),selected_item,'cigarette', (index), cig_cue_individ_subject_counts[index], cig_individ_subject_nrusedtrials[index], cig_cue_individ_subject_mean[index]];
# 				data[index].loc[index_counter+2] = [int(subj_nr+1),int(ttype),selected_item,'neutral', (index), neu_individ_subject_counts[index], neu_individ_subject_nrusedtrials[index], neu_individ_subject_mean[index]];
# 			index_counter+=3;
# 						
# 			print "completed subject %s.. \n\n"%subj_nr							
# 
# 		#plot each likelihood looking at items				
# 		for  subj_ms, cue_name, c, a in zip([alc_subject_means_array, cig_cue_subject_means_array, neu_subject_means_array], ['alcohol','cigarette','neutral'], colors, alphas):							
# 			mews = array([nanmean(subj) for subj in subj_ms]); # gaze_array/counts
# 			sems = array([compute_BS_SEM(subj) for subj in subj_ms]);
# 			ax1.plot(linspace(0,2000,2000), mews, lw = 4.0, color = c, alpha = a);
# 			#plot the errorbars
# 			#for x,m,s in zip(linspace(0,1000,1000),mews,sems):
# 			ax1.fill_between(linspace(0,2000,2000), mews-sems, mews+sems, color = c, alpha = a*0.4);
# 			legend_lines.append(mlines.Line2D([],[],color=c,lw=6,alpha = a, label='likelihood(looking at %s) '%cue_name));
# 		#plot the sum of each for a sanity emasure to ensure they equate to one
# 		#agg = [(nanmean(a)+nanmean(b)+nanmean(c)) for a,b,c in zip(alc_subject_means_array, cig_cue_subject_means_array, neu_subject_means_array)];
# 		#ax1.plot(linspace(0,1000,1000),agg,color = 'gray', lw = 3.0);
# 		#legend_lines.append(mlines.Line2D([],[],color='gray',lw=4, alpha = 1.0, label='sum of all'));
# 		ax1.plot(linspace(0,2000,2000),linspace(0.33,0.333,2000),color = 'gray', lw = 3.0, ls='dashed');
# 		legend_lines.append(mlines.Line2D([],[],color='gray',lw=4, alpha = 1.0, ls = 'dashed', label='random'));	
# 		ax1.spines['right'].set_visible(False); ax1.spines['top'].set_visible(False);
# 		ax1.spines['bottom'].set_linewidth(2.0); ax1.spines['left'].set_linewidth(2.0);
# 		ax1.yaxis.set_ticks_position('left'); ax1.xaxis.set_ticks_position('bottom');
# 		ax1.legend(handles=[legend_lines[0],legend_lines[1], legend_lines[2], legend_lines[3]],loc = 2,ncol=1,fontsize = 11); # legend_lines[4]]
# 		title('STIMULUS LOCKED RTCUTOFF %s Average Temporal Gaze Profile, \n Chose %s Trials'%(name, selected_item), fontsize = 22);
# 
# 	#save the databases
# 	[d.to_csv(savepath+'STIMLOCKED_%s_timepoint_%s_temporal_gaze_profile_LONG_RTCUTOFF.csv'%(name, (i)),index=False) for d,i in zip(data, arange(2000))]; #data.to_csv(savepath+'%s_temporal_gaze_profile.csv'%name,index=False);
# 	# ends here
# 
# 	print "\n\ncompleted trial type %s.. \n\n\n\n"%name
################################################################################################################################################################## 
# 
# def computeLongStimulusLockedTemporalGazeProfilesRTCUTOFFAGGREGATED(blocks, ttype, eyed = 'agg'):
# 	#performs the temporal gaze profile analysis from for the STIMULUS-LOCKED data but cuts out trials that are too early/slow on a group level
# 	#i.e. looks at the 2000 ms after stimulus onset
# 	#This likely doesn't change much as far as cutting out the early timepoints
# 	#should I consider the individuals subject data?
# 
# 	db = subject_data;
# 	index_counter = 0; #for database calculation
# 	
# 	time_bin_spacing = 0.001;
# 	time_duration = 2.0;
# 
# 	#loop through and get all the trials for each subject
# 	trial_matrix = [[tee for b in bl for tee in b.trials if (tee.skip==0)] for bl in blocks];
# 	
# 	#collect which trial type to run this analysis for
# 	#ttype = int(raw_input('Which trial type? 1 = HighC/HighA, 2 = HighC/LowA, 3 = LowC/HighA, 4 = LowC/LowA: '));
# 	
# 	name = ['high_pref', 'highC_lowA','lowC_highA','lowC_lowA'][ttype-1];
# 	
# 	#create 2000 dataframe objects that will correspond to each time point
# 	data = [pd.DataFrame(columns = ['sub_id','trial_type','selected_item','looked_at_item','timepoint','nr_trials','nr_trials_used_for_likelihood','mean_fix_likelihood']) for i in arange(2000)];
# 	#nr of trials used is the total number of trials used for tht time point (a trial where at least one item was looked at)
# 	#nr_trials_used_for_likelihood is the nr of trials where that specific item was looked at, at the given timepoint
# 	
# 	for selected_item in ['alcohol','cigarette','neutral']:
# 		
# 		fig = figure(); ax1 = gca();
# 		ax1.set_ylim(0.0, 1.0); ax1.set_yticks(arange(0,1.01,0.1)); ax1.set_xlim([0,2000]);
# 		ax1.set_ylabel('Likelihood of fixating',size=18); ax1.set_xlabel('Time with respect to stimulus onset, ms',size=18,labelpad=11);
# 		ax1.set_xticks([0,500, 1000, 1500, 2000]);
# 		#ax1.set_xticklabels(['-2000', '-1500', '-1000', '-500', '0']);
# 		colors = ['red','blue', 'green']; alphas = [1.0, 1.0, 1.0]; legend_lines = [];		count = 0;	
# 	
# 		# #define arrays for the neutral, alcohol and cigarette items
# 		neu_gaze_array = zeros(time_duration/time_bin_spacing);
# 		neu_counts = zeros(shape(neu_gaze_array));
# 		neu_subject_means_array = [[] for i in range(2000)]; #use this to store each individual subjects' mean for each time point
# 		neu_subject_agg_counts = []; 
# 		alc_gaze_array = zeros(time_duration/time_bin_spacing);
# 		alc_counts = zeros(shape(alc_gaze_array));
# 		alc_subject_means_array = [[] for i in range(2000)];
# 		alc_subject_agg_counts = []; 
# 		cig_cue_gaze_array = zeros(time_duration/time_bin_spacing);
# 		cig_cue_counts = zeros(shape(cig_cue_gaze_array));
# 		cig_cue_subject_means_array = [[] for i in range(2000)];
# 		cig_subject_agg_counts = []; 	
# 	
# 		#first, get ALL subjects'RTs together
# 		# then calculate group level average RT information (mean and standard deviations) by collecting all valid RTs in a holder
# 		all_rts = [];
# 		for subj_nr,subj in enumerate(trial_matrix):
# 			for t in subj:
# 				if ((t.dropped_sample == 0)&(t.didntLookAtAnyItems == 0)&(t.skip == 0)&(sqrt(t.eyeX[0]**2 + t.eyeY[0]**2) < 2.5) \
#                     &(t.trial_type == ttype)&(t.preferred_category == selected_item)):
# 
# 					all_rts.append(t.response_time);
# 		#calculate group level RT stats			
# 		mew_rt = mean(all_rts);
# 		sd_rt = std(all_rts);
# 		#get the lower and upper bounds for the group level
# 		low_bound = mew_rt - 2*sd_rt;
# 		up_bound = mew_rt + 2*sd_rt;						
# 			
# 		for subj_nr,subj in enumerate(trial_matrix):			
# 			neu_individ_subject_sum = zeros(time_duration/time_bin_spacing);
# 			neu_individ_subject_counts = zeros(time_duration/time_bin_spacing);
# 			neu_individ_subject_nrusedtrials = zeros(time_duration/time_bin_spacing);
# 			alc_individ_subject_sum = zeros(time_duration/time_bin_spacing);
# 			alc_individ_subject_counts = zeros(time_duration/time_bin_spacing);
# 			alc_individ_subject_nrusedtrials = zeros(time_duration/time_bin_spacing);			
# 			cig_cue_individ_subject_sum = zeros(time_duration/time_bin_spacing);
# 			cig_cue_individ_subject_counts = zeros(time_duration/time_bin_spacing);
# 			cig_individ_subject_nrusedtrials = zeros(time_duration/time_bin_spacing);	
# 	
# 			for t in subj:
# 				#conditional to differentiate between not-cue trials when selecteing the non-cue or not
# 				#the second conditional include nuetral trials that were preferred only
# 				#notice the last conditional term is determing if the RT is within the bounds
# 				if ((t.dropped_sample == 0)&(t.didntLookAtAnyItems == 0)&(t.skip == 0)&(sqrt(t.eyeX[0]**2 + t.eyeY[0]**2) < 2.5) \
#                     &(t.trial_type == ttype)&(t.preferred_category == selected_item)&((t.response_time >= low_bound)&(t.response_time <= up_bound))):
# 					
# 					#cycle through each time point, aggregating the data accordingly
# 					
# 					for i in (arange(2000)):
# 						if (i>=len(t.lookedAtNeutral)):
# 							continue;
# 						elif (isnan(t.lookedAtNeutral[i])):
# 							continue; #nan means they weren't looking at anything at this timepoint
# 						neu_gaze_array[i] += t.lookedAtNeutral[i];
# 						neu_counts[i] += 1;
# 						#put the individual subject data together
# 						neu_individ_subject_sum[i] += t.lookedAtNeutral[i];
# 						neu_individ_subject_counts[i] += 1;
# 						neu_individ_subject_nrusedtrials[i] += t.lookedAtNeutral[i];
# 
# 					for i in (arange(2000)):
# 						if (i>=len(t.lookedAtAlcohol)):
# 							continue;
# 						elif (isnan(t.lookedAtAlcohol[i])):
# 							continue;
# 						#store the alcohol gaze patterns as the cue item
# 						alc_gaze_array[i] += t.lookedAtAlcohol[i];
# 						alc_counts[i] += 1;
# 						#put the individual subject data together
# 						alc_individ_subject_sum[i] += t.lookedAtAlcohol[i];
# 						alc_individ_subject_counts[i] += 1;
# 						alc_individ_subject_nrusedtrials[i] += t.lookedAtAlcohol[i];
# 						
# 					for i in (arange(2000)):
# 						if (i>=len(t.lookedAtCigarette)):
# 							continue;
# 						elif (isnan(t.lookedAtCigarette[i])):
# 							continue;							
# 						#store the cigarette items as the not_cue item
# 						cig_cue_gaze_array[i] += t.lookedAtCigarette[i];
# 						cig_cue_counts[i] += 1;
# 						#put the individual subject data together
# 						cig_cue_individ_subject_sum[i] += t.lookedAtCigarette[i];
# 						cig_cue_individ_subject_counts[i] += 1;
# 						cig_individ_subject_nrusedtrials[i] += t.lookedAtCigarette[i];
# 						
# 			neu_individ_subject_mean = neu_individ_subject_sum/neu_individ_subject_counts; #calculate the mean for this subject at each time point
# 			[neu_subject_means_array[index].append(ind_mew) for index,ind_mew in zip(arange(2000),neu_individ_subject_mean)]; #append this to the array for each subject
# 			[neu_subject_agg_counts.append(ct) for ct in neu_individ_subject_counts]; #store number of trials here		
# 			alc_individ_subject_mean = alc_individ_subject_sum/alc_individ_subject_counts; #calculate the mean for this subject at each time point
# 			[alc_subject_means_array[index].append(ind_mew) for index,ind_mew in zip(arange(2000),alc_individ_subject_mean)]; #append this to the array for each subject
# 			[alc_subject_agg_counts.append(ct) for ct in alc_individ_subject_counts];
# 			cig_cue_individ_subject_mean = cig_cue_individ_subject_sum/cig_cue_individ_subject_counts; #calculate the mean for this subject at each time point
# 			[cig_cue_subject_means_array[index].append(ind_mew) for index,ind_mew in zip(arange(2000),cig_cue_individ_subject_mean)]; #append this to the array for each subject
# 			[cig_subject_agg_counts.append(ct) for ct in cig_cue_individ_subject_counts];						
# 						
# 			for index in arange(2000):
# 				#make sure to reverse the time point from index...
# 				data[index].loc[index_counter] = [int(subj_nr+1),int(ttype),selected_item,'alcohol', (index), alc_individ_subject_counts[index], alc_individ_subject_nrusedtrials[index], alc_individ_subject_mean[index]];
# 				data[index].loc[index_counter+1] = [int(subj_nr+1),int(ttype),selected_item,'cigarette', (index), cig_cue_individ_subject_counts[index], cig_individ_subject_nrusedtrials[index], cig_cue_individ_subject_mean[index]];
# 				data[index].loc[index_counter+2] = [int(subj_nr+1),int(ttype),selected_item,'neutral', (index), neu_individ_subject_counts[index], neu_individ_subject_nrusedtrials[index], neu_individ_subject_mean[index]];
# 			index_counter+=3;
# 						
# 			print "completed subject %s.. \n\n"%subj_nr							
# 
# 		#plot each likelihood looking at items				
# 		for  subj_ms, cue_name, c, a in zip([alc_subject_means_array, cig_cue_subject_means_array, neu_subject_means_array], ['alcohol','cigarette','neutral'], colors, alphas):							
# 			mews = array([nanmean(subj) for subj in subj_ms]); # gaze_array/counts
# 			sems = array([compute_BS_SEM(subj) for subj in subj_ms]);
# 			ax1.plot(linspace(0,2000,2000), mews, lw = 4.0, color = c, alpha = a);
# 			#plot the errorbars
# 			#for x,m,s in zip(linspace(0,1000,1000),mews,sems):
# 			ax1.fill_between(linspace(0,2000,2000), mews-sems, mews+sems, color = c, alpha = a*0.4);
# 			legend_lines.append(mlines.Line2D([],[],color=c,lw=6,alpha = a, label='likelihood(looking at %s) '%cue_name));
# 		#plot the sum of each for a sanity emasure to ensure they equate to one
# 		#agg = [(nanmean(a)+nanmean(b)+nanmean(c)) for a,b,c in zip(alc_subject_means_array, cig_cue_subject_means_array, neu_subject_means_array)];
# 		#ax1.plot(linspace(0,1000,1000),agg,color = 'gray', lw = 3.0);
# 		#legend_lines.append(mlines.Line2D([],[],color='gray',lw=4, alpha = 1.0, label='sum of all'));
# 		ax1.plot(linspace(0,2000,2000),linspace(0.33,0.333,2000),color = 'gray', lw = 3.0, ls='dashed');
# 		legend_lines.append(mlines.Line2D([],[],color='gray',lw=4, alpha = 1.0, ls = 'dashed', label='random'));	
# 		ax1.spines['right'].set_visible(False); ax1.spines['top'].set_visible(False);
# 		ax1.spines['bottom'].set_linewidth(2.0); ax1.spines['left'].set_linewidth(2.0);
# 		ax1.yaxis.set_ticks_position('left'); ax1.xaxis.set_ticks_position('bottom');
# 		ax1.legend(handles=[legend_lines[0],legend_lines[1], legend_lines[2], legend_lines[3]],loc = 2,ncol=1,fontsize = 11); # legend_lines[4]]
# 		title('STIMULUS LOCKED RTCUTOFFAGGREGATED %s Average Temporal Gaze Profile, \n Chose %s Trials'%(name, selected_item), fontsize = 22);
# 
# 	#save the databases
# 	[d.to_csv(savepath+'STIMLOCKED_%s_timepoint_%s_temporal_gaze_profile_LONG_RTCUTOFFAGGREGATED.csv'%(name, (i)),index=False) for d,i in zip(data, arange(2000))]; #data.to_csv(savepath+'%s_temporal_gaze_profile.csv'%name,index=False);
# 	# ends here
# 
# 	print "\n\ncompleted trial type %s.. \n\n\n\n"%name
##################################################################################################################################################################

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