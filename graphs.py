import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
#    % matplotlib inline
sns.set(style="ticks")

youtube = pd.read_csv('~/Documents/CAvideos.csv')
youtube.head()
youtube.shape
youtube.describe()
youtube.describe(include = ['O'])
delete = ['comments_disabled', 'ratings_disabled', 'video_error_or_removed',  'description']

youtube = youtube.drop(delete, axis=1)
youtube.head()

youtube.duplicated().value_counts()

youtube['trending_date'] = pd.to_datetime(youtube['trending_date'], format='%y.%d.%m')
youtube['publish_time'] = pd.to_datetime(youtube['publish_time'], format='%Y-%m-%dT%H:%M:%S.%fZ')
youtube

youtube_cat = pd.read_json('~/Documents/CA_category_id.json')
id_to_category = {}
for category in youtube_cat['items']:
    id_to_category[category['id']] = category['snippet']['title']

youtube['category_id'] = youtube['category_id'].astype(str)

youtube.insert(4, 'categories', youtube['category_id'].map(id_to_category))

youtube

youtube1 = youtube.groupby(['categories']).sum()
youtube1.index

fig, ax = plt.subplots(figsize=(30,15))
sns.barplot(ax=ax,  x=youtube1.index, y= 'views',  data=youtube1)

youtube['category_id']

youtube.groupby(['categories']).sum()

fig, ax = plt.subplots(figsize=(30,15))
sns.lineplot(data=youtube1)
