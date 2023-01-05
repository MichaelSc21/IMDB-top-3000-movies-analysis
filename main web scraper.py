# %%
import requests
from lxml import html
import time
import pandas as pd
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
        var = None
        #print('the problem was this error:')
        #print(e)
    return var

def add_to_dictionary(subfield, i, xpath):
    var = get_text(i, xpath)
    dictionary[subfield].append(var)

def each_page(i):

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

    for page in range(1, 30):

        tree, the_list = rotating_pages(page)
        getting_data_each_page()



movies_df = pd.DataFrame(data=dictionary)
movies_df.to_csv('movies_scraped#1')


# %%
