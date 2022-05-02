from flask import Flask, flash, render_template, request, redirect, url_for
import logging, os
from tonie_api import TonieAPI

logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)

username = os.environ['MYTONIES_USER']
password = os.environ['MYTONIES_PASS']

api=TonieAPI(username, password)
status = api.me
basedir = 'upload/'

def list_household():
    householdsjson = api.households_update()
    for households in enumerate(householdsjson.keys()):
        print(households)
    return households
    
def list_kreativtonies(householdID):
    kreativTonieIDjson = api.households[householdID].creativetonies_update()
    for kreativTonieID in enumerate(kreativTonieIDjson.keys()):
        print(kreativTonieID)
    return kreativTonieID

def upload_choice(householdID, kreativTonieID,upload_dir):
    files = []
    dirs = os.listdir(basedir)
    files = os.listdir(basedir+dirs[upload_dir])
    files.sort()
    for file in files:
        title = file.strip('.m4a')	
        print(title)
        api.households[householdID].creativetonies[kreativTonieID].upload(basedir+dirs[upload_dir]+'/'+file, title)
 
def delete_all(householdID, kreativTonieID):
    api.households[householdID].creativetonies[kreativTonieID].remove_all_chapters()
    
def get_chapters(householdID, kreativTonieID):
    output = []
    chapters = api.households[householdID].creativetonies[kreativTonieID].chapters
    for tracks in chapters:
        print(tracks['title'] + " " + str(tracks['seconds']))
        output.append(tracks['title'] + " - " + str(int(tracks['seconds'])) +"s")
    return output

def refresh_capacity(householdID, kreativTonieID):
    kreativTonieInfo = api.households[householdID].creativetonies[kreativTonieID].properties
    capacity = 100 - kreativTonieInfo['secondsRemaining'] // 54
    return capacity

def delete_chapter(householdID, kreativTonieID, chapter):
    chapters = api.households[householdID].creativetonies[kreativTonieID].chapters
    chapters.pop(chapter)
    api.households[householdID].creativetonies[kreativTonieID]._patch_chapters(chapters)
    chapters = api.households[householdID].creativetonies[kreativTonieID].chapters
    return chapters

app = Flask(__name__)
app.secret_key = b'_5#y2Lfqf"agF4Q8z\n\xec]/'
global householdID, kreativTonieID, capacity
householdID = list_household()[1]
kreativTonieID = list_kreativtonies(householdID)[1]

@app.route("/")
def home():
    list_household()
    global householdID, kreativTonieID, capacity
    householdID = list_household()[1]
    kreativTonieID = list_kreativtonies(householdID)[1]
    capacity = refresh_capacity(householdID, kreativTonieID)
    image = api.households[householdID].creativetonies[kreativTonieID].properties['imageUrl']
    properties = api.households[householdID].creativetonies[kreativTonieID].properties
    return render_template("index.html", title='TonieApp', householdID=householdID, kreativTonieID=kreativTonieID, capacity=capacity, page='home', image = image, properties = properties)

@app.route("/info")
def info():
    list_household()
    global householdID, kreativTonieID
    householdID = list_household()[1]
    kreativTonieID = list_kreativtonies(householdID)[1]
    kreativTonieInfo = api.households[householdID].creativetonies[kreativTonieID].properties
    capacity = refresh_capacity(householdID, kreativTonieID)
    return render_template("info.html", householdID=householdID, kreativTonieID=kreativTonieID, status=status, page='info',capacity=capacity, kreativTonieInfo=kreativTonieInfo)

@app.route("/chapters", methods=['GET', 'POST'])
def chapters():
    list_household()
    householdID = list_household()[1]
    kreativTonieID = list_kreativtonies(householdID)[1]
    chapters = get_chapters(householdID, kreativTonieID)
    capacity = refresh_capacity(householdID, kreativTonieID)
    if request.method == 'POST':
        print("removing")
        remove = int(request.form.get('remove'))-1
        delete_chapter(householdID, kreativTonieID, remove)
        flash('Fertig !','alert-success')
        return redirect(url_for('chapters'))
    return render_template("chapters.html", chapters = chapters,capacity=capacity, page = 'chapters')

@app.route("/upload", methods=['GET', 'POST'])
def upload():
    number = []
    dirs = os.listdir(basedir)
    for i, dir in enumerate(dirs):
        number.append(len(os.listdir(basedir+dirs[i])))
    capacity = refresh_capacity(householdID, kreativTonieID)
    if request.method == 'POST':
        choice = int(request.form.get('choice'))-1
        checked = request.form.get('checkbox')
        print ("Result from form " + str(checked)) 
        if checked == None:
            flash ('Kein Titel gewählt','alert-danger')
        else:
            for selection in checked:
                #upload_choice(householdID, kreativTonieID, choice)
                print("Uploaded " + str(selection))
        #upload_choice(householdID, kreativTonieID, choice)
        flash('Fertig !','alert-success')
        return redirect(url_for('upload'))
    return render_template('upload.html', dirs=dirs, capacity=capacity,number=number,page = 'upload')

@app.route("/delete", methods=['GET', 'POST'])
def delete():
    if request.method == 'POST':
        if request.form.get('deleteall') == 'DELETE':
            delete_all(householdID, kreativTonieID)
            flash('Kreativ Tonie ' + str(kreativTonieID) + ' gelöscht','alert-success')
        elif request.method == 'GET':
            capacity = refresh_capacity(householdID, kreativTonieID)
            return render_template('delete.html', capacity=capacity)
    capacity = refresh_capacity(householdID, kreativTonieID)
    return render_template("delete.html", capacity=capacity,page='delete')

if __name__ == "__main__":
    app.run('0.0.0.0', 5000, debug=True)
