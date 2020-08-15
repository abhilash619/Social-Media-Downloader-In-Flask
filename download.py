from flask import Flask,render_template,request
import pytube
import fbdown as fb
import os
import random
import re
import instagram as ins
from win10toast import ToastNotifier
app = Flask(__name__)


@app.route("/")
def main():
    return render_template('MainPage.html')
    
@app.route("/facebook",methods=['GET','POST'])
def facebook():
    n = ToastNotifier()
    if ins.connection() == True:
        number = random.randint(0, 100000)
        home_folder = os.path.expanduser('~') + "\Downloads\\"+str(number)+".mp4"
        home_folder = home_folder.replace("\\", "/")
        result = " "
        if request.method=='POST':
            url=request.form["exampleInputUrl"]
            x = re.match(r'^(https:)[/][/]www.([^/]+[.])*facebook.com', url)
            if x:
                try:
                    fb.Facebook(url,home_folder)
                    result = "Successfully Downloaded"
                    n.show_toast("FACEBOOK", "Successfully Download", duration=10,
                                 icon_path="https://image.flaticon.com/icons/svg/174/174848.svg")
                    return render_template('loader.html', result=result)

                except Exception as e:
                    print(e)
            else:
                result = "Invalid URL"
            return render_template('loader.html', result=result)
    else:
        result = "Check Internet"
        return render_template('loader.html', result=result)
    return render_template('facebook.html')

@app.route("/instagram",methods=['GET','POST'])
def instagram():
    result = " "
    n = ToastNotifier()
    if ins.connection() == True:
       if request.method == 'POST':
            url = request.form["exampleInputUrl"]
            x = re.match(r'^(https:)[/][/]www.([^/]+[.])*instagram.com', url)
            if x:
                try:
                    ins.download_image_video(url)
                    result = "Successfully Downloaded"
                    n.show_toast("INSTAGRAM", "Successfully Download", duration=10,
                                 icon_path="https://image.flaticon.com/icons/svg/2111/2111463.svg")
                    return render_template('loader.html', result=result)

                except Exception as e:
                    print(e)
            else:
                result = "Invalid URL"
                return render_template('loader.html', result=result)
    else:
        result = "Check Internet"
        return render_template('loader.html', result=result)
    return render_template('instagram.html')

@app.route("/youtube",methods=['GET','POST'])
def youtube():
    n = ToastNotifier()
    str1=" "
    home_folder = os.path.expanduser('~') + "\Downloads"
    home_folder = home_folder.replace("\\", "/")
    result="Successfully Downloaded"
    HD=[]
    HD1=[]

    if ins.connection() == True:
        if request.method=='POST':
            url=request.form["exampleInputUrl"]
            x = re.match(r'^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$', url)
            print("url is",url)
            if x:
                try:
                    youtube=pytube.YouTube(url).streams
                    #print("Error is",youtube.filename)
                except Exception as e:
                    print(e)
                    print("Connection error")

                #to get input from radio button
                #str1=str1.join(request.form.getlist('exampleRadios'))
                #print('radio selected is',str1)

                webstreams=youtube.filter(type = "video",file_extension='mp4')
                for i in webstreams:
                    #print("Quality is",getattr(i,'resolution'))
                    HD = str(getattr(i, 'resolution'))

                    if(HD!="None" and str(getattr(i, 'audio_codec'))=="mp4a.40.2"):
                        HD1.append(HD[:-1])
                        print(HD)
                HD1=list(dict.fromkeys(HD1))
                HD1=sorted(HD1,reverse=True)
                print(HD1)
                webstreams = youtube.filter(res=HD1[0]+"p")

                try:
                    webstreams.first().download(home_folder)
                except Exception as e:
                    print(e)
                    result = "Error occured please try again"
                    print("Some Error!")
                print("Task Completed")
                n.show_toast("YOUTUBE", "Successfully Download", duration=10,
                             icon_path="https://image.flaticon.com/icons/svg/174/174883.svg")
                return render_template('loader.html',result=result)

            else:
                result = "Invalid URL"
                return render_template('loader.html', result=result)
    else:
        result = "Check Internet"
        return render_template('loader.html', result=result)

    return render_template('home.html')

app.run()

