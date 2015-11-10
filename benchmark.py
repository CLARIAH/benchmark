#!/usr/bin/python
# -*- coding: utf-8 -*-

from SPARQLWrapper import SPARQLWrapper, BASIC, JSON
from os import listdir
from datetime import datetime

sparql_virtuoso = SPARQLWrapper("http://virtuoso.clariah-sdh.eculture.labs.vu.nl/sparql")

sparql_stardog_canada = SPARQLWrapper("http://stardog.clariah-sdh.eculture.labs.vu.nl/canada1901/query")
sparql_stardog_canada.setHTTPAuth(BASIC)
sparql_stardog_canada.setCredentials("user", "pwd")

sparql_stardog_clio = SPARQLWrapper("http://stardog.clariah-sdh.eculture.labs.vu.nl/clio/query")
sparql_stardog_clio.setHTTPAuth(BASIC)
sparql_stardog_clio.setCredentials("user", "pwd")

sparql_stardog = SPARQLWrapper("http://stardog.clariah-sdh.eculture.labs.vu.nl/clariah/query")
sparql_stardog.setHTTPAuth(BASIC)
sparql_stardog.setCredentials("user", "pwd")


test_stardog = False  
test_virtuoso = True    

bufsize = 0
outfile = open('runtimes.dat','a', bufsize);


print "query \t\t\tstardog \t\tvirtuoso"
outfile.write("query\tstardog\tvirtuoso\n")

files = [ f for f in listdir("wp4-queries/") if f.endswith("rq") and f.startswith("")]
for f in files:
    query_virtuoso = file("wp4-queries/" + f).read()

    query_stardog = "" 
    for line in open("wp4-queries/" + f):
        if not (line.startswith("FROM") or line.startswith("#")):
            query_stardog += line
    

    print f + "\t",
    outfile.write(f + "\t",)
    
    if test_stardog: 
        try: 
            s0 = datetime.now()
            
            if (f.startswith("canada") or f.startswith("canfam")):
                
                sparql_stardog_canada.setQuery(query_stardog)
                sparql_stardog_canada.setReturnFormat(JSON)
                stardogresults = sparql_stardog_canada.query().convert()
                
                s1 = datetime.now()
                runtime = s1 - s0 
                print(format(runtime)),
                outfile.write(str(runtime.total_seconds()),)
                
            elif f.startswith("clio"):
                sparql_stardog_clio.setQuery(query_stardog)
                sparql_stardog_clio.setReturnFormat(JSON)
                stardogresults = sparql_stardog_clio.query().convert()
                
                s1 = datetime.now()
                runtime = s1 - s0 
                print(format(runtime)),
                outfile.write(str(runtime.total_seconds()),)
                                
            else:
                print "else"
                sparql_stardog.setQuery(query_stardog)
                sparql_stardog.setReturnFormat(JSON)
                stardogresults = sparql_stardog.query().convert()
                
                s1 = datetime.now()
                runtime = s1 - s0 
                print(format(runtime)),
                outfile.write(str(runtime.total_seconds()),)
            
        except Exception,e: 
            print str(e), 
    
    else: 
        print "-",
        outfile.write("NA",)
        
    if test_virtuoso: 
        try: 
            v0 = datetime.now()
            sparql_virtuoso.setQuery(query_virtuoso)
            sparql_virtuoso.setReturnFormat(JSON)
            virtuosoresults = sparql_virtuoso.query().convert()
            
            v1 = datetime.now()
            runtime = v1 - v0 
            print "\t\t " + format(v1-v0)
            outfile.write("\t" + str(runtime.total_seconds()) + "\n")
            
        except Exception,e: 
            print str(e)
            
    else:
        print "-"
        outfile.write("NA\n")


                    
#      

#     samelength = len(stardogresults["results"]["bindings"]) == len(virtuosoresults["results"]["bindings"])
#     if not samelength: 
#         print
#         print "Resultsets are not of the same length: " + str()
#         print "length stardogresults: " + str(len(stardogresults["results"]["bindings"]))
#         print "length virtuosoresults: " + str(len(virtuosoresults["results"]["bindings"]))
    
#     print 
#     for result in stardogresults["results"]["bindings"]:
#         print result 
#           
#     print 
#      
#     for result in virtuosoresults["results"]["bindings"]:
#         print result 
      
      
outfile.close()

  
#     print "Resultset identical: " + str(stardogresults["results"]["bindings"] == virtuosoresults["results"]["bindings"])
#     resultset comparison more complicated, because stardog returns literals and virtuoso typed-literals... 

# print results.info()
# print results.convert()
# print json.dumps(results, sort_keys=True,indent=4, separators=(',', ': '))
