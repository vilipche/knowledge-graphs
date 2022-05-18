# %%
# import libraries
from rdflib import Graph,Literal,RDF,URIRef
from rdflib.namespace import FOAF,XSD,RDFS
from rdflib import Namespace
import pandas as pd
import string
import random
import numpy as np

# ignore the warning
import warnings
warnings.filterwarnings('ignore')

# %%
# Initialize Graph
g = Graph()

# %% [markdown]
# # Supporting Functions

# %%
KG_SDM = Namespace("http://kg_sdm.org/")
g.bind("kg_sdm",KG_SDM) 

# %%
def save_rdf_file(g,filename,rdf_format='ttl'):
    g.serialize(filename+'.'+rdf_format,format= rdf_format)

# %%
# we created this parser as there should not be any forbiden characters in the URI
def URLparse(url:str):
    url=url.replace("\'","_").replace("\"","_")
    for i in string.punctuation:
        url = url.replace(i,"_")
    url = url.replace(" ","_")
    return url

# %% [markdown]
# # Schema Design
# * Once we have created the schema and the TBOX, it's time to populate the graph using triples. 
# * On the image you can see the schema that we will be following in this ABOX
# * We are showing the process of grouping the data from csv files and adding them to the knowledge graph.
# * The upload will be done in parts, each part uploading a different part of the graph

# %% [markdown]
# ![title](B1_TBOX-Sotiroski_Choudhary.png)

# %% [markdown]
# # ABOX Defination

# %% [markdown]
# ## 1. Person

# %%
people_names = pd.read_csv('data_kg_sdm/authors.csv') # getting all the the people names from the authors file
people_names.rename(columns = {'name':'person_name'}, inplace=True)
people_names.head()

# %%
# using the bridge table to connect the author with the school / institution
author_school = pd.read_csv('data_kg_sdm/author_belongs_school.csv')
author_school['author_ID'] = author_school['author_ID'].astype(int)
author_school.head()

# %%
# getting the data for each school
schools = pd.read_csv('data_kg_sdm/schools.csv')
schools.rename(columns = {'name':'school_name'}, inplace=True)
schools.head()

# %%
# merging the academics / people in one table with their related school
academics = pd.merge(schools, author_school, left_on='ID', right_on='org_ID')
academics = pd.merge(academics, people_names, left_on='author_ID', right_on='ID')
academics.head()

# %% [markdown]
# * Once we have all the people/academics we want to divide them depending on their role. 
# We suppose 60% are Authors, 20% Reviewsrs, 10% Chair and Editor.
# 
# * Every variable will hold either the four types of academics which will be used in other parts of the notebook when uploading the triples

# %%
total = len(academics)
nb_auth = int(total * 0.6)
nb_rev = int(total * 0.2)
nb_chair_editor = int(total * 0.1)

# %%
authors = academics.loc[:nb_auth]
reviewers = academics.loc[nb_auth : nb_auth + nb_rev]
chair = academics.loc[nb_auth + nb_rev : nb_auth + nb_rev + nb_chair_editor ]
editor = academics.loc[ nb_auth + nb_rev + nb_chair_editor :nb_auth + nb_rev + nb_chair_editor + nb_chair_editor]

# %%
person_type_list = [authors,reviewers,chair,editor]
person_sub_type_ls = ["Author","Reviewers","Chair","Editor"]

Person = URIRef("http://kg_sdm.org/Person")

for i,person_tp in enumerate(person_type_list):
    # creating the URI for each person type
    preson_sub_type = URIRef(f"http://kg_sdm.org/{person_sub_type_ls[i]}")
    
    for name, school in zip(person_tp['person_name'], person_tp['school_name']):
        # assigning each person a URI
        parsed_name = URLparse(name)
        person_node = URIRef(f"http://kg_sdm.org/Person/{parsed_name}")
        # their literals
        name_lit = Literal(str(name))
        school_lit = Literal(str(school))

        # Connecting the nodes
        # add subclass type
        g.add((person_node, RDF.type, preson_sub_type))
        # add school
        g.add((person_node, KG_SDM.school, school_lit))
        # add name of person
        g.add((person_node, FOAF.name, name_lit))

# %%
# save_rdf_file(g,'person_links','ttl')

# %% [markdown]
# ## 2. Submissions
# In submission we store the articles from an author submitted to a conference

# %% [markdown]
# ### a. Adding Articles(Papers)

# %%
# loading articles
articles = pd.read_csv('data_kg_sdm/articles.csv')

# %%
# The bridge table that connects the articles that an author wrote
author_article = pd.read_csv('data_kg_sdm/author_written_article.csv')
author_article['author_ID'] = author_article['author_ID'].astype(int)
author_article.head()

# %%
paper_type = ['Demo','FullPaper', 'Poster', 'Short']
keywords = ['ML', 'NLP', 'Database', 'Graph']

# %%
# As we don't have some of the data, we are generating the year randomly, 
# the paper type as well as if a paper is accepted or not.
# As we have to label the paper submissions as accepted or rejected, we take the first 500 articles as accepted

articles['year'] = [ random.randint(2000,2022) for i in range(len(articles))]
articles['type'] = [random.choice(paper_type) for i in range(len(articles))]
articles['keyword'] = [random.choice(keywords) for i in range(len(articles))]
articles['accepted'] = ""
articles['accepted'].loc[:500] = True
articles['accepted'].loc[500:] = False

# %%
articles.head()

# %%
# only authors are writing the papers
authors.head()

# %%
# joining the authors and articles with the bridge table
article_pub = pd.merge(articles, author_article, left_on='ID', right_on='article_ID')
articles_publishedin = pd.merge(article_pub, authors, left_on='author_ID', right_on='author_ID')
articles_publishedin = articles_publishedin[['title', 'year', 'type', 'keyword', 'accepted', 'person_name', 'school_name']]

# %%
articles_publishedin.head()

# %%
for _, article_title, year, paper_type, keyword, accepted, author_name, school_name in articles_publishedin.itertuples():
    # get the author node
    author_node = URIRef(f"http://kg_sdm.org/Person/{URLparse(author_name)}")
    
    # create the submission onde
    submission_node = URIRef(f"http://kg_sdm.org/Submission/{URLparse(article_title)}")
    g.add((submission_node, RDF.type, KG_SDM.Submission))
    
    # author wrote a paper
    g.add((author_node, KG_SDM.writes, submission_node))
    
    # data for submission
    paper_title_lit = Literal(str(article_title))
    paper_year_lit = Literal(int(year))
    g.add((submission_node, KG_SDM.paper_title, paper_title_lit))
    g.add((submission_node, KG_SDM.paper_year, paper_year_lit))
                            
    # adding the keywords
    keyword_node = URIRef(f"http://kg_sdm.org/{keyword}")
    g.add((submission_node, KG_SDM.related_to, keyword_node))

    # adding the paper type
    paper_node = URIRef(f"http://kg_sdm.org/{URLparse(paper_type)}")
    g.add((submission_node, KG_SDM.of_type, paper_node))

# %%
# save_rdf_file(g,'submission_links','ttl')

# %% [markdown]
# ### b. DecisionProcess
# Creating the reviewers, their votes and connecting them with the submission

# %%
reviewProcess = articles_publishedin.drop_duplicates(subset=['title'])
reviewProcess.head()

# %%
reviews = []
comments = []
rejacc = []

for i in range(len(reviewProcess)):
    # create N reviewers and comments
    N = random.randint(2,4)
    # assign N reviewers (get a random sample)
    rev_list = list(reviewers.sample(N)['person_name'])
    # for every reviewer get 
    acc = [random.random()>0.5 for i in range(N)]
    com_list = []
    for j in range(N):
        # generating a random comment
        comment = ''.join((random.choice('abcdefghijklmnopqrstuvwxyz') for i in range(5)))
        com_list.append(comment)
    reviews.append(rev_list)
    comments.append(com_list)
    rejacc.append(acc)
    
reviewProcess['reviewer_name'] = reviews
reviewProcess['comment'] = comments
reviewProcess['decision'] = rejacc

# %% [markdown]
# * As you may have noticed, in DecisionProcess we are randomly assigning the accepted/rejected decision for every reviewer, but we have manually created the accepted/rejected submission in the Submission node. 
# 
# * The reason why we did this is because it is more complicated to randomly generate the decisions and then connect with the Submisison node. And also because of the fact that it is artificial data and we won't need to query the accepted/rejected decision.
# 
# * With the way we did the graph, every article that was accepted can be found using a publication.
# 

# %%
reviewProcess.head()

# %%
# because we were storing the comments and decisions and reviewers in an array
# we will use the explode function to have each reviewer connected to the paper
reviewProcess.apply(pd.Series.explode)

# %%
for _, article_name, year, _, _, _, _, _, reviewer_name, comment, accepted in reviewProcess.itertuples():
    # get the submission node
    submission_node = URIRef(f"http://kg_sdm.org/Submission/{URLparse(article_title)}")

    # create the reviewProcess node
    review_process = URIRef(f"http://kg_sdm.org/DecisionProcess/{URLparse(author_name+'_'+article_name)}")
    g.add((review_process, RDF.type, KG_SDM.DecisionProcess))
    
    # connect submission and review process
    g.add((submission_node, KG_SDM.goes_through, review_process))
    
    # get the reviewer node
    reviewer_node = URIRef(f"http://kg_sdm.org/Person/{URLparse(author_name)}")
    g.add((reviewer_node, KG_SDM.participates_in, review_process))
    
    # add the literals
    comment_lit = Literal(str(comment))    
    decision_lit = Literal(bool(accepted))
    g.add((review_process, KG_SDM.comment, comment_lit))
    g.add((review_process, KG_SDM.decision, decision_lit))

# %% [markdown]
# ## 3. Venues
# Loading the Venue file which contains journal and conferences and assigning them

# %% [markdown]
# ### a. Adding Conferences and Journals 

# %%
publications = pd.read_csv('data_kg_sdm/publications.csv')
publications.head()

# %%
journals = publications[publications['Type']=='Journal']
journals.head()

# %%
conferences = publications[publications['Type']!='Journal']
conferences.head()

# %%
# from conferences we split them in 60% worshops and 40% symposiums 
total = len(conferences)
workshops = conferences.iloc[:int(0.4*total):]
symposium = conferences.iloc[int(0.4*total):]

# %%
venue_type_list = [journals,workshops,symposium]
venue_sub_type_ls = ["Journal","Workshop","Symposium"]


for i,venue_tp in enumerate(venue_type_list):
    print(venue_sub_type_ls[i])
    venue_type = venue_sub_type_ls[i]
    venue_sub_type = URIRef(f"http://kg_sdm.org/{venue_type}")
    
    for index,row in venue_tp.iterrows():
        confname = row['name']
        
        # parsing conference
        conf_title = URLparse(confname)
        conf_node = URIRef(f"http://kg_sdm.org/Venue/{conf_title}")
        venue_lit = Literal(str(conf_title))

        # add subclass type
        g.add((conf_node, RDF.type, venue_sub_type))
        # add name of venue
        g.add((conf_node, KG_SDM.venue_title, venue_lit))



# %%
# save_rdf_file(g,'Venue','ttl')

# %% [markdown]
# ### b. Adding submissions submitted in Venues

# %%
# read the articles
articles = pd.read_csv('data_kg_sdm/articles.csv')
articles.head()

# %%
# read all the Venues
publications = pd.read_csv('data_kg_sdm/publications.csv')
publications

# %%
# load article venue merge link
article_publisher_link = pd.read_csv('data_kg_sdm/article_published_by.csv')
article_publisher_link

# %%
# merge article submitted to Venue
article_pub = pd.merge(articles, article_publisher_link, left_on='ID', right_on='article_ID')
articles_publishedin = pd.merge(article_pub, publications, left_on='publisher_ID', right_on='ID',how='left')
articles_publishedin

# %%
# iterating over above combined dataframe and loading the submission submitted_to venues
for index,row in articles_publishedin.iterrows():
    year = row['year']
    year_literal = Literal(int(year))
    submissiontitle = row['title']
    confname = row['name']
    
    # parsing conference
    conf_title = URLparse(confname)
    conf_node = URIRef(f"http://kg_sdm.org/Venue/{conf_title}")

    # parsing submission
    sub_title = URLparse(submissiontitle)
    sub_node = URIRef(f"http://kg_sdm.org/Submission/{sub_title}")
    
    # connect conference and submission
    g.add((sub_node,KG_SDM.submitted_to,conf_node))



# %%


# %%


# %% [markdown]
# ### c. Adding Submissions in Publication 

# %%
articles = pd.read_csv('data_kg_sdm/articles.csv')
articles['accepted'] = ""
articles['accepted'].loc[:500] = True
articles['accepted'].loc[500:] = False
articles.head()

# %%
# load article venue merge link
article_publisher_link = pd.read_csv('data_kg_sdm/article_published_by.csv')
article_publisher_link

# %%
articles_publishedin = pd.merge(articles, article_publisher_link, left_on='ID', right_on='article_ID')
articles_publishedin

# %% [markdown]
# #### I. Adding Journal publications in Volume

# %%
# Get all the journals  
articles_publishedin_journal = pd.merge(articles_publishedin, journals, left_on='publisher_ID', right_on='ID')
articles_publishedin_journal

# %%
# Adding the journals in volumes only which are accepted (where decision = True )
for index,row in articles_publishedin_journal.iterrows():
    year = row['year']
    year_literal = Literal(int(year))
    submissiontitle = row['title']
    confname = row['name']
    decision = row['accepted']
    
    # parsing conference
    conf_title = URLparse(confname)
    conf_node = URIRef(f"http://kg_sdm.org/Venue/{conf_title}")

    
    # parsing submission
    sub_title = URLparse(submissiontitle)
    sub_node = URIRef(f"http://kg_sdm.org/Submission/{sub_title}")

    
    # parsing for publication
    # assuming only half of the articles got accepted
    if decision:
        Pub_title = conf_title+'_volume_'+str(random.randint(1, 5))
        Pub_title_lit = Literal(str(Pub_title))
        
        pub_node = URIRef(f"http://kg_sdm.org/Publication/{Pub_title}")
        g.add((pub_node, RDF.type, KG_SDM.Volume))
        g.add((sub_node,KG_SDM.published_in,pub_node))
        g.add((pub_node, KG_SDM.publication_title,Pub_title_lit))
        g.add((pub_node, KG_SDM.publication_year,year_literal))

# %% [markdown]
# #### II. Adding Conference publications in Proceddings

# %%
# get all the conferences
conferences = workshops.append(symposium)
conferences

# %%
articles_publishedin_conf = pd.merge(articles_publishedin, conferences, left_on='publisher_ID', right_on='ID')
articles_publishedin_conf

# %%
# Adding the conference in Proceddings only which are accepted (where decision = True )
for index,row in articles_publishedin_conf.iterrows():
    year = row['year']
    year_literal = Literal(int(year))
    submissiontitle = row['title']
    confname = row['name']
    decision = row['accepted']
    
    # parsing conference
    conf_title = URLparse(confname)
    conf_node = URIRef(f"http://kg_sdm.org/Venue/{conf_title}")

    
    # parsing submission
    sub_title = URLparse(submissiontitle)
    sub_node = URIRef(f"http://kg_sdm.org/Submission/{sub_title}")

    
    # parsing for publication
    # assuming only half of the articles got accepted
    if decision:
        Pub_title = conf_title+'_proceddings'
        Pub_title_lit = Literal(str(Pub_title))
        
        pub_node = URIRef(f"http://kg_sdm.org/Publication/{Pub_title}")
        g.add((pub_node, RDF.type, KG_SDM.Proceddings))
        g.add((sub_node,KG_SDM.published_in,pub_node))
        g.add((pub_node, KG_SDM.publication_title,Pub_title_lit))
        g.add((pub_node, KG_SDM.publication_year,year_literal))

# %%


# %% [markdown]
# ### d. Adding handlers
# 
# * conferences are handled by chair
# * Journals are handled by editor

# %%
# As defined in person
chair.head()

# %%
# editor as defined in journal
editor.head()

# %%
journals['editors'] = editor.iloc[:len(journals)]['person_name'].values
journals.head()

# %%
# getting list of chairs
chair_names = list(chair['person_name'].values)
# since we do not have chair in our data, generating random peopels from chair to handle the conferences
conf_chairs = [chair_names[random.randint(0,len(chair_names)-1)]  for i in range(len(conferences))]
# saving conference handlers
conferences['chair'] = conf_chairs
conferences

# %%
# adding the chair handlers
for index,row in conferences.iterrows():
    authorname = row['chair']
    confname = row['name']

    # parsing conference
    conf_title = URLparse(confname)
    conf_node = URIRef(f"http://kg_sdm.org/venue/{conf_title}")
    venue_lit = Literal(str(conf_title))

    # parsing authors
    per_title = URLparse(authorname)
    per_node = URIRef(f"http://kg_sdm.org/Person/{per_title}")


    g.add((per_node, KG_SDM.handles, conf_node))

# %%
# adding the editor handlers
for index,row in journals.iterrows():
    authorname = row['editors']
    confname = row['name']

    # parsing conference
    conf_title = URLparse(confname)
    conf_node = URIRef(f"http://kg_sdm.org/venue/{conf_title}")
    venue_lit = Literal(str(conf_title))

    # parsing authors
    per_title = URLparse(authorname)
    per_node = URIRef(f"http://kg_sdm.org/Person/{per_title}")


    g.add((per_node, KG_SDM.handles, conf_node))

# %%


# %% [markdown]
# ## 4. Saving the Graph

# %%
save_rdf_file(g,"abox",rdf_format='ttl')

# %%



