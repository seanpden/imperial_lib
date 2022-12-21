import streamlit as st
import plotly.express as px
import pandas as pd
import requests
from bs4 import BeautifulSoup

# --- CONFIG/SETUP ---

st.set_page_config("main_page.py", ":chart:", "wide")

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.title("README Page")
# --------------------

# --- DATA ---



# ------------

# --- FUNCTIONS ---



# -----------------

# --- PAGE CONTENT ---


with st.expander("__Intro__", True):
    '''

    This is an application created in the pursuit of learning basic web scraping and simple design concepts with streamlit.
    The goal here is to scrape various websites for data relating to the Elder Scrolls lore -- beginning with all the books available in-game --
    then clean, format, and store/display that data. \n

    __If you'd like to just view the results or otherwise use the tool, move on to the other pages in the sidebar!__
    The rest of this page contains information about my learning process and notes for future usage. \n
    
    I plan on expanding this project as I wish to learn and incorporate more about web scraping, data cleansing, and other topics.
    This application's current features, roadmap, and more will be listed both on this page and in my GitHub repository.  
    
    *For now, lets look at what I've implemented...*

    '''

with st.expander("__Write-up__"):
    '''

    This application is currently tuned to scrape for book data from The Elder Scrolls series. I began with 3 sources to scrape from, 
    with the goal to try a different methods of scraping on each source. The sources are:
    - [Fandom.wiki](www.google.com)
    - [UESP](www.google.com)
    - [Imperial Library](www.google.com)

    #### Fandom Wiki
    I decided to approach this source with Pandas own 'read_html' function.
    This is because the wiki provides large tables full of data on their 'books' pages. Since they do this, I curated a list
    of endpoints that include books from each game and concatonated them all together in a dataframe to show the
    end user a concise list of books from all games. A snippit of code that deals with books from TESV: Skyrim specifically is:
    ```py
    skyrim_books = "https://elderscrolls.fandom.com/wiki/Books_(Skyrim)"
    skyrim_books_df = pd.read_html(skyrim_books)
    skyrim_books_df = pd.concat(skyrim_books_df[0:len(skyrim_books_df)])
    ```

    '''

    if st.checkbox("View wiki dataframe..."):
        skyrim_books = "https://elderscrolls.fandom.com/wiki/Books_(Skyrim)"
        skyrim_books_df = pd.read_html(skyrim_books)
        skyrim_books_df = pd.concat(skyrim_books_df[0:len(skyrim_books_df)])
        st.dataframe(skyrim_books_df)
    else:
        pass

    '''

    This works perfectly well with each game but, when all games are concatonated together, provides a dataframe that is ugly and
    unorganized. This is fine for now, though. I simply wanted to explore what was available and how the pandas library handled data.
    I decided it was time to move on and tackle another data source that included tables, this time focusing on cleaning and merging the data.

    #### UESP

    Following a similar format to the wiki, I read the tables from each endpoint. I then tried to clean each table with the goal of having one large
    table of each endpoint to display to the user. Here is a snippit from the skyrim table:
    ```py
    skyrim_books = "https://en.uesp.net/wiki/Skyrim:Books"
    skyrim_books_df = pd.read_html(skyrim_books)
    skyrim_books_df = pd.concat(skyrim_books_df[1:len(skyrim_books_df)])
    skyrim_books_df.drop(columns=['Unnamed: 0', 'Unnamed: 2'], inplace=True)
    ```
    '''

    if st.checkbox("View UESP dataframe..."):
        skyrim_books = "https://en.uesp.net/wiki/Skyrim:Books"
        skyrim_books_df = pd.read_html(skyrim_books)
        skyrim_books_df = pd.concat(skyrim_books_df[1:len(skyrim_books_df)])
        skyrim_books_df.drop(columns=['Unnamed: 0', 'Unnamed: 2'], inplace=True)
        st.dataframe(skyrim_books_df)
    else:
        pass

    '''
    This works perfectly well, and the only change is in dropping the unneeded columns. This strategy even worked for all the games, barring one.
    TES IV: Oblivion threw indexing errors when using this strategy, and I couldn't find many resources about it except for some informing me to reset
    the index, but I still couldn't get them to concatonate correctly. The code for that is:
    ```py

    oblivion_books = "https://en.uesp.net/wiki/Oblivion:Books"
    oblivion_books_df = pd.read_html(oblivion_books)
    for i in range(len(oblivion_books_df)):
        oblivion_books_df[i].rename(columns={"Book Name (ID)": "Title (ID)"}, inplace=True)
        oblivion_books_df[i].rename(columns={"Book Name (ID)": "Title (ID)"}, inplace=True)
        oblivion_books_df[i].rename(columns={"Book Title (ID)": "Title (ID)"}, inplace=True)
        oblivion_books_df[i].rename(columns={"Where this book can be found": "Where to find"}, inplace=True)
        oblivion_books_df[i].rename(columns={"Marker": "Where to find"}, inplace=True) # <-- BUG HERE
    oblivion_books_df = pd.concat(oblivion_books_df[0:len(oblivion_books_df)])
    oblivion_books_df.drop(columns=['Unnamed: 0', 'Unnamed: 2'], inplace=True)
    ```
    ```out
    InvalidIndexError: Reindexing only valid with uniquely valued Index objects
    ```

    As you can see, this section turned into a mess. I wanted to rename the columns that did similar things, so that I could combine them and move on.
    This wouldn't work, as for whatever reason they had matching index's and could not concat. I tried reindexing at various points to no avail. 
    Eventually, this frustrated me enough to move onto my final endpoint to try and properly web scrape through manual HTML parsing... 

    #### Imperial Library

    My favorite source of TES lore, the imperial library has (AFAIK) the most extensive amount of resources for any information about TES universe,
    and conveniently, has not only a list of every book, but each book's text stored as its own endpoint. This inspires another step in my project, but for now
    I'll settle with scraping a list of all TES books. 

    The imperial library's webpage containing each book doesn't contain any tables, just a bunch of text that has a book title, a link to the book, a book author, and often
    a book summary. Because there is no table, I figured 'read_html' would not do the job for me. I decided to look into BeautifulSoup instead. 

    I don't have much knowledge of HTML or CSS, so looking into the different page elements was a lengthy process. I followed some beginner's guides for beautiful soup,
    mostly one from 'realpython', and got to work. 

    I of course firstly need to provide the URL I'll be hitting, then attempt to parse that URL. This is done using the requests library in python, then feeding that response to
    soup's constructor method:

    ```py
    URL = "https://www.imperial-library.info/books/all/by-title"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    ```

    Once here, I can view the raw html of the page. I decide my next step is to identify what element is storing the text for the book information, then storing that in a variable.
    ```py
    title_results = soup.find_all("span", class_="views-field views-field-title")
    ```

    This works perfectly, and I can check out each title at this point if I'd like.
    ```py
    title_fields = soup.find_all("span", class_="views-field views-field-title")
    for i in range(len(title_fields):
        title_fields[i].text.strip()
    ```
    Same if I were to replace the class name with the generic author field, or the generic summary...
    The only problem is, each section of title, author, and summary isn't housed in a div that is similarly named, so I can't just iterate down each element to read each title, author, and summary. 
    Each 'Section' is housed in an '<li> <\li>' with three 'spans', one housing a title, one housing an author, and one housing a summary. 
    The class name of each section is different, but I can create the class name by iterating through the length of the elements. 
    ex. class names:
    ```
    "views-row views-row-1 views-row-odd views-row-first"
    "views-row views-row-2 views-row-even"
    "views-row views-row-3 views-row-odd"
    "views-row views-row-4 views-row-even"
    ...
    "views-row views-row-5492 views-row-even views-row-last"
    ```

    My solution is not elegant, I'm sure there are significantly more effecient ways of doing this. However, this is my first time doing this so my naive approach works for now.
    ```py
    que_list = [] # list of class names generated

    print("Creating que list...")
    # Even or odd | first, other, last
    for i in range(len(title_results)):
        ind = i+1

        # even or odd
        if (ind) % 2 == 0:
            num_is = "even"
        else:
            num_is = "odd"

        if ind == 1:
            que = "views-row views-row-%s views-row-%s views-row-first" % (str(ind), num_is)
            # print(que)
        elif ind == len(title_results):
            que = "views-row views-row-%s views-row-%s views-row-last" % (str(ind), num_is)
        else:
            que = "views-row views-row-%s views-row-%s" % (str(ind), num_is)

        que_list.append(que)
    print("Done with que list...")

    df = pd.DataFrame({"cust_index": [], "Title": [], "Author": [], "Summary": []})

    print("iterate through groups...")
    for group in range(len(que_list)): # iterate through each section of text that contatins title, author, summ
        # print("iterate through items in groups...")
        for ele in soup.find_all("li", class_=que_list[group]): # iterate through each subsection of title, author, sum 
            title_ele = ele.find(class_="views-field views-field-title")
            if title_ele is not None:
                title_ele = title_ele.text.strip()
            author_ele = ele.find(class_="views-field views-field-field-author-value")
            if author_ele is not None:
                author_ele = author_ele.text.strip()
            summary_ele = ele.find(class_="views-field views-field-field-summary-value")
            if summary_ele is not None:
                summary_ele = summary_ele.text.strip()
            df_row = [group, title_ele, author_ele, summary_ele]

            df.loc[len(df)] = df_row

        print("{:.2f} percent complete...".format((group/len(que_list))*100))
    print("done with groups")
    ```

    the runtime of this is very long, as there are ~6,000 books listed and I am iterating over each section, then a title, an author, and a book summary, then constructing 
    a dataframe from that section. I will include a button that will run the code and provide the output below, but _*BE WARNED*_, the runtime is very long and is not worth 
    the wait. I instead ran this once, then stored the data in a CSV to access later. 
    '''

    if st.checkbox("DON'T DO IT! View Imperial Library dataframe..."):
        URL = "https://www.imperial-library.info/books/all/by-title"
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")

        title_results = soup.find_all("span", class_="views-field views-field-title")

        que_list = []

        print("Creating que list...")
        # Even or odd | first, other, last | 
        for i in range(len(title_results)):
            ind = i+1

            # even or odd
            if (ind) % 2 == 0:
                num_is = "even"
            else:
                num_is = "odd"

            if ind == 1:
                que = "views-row views-row-%s views-row-%s views-row-first" % (str(ind), num_is)
                # print(que)
            elif ind == len(title_results):
                que = "views-row views-row-%s views-row-%s views-row-last" % (str(ind), num_is)
            else:
                que = "views-row views-row-%s views-row-%s" % (str(ind), num_is)

            que_list.append(que)
        print("Done with que list...")


        df = pd.DataFrame({"cust_index": [], "Title": [], "Author": [], "Summary": []})

        print("iterate through groups...")
        for group in range(len(que_list)): # iterate through each section of text that contatins title, author, summ
            # print("iterate through items in groups...")
            for ele in soup.find_all("li", class_=que_list[group]): # iterate through each subsection of title, author, sum 
                title_ele = ele.find(class_="views-field views-field-title")
                if title_ele is not None:
                    title_ele = title_ele.text.strip()
                author_ele = ele.find(class_="views-field views-field-field-author-value")
                if author_ele is not None:
                    author_ele = author_ele.text.strip()
                summary_ele = ele.find(class_="views-field views-field-field-summary-value")
                if summary_ele is not None:
                    summary_ele = summary_ele.text.strip()
                df_row = [group, title_ele, author_ele, summary_ele]

                df.loc[len(df)] = df_row
                

            print("{:.2f} percent complete...".format((group/len(que_list))*100))
        print("done with groups")

        st.write(df)
    else:
        pass

    '''

    I am aware this is a mess, but it works for now. The resulting dataframe is what I wanted, though -- just without links to each book. I think my next goal is to
    grab the link to each book, store it in the dataframe, then access that endpoint and scrape for the book content. 

    Looking back at the tutorial, it seems that it would have been much easier if each container for the book information was named the same, then I could have just performed
    something like this:

    ```py
    job_elements = results.find_all("div", class_="card-content")
    for job_element in job_elements:
        title_element = job_element.find("h2", class_="title")
        company_element = job_element.find("h3", class_="company")
        location_element = job_element.find("p", class_="location")
        print(title_element)
        print(company_element)
        print(location_element)
        print()
    ```

    '''

with st.expander("Usage"):
    st.write("Usage")

with st.expander("Roadmap"):
    '''
    
    - [x] Explore the basics of web scraping
    - [x] Pull a list of books, book authors, and summaries from all in-game books 
    - [ ] Pull the links to each book, add them as a seperate column in the DF
    - [ ] Ability to search the list of books, then point to an address and display the book content

    
    '''
    # st.write("Roadmap")


# --------------------