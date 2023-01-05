# %%
import requests
import pandas as pd
import numpy as np
from lxml import html
import time
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
# %% 

def timeit(temp_list):
    def wrapper(func):
        def inner(*args, **wrapper_kwargs):
            start_time = time.perf_counter()
            result = func(*args, **wrapper_kwargs)
            end_time = time.perf_counter()
            diff_time = end_time-start_time
            print(f"Time taken: {diff_time}")
            temp_list.append(diff_time)
            return result
        return inner
    return wrapper


def get_text(idx, xpath):
    var =  tree.xpath(f'//div[@class="lister-item mode-detail"][{idx}]//div[2]//{xpath}')
    try:
        var = var[0].text
        #print(var)
    except Exception as e:
        var = 'N/A'
        #print('the problem was this error:')
        #print(e)
    return var

def add_to_dictionary(subfield, i, xpath):
    """var = get_text(i, xpath)
    if subfield == 'Year':
        var = int(var[1:-1])
    elif subfield=='Gross':
        var = float(var[1:-1])
    elif subfield=='Genre':
        var = var[1:]
    elif subfield == 'Duration':
        var = int(var[: -3])"""
    var = get_text(i, xpath)
    dictionary[subfield].append(var)

def each_page(i):
    print("""Adding values to dictionary
    --------------------------------
    """)
    add_to_dictionary('Title',      i, 'h3//a')
    add_to_dictionary('Year',       i, 'h3//span[2]')
    add_to_dictionary('Duration',   i, 'p[1]//span[@class="runtime"]')
    add_to_dictionary('Genre',      i, 'p[1]//span[@class="genre"]')
    add_to_dictionary('IMDB_score', i, 'div[1]/div[1]//span[2]')
    add_to_dictionary('Votes',      i, 'p[4]//span[2]')
    add_to_dictionary('Gross',      i, 'p[4]//span[5]')

time_taken_items=[]
time_taken_html=[]

@timeit(time_taken_items)
def getting_data_each_page():
    for i in range(1, len(the_list)+1):    
        each_page(i)

@timeit(time_taken_html)
def rotating_pages(page):
    html_content = requests.get(f'https://www.imdb.com/list/ls074451163/?sort=list_order,asc&st_dt=&mode=detail&page={page}')
    tree = html.fromstring(html_content.content)
    print("""Going on this page
    -----------------------------------------------------------
    """)
    print(tree)
    the_list = tree.xpath('//div[@class = "lister-item mode-detail"]')   
    return tree, the_list


# %%
if __name__ == '__main__':
    dictionary = {
        'Title':        [],
        'Year':         [],
        'Duration':     [],
        'Genre':        [],
        'IMDB_score':   [],
        'Votes':        [],
        'Gross':        []
    }

    for page in range(1, 3):

        tree, the_list = rotating_pages(page)
        print('getting the data off the page now')
        getting_data_each_page()



# %%
#movies_df = pd.DataFrame(data=dictionary)
#movies_df.to_csv('movies_scraped#1')
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
    fig, ax = plt.subplots(figsize = (14, 6))

    x = movies_df[xval] # x axis
    y = movies_df[yval]# y axis


    mask1 = ~x.isnull()
    mask2 = ~y.isnull()

    x = x[mask2][mask1]
    y = y[mask1][mask2]

    a, b = np.polyfit(x.to_numpy(), y.to_numpy(), 1
)


    ax.plot(x, a*x + b)

    ax.scatter(x, y, marker='o')

plot_graph('Votes', 'IMDB_score')


# %%
movies_df.dtypes
# %%
