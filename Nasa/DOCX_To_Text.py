#import sys
#from pdfminer.high_level import extract_text_to_fp, extract_text
#from pdfminer.layout import LAParams
from nltk.tokenize import word_tokenize
#from nltk.corpus import stopwords
#from io import StringIO
#from bs4 import BeautifulSoup
#from urllib import request
#from nltk.text import Text
import os
#import shutil
#import numpy as np
import pandas as pd
#import string
from pathlib import Path
#import csv
import Library_OF_Functions
import docx
#from docx import *

def Convert_Rows_Of_DOCX_To_Text(file_name, file_extension, Dir_name, Text_Formats_Dir_name, Datasets_Feautres_Dir_name, Patterns_Data, Data_Summary):
    Block_word_length=150
    Block_Start=0
    Block_End=0
    New_Words_Tokens=[]
    File_path_For_Patterns_Data=Path(Patterns_Data, "DOCX_Patterns").with_suffix('.csv')
    if(os.path.isfile(File_path_For_Patterns_Data)):
        File_path_For_Risk_Types=Path(Patterns_Data, "Risk_Types").with_suffix('.csv')
        if(os.path.isfile(File_path_For_Risk_Types)):
            open(File_path_For_Risk_Types, 'r')
            C_Dataframe=pd.read_csv(File_path_For_Risk_Types, sep=',')
            Classes_Dataframe = C_Dataframe['Risk_type'].tolist()
            Patterns_Dataframe=pd.read_csv(File_path_For_Patterns_Data, sep=',')
            #Pattern=[]
            File_path_For_CSV_Data=Path(Dir_name, file_name).with_suffix('.docx')
            doc = docx.Document(File_path_For_CSV_Data)
            text=''
            for para in doc.paragraphs:
                text=text+str(para.text)
            Words_Tokens=word_tokenize(text)
            Words_Tokens=Library_OF_Functions.Convert_To_Lower(Words_Tokens)
            Words_Tokens=Library_OF_Functions.Stop_removal(Words_Tokens)
            Words_Tokens=Library_OF_Functions.lemmatizer_Process(Words_Tokens)
            if len(Words_Tokens)>=60: 
                if len(Words_Tokens) >= 250:
                    No_Of_Blocks=Library_OF_Functions.Split_Text_To_Blocks(Words_Tokens, Block_word_length)
                    for Blocks in range(0,No_Of_Blocks):
                        New_Words_Tokens, Block_Start, Block_End= Library_OF_Functions.Select_Block_Words(Blocks, No_Of_Blocks, Words_Tokens, 30, Block_word_length, Block_Start, Block_End)
                        Analysis(New_Words_Tokens, Patterns_Dataframe, Datasets_Feautres_Dir_name, file_name, Text_Formats_Dir_name, Data_Summary, Classes_Dataframe, 0, 0, Blocks+1)       
                else:
                    Analysis(Words_Tokens, Patterns_Dataframe, Datasets_Feautres_Dir_name, file_name, Text_Formats_Dir_name, Data_Summary, Classes_Dataframe,1, 1, 1)
                        
        else:
            print ("The file risk types is not exist - File Risk_Types.csv is not found in the ", File_path_For_Patterns_Data)
    else:
        print ("The file Patterns of CSV files is not exist - File CSV_Patterns.csv is not found in the ", File_path_For_Patterns_Data)

def Analysis(New_Words_Tokens, Patterns_Dataframe, Datasets_Feautres_Dir_name, file_name, Text_Formats_Dir_name, Data_Summary, Classes_Dataframe, row, column, Partion):
    File_path_For_Text_Features=Path(Datasets_Feautres_Dir_name, "CSV").with_suffix('.csv')
    File_Handle = open(File_path_For_Text_Features,"w")
    Type="DOCX"
    for i in range(len(New_Words_Tokens)):
        print(New_Words_Tokens[i], file=File_Handle)
    File_Handle.close() 
    x,y=Patterns_Dataframe.shape
    for i in range(x):
        Pattern=Library_OF_Functions.A_Row_Of_Dataframe_to_List(Patterns_Dataframe, i)
        Percentage=Pattern[len(Pattern)-1]
        Pattern=Pattern[0:len(Pattern)-1]
        Pattern=Library_OF_Functions.Convert_To_Lower(Pattern)
        Found=Library_OF_Functions.Find_Patterns_Index_WithOut_Sequence_Order(New_Words_Tokens, Pattern, Datasets_Feautres_Dir_name, file_name, Text_Formats_Dir_name, i+1, Data_Summary, Type, Classes_Dataframe, row, column, Partion, Percentage)
        if Found==True:
           break 
