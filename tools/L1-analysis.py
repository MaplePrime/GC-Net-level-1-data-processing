# -*- coding: utf-8 -*-
"""
Created on %(date)s

@author: %(username)s

tip list:
    %matplotlib inline
    %matplotlib qt
    import pdb; pdb.set_trace()
"""
import os, sys
import PROMICE_toolbox as ptb
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import nead
import os.path
from os import path
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates
# Set the locator
years = mdates.YearLocator()   # every year
months = mdates.MonthLocator()  # every month
years_fmt = mdates.DateFormatter('%Y')

# %% L0 overview
path_to_L0N = 'L0M/'
site_list = pd.read_csv('metadata/GC-Net_location.csv',header=0)[1:2]

for site, ID in zip(site_list.Name,site_list.ID):
    plt.close('all')
    print('# '+str(ID)+ ' ' + site)
    filename = path_to_L0N+str(ID).zfill(2)+'-'+site+'.csv'
    if not path.exists(filename):
        print('Warning: No file for station '+str(ID)+' '+site)
        continue
    ds = nead.read(filename)
    df = ds.to_dataframe()
    df=df.reset_index(drop=True)
    df.timestamp = pd.to_datetime(df.timestamp)
    df = df.set_index('timestamp').replace(-999,np.nan)

    # % plotting variables
    def new_fig():
        fig, ax = plt.subplots(6,1,sharex=True, figsize=(15,15))
        plt.subplots_adjust(left = 0.1, right=0.9, top = 0.9, bottom = 0.1, wspace=0.2, hspace=0.05)
        return fig, ax


    fig, ax = new_fig()
    count = 0
    count_fig = 0
    for i, var in enumerate(df.columns):
        if var[-2:]=='qc':
            continue
        if var[-3:]=='max':
            continue
        if var[-5:]=='stdev':
            continue
        # print(var)

        if var+'_qc' in df.columns:
            print(var)

            for qc_code in np.flip(np.unique(df[var+'_qc'])):
                df.loc[df[var+'_qc']==qc_code,var].plot(ax=ax[count])
        else:
            df[var].plot(ax=ax[count])

        ax[count].set_ylabel(var)
        ax[count].grid()
        # if site != 'E-GRIP':
        #     ax[count].axes.xaxis.set_major_formatter(years_fmt)
        #     ax[count].axes.xaxis.set_major_locator(years)
            # ax[count].axes.xaxis.set_minor_locator(months)
        ax[count].set_xlim((df.index[0],df.index[-1]))
        count=count+1

        if count == 6:
            ax[0].set_title(site)
            plt.savefig('figures/L0_diagnostic/'+str(ID)+'_'+site+'_'+str(count_fig),bbox_inches='tight')
            print('![](../figures/L0_diagnostic/'+str(ID)+'_'+site+'_'+str(count_fig)+'.png)')
            count_fig = count_fig+1
            fig, ax = new_fig()
            count = 0
    if count < 6:
        count=count-1
        ax[count].xaxis.set_tick_params(which='both', labelbottom=True)
        if site != 'E-GRIP':
            ax[count].axes.xaxis.set_major_formatter(years_fmt)
            ax[count].axes.xaxis.set_major_locator(years)
            # ax[count].axes.xaxis.set_minor_locator(months)
        for k in range(count+1,len(ax)):
            ax[k].set_axis_off()
        ax[0].set_title(site)
        plt.savefig('figures/L0_diagnostic/'+str(ID)+'_'+site+'_'+str(count_fig),bbox_inches='tight')
        print('![](../figures/L0_diagnostic/'+str(ID)+'_'+site+'_'+str(count_fig)+'.png)')
# %run tocgen.py out/L0_overview.md out/L0_overview_toc.md


# %% L1 overview
site_list = pd.read_csv('metadata/GC-Net_location.csv',header=0)  #.iloc[7:,:]

for site, ID in zip(site_list.Name,site_list.ID):
    plt.close('all')
    print('# '+str(ID)+ ' ' + site)
    filename = 'L1/'+str(ID).zfill(2)+'-'+site+'.csv'
    if not path.exists(filename):
        print('Warning: No file for station '+str(ID)+' '+site)
        continue
    ds = nead.read(filename)
    df = ds.to_dataframe()
    df=df.reset_index(drop=True)
    df.timestamp = pd.to_datetime(df.timestamp)
    df = df.set_index('timestamp').replace(-999,np.nan)
    # df =df.loc['2019':,:]
    if df.shape[0] == 0:
        print('no data since 2019')
        continue
    # % plotting variables
    def new_fig():
        fig, ax = plt.subplots(6,1,sharex=True, figsize=(15,15))
        plt.subplots_adjust(left = 0.1, right=0.9, top = 0.95, bottom = 0.1, wspace=0.2, hspace=0.05)
        plt.suptitle(site)
        return fig, ax


    fig, ax = new_fig()
    count = 0
    count_fig = 0
    for i, var in enumerate(df.columns):
        if var[-2:]=='qc':
            continue
        if var[-3:]=='max':
            continue
        # if var[-5:]=='stdev':
        #     continue
        # print(var)

        
        df[var].plot(ax=ax[count])
        ax[count].set_ylabel(var)
        ax[count].grid()
        # ax[count].axes.xaxis.set_major_formatter(years_fmt)
        # ax[count].axes.xaxis.set_major_locator(years)
        # ax[count].axes.xaxis.set_minor_locator(months)
        ax[count].set_xlim((df.index[0],df.index[-1]))
        count=count+1
        if count == 6:
            ax[0].set_title(site)
            plt.savefig('figures/L1_overview/'+str(ID)+'_'+site+'_'+str(count_fig),bbox_inches='tight')
            print('![](figures/L1_overview/'+str(ID)+'_'+site+'_'+str(count_fig)+'.png)')
            count_fig = count_fig+1
            fig, ax = new_fig()
            count = 0
    if count < 6:
        ax[count].xaxis.set_tick_params(which='both', labelbottom=True)
        # ax[count].axes.xaxis.set_major_formatter(years_fmt)
        # ax[count].axes.xaxis.set_major_locator(years)
        for k in range(count+1,len(ax)):
            ax[k].set_axis_off()
        ax[0].set_title(site)
        plt.savefig('figures/L1_overview/'+str(ID)+'_'+site+'_'+str(count_fig),bbox_inches='tight')
        print('![](figures/L1_overview/all variables/'+str(ID)+'_'+site+'_'+str(count_fig)+'.png)')

# %run tocgen.py out/L1_overview.md out/L1_overview_toc.md

# %% L1 temperature overview
plt.close('all')
site_list = pd.read_csv('metadata/GC-Net_location.csv',header=0)#.iloc[:1]
for site, ID in zip(site_list.Name,site_list.ID):
    variable_list = np.array(['TA1', 'TA2', 'TA3', 'TA4'])

    print('# '+str(ID)+ ' ' + site)
    filename = 'L1/'+str(ID).zfill(2)+'-'+site+'.csv'
    if not path.exists(filename):
        print('Warning: No file for station '+str(ID)+' '+site)
        continue
    ds = nead.read(filename)
    df = ds.to_dataframe()
    df=df.reset_index(drop=True)
    df.timestamp = pd.to_datetime(df.timestamp)
    df = df.set_index('timestamp').replace(-999,np.nan)

    # % plotting variables
    fig, ax = plt.subplots(4,1,sharex=True, figsize=(15,15))
    plt.subplots_adjust(left = 0.1, right=0.9, top = 0.95, bottom = 0.1, wspace=0.2, hspace=0.05)
    plt.suptitle(site)
    count = 0
    count_fig = 0
    if len(variable_list)==0:
        variable_list = df.columns
    else:
        variable_list = variable_list[np.isin(variable_list, df.columns.values)]
    for i, var in enumerate(variable_list):       
        df[var].plot(ax=ax[count])
        ax[count].set_ylabel(var)
        ax[count].grid()
        # ax[count].axes.xaxis.set_major_formatter(years_fmt)
        # ax[count].axes.xaxis.set_major_locator(years)
        # ax[count].axes.xaxis.set_minor_locator(months)
        ax[count].set_xlim((df.index[0],df.index[-1]))
        count=count+1
    plt.savefig('figures/L1_overview/air temperature diagnostic/'+str(ID)+'_'+site+'_temperature',bbox_inches='tight')
    print('![](figures/L1_overview/air temperature diagnostic/'+str(ID)+'_'+site+'_temperature.png)')


# %run tocgen.py out/L1_overview.md out/L1_overview_toc.md

# %% L1 temperature TC vs C1000 comp
# plt.close('all')
site_list = pd.read_csv('metadata/GC-Net_location.csv',header=0)
for site, ID in zip(site_list.Name,site_list.ID):
    
    print('# '+str(ID)+ ' ' + site)
    filename = 'L1/'+str(ID).zfill(2)+'-'+site+'.csv'
    if not path.exists(filename):
        print('Warning: No file for station '+str(ID)+' '+site)
        continue
    ds = nead.read(filename)
    df = ds.to_dataframe()
    df=df.reset_index(drop=True)
    df.timestamp = pd.to_datetime(df.timestamp)
    df = df.set_index('timestamp').replace(-999,np.nan)
    if 'TA2' not in df.columns:
        df['TA2'] = np.nan
    # % plotting variables
    fig = plt.figure(figsize=(15,15))
    plt.suptitle(site)
    
    ax1 = fig.add_axes([0.1, 0.55, 0.5, 0.4])
    df['TA1'].plot(ax=ax1, label = 'TA1')
    df['TA3'].plot(ax=ax1, label = 'TA3')
    (df['TA1']-df['TA3']).plot(ax=ax1, label = 'TA1-TA3')
    ax1.set_ylabel('Air temperature \n Lower level')
    ax1.grid()
    ax1.legend()

    ax2 = fig.add_axes([0.65, 0.55, 0.32, 0.4])
    ax2.plot(df['TA1'],  df['TA3'], marker='.', linestyle='None')
    ax2.annotate('ME = %0.2f'%(df['TA1']- df['TA3']).mean(), (0.05,0.9), xycoords='axes fraction',fontweight = 'bold')
    ax2.annotate('ME = %0.2f'%(df['TA1']- df['TA4']).mean(), (0.05,0.8), xycoords='axes fraction')
    ax2.plot([-50, 10],[-50, 10],'k')
    ax2.set_xlabel('TA1')
    ax2.set_ylabel('TA3')
    ax2.grid()
    
    ax3 = fig.add_axes([0.1, 0.1, 0.5, 0.4])
    df['TA2'].plot(ax=ax3, label = 'TA2')
    df['TA4'].plot(ax=ax3, label = 'TA4')
    (df['TA2']-df['TA4']).plot(ax=ax3, label = 'TA2-TA4')
    # (df['TA2']-df['TA3']).plot(ax=ax3, label = 'TA2-TA3')
    ax3.set_ylabel('Air temperature \n Lower level')
    ax3.grid()
    ax3.legend()

    ax4 = fig.add_axes([0.65, 0.1, 0.32, 0.4])
    ax4.plot(df['TA2'],  df['TA4'], marker='.', linestyle='None')
    ax4.annotate('ME = %0.2f'%(df['TA2']- df['TA4']).mean(), (0.05,0.9), xycoords='axes fraction',fontweight = 'bold')
    ax4.plot([-50, 10],[-50, 10],'k')
    ax4.set_xlabel('TA2')
    ax4.set_ylabel('TA4')
    ax4.grid()
    # break
    fig.savefig('figures/L1_overview/air temperature diagnostic/'+str(ID)+'_'+site+'_temperature_diag',bbox_inches='tight')
    print('![](figures/L1_overview/air temperature diagnostic/'+str(ID)+'_'+site+'_temperature_diag.png)')
    
# %% RH1 vs RH2
plt.close('all')
site_list = pd.read_csv('metadata/GC-Net_location.csv',header=0)[0:1]
for site, ID in zip(site_list.Name,site_list.ID):
    print('# '+str(ID)+ ' ' + site)
    filename = 'L1/'+str(ID).zfill(2)+'-'+site+'.csv'
    if not path.exists(filename):
        print('Warning: No file for station '+str(ID)+' '+site)
        continue

    ds = nead.read(filename)
    df = ds.to_dataframe()
    df=df.reset_index(drop=True)
    df.timestamp = pd.to_datetime(df.timestamp)
    df = df.set_index('timestamp').replace(-999,np.nan)
    if 'RH2' not in df.columns:
        df['RH2'] = np.nan
    #  plotting variables
    fig = plt.figure(figsize=(15,7))
    plt.suptitle(site)
    
    ax1 = fig.add_axes([0.1, 0.15, 0.5, 0.8])
    df['RH1'].plot(ax=ax1, label = 'RH1')
    df['RH2'].plot(ax=ax1, label = 'RH2')
    (df['RH1']-df['RH2']).plot(ax=ax1, label = 'RH1-RH2')
    ax1.set_ylabel('Relative Humidity (%)')
    ax1.grid()
    ax1.legend()

    ax2 = fig.add_axes([0.65, 0.15, 0.32, 0.8])
    ax2.plot(df['RH1'],  df['RH2'], marker='.', linestyle='None')
    ax2.annotate('ME = %0.2f'%(df['RH1']- df['RH2']).mean(), (0.05,0.9), xycoords='axes fraction',fontweight = 'bold')
    ax2.plot([20, 100],[20, 100],'k')
    ax2.set_xlabel('RH1')
    ax2.set_ylabel('RH2')
    ax2.grid()
    
    # break
    fig.savefig('figures/L1_overview/'+str(ID)+'_'+site+'_RH_diag',bbox_inches='tight')
    # print('![](figures/L1_overview/air temperature diagnostic/'+str(ID)+'_'+site+'_temperature.png)')
    
   
    # %% Time shift search
plt.close('all')
site_list = pd.read_csv('metadata/GC-Net_location.csv',header=0)
from pandas.tseries.offsets import DateOffset
for site, ID in zip(site_list.Name,site_list.ID):

    print('# '+str(ID)+ ' ' + site)
    filename = 'L1/'+str(ID).zfill(2)+'-'+site+'.csv'
    if not path.exists(filename):
        print('Warning: No file for station '+str(ID)+' '+site)
        continue
    
    ds = nead.read(filename)
    df = ds.to_dataframe()
    df=df.reset_index(drop=True)
    df.timestamp = pd.to_datetime(df.timestamp)
    df = df.set_index('timestamp').replace(-999,np.nan)
    
    # plt.figure()
    for year in df.index.year.unique()[:-1]:
        df1 = df.loc[df.index.year==year,:].resample('H').mean().copy()
        df2 = df.loc[df.index.year==year+1,:].resample('H').mean().copy()
        df2.index = df2.index - DateOffset(years=1)
        msk = df2.index.intersection(df1.index)
        df1 = df1.loc[msk,:]
        df2 = df2.loc[msk,:]
        df1 = df1[~df1.index.duplicated(keep='first')].fillna(0)
        df2 = df2[~df2.index.duplicated(keep='first')].fillna(0)
        
        if (df1['ISWR'] != 0).any() and (df2['ISWR'] != 0).any():
            lags, cor, _,_ = plt.xcorr(df1['ISWR'].values, df2['ISWR'].values, 
                      usevlines=False, maxlags=20, normed=True,
                      linestyle='-',
                      label=str(year)+' vs '+str(year+1))
            if lags[cor.argmax()] != 0:
                print(year, 'max cor at', lags[cor.argmax()], 'timesteps')
                fig = plt.figure(figsize=(15,7))
                plt.suptitle(site+': max cor at '+str(lags[cor.argmax()])+' timesteps')
                ax1 = fig.add_axes([0.1, 0.15, 0.8, 0.8])
                df1['ISWR'].plot(ax=ax1, label = str(year))
                df2['ISWR'].plot(ax=ax1, label = str(year+1))
                ax1.set_ylabel('ISWR')
                ax1.grid()
                ax1.legend()
    # plt.grid()

    # plt.legend()
        
    # fig.savefig('figures/L1_overview/'+str(ID)+'_'+site+'_ISWR_diag',bbox_inches='tight')
    
# %% Instrument height assessment and 2m T assessment
# from jaws_tools import extrapolate_temp

site_list = pd.read_csv('metadata/GC-Net_location.csv',header=0)
for site, ID in zip(site_list.Name,site_list.ID):
    
    print('# '+str(ID)+ ' ' + site)
    filename = 'L1/'+str(ID).zfill(2)+'-'+site+'.csv'
    if not path.exists(filename):
        print('Warning: No file for station '+str(ID)+' '+site)
        continue
    ds = nead.read(filename)
    df = ds.to_dataframe()
    df=df.reset_index(drop=True)
    df.timestamp = pd.to_datetime(df.timestamp)
    df = df.set_index('timestamp').replace(-999,np.nan)
    if 'TA2' not in df.columns:
        df['TA2'] = np.nan
    # % plotting variables

    fig, ax = plt.subplots(2,1,sharex=True)
    df.HW1.plot(ax=ax[0])
    df.HW2.plot(ax=ax[0])
    
    df.TA1.plot(ax=ax[1])
    df.TA2.plot(ax=ax[1])
    # T2m = extrapolate_temp(df, 2)
    
#%% Surface height overview

site_list = pd.read_csv('metadata/GC-Net_location.csv',header=0)

fig, ax = plt.subplots(4,5,figsize=(15,15))
ax = ax.flatten()
plt.subplots_adjust(left = 0.05, right=0.99, top = 0.94, bottom = 0.1, wspace=0.15, hspace=0.25)
count = 0
for site, ID in zip(site_list.Name,site_list.ID):
    print('# '+str(ID)+ ' ' + site)
    filename = 'L1/'+str(ID).zfill(2)+'-'+site+'.csv'
    if not path.exists(filename):
        print('Warning: No file '+filename)
        continue
    ds = nead.read(filename)
    df = ds.to_dataframe()
    df=df.reset_index(drop=True)
    df.timestamp = pd.to_datetime(df.timestamp)
    df = df.set_index('timestamp').replace(-999,np.nan).interpolate(limit=24*7).resample('D').mean()
    # plotting height
    df.HS1.plot(ax=ax[count])
    df.HS2.plot(ax=ax[count])
    ax[count].set_title(str(ID)+ ' ' + site)
    ax[count].set_xlabel('')
    ax[count].grid()
    # ax[i,j].axes.xaxis.set_major_locator(locator)
    count = count+1
for k in range(count,len(ax)):
    ax[k].set_axis_off()

fig.savefig('figures/L1_overview/HS_overview.png',bbox_inches='tight')

#%% Comparison with JoG dataset
import xarray as xr
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
gcnet_path = 'C:/Data_save/Data JoG 2020/Corrected/data out/'
site_list = ['CP1','DYE_2','NASA_SE','NASA_E','NASA_U','Saddle','TUNU_N','Summit', 'SouthDome']
site_list = sorted(site_list)

fig, ax = plt.subplots(3,3)
plt.subplots_adjust(left = 0.1, right=0.9, top = 0.9, bottom = 0.1, wspace=0.2, hspace=0.3)
for i, folder in enumerate(site_list):

    site = site_list[i]
    sys.stdout.flush()
    ds = xr.open_dataset(gcnet_path+'/'+site+'_surface.nc')
    df = ds.to_dataframe().resample('D').mean()
    i, j = np.unravel_index(i,np.shape(ax))


    trend = np.array([])
    for year in range(1998,2018):
        df2 = df.loc[df.index.year==year,:]

        X = df2.index.dayofyear.values
        Y = df2.H_surf_mod.values  -np.nanmean(df2.H_surf_mod.values)
        mask = ~np.isnan(X) & ~np.isnan(Y)
        lm = LinearRegression()
        if ~np.any(mask):
            continue
        lm.fit(X[mask].reshape(-1, 1), Y[mask].reshape(-1, 1))
        if lm.coef_[0][0]<0:
            continue
        Y_pred = lm.predict(X[mask].reshape(-1, 1))

        ax[i,j].plot(X,Y)
        ax[i,j].plot(X[mask].reshape(-1, 1),Y_pred,linestyle='--')
        ax[i,j].set_xlabel('')
        ax[i,j].set_title(site)
        trend=np.append(trend, lm.coef_[0][0]*365)
    trend_avg = np.nanmean(trend[trend>0])
    trend_std = np.nanstd(trend[trend>0])
    ax[i,j].text(100,ax[i,j].get_ylim()[1]*0.8,  ' '+str(round(trend_avg,2))+' $\pm$ '+str(round(trend_std,2))+' $m yr^{-1}$')
    print(site+' '+str(round(trend_avg,2))+' +/- '+str(round(trend_std,2))+' m yr-1')
    # print(lm.intercept_)

ax[1,0].set_ylabel('Surface height (m)')
ax[2,1].set_xlabel('Day of year')

#%% Data availability
site_list = pd.read_csv('metadata/GC-Net_location.csv',header=0)  #.iloc[7:,:]
plt.close('all')
for site, ID in zip(site_list.Name,site_list.ID):
    filename = 'L1/'+str(ID).zfill(2)+'-'+site.replace(' ','')+'.csv'
    if not path.exists(filename):
        continue
    ds = nead.read(filename)
    df = ds.to_dataframe()
    df=df.reset_index(drop=True)
    df.timestamp = pd.to_datetime(df.timestamp)
    df = df.set_index('timestamp').replace(-999,np.nan)

    df_m = df.resample('M').count()/31/24*100
    cols = [col for col in ['ISWR', 'OSWR','NSWR','TA1','TA2','TA3','TA4','RH1','RH2','VW1','DW1','VW2','DW2','P','HW1','HW2'] if col in df_m.columns]
    cols.reverse()
    df_m = df_m[cols]
 
    fig = plt.figure(figsize=(12,5))
    plt.pcolor(df_m.transpose(), cmap='magma')
    major_ticks = [d for d in df_m.index if d.month==1]
    ticks_labels = [d.year for d in df_m.index if d.month==1]
        
    plt.xticks(np.arange(np.where(df_m.index==major_ticks[0])[0],
                         len(major_ticks)*12, 12), ticks_labels)
    ax = plt.gca()
    ax.set_xticks(np.arange(0, len(df_m.index), 1), minor=True)
    plt.xticks(rotation = 45)
    plt.yticks(np.arange(0.5, len(df_m.columns), 1), df_m.columns)
    plt.colorbar(label='Data availability (%)')
    plt.title(site)
    fig.savefig('figures/L1_overview/data_availability_'+site.replace(' ','_')+'.png',bbox_inches='tight')
    print('![](../figures/L1_overview/data_availability_'+site.replace(' ','_')+'.png)')

# %% Instrument height assessment
name_alias = {'DY2': 'DYE2', 'CP1':'Crawford Point 1'}

site_list = pd.read_csv('metadata/GC-Net_location.csv',header=0)[19:]
# you can select a site by specifying f.e.:
# site_list  = site_list.iloc[2:3,:]
# site_list  = site_list.iloc[8:9,:] # Dye-2 
# site_list  = site_list.iloc[2:3,:] # Crawford Point 1
# site_list  = site_list.iloc[15:16,:] # nasa-se 
plt.close('all')
for site, ID in zip(site_list.Name,site_list.ID):
    print('# '+str(ID)+ ' ' + site)
    filename = 'L1/'+str(ID).zfill(2)+'-'+site.replace(' ','')+'.csv'
    if not path.exists(filename):
        print('Warning: No file for station '+str(ID)+' '+site)
        continue
    ds = nead.read(filename)
    df = ds.to_dataframe()
    df=df.reset_index(drop=True)
    df[df == -999] = np.nan
    df['time'] = pd.to_datetime(df.timestamp)
    df = df.set_index('time')

    # read observed instrument height data
    try:      
        url = 'https://docs.google.com/spreadsheets/d/172LNxgYevqwO892zrc98UDMAVTQmJ0XZB5kmMLme4GM/gviz/tq?tqx=out:csv&sheet='+site.replace(' ','%20')
        pd.read_csv(url).to_csv('metadata/maintenance summary/'+site+'.csv')
    except:
        print('Cannot download maintenance summary. Using local file.')
        pass

    obs_df = pd.read_csv('metadata/maintenance summary/'+site+'.csv')    
    obs_df['date'] = pd.to_datetime(obs_df['date'], utc=True)
    obs_df = obs_df.set_index('date')
    useful_columns = ['W1 before (cm)', 'W1 after (cm)',
                  'W2 before (cm)','W2 after (cm)',
                  'T1 before (cm)','T1 after (cm)',
                  'T2 before (cm)','T2 after (cm)']
    if obs_df[useful_columns].notnull().sum().sum() == 0:
        print('no intrument height reported at ', site)
        continue
    obs_df[useful_columns] = obs_df[useful_columns]/100
    
    # read photogrammetry heights
    df_photo = pd.read_csv('metadata/photogrammetry_instrument_height_20220425.csv')
    df_photo = df_photo.replace({'site': name_alias})
    df_photo = df_photo.loc[df_photo.site==site, :]
    df_photo['date'] = pd.to_datetime(df_photo[['year','month','day']])
    df_photo = df_photo.set_index('date').drop(columns = ['site','year','month','day'])
    
    fig = plt.figure()
    ax = plt.subplot(111)
    sym_size=20
    mult=0.6
    # Plotting observed instrument heights
    obs_df['W1 before (cm)'].plot(ax=ax, marker = '>', linestyle = 'None',
              markerfacecolor='none', markersize=sym_size*mult,c='C0',label='HW1 obs before')
    obs_df['W2 before (cm)'].plot(ax=ax, marker = '>', linestyle = 'None',
              markerfacecolor='none', markersize=sym_size*mult,c='C1',label='HW2 obs before')
    obs_df['W1 after (cm)'].plot(ax=ax, marker = '<', linestyle = 'None',
              markerfacecolor='none', markersize=sym_size*mult,c='C0',label='HW1 obs after')
    obs_df['W2 after (cm)'].plot(ax=ax, marker = '<', linestyle = 'None',
              markerfacecolor='none', markersize=sym_size*mult,c='C1',label='HW2 obs after')
    
    obs_df['T1 before (cm)'].plot(ax=ax, marker = '>', linestyle = 'None',
              markerfacecolor='none', markersize=sym_size*mult,c='C2',label='HT1 obs before')
    obs_df['T2 before (cm)'].plot(ax=ax, marker = '>', linestyle = 'None',
              markerfacecolor='none', markersize=sym_size*mult,c='C3',label='HT2 obs before')
    obs_df['T1 after (cm)'].plot(ax=ax, marker = '<', linestyle = 'None',
              markerfacecolor='none', markersize=sym_size*mult,c='C2',label='HT1 obs afer')
    obs_df['T2 after (cm)'].plot(ax=ax, marker = '<', linestyle = 'None',
              markerfacecolor='none', markersize=sym_size*mult,c='C3',label='HT2 obs after')
    
    df_photo[['Wz1','Wz2','THz1','THz2']].plot(ax=ax, marker='o', linestyle='None')

    df['HW1'].plot(ax =ax, c='C0',label='HW1')
    df['HW2'].plot(ax =ax, c='C1',label='HW2')
    
    plt.ylabel('Height above surface (m)')
    plt.title(site+' profile instrument heights')
    plt.legend()
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    
    plt.savefig('figures/L1_overview/instrument_height_assessment/'+site+'_height_comparison.png', bbox_inches='tight',dpi=250)
    print('![](../figures/L1_overview/instrument_height_assessment/'+site.replace(' ','%20')+'_height_comparison.png)')

#%run tools/tocgen.py out/L1_intrument_heights.md out/L1_intrument_heights_toc.md

