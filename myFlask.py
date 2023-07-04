from flask import Flask,render_template,request
import randomForestAI as myAI
import os

app=Flask(__name__,template_folder='templates')

@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')

@app.route('/Introduction')
def introduction():
    return render_template('Introduction.html')

@app.route('/Data_Analysis')
def Data_Analysis():
    return render_template('DataAnalysis.html')

@app.route('/Findings_and_Evaluation')
def Findings_and_Evaluation():
    return render_template('FindingsAndEvaluation.html')

@app.route('/Conclusion')
def Conclusion():
    return render_template('Conclusion.html')

@app.route('/excel_table')
def excel_table():
    return render_template('excel_table.html', html_table=myAI.data.to_html(index=False))

@app.route('/default_parameters')
def default_parameters():
    stat_folder = os.path.join(app.static_folder, 'img', 'stat')
    wordcloud_folder = os.path.join(app.static_folder, 'img', 'wordcloud')
    stat_image_filenames = os.listdir(stat_folder)
    wordcloud_image_filenames = os.listdir(wordcloud_folder)

    data=['title','sentence','post_id']
    accuracy=myAI.lunch_AImodel(data)

    return render_template('default_parameters.html',
                           accuracy=accuracy,
                           stat_image_filenames=stat_image_filenames,
                           wordcloud_image_filenames=wordcloud_image_filenames[:len(data)]
                           )


@app.route('/customized_parameters',methods=["POST","GET"])
def customized_parameters():
    stat_folder = os.path.join(app.static_folder, 'img', 'stat')
    wordcloud_folder = os.path.join(app.static_folder, 'img', 'wordcloud')
    stat_image_filenames = os.listdir(stat_folder)
    wordcloud_image_filenames = os.listdir(wordcloud_folder)

    data = []
    if request.method == "POST":
        data=request.form.getlist("selected_columns")

    accuracy=myAI.lunch_AImodel(data)
    return render_template('customized_parameters.html',
                           accuracy=accuracy,
                           stat_image_filenames=stat_image_filenames,
                           wordcloud_image_filenames=wordcloud_image_filenames[:len(data)]
                           )

@app.route('/form',methods=["POST","GET"])
def form():
    all_columns = myAI.data.columns.tolist()
    return render_template("customizationForm.html",all_columns=all_columns)

if __name__ == "__main__":
    app.run()