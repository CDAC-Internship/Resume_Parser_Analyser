import os 
import json
from django.shortcuts import render, HttpResponse, redirect
import spacy
from .models import *
from pdfminer.high_level import extract_text
import json
import gensim

import re

import pandas as pd 


# Create your views here.

def index (req) :
    return render(request=req, template_name="index.html")

jd = "jd given"

def send_files (req) :
    global jd
    if req.method == "POST" :
        name = req.POST.get("filename")
        jd = req.POST.get("jd")
        files = req.FILES.getlist("file_uploads")
        for file in files :
            upload_files(file_name = name, files = file, job_desc=jd).save()
        print(req)
        print(files, type(files))
    
    # return HttpResponse(str(req))
        return redirect("http://127.0.0.1:8000/results")

# Load model
def load_model() :
    nlp = spacy.load("en_core_web_sm")
    return nlp

def get_cad_skills(doc, db) :
    skills = []
    for token in doc :
        if token.text in db :
            skills.append(token.text)
    return skills

def extract_email(txt : str) :
    epat = "[\w\.-]+@[\w\.-]+"
    email = re.findall(epat, txt)
    return email

def extract_phone(org_text) :
    phpat = r"(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\d{3}\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})"
    ph = re.findall(phpat, org_text)
    return ph

def extract_exp(org_text) :
    exp_pat = "(?P<fmonth>\w+.\d+)\s*(\D|to)\s*(?P<smonth>\w+.\d+|present)"
    exp = re.findall(exp_pat, org_text)
    return exp

def get_similarity(jd_list, cad_skills) :
    pass

result = ""

def resume_parser_model (req) :
    global result
    files = os.listdir("resume_parser_app/media")

    nlp = load_model()

    with open("resume_parser_app/Data/skills_data.json", "r") as f :
        dec_Jdata = f.read()
    f.close()

    skills = json.loads(dec_Jdata)
    # skills = json.load("./Data/skills_data.json")
    res = []

    jd_doc = nlp(jd)

    for file in files :
        info = {}
        info["file_name"] = file
        print(file)
        txt = extract_text(f"resume_parser_app/media/{file}")
        
        # creating doc nlp object 
        doc = nlp(txt)
        
        # candidate skills 
        cad_skills = get_cad_skills(doc, skills)
        info["skills"] = cad_skills

        # candidate email 
        info["email"] = extract_email(txt)

        # candidate phone number 
        info["phone"] = extract_phone(txt)
        
        # candidate exp
        info["experience"] = extract_exp(txt)
        

        res.append(info)
        context = {
            "res" : res,
            "txt" : "text12345",
            "next_line" : "\n\n\n",
            "js" : json.dumps(res, indent=4)
        }
    json_obj = json.dumps(res, indent=4)
    result = json_obj
    # return json_obj
    return render(req, "index.html", context=context)
    # return HttpResponse(str(res))

def export_json(req) :

    response = HttpResponse(result, content_type="json")
    response["Content-Disposition"] = "attachment; filename=output.json"
    return response

def export_csv(req) :
    # df = pd.DataFrame(result)
    data = pd.read_json(result)
    data.to_csv("resume_parser_app/Data/post.csv")
    data = pd.read_csv("resume_parser_app/Data/post.csv")
    response = HttpResponse(data, content_type="csv")
    response["Content-Disposition"] = "attachment; filename=output.csv"
    return response 

def export_xlsx(req) :

    data = pd.read_csv("resume_parser_app/Data/post.csv")
    data.to_excel("resume_parser_app/Data/post.xlsx")
    data = pd.read_excel("resume_parser_app/Data/post.xlsx")
    response = HttpResponse(data, content_type="xlsx")
    response["Content-Disposition"] = "attachment; fiilename=output.xlsx"
    return response

def matching(data, jd) :
    df = pd.DataFrame(data)

    model = gensim.models.Word2Vec(
    window=10,
    min_count =1,
    workers=2
    )

    model.build_vocab(df.sklills,progress_per=1000)

    lst=[]  
    # s="process"
    for i in df.sklills[0]:
        for j in jd:
            p=model.wv.similarity(w1=i, w2=j)
            lst.append(p)
    sum=0;    
    for i in lst:
        if(i>0.5):
            sum+=1
    probability = sum/len(lst)
    return probability
