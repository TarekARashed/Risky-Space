import numpy as np
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction import text
import pandas as pd
import glob
from nltk.corpus import stopwords
import os

new_stopwords = ["all", "due", "to", "on", "daily", ',', ')', '(',':', '&','%', '?','#', '/', '.', '|', 'and', '\n', 'also']
stpwrd = list(stopwords.words('english'))
stpwrd.extend(new_stopwords)
Current_Directory = os.getcwd()
TFIDF_Features_Path=os.path.join(Current_Directory, "TFIDF_Features", "")
Text_Features_Path=os.path.join(Current_Directory, "Text_Features", "")
if (os.path.isdir(TFIDF_Features_Path) and os.path.isdir(Text_Features_Path)):
    text_files = glob.glob(f"{Text_Features_Path}/*.txt")
    text_titles = [Path(text).stem for text in text_files]
    regex1 = '[a-zA-Z]{3,12}'
    if len(text_files)>2: 
        #Tfidf_vectorizer = TfidfVectorizer(input='filename', lowercase=True, analyzer = 'word', decode_error='ignore', stop_words=stpwrd,max_features=400, token_pattern=r'\b[^_\d\W]+\b', min_df=20)
        Tfidf_vectorizer = TfidfVectorizer(input='filename', lowercase=True, analyzer = 'word', decode_error='ignore', stop_words=stpwrd,max_features=600, token_pattern=regex1, min_df=5)
        tf_Idf_vector = Tfidf_vectorizer.fit_transform(text_files)
        Tf_Idf= pd.DataFrame(tf_Idf_vector.toarray(), index=text_titles, columns=Tfidf_vectorizer.get_feature_names_out())
        File_Name=Path(TFIDF_Features_Path, 'TF_IDF').with_suffix('.csv')
        Tf_Idf.to_csv(File_Name, encoding = 'cp1252', errors='ignore')
    else:
        print ("There are no txt files to calcaluate TF-IDF weights")