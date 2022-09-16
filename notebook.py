#!/usr/bin/env python
# coding: utf-8

# # Internet adoption around the world
# This project is based on a study about the Internet adoption around the world and how the price, speed and country's development affects this data.

# ## Importing the libraries
# The first thing to do is importing the modules and making sure that they are installed correctly into our envirorment.

# In[1]:


# Uncomment the lines below if the following modules are not installed on your envirorment
#!pip install matplotlib
#!pip install pandas
#!pip install plotly
#!pip install seaborn
#!pip install kaleido

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px


# ## Project structure
# 

# The `datasets/` folder contains the following files.

# In[2]:


os.listdir("datasets")


# Datasets used for this projects:
# - `worldwide internet prices in 2022 - IN 2022.csv`: Contains informations about the price, plans available, and the price of most expensive and cheapest 1 GB for every country
# - `worldwide internet speed in 2022 - avg speed.csv`: Contains the average speed in Mbit per second for every country
# - `worldwide internet users - users.csv`: Contains the number of internet users and the total population for every country
# - `GDP2021.csv`: Contains the GDP (Gross Domestic Product) per capita for every country. This index measures a country's economic output per person and is calculated by dividing the GDP of a country by its population.
# - `HDR2020.csv`: Contains the HDI (Human Development Index) for every country. This index is a summary measure of average achievement in key dimensions of human development.

# Sources:
# - Worldwide internet data in 2022: https://www.kaggle.com/datasets/ramjasmaurya/1-gb-internet-price
# - HDI (Human Development Index) 2019: https://hdr.undp.org/data-center/documentation-and-downloads
# - GDP per capita (in USD): https://data.worldbank.org/indicator/NY.GDP.PCAP.CD
# 

# ## Data cleaning
# The datasets just presented contain a lot of data, however, we will not need all of them and some of them are not consistent, so we have to face a data cleaning process, removing the columns that we do not need and managing null or non-consistent values.

# In[3]:


data_folder = "datasets"


# ### `GDP2021.csv` cleaning

# First we import the dataset and initialize the DataFrame.

# In[4]:


df_gdp = pd.read_csv(os.path.join(data_folder, "GDP2021.csv"))
df_gdp


# As we can see, the dataset contains the data for each country from 1960 to today, for what we have to do we are enough data on the GDP per capita of the year 2020 (we do not choose those of 2021 due to the fact that different countries have null values )

# In[5]:


df_gdp2020 = df_gdp[["Country Name", "Country Code", "2020"]]
df_gdp2020


# Let's rename the columns now.

# In[6]:


df_gdp2020 = df_gdp2020.rename(columns={
    "2020": "GDP"
}, copy=True, inplace=False)
df_gdp2020


# Cleaning the data.

# In[7]:


df_gdp2020 = df_gdp2020.loc[df_gdp2020["GDP"].notna()]
df_gdp2020.info()


# ### `HDR2020.csv` cleaning

# Importing the dataset into a pandas DataFrame.

# In[8]:


df_hdi = pd.read_csv(os.path.join(data_folder, "HDR2020.csv"))
df_hdi


# The dataset also contains information about regions and other subsets of states, which we do not need, so we exclude them and take only the HDI of the countries in 2019 (the most recent year)

# In[9]:


df_hdi2019 = df_hdi.loc[df_hdi["iso3"].notna()][["country", "hdi_2019"]]
df_hdi2019


# Now we rename the columns.

# In[10]:


df_hdi2019 = df_hdi2019.rename(columns={
    "country": "Country Name",
    "hdi_2019": "HDI"
}, copy=True, inplace=False)
df_hdi2019


# Cleaning the data.

# In[11]:


df_hdi2019 = df_hdi2019.loc[df_hdi2019["HDI"].notna()]
df_hdi2019.info()


# ### `worldwide internet prices in 2022 - IN 2022.csv` cleaning

# Importing the dataset into a pandas DataFrame.

# In[12]:


df_prices = pd.read_csv(os.path.join(data_folder, "worldwide internet prices in 2022 - IN 2022.csv"))
df_prices


# Selecting the columns that we need for our study.

# In[13]:


df_prices = df_prices[["Name", "Average price of 1GB (USD)", "NO. OF Internet Plans "]]
df_prices


# Renaming the colunms.

# In[14]:


df_prices = df_prices.rename(columns={
    "Name": "Country Name",
    "Average price of 1GB (USD)": "Average price of 1GB",
    "NO. OF Internet Plans ": "Number of plans"
}, copy=True, inplace=False)
df_prices


# We need to get rid of the dollar sign '`$`' in order to convert the price value to numeric. For doing that we use regular expressions.

# In[15]:


df_prices = df_prices.copy()
df_prices = df_prices.loc[df_prices["Number of plans"].notna()]
df_prices["Average price of 1GB"] = df_prices["Average price of 1GB"].replace('[\$,]', '', regex=True).astype(float)
df_prices


# ### `worldwide internet speed in 2022 - avg speed.csv` cleaning

# Importing the dataset into a pandas DataFrame.

# In[16]:


df_speeds = pd.read_csv(os.path.join(data_folder, "worldwide internet speed in 2022 - avg speed.csv"))
df_speeds


# Renaming the columns.

# In[17]:


df_speeds = df_speeds.rename(columns={
    "Country": "Country Name",
    "Avg \n(Mbit/s)Ookla": "Average speed"
}, copy=True, inplace=False)
df_speeds


# Cleaning the data.

# In[18]:


df_speeds = df_speeds.loc[df_speeds["Average speed"].notna()]
df_speeds.info()


# ### `worldwide internet users - users.csv` cleaning

# Importing the dataset into pandas DataFrame.

# In[19]:


df_users = pd.read_csv(os.path.join(data_folder, "worldwide internet users - users.csv"), thousands=",")
df_users


# Selecting the columns that we need for our study.

# In[20]:


df_users = df_users[["Country or area", "Internet users", "Population"]]
df_users


# Renaming the columns.

# In[21]:


df_users = df_users.rename(columns={
    "Country or area": "Country Name"
})
df_users


# Cleaning the data.

# In[22]:


df_users = df_users.loc[df_users["Population"].notna()]
df_users.info()


# # Dataset analysis
# Now that we have cleaned up and made consistent all the necessary datasets, we can begin to carry out the analyzes on them.

# ## Question 1: Is there a greater adoption of Internet in more developed countries?

# In order to assess whether there is a relationship between the development of a nation and the Internet adoption of its population, we will use two indices:
# - **Human Development Index**, which is a statistic composite index of life expectancy, education, and per capita income indicators, which are used to rank countries's human and social development.
# - **GDP per capita**, which measures a country's economic output per person.
# 
# The reason why it is not possible to use only one index is because there is no such generic index, and therefore the ideal compromise is to use two indices: one that tracks economic development (GDP per capita), the other that tracks social development (HDI) of each country.

# In[23]:


fig, axes = plt.subplots(figsize=(17, 5), nrows=1, ncols=2)

df_gdp2020 = df_gdp2020.sort_values('GDP', ascending=False)
df_gdp2020.head(30).plot.bar(ax=axes[0], x='Country Name', y='GDP')

df_hdi2019 =  df_hdi2019.sort_values('HDI', ascending=False)
df_hdi2019.head(30).plot.bar(ax=axes[1], x='Country Name', y='HDI')


# We can also use violinplots to visualize the distribution of the data.

# In[24]:


fig, axes = plt.subplots(figsize=(17, 5), nrows=1, ncols=2)

sns.violinplot(
    data=df_gdp2020, 
    x="GDP",
    ax=axes[0]
)

sns.violinplot(
    data=df_hdi2019, 
    x="HDI",
    ax=axes[1]
)


# Only by viewing the data with a bar chart can we see that the HDI index is much more homogeneous in the distribution of values, however with this type of diagrams it is not possible to have a clear overall view of the data, so it is better to visualize the data on a world map.

# In[27]:


fig_gdp = px.choropleth(
    df_gdp2020, 
    locations='Country Name', 
    locationmode='country names', 
    scope='world', 
    color='GDP',
    color_continuous_scale='Viridis_r'
)

fig_gdp.update_layout(coloraxis_colorbar=dict(
    title = 'GDP per capita',
    ticks = 'outside',
))

fig_hdi = px.choropleth(
    df_hdi2019, 
    locations='Country Name', 
    locationmode='country names', 
    scope='world', 
    color='HDI',
    color_continuous_scale='solar'
)

fig_gdp.show("svg") #remove "svg" parameter to have interactive maps
fig_hdi.show("svg")


# In order to analyze a possible relationship between the development of a country and the adoption of the Internet within it, we need the percentage of the population of Internet users, which we can calculate by dividing the number of people who use the Internet by the population of every country. 
# 
# Let's create a new `Users Percentage` column.

# In[28]:


df_users = df_users.copy()
df_users["Users Percentage"] = df_users["Internet users"] / df_users["Population"] * 100
df_users.round(2)


# Now we can visualize Internet adoption data.

# In[29]:


df_users = df_users.sort_values("Users Percentage", ascending=False)
df_users.head(50).plot.bar(x="Country Name", y="Users Percentage", figsize=(13, 5))


# In[30]:


fig_users = px.choropleth(
    df_users, 
    locations='Country Name', 
    locationmode='country names', 
    scope='world', 
    color='Users Percentage',
    color_continuous_scale='solar'
)

fig_users.update_layout(coloraxis_colorbar=dict(
    title = 'Users Percentage',
    ticks = 'outside',
))

fig_users.show("svg")


# Just by comparing the map just obtained with the previous two it can be seen that in less developed countries the percentage of people who use the internet is considerably lower, however with a scatter diagram it is possible to make much more accurate considerations.
# 
# The idea is to merge the 3 dataframes we have built, and build two scatter subplots, one for the GDP and one for the HDI.
# 
# We start joining `df_users` and `df_gdp2020` dataframes. Using the inner join method that uses the intersection of the keys of both frames, which allows us not to have rows with null values.

# In[31]:


df_users_merged_gdp = pd.merge(
    left=df_users, 
    right=df_gdp2020, 
    on="Country Name", 
    how="inner",
)

df_users_merged_gdp = df_users_merged_gdp.sort_values("GDP").reset_index(drop=True)
df_users_merged_gdp


# In[32]:


df_users_merged_gdp.info()


# Now let's merge the dataframe just obtained and `df_hdi2019`, again with the inner method.

# In[33]:


df_users_merged_hdi = pd.merge(
    left=df_users,
    right=df_hdi2019,
    on="Country Name",
    how="inner"
)

df_users_merged_hdi = df_users_merged_hdi.sort_values("HDI").reset_index(drop=True)
df_users_merged_hdi


# In[34]:


df_users_merged_hdi.info()


# Now that we've merged the dataframes and made sure they don't have data inconsistencies, we can proceed to build the scatter plots.

# In[35]:


sns.relplot(
    data=df_users_merged_gdp, 
    x="GDP",
    y="Users Percentage", 
    kind="scatter",
    hue="GDP",
    height=5,
    aspect=11.7/8.27
)


# In[36]:


sns.relplot(
    data=df_users_merged_hdi, 
    x="HDI",
    y="Users Percentage", 
    kind="scatter",
    hue="HDI",
    height=4.5
)


# Now it is very clear that economic development and especially social development greatly influence the percentage of internet users, we can visualize it even better using a regplot.

# In[37]:


sns.set(rc={'figure.figsize':(10, 7)})

sns.regplot(
    data=df_users_merged_hdi, 
    x="HDI",
    y="Users Percentage"
)

sns.reset_orig()


# Now we can see, even with the help of the regression line, how linear the trend in the percentage of users is: with the growth of development (in the social one it is even more evident given the homogeneity of distribution) the percentage of internet users increases equally.
# 
# The reasons for this correlation can be various, and will be the subject of study for the next questions.

# ## Queston 2: Is there a relationship between the average price of navigation and the speed of it?

# In order to find out more about a possible relationship between the average Internet price and average speed, we will need the related datasets that we have already worked on by cleaning the data:
# - `df_prices`
# - `df_speeds`

# First we begin to get an idea of the distribution of prices and speeds by using two swarmplots.

# In[38]:


fig, axes = plt.subplots(figsize=(15, 5), nrows=1, ncols=2)

sns.swarmplot(y="Average price of 1GB", data=df_prices, ax=axes[0])
sns.swarmplot(y="Average speed", data=df_speeds, ax=axes[1])


# We can see that most of the prices are concentrated below 10 dollars per GB, while there is a relatively more uniform distribution in terms of speeds, which, although they are more distributed below 60MBit/s, their distribution is much more homogeneous. Now let's visualize the prices and speeds on the world map.

# In[39]:


fig_prices = px.choropleth(
    df_prices, 
    locations='Country Name', 
    locationmode='country names', 
    scope='world', 
    color='Average price of 1GB',
    color_continuous_scale='Viridis_r'
)

fig_speeds = px.choropleth(
    df_speeds, 
    locations='Country Name', 
    locationmode='country names', 
    scope='world', 
    color='Average speed',
    color_continuous_scale='Viridis_r'
)

fig_prices.show("svg")
fig_speeds.show("svg")


# Looking at the map we have the confirmation that prices are on average under 10 dollars per gb, exceptions are made by few developing countries (such as Chad, Equatorial Guinea, Namibia, Turkmenistan) or in countries with a high cost of living ( such as Norway or Canada), which justifies the slightly higher prices. We cannot say the same about speeds, whose values have much higher volatility.
# 
# To be able to accurately analyze the changes in prices as the average speed increases, we need to merge the two datasets.

# In[40]:


df_prices_and_speeds = pd.merge(left=df_prices, right=df_speeds, how="inner", on="Country Name")
df_prices_and_speeds.info()


# We can now visualize the data through a scatter plot.

# In[41]:


sns.regplot(x="Average speed", y="Average price of 1GB", data=df_prices_and_speeds)


# As we can see, there is no strong correlation between price and average speed, on the contrary, the data show that even if the average browsing speed rises significantly, the price remains almost stable. There are even some cases where, despite the speeds are very low (less than 20Mbit/s), the average price of 1GB is very high, sometimes more than 20 dollars.
# 
# A possible reason for this dynamic could be the fact that high speeds attract more customers, and therefore companies can afford to keep prices low, both to fight the competition and because they manage to have a higher profit margin. However, this topic deserves further analysis and will be the subject of the next question.

# ## Question 3: How does the high competition and variety of plans affect the price and number of users?

# Analyzing the consequences of high competition and variety of choice in terms of plans can be very useful to understand how the Internet market reacts in terms of users and prices. To begin to get an idea of the variety of plans in the various countries of the world, let's build a map.

# In[42]:


fig_prices = px.choropleth(
    df_prices, 
    locations='Country Name', 
    locationmode='country names', 
    scope='world', 
    color='Number of plans',
    color_continuous_scale='Viridis_r'
)

fig_prices.show("svg")


# What we can notice right away is that there is no direct correlation between the development of a country and the number of plans, contrary to what one might think. For example, a highly developed country like Ireland offers only 12 plans, while a developing country like Nigeria offers 60.
# 
# Now let's try to visualize this data through a boxplot, to better understand what kind of distribution we have.

# In[43]:


sns.boxplot(
    data=df_prices,
    y="Number of plans",
    palette=["g"],
)

sns.despine(trim=True)


# We can see how most of the number of plans is between 15 and 35, with a median of around 22 plans.
# 
# Let's now build the dataframe needed to analyze all the data.

# In[44]:


df_prices_users = pd.merge(left=df_prices, right=df_users, how="inner", on="Country Name")
df_prices_users


# Let's discard the columns that we do not need.

# In[45]:


df_prices_users = df_prices_users[["Country Name","Average price of 1GB", "Number of plans", "Users Percentage"]]
df_prices_users


# In[46]:


sns.set_theme(style="white", color_codes=True)

g = sns.JointGrid(
    data=df_prices_users, 
    y="Users Percentage", 
    x="Average price of 1GB", 
    space=0, 
    ratio=17,
    height=7
)

g.plot_joint(
    sns.scatterplot, 
    size=df_prices_users["Number of plans"], 
    sizes=(30, 120),
    color="r", 
    alpha=.6, 
    legend=True
)

g.plot_marginals(sns.rugplot, height=.9, color="r", alpha=1)


# As we can observe from the JointPlot, the size of the points has no relations with the y-axis ("User Percentage"), however, it seems that the number of plans available decreases as the average cost per 1GB increases. To better analyze this possible correlation we plot the data separately.

# In[47]:


df_prices_users = df_prices_users.copy()
fig, axes = plt.subplots(nrows=1, ncols=2)

df_prices_users.sort_values(by="Users Percentage", inplace=True)
df_prices_users.plot.line(y="Number of plans", x="Users Percentage", figsize=(17, 4), ax=axes[1])

df_prices_users.sort_values(by="Average price of 1GB", inplace=True)
df_prices_users.plot.line(y="Number of plans", x="Average price of 1GB", figsize=(17, 4), ax=axes[0])


# Leaving aside the second graph, of which we had already ascertained the non-correlation between the two data, as regards the first, we note how the extreme volatility that occurs at low prices gradually decreases the more prices rise, up to defining a fairly clear downtrend.
# We can therefore say that the countries characterized by the highest average price for 1GB also have the peculiarity of having very few plans available, and therefore little competition. However, the same cannot be said of the other way around.

# ## Question 4: Is a country's low social and economic development the cause of slower internet speeds?

# Determining whether low speeds are the cause or consequence of low economic / social development is certainly not a simple task, but by analyzing how the data at our disposal behave, we can try to raise hypotheses.
# 
# 
# Let's proceed with the merge of the three dataframes that contain respectively the data on HDI, GDP and average speeds, with the usual "inner" approach.

# In[48]:


df_development_speeds = pd.merge(left=df_hdi2019, right=df_gdp2020, how="inner", on="Country Name")
df_development_speeds = pd.merge(left=df_development_speeds, right=df_speeds, how="inner", on="Country Name")
df_development_speeds


# Now we proceed with removing the columns we don't need for this analysis.

# In[49]:


df_development_speeds.drop('Country Code', axis=1, inplace=True)  
df_development_speeds.info()


# As a first approach we use two lineplots to visualize the data of the average speeds in relation to the two HDI and GDP indices, in order to get a general idea on the behavior of the data.
# 
# From here on, to avoid confusion, we will use the red color in the graphs concerning the HDI index, and the green color for the GDP index.

# In[50]:


fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(30, 7))

sns.lineplot(
    data=df_development_speeds, 
    x="HDI", 
    y="Average speed", 
    ax=axes[0], 
    color="red"
)

sns.lineplot(
    data=df_development_speeds, 
    x="GDP", 
    y="Average speed", 
    ax=axes[1], 
    color="green"
)


# As already seen in the first question, the GDP index has a minor influence in the Internet market, or rather, it has a large influence in the very low values (below 20000), in fact, the speeds grow very quickly as the values of GDP per capita, but once the 20,000 range is exceeded, speeds tend to stabilize around 65 - 70mbit / s. 
# On the other hand, as human and social development increases, speeds begin to increase at higher values, and they do so with greater linearity. 
# As we observe from the graph, the speeds remain almost stable around 18mbit / s up to HDI levels around 0.7, but then they begin to rise uniformly until they reach the peak and stabilize.
# 
# These data, however, are very volatile, it would be much better to work on a moving average of these values, in order to have a line that describes the trend of average speeds in a more gentle way.
# We then create a 10-period moving average and visualize it.

# In[51]:


df_development_speeds["10MA"] = df_development_speeds["Average speed"].rolling(10).mean().shift(-3)

sns.set_theme(
    style="whitegrid", 
    palette="pastel"
)

plt.figure(figsize=(20,5))

sns.lineplot(
    data=df_development_speeds, 
    x="HDI", 
    y="10MA", 
    label="10 Periods Moving Average", 
    ci=None, 
    color="red"
)


# In[52]:


plt.figure(figsize=(20,5))
sns.lineplot(
    data=df_development_speeds, 
    x="GDP", 
    y="10MA", 
    label="10 Periods Moving Average", 
    ci=None, 
    color="green"
)


# Now we use a regression line (of order 4) to visualize the trend of the moving average more smoothly.

# In[53]:


fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(20, 5))

sns.regplot(
    data=df_development_speeds, 
    x="HDI", 
    order=4, 
    y="10MA", 
    ci=100, 
    truncate=True,  
    scatter_kws={"s": 1},
    ax=axes[0],
    color="red"
)

sns.regplot(
    data=df_development_speeds, 
    x="GDP", 
    y="10MA", 
    order=4, 
    ci=50, 
    truncate=True,  
    scatter_kws={"s": 1},
    ax=axes[1],
    color="green"
)

sns.reset_orig()


# We now have a clearer picture that confirms the previous one: the initial rise in GDP leads to very steep growth in speeds, which then tends to stabilize, while we see this growth much later and much more linearly as HDI increases.
# 
# We can therefore say that the less socially developed countries suffer from lower average speeds, while economically relatively less developed countries still have acceptable average speeds (this does not apply to countries with very low economic development (below 10,000), which also have speeds very low)

# ## Question 5: Which are the countries with the best ratio between Internet cost and speed? What level of development do they have? Does this convenience involve more users?

# In order to evaluate the convenience of the Internet in each country we need an index that we will create by dividing the average cost of 1GB by the average speed of each country. The countries where the Internet is cheaper will therefore be those where the price is low and at the same time the speed is high.
# Let's proceed to create the `Convenience Index` column in the `df_prices_and_speeds` DataFrame created before.

# In[54]:


df_prices_and_speeds["Convenience Index"] = df_prices_and_speeds["Average speed"] / df_prices_and_speeds["Average price of 1GB"]
df_prices_and_speeds


# In[55]:


df_prices_and_speeds.sort_values(by="Convenience Index", inplace=True, ascending=False)
df_prices_and_speeds.head(75).plot.bar(x="Country Name", y="Convenience Index", figsize=(15, 5))


# Leaving aside the particular case of Israel, we can see how the distribution of values is quite homogeneous. Let's visualize it more clearly with the world map.

# In[58]:


fig_convenience = px.choropleth(
    df_prices_and_speeds, 
    locations='Country Name', 
    locationmode='country names', 
    scope='world', 
    color='Convenience Index',
    color_continuous_scale='Viridis_r'
)

fig_convenience.show("svg")


# Thanks to these graphs we can see that the country where the Internet is more convenient is Israel, followed by China, France, Italy, Fiji, Denmark, and so on.
# At first glance it seems that the most economically and socially developed countries are not always the most convenient ones, indeed, sometimes it is just the opposite. To better analyze this dynamic we use three scatter plots, the first two which relate the convenience with the two development indices, the other which relates the convenience with the number of plans. Obviously before we can do this we need to merge the dataframes.

# In[59]:


df_prices_and_speeds = pd.merge(left=df_prices_and_speeds, right=df_hdi2019, how="inner", on="Country Name")
df_prices_and_speeds = pd.merge(left=df_prices_and_speeds, right=df_gdp2020, how="inner", on="Country Name")
df_prices_and_speeds


# In[60]:


df_prices_and_speeds_and_users = pd.merge(left=df_prices_and_speeds, right=df_users, on="Country Name", how="inner")
df_prices_and_speeds_and_users


# We discard the columns we don't need.

# In[61]:


df_prices_and_speeds_and_users = df_prices_and_speeds_and_users[[
    "Country Name", 
    "Average price of 1GB", 
    "Number of plans", 
    "Average speed", 
    "Convenience Index",
    "HDI", 
    "GDP", 
    "Users Percentage"
]]
df_prices_and_speeds_and_users


# In[62]:


fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(20, 5))

df_prices_and_speeds_and_users.plot.scatter(x="GDP", y="Convenience Index", figsize=(20, 5), ax=axes[1], color="green")
df_prices_and_speeds_and_users.plot.scatter(x="HDI", y="Convenience Index", figsize=(20, 5), ax=axes[0], color="red")
df_prices_and_speeds_and_users.plot.scatter(x="Number of plans", y="Convenience Index", figsize=(15, 4))


# Economic development does not particularly affect convenience, while social development does, but not excessively. Same thing for the number of plans, although there is no strong correlation, a positive trend remains. It is good to observe the graphs carefully, in fact, you can be misled due to the very high convenience of Israel, which to be shown, compacts all the other values downwards, making it difficult to analyze the trend of the points. To prevent this from happening without removing Israel from the dataset (which would be incorrect) we can use Plotly's interactive charts.

# In[63]:


#!pip install statsmodels

fig_convenience = px.scatter(
    df_prices_and_speeds_and_users,
    x="GDP",
    y="Convenience Index",
    hover_data=["Country Name"],
    trendline="ols",
)

fig_convenience.show()


fig_convenience = px.scatter(
    df_prices_and_speeds_and_users,
    x="HDI",
    y="Convenience Index",
    hover_data=["Country Name"],
    trendline="ols",
)

fig_convenience.show()


fig_convenience = px.scatter(
    df_prices_and_speeds_and_users,
    x="Number of plans",
    y="Convenience Index",
    hover_data=["Country Name"],
    trendline="ols",
)

fig_convenience.show()


# If we select the part that interests us excluding the very high value of Israel, we can see even better the positive trend (which is still fairly moderate) in all three graphs. We can therefore say that high competition and high human and social development have as a consequence a high convenience of the Internet, intended as a good quality / price ratio ((there are however several exceptions to this trend).
# 
# A final interesting analysis that can be conducted is that relating to the number of users, in fact, it is intuitive to think that if it is easily possible to buy a high-speed connection at a low price, then there will be more people willing to buy it. Let's check if this really happens.

# In[64]:


df_prices_and_speeds_and_users.plot.scatter(y="Convenience Index", x="Users Percentage", figsize=(15, 5))


# Let's use plotly's interactive charts again.

# In[65]:


fig_convenience = px.scatter(
    df_prices_and_speeds_and_users,
    x="Users Percentage",
    y="Convenience Index",
    hover_data=["Country Name"],
    trendline="ols",
)

fig_convenience.show()


# We have the confirmation of our hypothesis: greater convenience tends to translate into an increase in users who use the Internet. In this case the trend is more marked than those seen previously, as in addition to having a more marked positive trend, we also have a greater concentration of values as the percentage of users increases.
# 
