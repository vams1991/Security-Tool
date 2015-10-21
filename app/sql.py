import mechanize
import cookielib
from BeautifulSoup import BeautifulSoup
import html2text
import socket
import xml.dom.minidom as XY
import os
import xml
from HTMLParser import HTMLParser
import cPickle
import Form
import re
import sys
from crawler import main
import xml.etree.ElementTree as ET
from flask import render_template, flash, redirect,jsonify
import flask

reload(sys)  
sys.setdefaultencoding('utf8')
#SOCKS_PROXY_HOST = '127.0.0.1'
#SOCKS_PROXY_PORT = 8080

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

def chkSQLInjection(opstring):

    flash("Analysing response...")
    tree = ET.parse('app/errors.xml')
    root=tree.getroot()
    errorList=root.findall('error')
    i=0
    # file = open('Output.txt', 'r')
    for line in errorList:
        error=(str(errorList[i].attributes["regexp"].value))
        i=i+1
        if re.search(error,opstring):
            return flask.make_response("Possible SQL vulnerability")
           #flash ("Possible SQL vulnerability ")


def create_connection(address, timeout=None, source_address=None):
    sock = socks.socksocket()
    sock.connect(address)
    return sock


def SQL_Module(seed_url,obj):
    flash("Total # urls: " + str(len(obj.getUrlList())))
    socks_enable=0;
    #Create a browser
    ua = 'Mozilla/5.0 (X11; Linux x86_64; rv:18.0) Gecko/20100101 Firefox/18.0 (compatible;)'
    br = mechanize.Browser()
    br.set_handle_robots(False) # ignore robots
    br.addheaders = [('User-Agent', ua), ('Accept', '*/*')]
    
    #SQL Injection
    flash("\n>>Trying level 3 with SQL Injection..")

    tree = ET.parse('app/sqlAttacks.xml')
    root=tree.getroot()
#     for attack in root.findall('attack'):
#         code = attack.find('code').text
#         print code
    try:
        for list in obj.getUrlList():
            i=0
            #open url
            flash(list)
            page= br.open(list)
    
            #Get list of forms
            urlObj=Form.URL(list)
            forms = urlObj.getForms(br)
    
            #loop through the forms
            for attack in root.findall('attack'):
                code = attack.find('code').text
                print ("\n>>Trying "+str(code)) 
                form_number=0
                for form in forms:
                    # form_name=fe.getName()
                    br.select_form(nr=form_number)
                    br.form.set_all_readonly(False)
                    #loop through elements in form
                    for elem in form.getElements():
                        element_name=str(elem["Name"])
                        # print(element_name)
                        br[element_name]=code
                    form_number=form_number+1
    
    
                res = br.submit()
                content=strip_tags(res.read());
                flash (">>Response of SQL Injection")
                content=os.linesep.join([s for s in content.splitlines() if s])
                #flash (content)
                chkSQLInjection(content)
                i=i+1;
                br.back()
    except:
        flash("Link in infinite redirect")



























#Reference
#http://stackoverflow.com/questions/753052/strip-html-from-strings-in-python