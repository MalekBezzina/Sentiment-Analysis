### task 1 LOAD THE DATASET ###
import pandas as pd 

df=pd.read_csv('data\moviedata.csv', engine='python', encoding='utf-8', error_bad_lines=False )
print(df.head(10))

### task 2 transforming documents to feature vectors ###

import numpy as np 
from sklearn.feature_extraction.text import CountVectorizer

count=CountVectorizer()
docs =np.array(['The sun is shining','The weather is sweet','The sun is shining,The weather is sweet,and one and one is two'])
bag=count.fit_transform(docs)

print(count.vocabulary_)
print(bag.toarray())

### task 3 TF IDF  ###

from sklearn.feature_extraction.text import TfidfTransformer

tfidf=TfidfTransformer(use_idf=True,norm='l2',smooth_idf=True)
print(tfidf.fit_transform(bag).toarray())

### task 4 Data preparation  ###
print(df.loc[0,'review'][-50:])

import  re
def preprocessor(text):
    text = re.sub('<[^>]*>', '', text)
    emoticons = re.findall('(?::|;|=)(?:-)?(?:\\)|\\(|D|P)', text)
    text = re.sub('[\\W]+', ' ', text.lower()) +\
         ' '.join(emoticons).replace('-', '')
    return text

print(preprocessor(df.loc[0,'review'][-50:]))

print(preprocessor("</a>This :) is a :( test :-)!"))


df['review']=df['review'].apply(preprocessor)

### task 5 tokenization of documents  ###

from nltk.stem.porter import PorterStemmer

porter = PorterStemmer()

def tokenizer(text):
    return text.split()
def tokenizer_porter(text):
    return[porter.stem(word) for word in text.split()]

print(tokenizer('runners like running and thus they run'))
print(tokenizer_porter('runners like running and thus they run'))


import nltk

nltk.download('stopwords')


from nltk.corpus import stopwords

stop =stopwords.words('english')
[w for w in tokenizer_porter ('a runner likes running and runs a lot ')[-10:] if w not in stop ]


### task 6 transform text data into tf idf vectors   ###

from sklearn.feature_extraction.text import TfidfVectorizer
tfidf=TfidfVectorizer(
    strip_accents=None,
    lowercase=False,
    preprocessor=None,
    tokenizer=tokenizer_porter,
    use_idf=True,
    norm='l2',
    smooth_idf=True
    )

y=df.sentiment.values
X=tfidf.fit_transform(df.review)

### task 7 Document classification using logistic regression ###

from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test=train_test_split(X,y,random_state=1,test_size=0.5,shuffle=False)

import pickle
from sklearn.linear_model import LogisticRegressionCV

clf=LogisticRegressionCV(cv=5,scoring='accuracy',random_state=0,n_jobs=-1,verbose=3,max_iter=300).fit(x_train,y_train)
saved_model=open('saved_model.sav','wb')  
pickle.dump(clf,saved_model)
saved_model.close()        


### task8 Model Evaluation ###

filename='saved_model.sav'
saved_clf=pickle.load(open(filename,'rb'))

saved_clf.score(x_test,y_test)











