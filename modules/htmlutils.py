import os
from datetime import datetime
import shutil
from bs4 import BeautifulSoup
import pandas as pd
import json
import pyarrow as pa

class HTMLUtils:
    projectdir=""
    outputdir=""
    active_section_index=0

    def __init__(self,projectdir):
        self.projectdir = projectdir
        self.outputdir = os.path.join(self.projectdir,".output")
        if(not(os.path.isdir(self.outputdir))):
            os.mkdir(self.outputdir)
        self.remove_all_files()
        template_path = os.path.join(self.projectdir,".vimtemplates")
        shutil.copy(os.path.join(template_path,"index.html"),os.path.join(self.projectdir,"index.html"))
        shutil.copy(os.path.join(template_path,"index.css"),os.path.join(self.projectdir,"index.css"))

    def remove_all_files(self):
        all_files = os.listdir(self.outputdir) 
        for f in all_files: 
            os.remove(os.path.join(self.outputdir,f))

    def close_section(self):
        self.active_section_index+=1
        
    def write_text(self,text):
        current_time = datetime.now().timestamp()
        file_path = os.path.join(self.outputdir,f"{current_time}.txt")
        fh = open(file_path,"w")
        fh.write(text)
        fh.close()
        self.add_to_output(file_path)

    def write_image(self,plt):
        current_time = datetime.now().timestamp()
        file_path = os.path.join(self.outputdir,f"{current_time}.png")
        plt.tight_layout(h_pad=2.5)
        plt.savefig(file_path)
        self.add_to_output(os.path.join('/.output',f"{current_time}.png"))
        #plt.clf()
        plt.cla()


    def write_dataframe(self,title,df):
        current_time = datetime.now().timestamp()
        file_path = os.path.join(self.outputdir,f"{current_time}.csv")
        df.to_csv(file_path,sep=',',index=True,header=True)
        self.add_to_output(file_path,title)

    def add_to_output(self,out_file,title=""):
        if ".txt" in out_file:
            with open(os.path.join(self.outputdir,out_file),'r') as file:
                data = file.read()
                file.close()
                self.generate_HTML_text(data)
        elif ".png" in out_file:
            self.generate_HTML_img(os.path.join('/.output',out_file))
        elif ".csv" in out_file:
            df = pd.read_csv(os.path.join(self.outputdir,out_file))
            self.generate_HTML_table(df,title)


    def generate_HTML_text(self,data):
        with open(os.path.join(self.projectdir,"index.html"),"r+") as f:
            contents = f.read()
            soup = BeautifulSoup(contents,'lxml')
            root = soup.find("main",{"id":"root"})
            root_children = root.findChildren(recursive=False)
            new_p = soup.new_tag("p")
            new_p.string=data
            if len(root_children)==self.active_section_index:
                new_div = soup.new_tag("div",attrs={'class':'container'})
                new_div.append(new_p)
                root.append(new_div)
            else:
                last_div = root_children[-1]
                last_div.append(new_p)
            f.seek(0)
            f.write(str(soup))
            f.truncate()
            f.close()

    def generate_HTML_img(self,img_path):
        with open(os.path.join(self.projectdir,"index.html"),"r+") as f:
            contents = f.read()
            soup = BeautifulSoup(contents,'lxml')
            root = soup.find("main",{"id":"root"})
            root_children = root.findChildren(recursive=False)
            img_tag = soup.new_tag("img",attrs={'class':'container-img','src':img_path})
            if len(root_children)==self.active_section_index:
                new_div = soup.new_tag("div",attrs={'class':'container'})
                new_div.append(img_tag)
                root.append(new_div)
            else:
                last_div = root_children[-1]
                last_div.append(img_tag)
            f.seek(0)
            f.write(str(soup))
            f.truncate()
            f.close()
    
    def generate_HTML_table(self,dataframe,title):
        table_soup = BeautifulSoup(dataframe.to_html(),'lxml')
        tables = table_soup.findAll("table")
        for table in tables:
            table['class']="table"

        with open(os.path.join(self.projectdir,"index.html"),"r+") as f:
            contents = f.read()
            soup = BeautifulSoup(contents,'lxml')
            section_title = soup.new_tag("h2",attrs={'class':'title title-section'})
            section_title.string = title
            root = soup.find("main",{"id":"root"})
            root_children = root.findChildren(recursive=False)
            if len(root_children)==self.active_section_index:
                new_div = soup.new_tag("div",attrs={'class':'container'})
                new_div.append(section_title)
                new_div.append(table_soup)
                root.append(new_div)
            else:
                last_div = root_children[-1]
                last_div.append(section_title)
                last_div.append(table_soup)
            f.seek(0)
            f.write(str(soup))
            f.truncate()
            f.close()

