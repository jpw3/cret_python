from pylab import *
import pandas
 
 
path = '/Users/jameswilmott/Desktop/ET_data.xlsx';
data = read_excel(path, header = 0);
colors=['blue','red','white'];

#Chosen alcohol trials

alc = data.chose_alc_alc_avg_total_time
cig = data.chose_alc_cig_avg_total_time
neu = data.chose_alc_neu_avg_total_time

fig = figure(figsize = (12.8,7.64)); ax1=gca();
ax1.set_xlim([0.4,3.3]); ax1.set_xticks([1,1.7,2.4]);
ax1.set_xticklabels(['Alcohol','Cigarettes','Neutral']);
ax1.set_ylim(0.,700); ax1.set_yticks(array([0,100,200,300,400,500,600,700]));


ax1.bar(1, mean(alc), color = colors[0], width = 0.6, edgecolor='black', linewidth=1.5);
ax1.bar(1.7, mean(cig), color = colors[1], width = 0.6, edgecolor='black', linewidth=1.5);
ax1.bar(2.4, mean(neu), color = colors[2], width = 0.6, edgecolor='black', linewidth=1.5);

#errorbars
ax1.errorbar(1, mean(alc), yerr=[[0],[compute_BS_SEM(alc)]],color='black',lw=1.5, capsize = 20);
ax1.errorbar(1.7, mean(cig), yerr=[[0],[compute_BS_SEM(cig)]],color='black',lw=1.5, capsize = 20);
ax1.errorbar(2.4, mean(neu), yerr=[[0],[compute_BS_SEM(neu)]],color='black',lw=1.5, capsize = 20);
 
ax1.spines['right'].set_visible(False); ax1.spines['top'].set_visible(False);
ax1.spines['bottom'].set_linewidth(2.0); ax1.spines['left'].set_linewidth(2.0);
ax1.yaxis.set_ticks_position('left'); ax1.xaxis.set_ticks_position('bottom');

savefig('/Users/jameswilmott/Desktop/selected_alc.png',dpi=400);

labels = [item.get_text() for item in ax1.get_xticklabels()]; labels[0]=''; labels[1]=''; labels[2]='';
ax1.set_xticklabels(labels);
ax1.set_yticklabels(['','','','','','','','','','','','','','']);

savefig('/Users/jameswilmott/Desktop/selected_alc_NAKED.eps',dpi=400);

 #Chosen cigarette trials
 
alc = data.chose_cig_alc_avg_total_time
cig = data.chose_cig_cig_avg_total_time
neu = data.chose_cig_neu_avg_total_time

fig = figure(figsize = (12.8,7.64)); ax1=gca();
ax1.set_xlim([0.4,3.3]); ax1.set_xticks([1,1.7,2.4]);
ax1.set_xticklabels(['Alcohol','Cigarettes','Neutral']);
ax1.set_ylim(0.,700); ax1.set_yticks(array([0,100,200,300,400,500,600,700]));


ax1.bar(1, mean(alc), color = colors[0], width = 0.6, edgecolor='black', linewidth=1.5);
ax1.bar(1.7, mean(cig), color = colors[1], width = 0.6, edgecolor='black', linewidth=1.5);
ax1.bar(2.4, mean(neu), color = colors[2], width = 0.6, edgecolor='black', linewidth=1.5);

#errorbars
ax1.errorbar(1, mean(alc), yerr=[[0],[compute_BS_SEM(alc)]],color='black',lw=1.5, capsize = 20);
ax1.errorbar(1.7, mean(cig), yerr=[[0],[compute_BS_SEM(cig)]],color='black',lw=1.5, capsize = 20);
ax1.errorbar(2.4, mean(neu), yerr=[[0],[compute_BS_SEM(neu)]],color='black',lw=1.5, capsize = 20);
 
ax1.spines['right'].set_visible(False); ax1.spines['top'].set_visible(False);
ax1.spines['bottom'].set_linewidth(2.0); ax1.spines['left'].set_linewidth(2.0);
ax1.yaxis.set_ticks_position('left'); ax1.xaxis.set_ticks_position('bottom');

savefig('/Users/jameswilmott/Desktop/selected_cig.png',dpi=400);

labels = [item.get_text() for item in ax1.get_xticklabels()]; labels[0]=''; labels[1]=''; labels[2]='';
ax1.set_xticklabels(labels);
ax1.set_yticklabels(['','','','','','','','','','','','','','']);

savefig('/Users/jameswilmott/Desktop/selected_cig_NAKED.eps',dpi=400);


 #Chosen neutral trials
 
alc = data.chose_neu_alc_avg_total_time
cig = data.chose_neu_cig_avg_total_time
neu = data.chose_neu_neu_avg_total_time

fig = figure(figsize = (12.8,7.64)); ax1=gca();
ax1.set_xlim([0.4,3.3]); ax1.set_xticks([1,1.7,2.4]);
ax1.set_xticklabels(['Alcohol','Cigarettes','Neutral']);
ax1.set_ylim(0.,700); ax1.set_yticks(array([0,100,200,300,400,500,600,700]));


ax1.bar(1, mean(alc), color = colors[0], width = 0.6, edgecolor='black', linewidth=1.5);
ax1.bar(1.7, mean(cig), color = colors[1], width = 0.6, edgecolor='black', linewidth=1.5);
ax1.bar(2.4, mean(neu), color = colors[2], width = 0.6, edgecolor='black', linewidth=1.5);

#errorbars
ax1.errorbar(1, mean(alc), yerr=[[0],[compute_BS_SEM(alc)]],color='black',lw=1.5, capsize = 20);
ax1.errorbar(1.7, mean(cig), yerr=[[0],[compute_BS_SEM(cig)]],color='black',lw=1.5, capsize = 20);
ax1.errorbar(2.4, mean(neu), yerr=[[0],[compute_BS_SEM(neu)]],color='black',lw=1.5, capsize = 20);
 
ax1.spines['right'].set_visible(False); ax1.spines['top'].set_visible(False);
ax1.spines['bottom'].set_linewidth(2.0); ax1.spines['left'].set_linewidth(2.0);
ax1.yaxis.set_ticks_position('left'); ax1.xaxis.set_ticks_position('bottom');

savefig('/Users/jameswilmott/Desktop/selected_neu.png',dpi=400);

labels = [item.get_text() for item in ax1.get_xticklabels()]; labels[0]=''; labels[1]=''; labels[2]='';
ax1.set_xticklabels(labels);
ax1.set_yticklabels(['','','','','','','','','','','','','','']);

savefig('/Users/jameswilmott/Desktop/selected_neu_NAKED.eps',dpi=400);


