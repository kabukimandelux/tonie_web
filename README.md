# tonies_web
Web Interface to Manage / Upload Songs to a TonieBox KreativTonie  
Build using the Python Tonie Api https://github.com/moritzj29/tonie_api and Flask  
Feel free to improve the code, I'm a python noob 

![image](https://user-images.githubusercontent.com/18744493/165509616-dfc7199e-8aa6-4648-afb6-3a4e2bbf17fd.png)

## Install
I developed this to have a super easy install.  
You need to provide 3 things:
- your mytonies user
- your mytonies pass
- a folder where you put subdirectories with music or songs in them

        docker image build -t tonie_web .
        docker run -p 5000:5000 -e MYTONIES_USER=youremail -e MYONIES_PASS=yourpass --mount type=bind,source=/yourhostdir,target=/app/upload tonie_web:latest

## Features
![image](https://user-images.githubusercontent.com/18744493/165516260-d04ec3f1-448b-4793-9c02-021254340908.png)


- View all chapters=songs on your creative Tonie
- Delete all or single chapters
- View all the subdirs in your upload folder
- Upload entire subdirs to the Tonie

## ToDo
- Limited to 1 creative Tonie, currently only owning one but will try to add
- Uploading single songs instead of entire directory

![image](https://user-images.githubusercontent.com/18744493/165516423-e82fc4ac-1326-4e73-aef9-bedd35982ac3.png)
