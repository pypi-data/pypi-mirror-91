#!/usr/bin/env python
# coding: utf-8

# # Surface Complexation Analytic Workbook
# 
# 
# ### This interactive workbook is an streamlined analytic workflow enabling scientists to perform data visualization techniques and stastical analyses to learn about their surface complexation dataset and to build a surface complexation model using a random forest algorithm.

# ### Required Imports

# In[1]:


#importing package dependencies
import csv
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn import preprocessing
from scipy import stats
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, RandomForestRegressor
from sklearn import metrics
from sklearn.feature_selection import SelectFromModel
from pprint import pprint
from sklearn.model_selection import RandomizedSearchCV
import warnings
from pprint import pprint
from sklearn.model_selection import cross_val_score
from sklearn.metrics import recall_score
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import RobustScaler


# 

# ### Import your data

# In[2]:


#----------Description-----------
#Purpose: This function imports user data
#Returns: Pandas DataFrame of user's data
def import_data(data):
    """
    Function import_data() imports user's csv and returns it as a pandas data frame.
    This function is repetitive, but if someone isn't familiar with python, it could be easier for them to
    use especially if they do not want to invest the time to study python and package syntax.
    Args:
        data (str): Name of CSV file
    Returns:
        pandas dataframe
    Notes:
        user's csv file name should originate from Mavrik's database.
   
    
    """
    df=pd.read_csv(data) # consider adding excel functionality
    return df


# 

# In[3]:


# df=import_data('nick_csv.csv')
# df


# In[ ]:





# # SETTING YOUR TARGET

# In[4]:


def set_target(target='KD'):
    
    """
    
    Function set_target() gives the user the power to set the variable 
    they wish to run analytics on. By default the target variable is set
    to KD. Other input options include KA or KDU.
    
    Args:
        target (str): single string, either KD, KDU, KA. Defaults to KD.
        Returns:
        target (str) - GLOBAL VARIABLE
     Notes:
        Array of targets functionality has not been tested, stick to 
        string as of 7/15
    
    
    """
    
    
    z=True #arbitrary truth setting
    if len(target[0])==1 and len(target)<1:
        if target=='KD' or target=='KA' or target=='KDU':
               z=True
            
        else:
            
            warnings.warn("\n\n %s is not a valid target variable" %target)
            z=False
            
    if len(target[0])>1:
        for i in range(len(target)):
            if target[i]=='KA' or target[i]=='KDU' or target[i]=='KD':
                z=True
                
            else:
                z=False
                warnings.warn("\n\n %s is not a valid target variable" %target[i])
 
    global target_var
    if z==True:
         target_var= [target]
    else:
        target_var=None
    


# In[5]:


# set_target()


# In[6]:


# target_var


# In[ ]:





# In[ ]:





# In[ ]:





# In[35]:


def pull_data(userdata,target,add_target=False):
    """Function pull_data simplifies Mavrik's dataset for the purpose of
    running data analytics
    
    Args:
        userdata (str or pandas dataframe): If str(), csv imported as pandas
            dataframe. If userdata is pandas dataframe, dataset is stored.
        target (str) : target must equal one of these.('KD','KA','KDU'). 
            Target default is 'KD'
        add_target (bool): True - target appended to end of df. 
    Returns:
        pandas dataframe : Reference,Mineral_source,pH, Sorbent initial 
            concentration,Concentration Sorbed material 
            Electrolytes Sorbent initial concentration, Amot Sorbed, pH, 
            site density, and target variable(s) are the columns.
   
    """
    if isinstance(userdata,str):
        df=pd.read_csv(userdata) #user data could be string linking LLNL csv to filepoath
    if isinstance(userdata,str)==False:
        df=userdata  #user data could be string already defined as a Pandas DataFrame
  
    
   
    ###Defining new columns to add to nick's dataframe
    #desired columns we hope to extract which are unknown to us as these exist within the data
    # and not as columns themselves
    subs = [ 'Sorbent', 'Electrolyte','Gas','Mineral']
    ncols = df.columns
    extract=[]
    mineral=[]
    ### This extracts the columns which need to be sorted for potentional column names
    for i in subs:
        res = list(filter(lambda x: i in x, ncols))  
        if i ==subs[0]:
            extract.append(res[0])
        if i==subs[1]:
            for a in range(len(res)):
                if a%4==0:
                    extract.append(res[a])               
        if i==subs[2]:
            for a in range(len(res)):
                if a%4==0:
                    extract.append(res[a])
        if i==subs[3]:
            for a in range(len(res)):
                if a==3 or a==6 or a==9:
                    mineral.append(res[a])


    ##Now that we have the column names that we need to check, we  now need to pull the unique input values

    #defining empty array
    extract2=[] # will be filled with unique electrlytes, gases, and sorbents

    for i in extract:
        u=df[i].unique()
        extract2.append(u)
    #extract2 contains unique and nan values
    ## need to get rid of nan values

    cleanedlist=[]
    extdf = pd.DataFrame(extract2)
    for i in range(len(extract2)):
        for j in range(len(extract2[i])):
            idx = extract2[i][j]
            cleanedlist.append(idx)
    unique_vals=[]
    for i in range(len(cleanedlist)):
        idx = cleanedlist[i]
        if idx is np.nan or pd.isna(idx):
            pass
        else:
            unique_vals.append(idx)

    testdf=pd.DataFrame([],columns=unique_vals,index=df.index)
    # unique_vals
    # testdf

    for j in range(len(extract)): #indexing into Nicks dataframe using my extracted column names
        ndfcol = df[extract[j]]  #series  of a specific column from nicks dataframe
        for i in range(len(unique_vals)): #iterating through my list of unique gases and electrolytes
            for row in range(len(ndfcol)): #iterating through the column
                if ndfcol[row]==unique_vals[i]: #checks to see if column value is equal to the unique vals
                    #need to find column index
                    ncols=df.columns # nick's columns
                    for dfcol in range(len(ncols)):
                        if extract[j]==ncols[dfcol]:
                            testdf.iloc[row][i]=df.iloc[row][dfcol+1]
    
    
    mineraldf=pd.DataFrame([],columns=mineral)
    mineraldf
    p=[]
    for dfcol in range(len(ncols)):
        for a in range(len(mineral)):
            z=mineral[a]
            if z == ncols[dfcol]:
                testdf[z]=df.iloc[:,dfcol]
    
    idxcols=['Reference','Mineral_source','pH']
    newz={df.columns.get_loc(c): c for idxcols, c in enumerate(df.columns)}
    for i in range(len(newz)):
        for j in range(len(idxcols)):
            if idxcols[j] == newz[i]:
                testdf.insert(j,idxcols[j],df.iloc[:,i])
    testdf.insert(4,'Sorbed_val',df['Sorbed_val']) 
    
    def calc_target_variable(df):
        #returns not just the target variable, but all KD, KDU, and KA values
        species_sorbed=df.iloc[:,4]
        initial_species=df.iloc[:,3]
        species_aq =initial_species-species_sorbed
        KD=species_sorbed/species_aq

        gml=1/1000 * df.iloc[:,16]
        KDU=KD/gml

        m2g=df.iloc[:,17]
        KA=KDU/m2g
        data=[KD,KDU,KA]
        shape=np.shape(data)
        data_trans=np.transpose(data)
        datadf=pd.DataFrame(data_trans,columns=['KD','KDU','KA'])
        return datadf
    def site_density(df):
        SD=pd.DataFrame(df.iloc[:,18]*df.iloc[:,17]*df.iloc[:,16]*10**18, columns=['sites/L'])
        return SD
        
        
        
    testdf=pd.concat([testdf,site_density(testdf)],axis=1)    
    KDdata=calc_target_variable(testdf)
    KDtarget_data=pd.DataFrame([])
    if add_target==True:
        KD_columns=KDdata.columns
        for j in target:
            if j in KD_columns:
                KDtarget_data=pd.concat([KDtarget_data,KDdata[j]],axis=1)
        finaldf=pd.concat([testdf,KDtarget_data],axis=1)
    if add_target==False:
        finaldf=pd.concat([testdf,KDdata],axis=1)

                
    
#     if add_target==True:
        
#         tcols = calc_target_variable(testdf)
#         testdf=pd.concat([testdf,tcols],axis=1) 
#     else:
#         pass
        
    #portion where target variable can be conconcated:
    finaldf.index.name='Experiment'
    finaldf.index+=1
    finaldf=finaldf.drop(['Mineralsites','MineralSA','Mineral_val'],axis=1)
#     finaldf=finaldf.replace(np.nan,0)
    return finaldf


# In[8]:


# df=pull_data('nick_csv.csv',add_target=False)


# In[9]:


# df


# In[10]:


def scale_data(df,scale='log10',remove_nan=False,scale_target=False):
    """
    
    Function scale_data scales the data by using log10 or by standardizing. 
    The standardization protocol centers data around 0 with a range of 
    [-1,1].
    Args:
        df (pandas dataframe) : dataframe must come from the pull_data() 
                function.
        scale (str) : 'log10' or 'standardize'.
        remove_na (bool) : enables users to remove nan data as KD and 
                sorbed values can return NaN if logged.
        
    Returns:
        Pandas dataframe : structure from pull_data is preserved but been
                scaled.
    
    
    """


    df2=df.copy() #dataframe with scaled values
    if len(df2[df2.iloc[:,4]<0])>1: #pulling out negative sorbed values
        df2 = df2[df2.iloc[:,4]>0]
    df2_cols=df2.columns
    df3=df2.drop(df2.iloc[:,0:2],axis=1)

    # moves data and logs data such that pH is untouched and everything else is logged10
    if scale=='log10':
        df3.iloc[:,0]=10**df2.iloc[:,2]
        df3_zero=df3.fillna(0.0)
        for i in df3.columns:
            df3[i]=np.log10(df3_zero[i])
        scaledf=df3.replace(-np.inf,np.nan)
        scaledf.insert(0,'Reference',df.iloc[:,0])
        scaledf.insert(1,'Material_source',df.iloc[:,1])
     


    #standardizes data
    if scale=='standardize':          
        scaler=StandardScaler()
        scaler.fit(df3)
        sk_scaled_df=scaler.transform(df3)
        df2.iloc[:,2:len(df2_cols)]=sk_scaled_df
        scaledf=df2
    #normalizes data 
    if scale=='normalize':
      
        scaler = MinMaxScaler() 
        sk_scaled_df = scaler.fit_transform(df3)
        df2.iloc[:,2:len(df2_cols)]=sk_scaled_df
        scaledf=df2
    #sklearn robust scaling    
    if scale =='robust':
        scaler=RobustScaler()
        sk_scaled_df=scaler.fit_transform(df3)
        df2.iloc[:,2:len(df2_cols)]=sk_scaled_df
        scaledf=df2
    
    #does not scale data
    if scale =='none':
        
        scaledf=df2
    
    if scale_target:
        pass
    else:
        KDvals = df.iloc[:,[-3,-2,-1]]
        scaledf.iloc[:,[-3,-2,-1]]=KDvals
      
    
    return scaledf
            #return flagger(scaledf)[0], flagger(scaledf)[1]

    

        
#     scaled_df_with_flags=flagger(scaledf)
#     if len(scaled_df_with_flags)>0 and remove_nan==False:
#         warnings.warn("\n\n*************************WARNING***WARNING***WARNING***WARNING***WARNING***WARNING***WARNING***************************"
#             "\nScaling produced NaN values, consider removal by setting input remove_na=True."
#             "\nTo view scaled data with NaN: scale_data()[0]"
#             "\nTo view only NaN sorbed and KD data: scale_data()[1]")
#         return scaled_df_with_flags
#     if len(scaled_df_with_flags)==2 and remove_nan==True:
#         warnings.warn("\n You have NaN data but they have been removed")
#         return scaled_df_with_flags[0]
#     else: 
#         return  scaled_df_with_flags
    
# def flagger(flaggerdf):


#     """
#     Function flagger() flags indexes which data happens to be nan and 
#     returns dataframe.

#     Args:
#         flaggerdf (pandas dataframe) : dataframe user wants to be flagged
#     Returns:
#         IF NAN VALUES:
#             pandas dataframe : dataset indexed into important nan data.
#             pandas dataframe : dataset with scaled data.
#         NO NAN VALUES:
#             pandas dataframe: data set with scaled data.
    
#         """
    
#     if len(flaggerdf[flaggerdf.iloc[:,4]<0])>1:
#         na_free = flaggerdf[flaggerdf.iloc[:,4]>0]
#     if len(flaggerdf[~flaggerdf.iloc[:,4].notna()])>1:
#         na_free=flaggerdf[flaggerdf.iloc[:,4].notna()]
    
    
# #         na_free = flaggerdf[flaggerdf.iloc[:,4].notna()]
# #     if scale =='none':
# #         na_free = flaggerdf[flaggerdf.iloc[:,4]>1]
#     only_na = flaggerdf[(~flaggerdf.index.isin(na_free.index))]
#     if len(only_na)>0:

#         return  na_free, only_na
#     if len(only_na)==0:
#         return na_free

    
        


# In[ ]:





# In[11]:


# scaled_data=scale_data(df,remove_na=True)




def df_for_plots(df):
    """returns dataframe usable for plotting routines"""
    returndf = df.drop(df.iloc[:,0:2], axis=1)
    returndf = returndf.replace(np.nan,0)
    return returndf


# In[12]:





# In[36]:


def plot_target(df,target):
    """
    Function plot_target returns a distrubtion plot of the target variable
    Args:
        df (pandas dataframe) : dataframe, the return from either from pull_data or scale_data
        target (str) : Either 'KD', 'KA', 'KDU'. Default set to 'KD' 
    Returns:
        plot: Distrubtion plot of target variable
    
    """
    
### column name must be a string
    print(df[target].describe())
    plt.figure(figsize=(9, 8))
    sns.distplot(df[target], color='g', bins=100, hist_kws={'alpha': 0.4});


# In[14]:





# In[15]:


def plot_hist(df):
    
    """
    Function plot_hist plots a histogram of all the data in the user's dataframe
    
    Args:
        df (pandas.dataframe) : return df from pull_data() or scale_data()
    Returns:
        histogram plot : n x 5 histogram of features and targets
    
    
    """
    df.hist(figsize=(16, 20), bins=50, xlabelsize=8, ylabelsize=8);


# In[16]:





# In[37]:


def find_corr(df,r_corr_min,p_val_max,target):
    """
    
    Function find_corr computes correlations, pvalues and features of input dataset with respect to target and
    input criteria.
    Args:
        df (pandas dataframe) : return from pull_data() or scale_data()
        r_corr_min (int) : minimum value correlation you wish your features to have
        p_val_max (int) : maximum value p-value you wish your features to have
        target (str) : can be 'KD','KDU','KA'. Default is 'KD' 
    Returns:
        dataframe : yields r-correlations and pvalues of all features taken with respect to target
        list :  containing strings representing features from data meeting user's criteria.
    
    """
    df=df.drop(df.iloc[:,0:2],axis=1) #drops the first two columns
# target_indices = []
# for i in target:
#     idx=list(df.columns).index(i)
#     target_indices.append(idx)
# df=scaled_data
# r_corr_min=.01
# p_val_max = .2
    rdf=[]
    pdf=[]
    features=[]
    rp_array_cols = []
    target=target_var
    target_indice = list(df.columns).index(target[0])
    X=[]
    Y=[]

    df_cols = list(df.columns.values)
    for i in range(len(df.columns)):
        good_idxs = df.loc[:,df_cols[i]].dropna(how='all').index
        x = df.loc[good_idxs,df_cols[i]].values
    #     X.append(x)
    #     print(len(df_cols))
    #     print(np.shape(X))

        y = df.loc[good_idxs,df_cols[len(df_cols)-1]].values
        r,p=stats.pearsonr(x,y)
        rdf.append(r)
        pdf.append(p)
        if abs(r)>=r_corr_min and abs(p)<=p_val_max:
            features.append(df.columns[i])


    rparray=[[rdf],[pdf]]
    a,b,c,=np.shape(rparray)

    rpar=np.reshape(rparray,[a,c])


    rpdf=pd.DataFrame(rpar,columns=df.columns,index=['r corr','p-value'])
    return rpdf,features


# In[18]:


# find_corr(df_log,.2,.1)[0]


# In[19]:


# find_corr(df_log,.2,.1)[1]


# In[38]:


def find_randp(df, target):
    """
     
     Function find_randp() returns find_corr() first return value which is the r and p dataframe.

     Args:
         df (pandas dataframe) : from pull_data or scale_Data
         
     Returns:
         pandas dataframe : containg pvalues and correlations with respect to user defined target
     
     """
    r_corr_min=0.001
    p_val_max=.9
    return find_corr(df,r_corr_min,p_val_max)[0]

    


# In[21]:


# find_randp(df_log)


# In[22]:


# def find_features(df, r_corr_min,p_val_max):
def find_features(df, r_corr_min, p_val_max):

    """

    Function find_features returns find_corr()'s second return value which is a list of strings containing
    features that fit the users criteria for feature selection

    Args:
        df (pandas dataframe) : from pull_data() or scale_data()
        r_corr_min (int) : Minimum correlation user wants to select for features.
        p_val_max (int) : Maximum p value user wants to use to select for features.

    Returns:
        list : features meeting user criteria stored in list contained as strings [GLOBAL VARIABLE]

    """
    
    global df_feats
    feats_wKD = find_corr(df,r_corr_min,p_val_max)[1] 
    feats=[]
    for i in feats_wKD:
        if 'K' in i and len(i)<4:
            pass
        else:
            feats.append(i)
    df_feats=feats
    return feats
    
            
           
            
     
#     global f_feature
#         f_feature = function_features
#     return function_features


# In[23]:


# z=find_features(df_log,.01,.9)


# In[39]:


def plot_pairplot(df,target):
    
    """
    Function plot_pairplot returns array of plots, feature as independent and target as dependent variable
    
    Args:
        df (pandas dataframe) : from pull_data() or scale__data()
        target (str) : can be either 'KD', 'KA', or 'KDU'. Default set to 'KD'
    
    Returns:
        array of plots : showing target dependencies on fetures
    
    """
    for i in range(0, len(df.columns), 5):
        sns.pairplot(data=df,
                    x_vars=df.columns[i:i+5],
                    y_vars=target[0])


# In[25]:





# In[26]:


# df_plots=df_for_plots(df_log)


# In[27]:


# plot_pairplot(df_plots)


# In[29]:




# def corrdot(*args, **kwargs):
#     corr_r = args[0].corr(args[1], 'pearson')
#     corr_text = round(corr_r, 2)
#     ax = plt.gca()
#     font_size = abs(corr_r) * 80 + 5
#     ax.annotate(corr_text, [.5, .5,],  xycoords="axes fraction",
#                 ha='center', va='center', fontsize=font_size)

# def corrfunc(x, y, **kws):
#     r, p = stats.pearsonr(x, y)
#     p_stars = ''
#     if p <= 0.05:
#         p_stars = '*'
#     if p <= 0.01:
#         p_stars = '**'
#     if p <= 0.001:
#         p_stars = '***'
#     ax = plt.gca()
#     ax.annotate(p_stars, xy=(0.65, 0.6), xycoords=ax.transAxes,
#                 color='red', fontsize=70)
def plot_corrscatt(df):
    
    """
    Function plot_corrscatt plots the scatterplots, regression of the scatterplots and prints 1-3 stars based upon 
    the p-value rank. Three stars is low p-value, 1 is high. See code for limit.
    
    Args:
    df (pandas dataframe) : user data
    
    Return:
    plot n*n size where n is your number of columns in your input dataframe.
    
    """
    
    def corrdot(*args, **kwargs):
        corr_r = args[0].corr(args[1], 'pearson')
        corr_text = round(corr_r, 2)
        ax = plt.gca()
        font_size = abs(corr_r) * 80 + 5
        ax.annotate(corr_text, [.5, .5,],  xycoords="axes fraction",
                    ha='center', va='center', fontsize=font_size)

    def corrfunc(x, y, **kws):
        r, p = stats.pearsonr(x, y)
        p_stars = ''
        if p <= 0.05:
            p_stars = '*'
        if p <= 0.01:
            p_stars = '**'
        if p <= 0.001:
            p_stars = '***'
        ax = plt.gca()
        ax.annotate(p_stars, xy=(0.65, 0.6), xycoords=ax.transAxes,
                    color='red', fontsize=70)
    
    
    sns.set(style='white', font_scale=1.6)
    iris = df 
    g = sns.PairGrid(iris, aspect=1.5, diag_sharey=False, despine=False)
    g.map_lower(sns.regplot, lowess=True, ci=False,
                line_kws={'color': 'red', 'lw': 1},
                scatter_kws={'color': 'black', 's': 20})
   
    g.map_diag(sns.distplot, color='black',
           kde_kws={'color': 'red', 'cut': 0.7, 'lw': 1,'bw':1.5},
           hist_kws={'histtype': 'bar', 'lw': 2,
                     'edgecolor': 'k', 'facecolor':'grey'})
#     except RuntimeError as re:
#         if str(re).startswith("Selected KDE bandwidth is 0. Cannot estimate density."):
#             sns.distplot(
#                 kde_kws={'bw': 0.1})
#         else:
#             raise re
    g.map_diag(sns.rugplot, color='black')
    g.map_upper(corrdot)
    g.map_upper(corrfunc)
    g.fig.subplots_adjust(wspace=0, hspace=0)

    # Remove axis labels
    for ax in g.axes.flatten():
        ax.set_ylabel('')
        ax.set_xlabel('')

    # Add titles to the diagonal axes/subplots
    for ax, col in zip(np.diag(g.axes), iris.columns):
        ax.set_title(col, y=0.82, fontsize=26)
        


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[30]:


# plotdf=scaled_data.drop(scaled_data.iloc[:,4:6],axis=1)
# plotdf=plotdf.drop(plotdf.iloc[:,5:9],axis=1)
# plotdf


# In[ ]:





# In[ ]:





# In[31]:






def plot_corrheatmap(userdf,r_corr_min,p_val_max):
    """
    Function plot_corrheatmap visually represnts correlation values between features and targets in user data
    on an n*n sized grid, where n is number of features and targets in data.
    
    Args:
    usedf (pandas dataframe) : user data
    r_corr_min (int,float) : minimum correlation threshold to plot on grid
    p_val_max (int,float) : maximum p_value threshold to plot on grid
    
    Returns:
    heatmap
    
    
    
    """
    
    df = df_for_plots(userdf)
    #plots correlation with a restriction based on the pvalue and pearson correlation
    #Functoinality to add only  pval heatmap can be done.

    df_corr = pd.DataFrame() # Correlation matrix
    df_p = pd.DataFrame()  # Matrix of p-values
    for x in df.columns:
        for y in df.columns:
            corr = stats.pearsonr(df[x], df[y])
            df_corr.loc[x,y] = corr[0]
            df_p.loc[x,y] = corr[1]


    plt.figure(figsize=(12,10))

    sns.heatmap(df_corr[(abs(df_corr)>=r_corr_min) & (abs(df_p)<=p_val_max)],
            cmap='viridis', vmax=1.0, vmin=-1.0, linewidths=0.1,
            annot=True, annot_kws={"size": 8}, square=True);
    return df_corr


# In[ ]:





# In[32]:


#checkfornan

# plot_corrheatmap(df,.4,.5)


# In[ ]:





# In[34]:


def find_PCA(df,features,target,n_components=2,plot=False,clustering=False):

    """
    Function find_PCA performs pca analysis and returns the option of three plots. The first plot is normal biplot
    with coloring scaled with KD. The second plot is biplot with color scaled to lab ID. Third plot is biplot with 
    color scaled to material source.
    
    Args:
        df (pandas dataframe) : from pull_data() or scale_data()
        n_components (int) : number of components for PCA. Default =2.
        features (list of str()) : features user wants to use for PCA. Default is features returned after executing
                                   find_features()
        target (str) : Either 'KD', 'KA', 'KDU'. Default is 'KD'
         
        plot (bool) : True - returns KD color coded plot. False - returns no KD color coded plot. Default = False.
        clustering (bool) : True - returns two plots, color coded for lab ID and Material sources. Default = False.
        
    Returns:
        plot 1 and or plot 2 and plot 3
    
    """
  


    df2=df.copy()
    df2_zeros=df2.replace(np.nan,0)
    df_pca=df2_zeros.drop(df2_zeros.iloc[:,0:2],axis=1)
    df_pca=df_pca.drop(['KDU','KA','KD'],axis=1)
    

    #input#1: n_components - default 2
    n_components = 2
    #inputs#2: features - default - using build in command find feature

  
    # features

    #PCA analyses:

    scaler=StandardScaler()
    pca=PCA(n_components=n_components)
    # # Separating out the features from the dataset
    x = df_pca[features]
    # #applying scaler to ideal data
    scaler.fit(x)
    x=scaler.transform(x)
    # #import PCA 

    # Separating out the target from the dataset
    y = df[target].values
    yvec=y.reshape(y.shape[0])
    # Standardizing the features
    x_new = pca.fit_transform(x)
    resultant = pd.DataFrame(y,columns=[target[0]])
    x_newdf = pd.DataFrame(x_new, columns=['PC 1', 'PC 2'])
    result=pd.concat([x_newdf,resultant],axis=1)

    if plot==False:
        return result
    if plot==True:




    #PLOTTING SEGMENT



        labeldf = df2.iloc[:,0:2]
        labeldf
        lab_labels=labeldf.iloc[:,0]
        source_label = labeldf.iloc[:,1]
        source_label
        lab_uniqs=lab_labels.unique().tolist()
        source_uniqs=source_label.unique().tolist()
        mylabels=[lab_uniqs, source_uniqs]
        lab_label_dict={}
        source_label_dict={}
        ##setting up color dictionaries
        colors='black', 'darkorange', 'darkgreen', 'royalblue','teal','yellow','salmon','lightgreen', 'dodgerblue','magenta'
        for i in range(len(mylabels)):
            for y in range(len(mylabels[i])):
                if i==0:
                    lab_label_dict.update({mylabels[i][y]:colors[y]})
                if i ==1:
                    source_label_dict.update({mylabels[i][y]:colors[y]})
        #color vector for each label
        cvec_lab = [lab_label_dict[label] for label in lab_labels]
        cvec_source=[source_label_dict[label] for label in source_label]

        cvecs=[cvec_lab,cvec_source]
        dictlabels=[lab_label_dict,source_label_dict]


        #**************************************************************************


        #def myplot(score,coeff,labels=None):
        xs = x_new[:,0]
        ys = x_new[:,1]
        coeff=np.transpose(pca.components_[0:2, :])

        n = np.shape(coeff)[0]
        scalex = 1/(xs.max() - xs.min())
        scaley = 1/(ys.max() - ys.min())

        pltx=xs*scalex
        plty=ys*scaley
        #plt.scatter(xs * scalex,ys * scaley, c = y,cmap='seismic')

        #cbar = plt.colorbar()
        #cbar.set_label("Standardized "+str(targetvar))


        labels=None      
        plt.figure(figsize=(8,8))
        plt.scatter(pltx,plty, c=yvec,edgecolor='', alpha=0.5,)
        cbar=plt.colorbar()
        cbar.set_label(str(target))
        aws=.75

        for i in range(n):
            plt.arrow(0, 0, coeff[i,0], coeff[i,1],color = 'red',alpha = .25)
            if labels is None:
                plt.text(coeff[i,0]*aws , coeff[i,1] * aws, features[i], color = 'g', ha = 'center', va = 'center')
            else:
                plt.text(coeff[i,0]* aws, coeff[i,1] * aws, labels[i], color = 'g', ha = 'center', va = 'center')
        # markers = [plt.Line2D([0,0],[0,0],color=color, marker='o', linestyle='') for color in source_label_dict.values()]
        # plt.legend(markers, source_label_dict.keys(), numpoints=1, loc='center left', bbox_to_anchor=(1, 0.5))
        #cbar.set_label("Standardized "+str(targetvar))
        plt.xlim(-1,1)
        plt.ylim(-1,1)
        # Add the axis labels
        plt.xlabel('PC 1 (%.2f%%)' % (pca.explained_variance_ratio_[0]*100))
        plt.ylabel('PC 2 (%.2f%%)' % (pca.explained_variance_ratio_[1]*100)) 

        # Done
        plt.show()

        if clustering==True:
            for j in range(len(dictlabels)):



                labels=None      
                plt.figure(figsize=(8,8))
                plt.scatter(pltx,plty,c=cvecs[j], edgecolor='', alpha=0.5)


                for i in range(n):
                    plt.arrow(0, 0, coeff[i,0], coeff[i,1],color = 'red',alpha =.25)
                    if labels is None:
                        plt.text(coeff[i,0]*aws , coeff[i,1] * aws, features[i], color = 'g', ha = 'center', va = 'center')
                    else:
                        plt.text(coeff[i,0]* aws, coeff[i,1] * aws, labels[i], color = 'g', ha = 'center', va = 'center')
                markers = [plt.Line2D([0,0],[0,0],color=color, marker='o', linestyle='') for color in dictlabels[j].values()]
                plt.legend(markers, dictlabels[j].keys(), numpoints=1, loc='center left', bbox_to_anchor=(1, 0.5))

                plt.xlim(-1,1)
                plt.ylim(-1,1)
                # Add the axis labels
                plt.xlabel('PC 1 (%.2f%%)' % (pca.explained_variance_ratio_[0]*100))
                plt.ylabel('PC 2 (%.2f%%)' % (pca.explained_variance_ratio_[1]*100))
                
     


# In[ ]:


# z=find_features(df,.001,.8)
# type(z)
# # z.remove(target_var[0])
# df # actual dataset
# df_std = scale_data(df,'standardize')
# df_log = scale_data(df,remove_nan=True)
# find_PCA(df,n_components=2,plot=True,clustering=True)


# In[ ]:


# find_PCA(df_log,plot=True,clustering=True)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:


##Regresion analysis 
#input df is 
#step 1 - data preprocessing
#drop sorbed value
def RF_analysis(df,target,n_estimators=50,test_size=.20,
                random_state=int(np.random.randint(0,100,[1,1])),feature_ranks=False,analysis=False,plot=False):
   
   """
   
   Function RF_regressor runs sklearn random forest regressor once and conducts analyses on the single run. 
   Analyses include model evaluation metrics, MAE, MSE, RMSE, and R2 score. Hyperparameters are not considered
   
   Args:
       df (pandas dataframe) : from pull_data or scale_data
       target (str) : 'KD','KA', or 'KDU'. Default is 'KD'
       n_estimations (int) : number of branches for RF to run. Default = 50.
       test_size (int) : percent of data removed to be tested. Default = .2, 20%
       random_state (int) : random_state for regression. Default = 0.
       feature_ranks (bool) : True - returns importance ranking plot. Default is False, no plot return.
       analysis (bool) : True - returns model evaluation metrics. Default is False.
       plot (bool) : True - returns plot of predicted vs actual target values.
   
   Returns:
       pandas dataframe : model evaluation metrics
       scatter plot : plot depicting model's prediction ability, blue = real, red = predicted
       bar chart : feature importance ranking depicting feature importance in model prediction.
       
   """
   df_drop = df.drop(df.iloc[:,0:2],axis=1)
   df_drop=df_drop.drop('Sorbed_val',axis=1)
   df_drop=df_drop.iloc[:,:-3]
   df_nonan = df_drop.replace(np.nan,0)
   x = df_nonan
   y = np.reshape(df[target].values,(len(df[target],)))
   xtrain,xtest,ytrain,ytest=train_test_split(x,y,test_size=test_size)
   reg=RandomForestRegressor(n_estimators=n_estimators,random_state=random_state)
   #fitting model to data
   reg.fit(xtrain,ytrain)
   ypred=reg.predict(xtest)
   
   model_results = evaluate(reg,xtest,ytest)
   col1='Mean Absolute Error'
   MAE = metrics.mean_absolute_error(ytest,ypred)
   col2='Mean Squared Error'
   MSE = metrics.mean_squared_error(ytest,ypred)
   col3= 'Root Mean Squared Error'
   RMSE=np.sqrt(metrics.mean_squared_error(ytest,ypred))
   col4='r2_score'
   rsquared=metrics.r2_score(ytest,ypred)
   
   
   
   def RF_feat_rank():
       """
       Function RF_feat_rank() uses inputs from RF_regressor to product feture importance ranking
       
       Args:
           None
       
       Returns:
           bar graph : feature importance ranking
       
       
       """
       feature_imp=pd.Series(reg.feature_importances_,index=x.columns).sort_values(ascending=False)
       feature_imp

       #plotting the important features
       feat_plot=sns.barplot(x=feature_imp, y=feature_imp.index)
       plt.xlabel('Importance Score')
       plt.ylabel('Features')
       plt.title("Important Features")
       plt.show()
       return feat_plot
   
  
#return section:
   def plot_RF_predict():
       
       """
       Function plot_RF_predict() produces scatter plot of test and predicted target values
       
       Args:
           None
           
       Returns:
           scatter plot : model predicted values vs test values
       
       """
       
       plt.scatter(ytest,ypred)
       ymin = min(ytest)
       ymax = max(ytest)
       plt.plot([ymin,ymax],[ymin,ymax])
       plt.xlabel('Experimental Kd')
       plt.ylabel('ML Predicted Kd')
       plt.title('ML R2 Score (scaled)')
       plt.show()
       return plt

   
   
   if plot==True:
#         r3=True
       plot_RF_predict()
   else:
       ax2=None
 
       
       
       
       

   if feature_ranks==True:

       feat_plot=RF_feat_rank()
   else:
       feat_plot=None
   if analysis==True:
       results=pd.DataFrame(model_results, index=['Accuracy','Degree of Error','R2',col1,col2,col3],columns=[''])
       return results

   else:
       analysis=None
   

   
   

        
       
           


# In[ ]:


def evaluate(model, test_features, test_labels):
    
    """
    Function evaluate evaluates model based on accuracy, degree of error, and on r2.
    
    Args:
    model (sklearn regression) 
    test_features (array of floats) : feature test data
    testlabels (array of floats) : target test data
    
    Return:
    numpy array, 3x1 in shape, containing model performances.  Accuracy, Errors, R2.
    
    
    """
#     base_model = RandomForestRegressor(n_estimators = 1, random_state = 0)
    
    # test_features=xtest
    # test_labels=ytest
   
    global testing, predictions
    testing = test_labels
    predictions = model.predict(test_features)
    errors = abs(predictions - test_labels)
    mape = 100 * np.mean(errors / test_labels)
    accuracy = 100 - mape
    
    col1='Mean Absolute Error'
    MAE = metrics.mean_absolute_error(test_labels,predictions)
    col2='Mean Squared Error'
    MSE = metrics.mean_squared_error(test_labels,predictions)
    col3= 'Root Mean Squared Error'
    RMSE=np.sqrt(metrics.mean_squared_error(test_labels,predictions))
    col4='r2_score'
    rsquared=metrics.r2_score(test_labels,predictions)
    # print('Model Performance')
    # print('Average Error: {:0.4f} degrees.'.format(np.mean(errors)))
    # print('Accuracy = {:0.2f}%.'.format(accuracy))
    # print('R2 = {:0.2f}%.'.format(r2))
    # print('mape ={:0.2f}'.format(mape))
    return_metrics = np.reshape(np.array([accuracy,np.mean(errors),rsquared,MAE,MSE,RMSE]),[6,1])
    
    return return_metrics


# In[ ]:


# df_log_false=scale_data(df,remove_nan=True,scale_target=False)


# In[ ]:


# RF_analysis(df_log,test_size=.2,analysis=True,feature_ranks=True,plot=True)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:

































        


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:


# test_arrays=[df_log,df_std,df_norm,df_robust]
# test_str_ar = ['df_log','df_std','df_norm','df_robust']


# In[ ]:




def RF_optimizer(df,branch_range,depth_range,split_min,samples_min,test_size,iterations):
    
    """
    RF_optimizer attempts to optimize the RF regression by using a randomsearchCV technique to fit 
    the random forest regressor using the best parameters that maximizes the r2 score.
    
    args:
    df (pandas dataframe) : scaled or unscale dataset
    branch_range (list,int) : [int1,int2,int3]. int1 = start range, int2 = end range, int3 = # of vals
                             between start and end.
    depth_range (list , int): same as branch_range format.
    split_min (singular or list, int) : minimum number of samples before splitting node
    samples_min (singular or list, int) : minimum number of samples required at each leaf node
    test_size (float) : percentage of target data to be witheld from the training set for testing.
    iterations (int) : number of gridsearches attempted before fitting model with best_params found.
    trials (int) : default = 1. Number of trials attempted. User can run multiple trials to average r2 scores.
    
    returns:
    pandas dataframe : mape, accuracy and r2 scores with baes and optimized models.
    
    Notes:
    global variable: best_params : (Dictionary) :  best parameters yielded from gridsearch and trials.
    
    """
    
#     base_array = np.zeros([1,trials])
#     base_columns = []
#     for i in range(trials):
#         column_num = 'trial'+ str(i+1)
#         base_columns.append(column_num)
#     all_metrics=pd.DataFrame(base_array, index=['Metrics'],columns=base_columns,dtype=object)

#     all_bestparamsdf=pd.DataFrame(base_array, index=['Hyper Params'], columns=base_columns, dtype=object)
#     all_randstates=pd.DataFrame(base_array, index=['Random_States'], columns=base_columns, dtype=object)
    
#     all_bestparams = []
# #     all_metrics=[]


    other_targets = ['KA','KDU','KD']
    df=df.drop(df.iloc[:,0:2],axis=1)
    df=df.drop('Sorbed_val',axis=1)
    if target_var[0] in other_targets:
        other_targets.remove(target_var[0])
        for i in other_targets:
            if i in df.columns:
                z=df[i]
                df=df.drop(i,axis=1)
#     for trial in range(trials):
    Metrics = pd.DataFrame([])




    df=df.replace(np.nan,0)
    y=df[target_var[0]].values
    x =df.iloc[:,:-1]
    random_int = int(np.random.randint(0,100,[1,1]))
    xtrain,xtest,ytrain,ytest = train_test_split(x,y,test_size=test_size,random_state=random_int)

    #branch range
    n_estimators = [int(x) for x in np.linspace(start=branch_range[0],stop=branch_range[1],num=branch_range[2])]
    max_features=['auto','sqrt']
    #depth_range
    max_depth=[int(x) for x in np.linspace(depth_range[0],depth_range[1], num=depth_range[2])]
    max_depth.append(None)

    #split_min
    # Minimum number of samples required to split a node
    min_samples_split = split_min

    #samples_min
    # Minimum number of samples required at each leaf node
    min_samples_leaf = samples_min
    # Method of selecting samples for training each tree
    bootstrap = [True, False]

    # Create the random grid
    random_grid = {'n_estimators': n_estimators,
                   'max_features': max_features,
                   'max_depth': max_depth,
                   'min_samples_split': min_samples_split,
                   'min_samples_leaf': min_samples_leaf,
                   'bootstrap': bootstrap}

    # First create the base model to tune
    rf = RandomForestRegressor(random_state = 0)
    # Random search of parameters, using 3 fold cross validation, 
    # search across 100 different combinations, and use all available cores
    rf_random = RandomizedSearchCV(estimator=rf, param_distributions=random_grid,
                                  n_iter = iterations, scoring='r2', 
                                  cv = 3, verbose=2, random_state=random_int, n_jobs=-1,
                                  return_train_score=True)

    # Fit the random search model
    rf_random.fit(xtrain, ytrain);

    base_model = RandomForestRegressor(n_estimators = 1, random_state = random_int)
    base_model.fit(xtrain, ytrain)
    best_params = rf_random.best_params_
    scm_model = RandomForestRegressor(random_state=random_int,**best_params)
#         Trialsofmodels.append(scm_model)
    scm_model.fit(xtrain,ytrain)
    models = [base_model,rf_random,scm_model]
    cv_results = rf_random.cv_results_

    for j in range(len(models)):

        model_evaluation = evaluate(models[j], xtest, ytest)

        metricsdf=pd.DataFrame(model_evaluation)

        Metrics = pd.concat([Metrics,metricsdf],axis=1)

    Metrics.columns=['base','rf_random','scm_model']
    Metrics.index=['Accuracy','Error','R2','MAE','MSE','RMSE']


#     all_metrics.append(Metrics)
#     all_randstates.iloc[:,trial]=[random_int]
#     all_bestparamsdf.iloc[:,trial]=[best_params]
#     all_metrics.iloc[:,trial]=[Metrics]
#     all_bestparamsdf=all_bestparamsdf.transpose()
#     all_metrics=all_metrics.transpose()
#     all_randstates = all_randstates.transpose()
#         optimized_results.iloc[:,trial]=[Trialsofmetrics,Trialsofmodels,Trialsofbestparams]
#     all_metrics = np.transpose(all_metrics)
#     all_metricsdf = pd.DataFrame(all_metrics, columns=base_columns)


    return  Metrics, best_params, random_int, x,y,cv_results


# In[ ]:


# mydata, myparam,r_states,X,Y,results=RF_optimizer(df_log,[1,1000,30],[1,20,10],[2,5,10,20],[1,5,10,15],.2,1)


# In[ ]:


# # r_states,myparam
# rstate = r_states.iloc[0,0]
# newscm = RandomForestRegressor(random_state = rstate,**myparam.iloc[0,0])
# xtrain,xtest,ytrain,ytest = train_test_split(X,Y,test_size=0.2,random_state=rstate)
# newscm.fit(xtrain,ytrain)
# y_pred=newscm.predict(xtest)
# meval = metrics.r2_score(ytest,y_pred)


# In[ ]:


# mydata.iloc[0,0], meval


# In[ ]:


# mydata


# In[ ]:





# In[ ]:


# ##this code tests the viability of each scaling method using cross val score sklearn 

# scales_list=['log10','standardize','normalize','robust','none']
# output_options = ['True', 'False'] # ['True','True','False','False'] #true = output is scaled
# blank_array = np.zeros([len(scales_list),len(output_options)])
# test_results = pd.DataFrame(blank_array, index = scales_list, columns = output_options)
# metricsarray = []
# testparamsarray = []
# testrstatearray = []
# for i in range(len(scales_list)):
#     for j in range(len(output_options)):
#         scale = scales_list[i]
#         output_scale = output_options[j]
#         test_df = scale_data(df,scale=scale,remove_nan=True,scale_target=output_scale)
#         testmetrics,testparams,testrstate, X, y, p = RF_optimizer(test_df,[1,1000,30],[1,40,10],[2,10,50,20],[1,10,30,15],.2,100,trials=1)
#         metricsarray.append(testmetrics)
#         testparamsarray.append(testparams)
#         testrstatearray.append(testrstate)
#         trial_r2=[]
#         for b in range(len(testmetrics)):
#             r2 = testmetrics.iloc[b,0].iloc[2,2]
#             trial_r2.append(r2)
#         max_r2 = max(trial_r2)
#         idx_max_r2 = trial_r2.index(max_r2)
#         best_hparam = testparams.iloc[idx_max_r2,0]
#         best_r_state = testrstate.iloc[idx_max_r2,0]
#         best_scm = RandomForestRegressor(random_state=best_r_state, **best_hparam)
#         xtrain,xtest,ytrain,ytest = train_test_split(X,y,test_size=0.3,random_state=int(np.random.randint(0,100,[1,1])))
#         best_scm.fit(xtrain,ytrain)
#         scm_score_avg = np.mean(cross_val_score(best_scm,X,y,cv=5,scoring='r2'))
#         test_results.iloc[i,j]=scm_score_avg

        


# In[ ]:


# def myfun(d1f):
#     df = scale_data(d1f,remove_nan=True,scale='log10',scale_target='False')
#     other_targets = ['KA','KDU','KD']
#     df=df.drop(df.iloc[:,0:2],axis=1)
#     df=df.drop('Sorbed_val',axis=1)
#     if target_var[0] in other_targets:
#         other_targets.remove(target_var[0])
#         for i in other_targets:
#             if i in df.columns:
#                 z=df[i]
#                 df=df.drop(i,axis=1)

#     Metrics = pd.DataFrame([])




#     df=df.replace(np.nan,0)
#     y=df[target_var[0]].values
#     x =df.iloc[:,:-1]

#     trials=2
#     for i in range(trials):
#         rstate=71#int(np.random.randint(0,100,[1,1]))
#         xtrain,xtest,ytrain,ytest = train_test_split(X,y,test_size=0.2,random_state=rstate)

#         scm =RandomForestRegressor(random_state=rstate, **scm_param)
#         scm.fit(xtrain,ytrain)
#         predictions = scm.predict(xtest)
#         r2 = metrics.r2_score(ytest,predictions)
#         if r2>0.9:
#             goodr2=r2
#             break

#     #Whole data test test
#     allX=X
#     allKD=y
#     allKdpredictions = scm.predict(allX)
#     newr2 = metrics.r2_score(y,allKdpredictions)
#     return goodr2,newr2,allKdpreidctions


# In[ ]:





# In[ ]:


# scales_list=['log10','standardize','normalize','robust','none']
# output_options = ['Y Scaled', 'Y Unscaled']
# lenindex = len(scales_list)
# lencols = len(output_options)
# datadict={}
# paramdict={}
# rstatesdict={}
# for i in range(lencols):
#     for j in range(lenindex):
#         results_df.iloc[j,i]= metricsarray[0].iloc
#         data = {scales_list[j]+' '+output_options[i] :metricsarray[i+2*j].iloc[0,0]}
#         datadict.update(data)
#         param={scales_list[j] + ' '+ output_options[i]:testparamsarray[i+2*j].iloc[0,0]}
#         paramdict.update(param)
#         states= {scales_list[j] + ' '+ output_options[i]:testrstatearray[i+2*j].iloc[0,0]}
#         rstatesdict.update(states)
        
        
        



# In[ ]:


# scm_param=paramdict['log10 Y Unscaled']
# rstatesdict['log10 Y Unscaled']
# metricsarray[1].iloc[0,0]


# In[ ]:





# In[ ]:


# 


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:







# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:



            


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




       


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:






# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:







# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




