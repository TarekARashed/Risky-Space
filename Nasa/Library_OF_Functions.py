from nltk.corpus import stopwords
from nltk.stem import 	WordNetLemmatizer
from nltk import pos_tag
import pandas as pd
from pathlib import Path
import os


def Extract_Parts_Of_Sentence(Start_Block, End_Block, Words_List):
    List_Of_Needed_Word=[]
    Words_List=Words_List[Start_Block:End_Block]
    Tuple_Cat = pos_tag(Words_List)
    for i in range(0, len(Tuple_Cat)):
        Type=Tuple_Cat[i][1]
        if(Type == 'NN' or Type == 'NNS' or Type == 'NNPS' or Type == 'NNP' or Type == 'JJ'):
            List_Of_Needed_Word.append(Tuple_Cat[i][0])
    return(List_Of_Needed_Word)           

def Print_List_Of_Needed_Patterns(List_Of_Needed_Patterns, Patterns_Data, Pattern_Data_File_Name):
    File_path_For_Patterns_Data=Path(Patterns_Data, Pattern_Data_File_Name).with_suffix('.csv')
    Non_Duplicated_Word_List = sorted(set(List_Of_Needed_Patterns), key=lambda x:List_Of_Needed_Patterns.index(x))
    if len(Non_Duplicated_Word_List)>0:
        if(os.path.isfile(File_path_For_Patterns_Data)):
            Print_To_File(Non_Duplicated_Word_List, File_path_For_Patterns_Data, True)
        else:
            Print_To_File(Non_Duplicated_Word_List, File_path_For_Patterns_Data, False)
        
def Select_Block_Words(Blocks, No_Of_Blocks, Words_Tokens, addition, Block_word_length, Block_Start, Block_End):
    New_Words_Tokens=[]
    if Blocks==0:
        Block_Start=0
        Block_End=Block_word_length
    else:
        if Blocks == No_Of_Blocks -1:
            Block_Start=(Block_End-1)-addition
            Block_End=len(Words_Tokens)
        else:
            Block_Start=(Block_End-1)-addition
            Block_End=Block_Start+ Block_word_length 
    for i in range(Block_Start, Block_End):
            New_Words_Tokens.append(Words_Tokens[i])
    return (New_Words_Tokens, Block_Start, Block_End)

def Print_To_File(Non_Duplicated_Word_List, File_path_For_Patterns_Data, Insert_F):
        Block_Start=0
        Block_word_length=10
        Flag=True
        #Features_Str=[]
        Block_End=0
        if Insert_F == True:
            CSV_Dataframe=pd.read_csv(File_path_For_Patterns_Data, sep=',', encoding='cp1252')
            Df_Row=pd.DataFrame(columns =["Pattern_1", "Pattern_2", "Pattern_3", "Pattern_4", "Pattern_5", "Pattern_6", "Pattern_7", "Pattern_8", "Pattern_9", "Pattern_10", "Matches"])
        else:
            df = pd.DataFrame(columns =["Pattern_1", "Pattern_2", "Pattern_3", "Pattern_4", "Pattern_5", "Pattern_6", "Pattern_7", "Pattern_8", "Pattern_9", "Pattern_10", "Matches"])
        while (Block_End<len(Non_Duplicated_Word_List) and Flag==True):
            Block_End=Block_Start+Block_word_length
            One_Feature=[]
            #Features_Str=[]
            if  Block_End <=len(Non_Duplicated_Word_List):
                for j in range(Block_Start, Block_End):
                    One_Feature.append(Non_Duplicated_Word_List[j])
                One_Feature.append('0.5')      
                Block_Start= Block_End
                if Insert_F == True :
                    Df_Row=pd.DataFrame()
                    Df_Row=Df_Row.append(pd.DataFrame([One_Feature],columns=["Pattern_1", "Pattern_2", "Pattern_3", "Pattern_4", "Pattern_5", "Pattern_6", "Pattern_7", "Pattern_8", "Pattern_9", "Pattern_10", "Matches"]), ignore_index=True)
                    CSV_Dataframe = pd.concat([Df_Row, CSV_Dataframe]).reset_index(drop = True)

                else:
                    df=df.append(pd.DataFrame([One_Feature],columns=["Pattern_1", "Pattern_2", "Pattern_3", "Pattern_4", "Pattern_5", "Pattern_6", "Pattern_7", "Pattern_8", "Pattern_9", "Pattern_10", "Matches"]), ignore_index=True)
            else:
                m=0
                for j in range(Block_Start, len(Non_Duplicated_Word_List)):
                    One_Feature.append(Non_Duplicated_Word_List[j])
                    m+=1
                End=Block_word_length+1
                for k in range(m, End):
                    if k < Block_word_length:
                        One_Feature.append('')
                    else:
                        One_Feature.append('0.5')
                if Insert_F == True :
                    Df_Row=pd.DataFrame()
                    Df_Row=Df_Row.append(pd.DataFrame([One_Feature],columns=["Pattern_1", "Pattern_2", "Pattern_3", "Pattern_4", "Pattern_5", "Pattern_6", "Pattern_7", "Pattern_8", "Pattern_9", "Pattern_10", "Matches"]), ignore_index=True)
                    CSV_Dataframe = pd.concat([Df_Row, CSV_Dataframe]).reset_index(drop = True)
                    #CSV_Dataframe.to_csv(File_path_For_Patterns_Data, index=False)
                else:
                    df=df.append(pd.DataFrame([One_Feature],columns=["Pattern_1", "Pattern_2", "Pattern_3", "Pattern_4", "Pattern_5", "Pattern_6", "Pattern_7", "Pattern_8", "Pattern_9", "Pattern_10", "Matches"]), ignore_index=True)
                    #df.to_csv(File_path_For_Patterns_Data, index=False)
                Flag==False  
        if Insert_F == True :
            CSV_Dataframe.to_csv(File_path_For_Patterns_Data, index=False)
        else:
            df.to_csv(File_path_For_Patterns_Data, index=False)     

def Find_Patterns_Index_WithOut_Sequence_Order(Words_List, Pattern, Datasets_Feautres_Dir_name, file_name, Text_Formats_Dir_name,Check_Row, Data_Summary, F_type, Classes_Dataframe, row, column, Partion, Percentage):
   
    Case=0
    if (float(Percentage) ==1):
        Found=all(item in Words_List for item in Pattern)
        if (Found == True):
            Case=1
    else:
        Item_F=0
        for i in range(0, len(Pattern)):
            if Pattern[i] in Words_List:
                Item_F+=1
        Match=Item_F/len(Pattern)
        if (Match >= float(Percentage)):
            Case=2
    if Case !=0 :
        End_Block=len(Words_List)
        if(End_Block>=10):
            row=F_type+str(row)
            column='_'+str(column)
            File_name=Generate_File_Name(column, Partion,row, file_name)
            Print_Tokens_To_File(0, End_Block, Words_List, Text_Formats_Dir_name, File_name)
            #File_name=Generate_File_Name(column, Partion,row, file_name)
            #Print_Tokens_To_File(0, End_Block, Words_List, Data_Summary, File_name)
            Class_Labels=Find_Classes_For_Data(0, End_Block, Words_List, Classes_Dataframe)
            Print_Class_Labels_Of_Text(Class_Labels, Classes_Dataframe, Datasets_Feautres_Dir_name)
            return True
    else:
        return False       
        

def Split_Text_To_Blocks(Words_Tokens, Block_word_length):
    Maximum_No_Of_Blocks=100
    for j in range(Maximum_No_Of_Blocks):
        Equivelent=Block_word_length*(j+1)
        if (Equivelent>=len(Words_Tokens)):
            No_Of_Blocks=j+1
            return No_Of_Blocks
        
def Count_WOrds_in_A_Sentence(str): 
    WordCount = 0;  
    for i in range(0, len(str)-1):  
        if(str[i] == ' ' and str[i+1].isalpha() and (i > 0)):  
            WordCount +=WordCount  
    return WordCount
    
def A_Row_Of_Dataframe_to_List(Dataframe, Index_no):
    List=[]
    for i in range(0, len(Dataframe.axes[1])):
        Value=str(Dataframe.values[Index_no][i])
        if Value !="nan":
            List.append(Value)
    return List
def Convert_To_Lower(Pattern):
    for i in range(len(Pattern)):
        Pattern[i] = Pattern[i].lower()
    return (Pattern)

def lemmatizer_Process(Words_Tokens):
    Li=[]
    lemmatizer = WordNetLemmatizer()
    for w in Words_Tokens:
        Li.append(str(lemmatizer.lemmatize(w)))
    return Li

def Stop_removal(Tokens):

    global stopwords
    new_stopwords = ["all", "due", "to", "on", "daily", ',', ')', '(',':', '&','%', '?','#', '/', '.', '|', '[', ']']
    stpwrd = stopwords.words('english')
    stpwrd.extend(new_stopwords)
    Tokens = [word for word in Tokens if not word in stpwrd]
    return(Tokens)

def Identify_Words_And_Indexes(indexes, Words_List):
    List_Of_Words_In_Order=[]
    index_Words_In_Order=[]
    for i in range(len(indexes)):
        List_Of_Words_In_Order.append(Words_List[indexes[i]])
        index_Words_In_Order.append(indexes[i])
    return List_Of_Words_In_Order, index_Words_In_Order
def DeLete_One_Word_Char(List_Of_Words_In_Order, index_Words_In_Order):
    Li_W=[]
    Li_I=[]
    for i in range(0, len(List_Of_Words_In_Order)):
        if len(List_Of_Words_In_Order[i])!=1:
            Li_W.append(List_Of_Words_In_Order[i])
            Li_I.append(index_Words_In_Order[i])
        else:
            if List_Of_Words_In_Order[i].isnumeric() and len(List_Of_Words_In_Order[i])==2:
                Li_W.append(List_Of_Words_In_Order[i])
                Li_I.append(index_Words_In_Order[i])
    return Li_W, Li_I
                
def Find_Patterns_Index_In_Sequence_Order(List_Of_Words_In_Order,index_Words_In_Order, Words_List, Pattern, Datasets_Feautres_Dir_name, file_name, Text_Formats_Dir_name,Check_Row, Data_Summary, F_type, Classes_Dataframe, Patterns_Data):
            Pattern_Index=0
            Words_List_Index=0
            Round1=0
            flag=False
            List_Of_Words_In_Order, index_Words_In_Order=DeLete_One_Word_Char(List_Of_Words_In_Order, index_Words_In_Order)
            while (Words_List_Index>=0 and Words_List_Index<len(List_Of_Words_In_Order) and len(List_Of_Words_In_Order)>0):
                    if (Pattern_Index >=0 and Pattern_Index<=len(Pattern)-1):
                        if (str(List_Of_Words_In_Order[Words_List_Index])== str(Pattern[Pattern_Index])):
                            Pattern_Index+=1
                            Words_List_Index+=1
                            flag=True
                        else:
                            k=0
                            while k>=0 and k<=Words_List_Index:
                                Backup_List=[]
                                Backup_List=Delete_One_by_One_Item_From_List(List_Of_Words_In_Order)
                                List_Of_Words_In_Order=[]
                                List_Of_Words_In_Order = Backup_List.copy()
                                Backup_List=[]
                                Backup_List=Delete_One_by_One_Item_From_List(index_Words_In_Order)
                                index_Words_In_Order=[]
                                index_Words_In_Order = Backup_List.copy()
                                k+=1
                            Pattern_Index=0 
                            Words_List_Index=0
                            flag=False
                    else:
                        if flag==True and Pattern_Index==len(Pattern):
                            Round1+=1
                            Start_Block=index_Words_In_Order[0]
                            End_Block=index_Words_In_Order[Pattern_Index-1]
                            if ((End_Block-Start_Block)>=10):
                                File_name=Generate_File_Name(Check_Row,Round1,F_type, file_name)
                                Print_Tokens_To_File(Start_Block, End_Block, Words_List, Text_Formats_Dir_name, File_name)
                                Class_Labels=Find_Classes_For_Data(Start_Block, End_Block, Words_List, Classes_Dataframe)
                                Print_Class_Labels_Of_Text(Class_Labels, Classes_Dataframe, Datasets_Feautres_Dir_name)
                                List_Of_Needed_Patterns=Extract_Parts_Of_Sentence(Start_Block, End_Block, Words_List)
                                Print_List_Of_Needed_Patterns(List_Of_Needed_Patterns, Patterns_Data,'CSV_Patterns')
                                Print_List_Of_Needed_Patterns(List_Of_Needed_Patterns, Patterns_Data, 'DOCX_Patterns')
                                k=0
                            while k>=0 and k<=Words_List_Index-1:
                                Backup_List=[]
                                Backup_List=Delete_One_by_One_Item_From_List(List_Of_Words_In_Order)
                                List_Of_Words_In_Order=[]
                                List_Of_Words_In_Order = Backup_List.copy()
                                Backup_List=[]
                                Backup_List=Delete_One_by_One_Item_From_List(index_Words_In_Order)
                                index_Words_In_Order=[]
                                index_Words_In_Order = Backup_List.copy()
                                k+=1
                        Pattern_Index=0 
                        Words_List_Index=0
                        flag=False
            
            if flag==True and Words_List_Index==len(List_Of_Words_In_Order):
                Round1+=1
                Start_Block=index_Words_In_Order[0]
                End_Block=index_Words_In_Order[Pattern_Index-1]
                if ((End_Block-Start_Block)>=10):
                    File_name=Generate_File_Name(Check_Row,Round1,F_type, file_name)
                    Print_Tokens_To_File(Start_Block, End_Block, Words_List, Text_Formats_Dir_name, File_name)
                    Class_Labels=Find_Classes_For_Data(Start_Block, End_Block, Words_List, Classes_Dataframe)
                    Print_Class_Labels_Of_Text(Class_Labels, Classes_Dataframe, Datasets_Feautres_Dir_name)
                    List_Of_Needed_Patterns=Extract_Parts_Of_Sentence(Start_Block, End_Block, Words_List)
                    Print_List_Of_Needed_Patterns(List_Of_Needed_Patterns, Patterns_Data,'CSV_Patterns')
                    Print_List_Of_Needed_Patterns(List_Of_Needed_Patterns, Patterns_Data, 'DOCX_Patterns')
                    
def Find_Classes_For_Data(Start_Block, End_Block, Words_List, Classes_Dataframe):
    Li=[]
    Found=False
    for i in range(Start_Block, End_Block):
        for j in range (len(Classes_Dataframe)):
            Value=str(Classes_Dataframe[j])
            Value=Value.lower()
            if str(Words_List[i])== str(Value):
                Li.append(str(Value))
                Found=True
                break
    if Found==False:
        Index=len(Classes_Dataframe)-1
        Li.append(str(Classes_Dataframe[Index].lower()))
    return Li

def Generate_File_Name(P,Round, s, file_name):
    Generate_file_name=Path(file_name).stem
    Part__Of_file_name=str(s)+str(P) + '_'+ str(Round)
    incre=str(Generate_file_name+Part__Of_file_name)
    return(Path(incre).stem)

def Delete_One_by_One_Item_From_List(A_List):
    del A_List[0]
    return A_List 
def Print_Tokens_To_File(S, E, Features, Text_Formats_Dir_name, File_name):
    File_path_For_Text_Features=Path(Text_Formats_Dir_name, File_name).with_suffix('.txt')
    File_Handle = open(File_path_For_Text_Features,"w")
    for i in range(S,E):
        Feature=str(Features[i])
        print(Feature, file=File_Handle)
    File_Handle.close() 
def Print_Class_Labels_Of_Text(Class_Labels, Classes_Dataframe, Datasets_Feautres_Dir_name):
    File_path_For_Class_Labels=Path(Datasets_Feautres_Dir_name, "Classes").with_suffix('.csv')
    if(os.path.isfile(File_path_For_Class_Labels)):
        File_Handle=open(File_path_For_Class_Labels, 'a')
    else:
        File_Handle=open(File_path_For_Class_Labels, "w")
        
    Li=['0']*len(Classes_Dataframe)
    for i in range(len(Class_Labels)):
        for j in range(len(Classes_Dataframe)):
            if str(Classes_Dataframe[j].lower())== str(Class_Labels[i].lower()):
                Li[j]=1
                break
            else:
                Li[j]=0
    Class_str=','.join([str(item) for item in Li])
    print (Class_str, file=File_Handle)
    File_Handle.close()
   
