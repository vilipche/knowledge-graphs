# import libraries
from rdflib import Graph,Literal,RDF,URIRef
from rdflib.namespace import FOAF,XSD,RDFS
from rdflib import Namespace

# %%
g = Graph()

# name space is used for the graph general URIref, now we can add 
# multiple objects with kg_sdm uri (/Author, /School) etc.
KG_SDM = Namespace("http://kg_sdm.org/")
g.bind("kg_sdm",KG_SDM)


#======================================================================================================
# Properties

g.add((KG_SDM.comment, RDFS.domain, KG_SDM.DecisionProcess))
g.add((KG_SDM.comment, RDFS.range, XSD.string))
g.add((KG_SDM.comment, RDFS.label, Literal("comment")))



g.add((KG_SDM.goes_through, RDFS.domain, KG_SDM.Submission))
g.add((KG_SDM.goes_through, RDFS.range, KG_SDM.DecisionProcess))
g.add((KG_SDM.goes_through, RDFS.label, Literal("goes_through")))



g.add((KG_SDM.handles, RDFS.domain, KG_SDM.Handler))
g.add((KG_SDM.handles, RDFS.range, KG_SDM.Venue))
g.add((KG_SDM.handles, RDFS.label, Literal("handles")))


g.add((FOAF.name, RDFS.domain, FOAF.Person))
g.add((FOAF.name, RDFS.range, XSD.string))
g.add((FOAF.name, RDFS.label, Literal("name")))


g.add((KG_SDM.of_type, RDFS.domain, KG_SDM.Submission))
g.add((KG_SDM.of_type, RDFS.range, KG_SDM.PaperType))
g.add((KG_SDM.of_type, RDFS.label, Literal("of_type")))


g.add((KG_SDM.paper_title, RDFS.domain, KG_SDM.Submission))
g.add((KG_SDM.paper_title, RDFS.range, XSD.string))
g.add((KG_SDM.paper_title, RDFS.label, Literal("paper_title")))



g.add((KG_SDM.paper_year, RDFS.domain, KG_SDM.Submission))
g.add((KG_SDM.paper_year, RDFS.range, XSD.integer))
g.add((KG_SDM.paper_year, RDFS.label, Literal("paper_year")))


g.add((KG_SDM.publication_title, RDFS.domain, KG_SDM.Publication))
g.add((KG_SDM.publication_title, RDFS.range, XSD.string))
g.add((KG_SDM.publication_title, RDFS.label, Literal("publication_title")))


g.add((KG_SDM.publication_year, RDFS.domain, KG_SDM.Publication))
g.add((KG_SDM.publication_year, RDFS.range, XSD.integer))
g.add((KG_SDM.publication_year, RDFS.label, Literal("publication_year")))



g.add((KG_SDM.published_in, RDFS.domain, KG_SDM.Submission))
g.add((KG_SDM.published_in, RDFS.range, KG_SDM.Publication))
g.add((KG_SDM.published_in, RDFS.label, Literal("published_in")))


g.add((KG_SDM.related_to, RDFS.domain, KG_SDM.Submission))
g.add((KG_SDM.related_to, RDFS.range, KG_SDM.Keyword))
g.add((KG_SDM.related_to, RDFS.label, Literal("related_to")))


g.add((KG_SDM.participates_in, RDFS.domain, KG_SDM.Reviewers))
g.add((KG_SDM.participates_in, RDFS.range, KG_SDM.DecisionProcess))
g.add((KG_SDM.participates_in, RDFS.label, Literal("participates_in")))



g.add((KG_SDM.school, RDFS.domain, KG_SDM.Academic))
g.add((KG_SDM.school, RDFS.range, XSD.string))
g.add((KG_SDM.school, RDFS.label, Literal("school")))



g.add((KG_SDM.submitted_to, RDFS.domain, KG_SDM.Submission))
g.add((KG_SDM.submitted_to, RDFS.range, KG_SDM.Venue))
g.add((KG_SDM.submitted_to, RDFS.label, Literal("submitted_to")))


g.add((KG_SDM.venue_title, RDFS.domain, KG_SDM.Venue))
g.add((KG_SDM.venue_title, RDFS.range, XSD.string))
g.add((KG_SDM.venue_title, RDFS.label, Literal("venue_title")))


g.add((KG_SDM.writes, RDFS.domain, KG_SDM.Author))
g.add((KG_SDM.writes, RDFS.range, KG_SDM.Submission))
g.add((KG_SDM.writes, RDFS.label, Literal("writes")))



#=================================================================================================================
# Subclasses

g.add((KG_SDM.Academic,RDFS.subClassOf,FOAF.Person))
g.add((KG_SDM.Academic, RDFS.label, Literal("Academic")))



g.add((KG_SDM.Author,RDFS.subClassOf,KG_SDM.Academic))
g.add((KG_SDM.Academic, RDFS.label, Literal("Author")))



g.add((KG_SDM.Reviewers,RDFS.subClassOf,KG_SDM.Academic))
g.add((KG_SDM.Reviewers, RDFS.label, Literal("Reviewers")))


g.add((KG_SDM.Handler,RDFS.subClassOf,KG_SDM.Academic))
g.add((KG_SDM.Handler, RDFS.label, Literal("Handler")))


g.add((KG_SDM.Chair,RDFS.subClassOf,KG_SDM.Handler))
g.add((KG_SDM.Chair, RDFS.label, Literal("Chair")))

g.add((KG_SDM.Editor,RDFS.subClassOf,KG_SDM.Handler))
g.add((KG_SDM.Editor, RDFS.label, Literal("Editor")))


g.add((KG_SDM.Conference,RDFS.subClassOf,KG_SDM.Venue))
g.add((KG_SDM.Conference, RDFS.label, Literal("Conference")))


g.add((KG_SDM.Symposium,RDFS.subClassOf,KG_SDM.Conference))
g.add((KG_SDM.Symposium, RDFS.label, Literal("Symposium")))


g.add((KG_SDM.Workshop,RDFS.subClassOf,KG_SDM.Conference))
g.add((KG_SDM.Workshop, RDFS.label, Literal("Workshop")))


g.add((KG_SDM.Journal,RDFS.subClassOf,KG_SDM.Venue))
g.add((KG_SDM.Journal, RDFS.label, Literal("Journal")))


g.add((KG_SDM.Demo,RDFS.subClassOf,KG_SDM.PaperType))
g.add((KG_SDM.Demo, RDFS.label, Literal("Demo")))


g.add((KG_SDM.FullPaper,RDFS.subClassOf,KG_SDM.PaperType))
g.add((KG_SDM.FullPaper, RDFS.label, Literal("FullPaper")))



g.add((KG_SDM.Short,RDFS.subClassOf,KG_SDM.PaperType))
g.add((KG_SDM.Short, RDFS.label, Literal("Short")))



g.add((KG_SDM.Poster,RDFS.subClassOf,KG_SDM.PaperType))
g.add((KG_SDM.Poster, RDFS.label, Literal("Poster")))


g.add((KG_SDM.Proceddings,RDFS.subClassOf,KG_SDM.Publication))
g.add((KG_SDM.Proceddings, RDFS.label, Literal("Proceddings")))


g.add((KG_SDM.Volume,RDFS.subClassOf,KG_SDM.Publication))
g.add((KG_SDM.Volume, RDFS.label, Literal("Volume")))



g.add((KG_SDM.ML,RDFS.subClassOf,KG_SDM.Keyword))
g.add((KG_SDM.ML, RDFS.label, Literal("ML")))


g.add((KG_SDM.NLP,RDFS.subClassOf,KG_SDM.Keyword))
g.add((KG_SDM.NLP, RDFS.label, Literal("NLP")))


g.add((KG_SDM.Graph,RDFS.subClassOf,KG_SDM.Keyword))
g.add((KG_SDM.GRAPH, RDFS.label, Literal("Graph")))


g.add((KG_SDM.Database,RDFS.subClassOf,KG_SDM.Keyword))
g.add((KG_SDM.Database, RDFS.label, Literal("Database")))


# ===================================================================================================================
# saving RDFS graph
# ## Saving TBOX

save_format = "ttl"
file_name = "tbox"+"."+save_format
g.serialize(file_name, format=save_format)

