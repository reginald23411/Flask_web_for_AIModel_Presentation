import string
import pandas as pd
import wordcloud as wc
import re
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
import seaborn as sns
import os

# read file
data=pd.read_excel("E:\\webDL\\10. Labelled_Dataset_22_23_v1.0.xlsx")
data=data[1:999].drop(data.columns[0],axis=1)

# word db
def setCourpus(name):

    varbs = []
    for var in name:
        varbs.append(list(map(lambda text:str(text).translate(str.maketrans('','',string.punctuation)),data[var])))
    return varbs

# modify the format of validation dataset
def setValidationDataSet():

    job_code=data["job_code_1A"].copy().tolist()
    str1=""
    for index,value in enumerate(job_code):
        if bool(re.search('[^\w\s]', str(value))) or str(value)=="0":
            job_code[index]="000"
        if len(str(value))>5:
            job_code[index]=(str(value).split("/")[0])
        if len(str(value))>=6 and str(value).isdigit():
            for i in [*(str(value))][:3]:
                str1=str1+i
            job_code[index]=str1
    return job_code

# export the data
def export_cleaned_excel(column_list):
    data_cleaned=setCourpus(column_list)
    data["job_code_1A"]=setValidationDataSet()
    for i in range(len(column_list)):
        data[column_list[i]]=data_cleaned[i]
    data.to_excel("E:\\PyProject\\cleaned_excel\\Cleaned Data.xlsx")

# create wordCloud
def generate_wordcloud(column_list):
        temp=data.loc[:,column_list].copy()
        for i in range(len(temp.columns)):
            wordcloud = wc.WordCloud(width=800, height=400, background_color="white").generate(str(temp.loc[:,column_list[i]]))
            plt.figure(figsize=(10, 5))
            plt.imshow(wordcloud, interpolation="bilinear")
            plt.axis("off")
            if os.path.exists("E:\\PyProject\\static\\img\\wordcloud\\{0}.png".format(('wordCloud'+str(i+1)))):
                os.remove("E:\\PyProject\\static\\img\\wordcloud\\{0}.png".format(('wordCloud'+str(i+1))))
                plt.savefig("E:\\PyProject\\static\\img\\wordcloud\\{0}.png".format(('wordCloud'+str(i+1))),format="png")
                plt.close()
            else:
                plt.savefig("E:\\PyProject\\static\\img\\wordcloud\\{0}.png".format(('wordCloud' + str(i + 1))),format="png")
                plt.close()

def setModelDataSet(independent_variable,dependent_variable):

    independent_variable_name=["data{0}".format(i) for i in range(1,len(independent_variable)+1)]
    independent_variable_data={}
    for index,item in enumerate(independent_variable_name):
        independent_variable_data[item]=independent_variable[index]
    independent_variable=pd.DataFrame(independent_variable_data)
    x_train,y_train=independent_variable.iloc[:750,:],list(map(str,dependent_variable[:750]))
    x_test,y_test=independent_variable.iloc[750:,:],list(map(str,dependent_variable[750:]))
    return x_train,y_train,x_test,y_test



def prediction(x_train,y_train,x_test,y_test):

    # Convert titles to numerical features using TF-IDF vectorizer
    vectorizer = TfidfVectorizer()
    x_train_vectorized = vectorizer.fit_transform([' '.join(map(str, row)) for row in x_train.values])
    x_test_vectorized = vectorizer.transform([' '.join(map(str, row)) for row in x_test.values])

    # Convert string job codes to numerical labels using label encoding
    label_encoder = LabelEncoder()
    y_train_encoded = label_encoder.fit_transform(y_train)
    y_test_encoded = label_encoder.transform(y_test)

    # Modeling
    rfc = RandomForestClassifier(n_estimators=45,random_state=30)
    rfc.fit(x_train_vectorized, y_train_encoded)
    result = rfc.score(x_test_vectorized, y_test_encoded)
    return result

def generate_combination_plot(column_list):
    features=data.loc[:,column_list].copy()
    reduced_features = features.apply(lambda x: pd.factorize(x)[0])
    reduced_features = reduced_features.dropna()

    plt1=plt.figure()
    sns.barplot(data=reduced_features)
    plt.savefig("E:\\PyProject\\static\\img\\stat\\{0}.png".format(("barplot")),format="png")
    plt.close(plt1)

    plt2 = plt.figure()
    sns.heatmap(data=reduced_features)
    plt.savefig("E:\\PyProject\\static\\img\\stat\\{0}.png".format(("heatmap")),format="png")
    plt.close(plt2)

    plt3=plt.figure()
    sns.histplot(data=reduced_features)
    plt.savefig("E:\\PyProject\\static\\img\\stat\\{0}.png".format(("histplot")),format="png")
    plt.close(plt3)

    plt4=plt.figure()
    sns.pairplot(data=reduced_features)
    plt.savefig("E:\\PyProject\\static\\img\\stat\\{0}.png".format(("reduced_features")), format="png")
    plt.close(plt4)

def generate_violinplot(column_list):
    features = data.loc[:, column_list].copy()
    reduced_features = features.apply(lambda x: pd.factorize(x)[0])
    reduced_features = reduced_features.dropna()
    sns.violinplot(data=reduced_features)
    plt.savefig("E:\\PyProject\\static\\img\\stat\\{0}.png".format(("violinplot")), format="png")

# plot operation
def visualizeData(column_list):
    generate_wordcloud(column_list)
    generate_combination_plot(column_list)
    generate_violinplot(column_list)

def lunch_AImodel(column_list):
    x_train, y_train, x_test, y_test=setModelDataSet(setCourpus(column_list),setValidationDataSet())
    visualizeData(column_list)
    return prediction(x_train, y_train, x_test, y_test)

# export_cleaned_excel(data.columns.tolist())