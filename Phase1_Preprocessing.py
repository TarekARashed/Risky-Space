import os
from pathlib import Path
import PDF_To_Text
import CSV_Rows_Columns_To_TextFile
import PPTX_To_Text
import DOCX_To_Text

# This is the main - Pre-processing dataset
def Load_Datasets(Dir_name, Files_extension, Datasets_Feautres_Dir_name, Text_Formats_Dir_name, Patterns_Data, Data_Summary):
    for files in os.listdir(Dir_name):
        if files.endswith(Files_extension):
            file_extension = Path(files).suffix
            if (file_extension=='.pdf'):
                PDF_To_Text.Convert_PDF_To_Text(files, file_extension, Dir_name, Text_Formats_Dir_name, Datasets_Feautres_Dir_name, Patterns_Data, Data_Summary)
            else:
                if (file_extension=='.pptx'):
                    PPTX_To_Text.Convert_PPTX_To_Text(files, file_extension, Dir_name, Text_Formats_Dir_name, Datasets_Feautres_Dir_name, Patterns_Data, Data_Summary)
        else:
            continue

    for files in os.listdir(Dir_name):
        if files.endswith(Files_extension):
            file_extension = Path(files).suffix
            if (file_extension=='.docx'):
                 DOCX_To_Text.Convert_Rows_Of_DOCX_To_Text(files, file_extension, Dir_name, Text_Formats_Dir_name, Datasets_Feautres_Dir_name, Patterns_Data, Data_Summary)
            else:
                if (file_extension=='.csv'):
                    CSV_Rows_Columns_To_TextFile.Convert_Rows_Of_CSV_To_Text(files, file_extension, Dir_name, Text_Formats_Dir_name, Datasets_Feautres_Dir_name, Patterns_Data, Data_Summary)
        else:
            continue

All_Features = []
Count_for_All_Feature99s = []
Document_Features = []
Files_extension=('.pdf','.html', '.csv', '.pptx', '.docx')
Current_Directory = os.getcwd()
Datasets_Path=os.path.join(Current_Directory, "Datasets", "")
if (os.path.isdir(Datasets_Path)):
    Patterns_Path=os.path.join(Current_Directory, "Patterns", "")
    if (not os.path.isdir(Patterns_Path)):
         print ("There is no {Patterns} folder. Please create {Patterns} Folder and load your Patterns and Risk_types in it")
    else:  
        Pattern1_File_Path=Path(Patterns_Path, "PPTX_Patterns").with_suffix('.csv')
        Pattern2_File_Path=Path(Patterns_Path, "PDF_Patterns").with_suffix('.csv')
        Pattern3_File_Path=Path(Patterns_Path, "CSV_Patterns").with_suffix('.csv')
        Pattern4_File_Path=Path(Patterns_Path, "DOCX_Patterns").with_suffix('.csv')
        Categories_File_Path=Path(Patterns_Path, "Risk_Types").with_suffix('.csv')
        if not (os.path.isfile(Pattern1_File_Path) and os.path.isfile(Pattern2_File_Path) and os.path.isfile(Pattern3_File_Path) 
        and os.path.isfile(Pattern4_File_Path) and os.path.isfile(Categories_File_Path)):
            print ("One of the follwing data are missing: 1-PPTX_Patterns, 2- PDF_Patterns, 3-CSV_Patterns, 4-DOCX_Patterns, 5-Risk_Types\n")
            print ("Please check the folder {Patterns}, load the missing files and try agoian \n")
        else:
            Text_Features_Path=os.path.join(Current_Directory, "Text_Features", "")
            if  (not os.path.isdir(Text_Features_Path)):
                os.mkdir('Text_Features')
            Summary_Path=os.path.join(Current_Directory, "Summary", "")
            if  (not os.path.isdir(Summary_Path)):
                os.mkdir('Summary')
            TFIDF_Features_Path=os.path.join(Current_Directory, "TFIDF_Features", "")
            if  (not os.path.isdir(TFIDF_Features_Path)):
                os.mkdir('TFIDF_Features')   
            Load_Datasets(Datasets_Path, Files_extension, TFIDF_Features_Path, Text_Features_Path, Patterns_Path, Summary_Path)
else:
    print ("There is no {Datasets} folder. Please create {Datasets} Folder and load your dataset in it")