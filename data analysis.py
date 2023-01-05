import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.optimize import curve_fit



movies_df=pd.read_csv('movies_scraped#1', 
    na_values=['N/A'], 
    decimal='.', 
    thousands = ',')

movies_df = movies_df.drop(movies_df.columns[0], axis=1)

def clean_gross(x):
    try:
        return float(str(x)[1:-1])
    except Exception as e:
        print(e)
        return None

def clean_duration(x):
    try: 
        return int(str(x)[:-3])
    except:
        return None

movies_df['Year'] = movies_df['Year'].apply(lambda x: str(x)[1:-1])
movies_df['Duration'] = movies_df['Duration'].apply(clean_duration)
movies_df['Genre'] = movies_df['Genre'].apply(lambda x: str(x)[1:])
movies_df['Gross'] = movies_df['Gross'].apply(clean_gross)
movies_df.dtypes
movies_df
# %%
fig, ax = plt.subplots(figsize = (14, 6))

duration = movies_df['Duration'] # x axis
IMDB_score = movies_df['IMDB_score']# y axis


mask1 = ~duration.isnull()
mask2 = ~IMDB_score.isnull()

duration = duration[mask2][mask1]
IMDB_score = IMDB_score[mask1][mask2]
print(type(duration[2]))
a, b = np.polyfit(duration.to_numpy(), IMDB_score.to_numpy(), 1)


ax.plot(duration, a*duration + b)

ax.scatter(duration, IMDB_score, marker='o')


# %%
def plot_graph(xval, yval):
    fig, (ax1, ax2) = plt.subplots(2, figsize = (14, 10))

    x = movies_df[xval] # x axis
    y = movies_df[yval]# y axis


    mask1 = ~x.isnull()
    mask2 = ~y.isnull()

    x = x[mask2 & mask1]
    y = y[mask1 & mask2]

    def model_f(x, b, c, d):
        return  b*np.sqrt(x) + c*x +d

    

    popt, pcov = curve_fit(model_f, x, y, p0=[1, 0, -100])
    b, c, d = popt
    y_data = model_f(x, b, c, d)

    print(popt)

    a, b = np.polyfit(x.to_numpy(), y.to_numpy(), 1
)


    #ax.plot(x, a*x + b)

    ax1.plot(x, y_data, color='red')
    ax1.scatter(x, y, marker='o')

    img = ax2.imshow(np.abs(pcov))
    plt.colorbar(img, ax=ax2)
    

plot_graph('Votes', 'IMDB_score')

plot_graph('Duration', 'Votes')

plot_graph('Gross', 'Votes')

plot_graph('Gross', 'IMDB_score')

plot_graph('Gross', 'Votes')

plot_graph('Gross', 'Duration')

# %%
