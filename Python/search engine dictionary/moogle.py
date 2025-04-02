#################################################################
# FILE : moogle.py
# WRITER : yair mahfud , yairthfc 
# EXERCISE : intro2cs ex6 2022-2023
# DESCRIPTION: A simple program that creates a search engine to given pages
# STUDENTS I DISCUSSED THE EXERCISE WITH: no one
# WEB PAGES I USED:
# NOTES: 
#################################################################
import sys
import urllib.parse
import bs4
import requests
import pickle
import copy

args = sys.argv
if (args[1] == 'crawl') or (args[1] == 'words_dict'):
    base_url = args[2]
    index_file = args[3]
    out_file = args[4]
if args[1] == 'page_rank':
    iterations = args[2]
    dict_file = args[3]
    out_file = args[4]
if args[1] == 'search':
    try:
        query = args[2]
        ranking_dict_file = args[3]
        words_dict_file = args[4]
        max_results = args[5]
    except:
        ranking_dict_file = args[2]
        words_dict_file = args[3]
        max_results = args[4]

def open_index_file():
    """opening the index file and getting the pages as a list"""
    list_of_names = []
    with open(index_file) as pages:
        for line in pages.readlines():
            list_of_names.append(line)
    for i in range(len(list_of_names)):
        if "\n" in list_of_names[i]:
            list_of_names[i] = list_of_names[i][:-1]
    return list_of_names

def list_of_urls():
    """getting the list of urls of the pages by combining the base url to the names list"""
    list_of_names = open_index_file()
    full_links = []
    for link in list_of_names:
        full_url = urllib.parse.urljoin(base_url, link)
        full_links.append(full_url)
    return full_links

def get_connections(html):
    """getting the connections(links) for a htmk given"""
    all_connected_links = []
    soup = bs4.BeautifulSoup(html, 'html.parser')
    paragraphs = soup.find_all("p")
    for p in paragraphs:
        for link in p.find_all("a"):
            target = link.get("href")
            all_connected_links.append(target)
    return all_connected_links

def connections_count(all_connections, url):
    """gets a url and list of connections an checks how many times the url is in there"""
    count = 0
    for x in range(len(all_connections)):
        if url == all_connections[x]:
            count +=1
    return count

def dict_for_each_link(html):
    """for every url in the list of urls, it checks how many times the url is in the html page
    and builds a dictionary for the html according to it"""
    all_names = open_index_file()
    all_urls = list_of_urls()
    link_dict = {}
    for i in range(len(all_names)):
        all_connections = get_connections(html)
        count = connections_count(all_connections, all_names[i])
        if count != 0:
            link_dict[all_names[i]] = count
    return link_dict


def traffic_dict():
    """the main dict which takes a url,gets its html and gets his own connections dict"""
    main_dict = {}
    all_names = open_index_file()
    all_urls = list_of_urls()
    all_htmls = []
    for j in range(len(all_urls)):
        response = requests.get(all_urls[j])
        all_htmls.append(response.text)
    for i in range(len(all_names)):
        html = all_htmls[i]
        main_dict[all_names[i]] = dict_for_each_link(html)
    return main_dict

if args[1] == 'page_rank':
    with open(dict_file, 'rb') as f:
        d = pickle.load(f)
    LIST_OF_KEYS = d.keys()

def key_number_of_outgoing():
    """get from the connections dictionary the number of links going out from a page"""
    outgoings_dict = {}.fromkeys(LIST_OF_KEYS, 0)
    for key in LIST_OF_KEYS:
        total = 0
        for key2 in d[key]:
            num = d[key][key2]
            total += num
        outgoings_dict[key] = total
    return outgoings_dict

def get_new_r(r):
    """getting the new score for each page using the formula"""
    outgoing_dict = key_number_of_outgoing()
    new_r = {}.fromkeys(LIST_OF_KEYS, 0)
    for key in LIST_OF_KEYS:
        for key2 in d[key]:
            new_r[key2] += ((r[key] * (d[key][key2])) / outgoing_dict[key])
    return new_r

def run_iterations():
    """run the new score function several times according to the number given"""
    r = {}.fromkeys(LIST_OF_KEYS, 1)
    for num in range(int(iterations)):
        temp_r = copy.deepcopy(r)
        for key in LIST_OF_KEYS:
            new_r = get_new_r(temp_r)
            r[key] = new_r[key]
    return r



def get_word_dict(html):
    """getting a word dict for an html given using a starting dict and counting the number of times
    each word id in the text"""
    word_dict = {}
    soup = bs4.BeautifulSoup(html)
    for p in soup.find_all("p"):
        content = p.text
        p_word_dict = starting_dict(content) 
        replaced = content.replace('\n', ' ')
        text_list = replaced.split(" ")
        for word in text_list:
            p_word_dict[word] += 1
        for word in p_word_dict:
            if len(word) > 0:
                if word in word_dict:
                    word_dict[word] += p_word_dict[word]
                else:
                    word_dict[word] = 0
                    word_dict[word] += p_word_dict[word]
    return word_dict
        

def starting_dict(content):
    """getting a starting dict for a text with each word count counts 0"""
    word_dict = {}
    replaced = content.replace('\n', ' ')
    text_list = replaced.split(" ")
    for word in text_list:
        word_dict[word] = 0
    return word_dict

def full_word_dict():
    """getting a page word dict and adding it to the full word dict, with adding each word of
    the page dict into the full word dict and adding tot the word dict the number of times its 
    in a page.doing it with every page until we have a full word dict containing all the words
    in all pages"""
    full_word_dict = {}
    all_names = open_index_file()
    all_urls = list_of_urls()
    all_htmls = []
    for j in range(len(all_urls)):
        response = requests.get(all_urls[j])
        all_htmls.append(response.text)
    for i in range(len(all_names)):
        page_dict = get_word_dict(all_htmls[i])
        for word in page_dict:
            if word in full_word_dict :
                full_word_dict[word][all_names[i]] = page_dict[word]
            else:
                full_word_dict[word] = {}
                full_word_dict[word][all_names[i]] = page_dict[word]
    return full_word_dict

if args[1] == 'search':
    with open(ranking_dict_file, 'rb') as f:
        ranking = pickle.load(f)
    with open(words_dict_file, 'rb') as f:
        word_dict = pickle.load(f)
    LIST_OF_RANKING_KEYS = ranking.keys()
    LIST_OF_WORD_DICT_KEYS = word_dict.keys()

def list_of_search_words():
    """spliting the given string into words and into a list"""
    list_of_words = query.split(" ")
    for word in list_of_words:
        if word not in LIST_OF_WORD_DICT_KEYS:
            list_of_words.remove(word)
    return list_of_words

def cut_uncommon_options():
    """take page options that does not contains all the words given and does not include them
    in a new possible page options list"""
    cutted_list = []
    search_word_list = list_of_search_words()
    for key in LIST_OF_RANKING_KEYS:
        counter = 0
        for word in search_word_list:
            if key in word_dict[word]:
                counter += 1
            else:
                break
        if counter == len(search_word_list):
            cutted_list.append(key)
    return cutted_list


def rank_possible_options():
    """rank the possible options out of the cutted list using sort according to the pages
    rank in the ranking dict"""
    list_of_options = cut_uncommon_options()
    values_list = []
    for option in list_of_options:
        key = ranking[option]
        values_list.append(key)
    values_list.sort(reverse=True)
    sorted_options_list = []
    for i in range(len(values_list)):
        for j in list_of_options:
            if ranking[j] == values_list[i]:
                sorted_options_list.append(j)
    return sorted_options_list

def get_max_results():
    """get the sorted options list and take the max results according to the number given"""
    max = int(max_results)
    sorted_options_list = rank_possible_options()
    maxed_sorted_list = []
    for i in range(max):
        maxed_sorted_list.append(sorted_options_list[i])
    return maxed_sorted_list

def get_lowest_num_of_references(page):
    """for a page take the lowest number of refrences out of the words given,in the page"""
    ref_num_list = []
    for word in list_of_search_words():
        ref_num = word_dict[word][page]
        ref_num_list.append(ref_num)
    ref_num_list.sort()
    return ref_num_list[0]

def calculated_score(page):
    """calculate the rank of a page given using the ranking and the lowest num of refrences"""
    z = get_lowest_num_of_references(page)
    y = ranking[page]
    return z*y

def sorted_final_ranking():
    """take the pages given from the max results and and sort them by their calculated score"""
    list_of_pages = get_max_results()
    pages_calculation = []
    for page in list_of_pages:
        value = calculated_score(page)
        pages_calculation.append(value)
    pages_calculation.sort(reverse=True)
    sorted_options_list = []
    for i in range(len(pages_calculation)):
        for j in list_of_pages:
            if calculated_score(j) == pages_calculation[i]:
                sorted_options_list.append(j)
    return sorted_options_list, pages_calculation

def return_page_rank():
    """prints the ranking"""
    if len(list_of_search_words()) == 0 or ("" in list_of_search_words()):
        return None
    else:
        pages, scores = sorted_final_ranking()
        for i in range(len(scores)):
            print(pages[i] + " " + str(scores[i]))

def main():
    if args[1] == 'crawl':
        with open(out_file, 'wb') as f:
            pickle.dump(traffic_dict(), f)
    if args[1] == 'page_rank':
        with open(out_file, 'wb') as f:
            pickle.dump(run_iterations(), f)
    if args[1] == 'words_dict':
        with open(out_file, 'wb') as f:
            pickle.dump(full_word_dict(), f)
    if args[1] == 'search':
        return_page_rank()

if __name__ == "__main__":
    main()
