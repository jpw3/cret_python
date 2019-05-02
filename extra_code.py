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

