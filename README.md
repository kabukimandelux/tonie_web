# tonies_web
Web Interface to Manage / Upload Songs to a TonieBox KreativTonie  
Build using the Python Tonie Api https://github.com/moritzj29/tonie_api and Flask  
Feel free to improve the code, I'm a python noob 

![image](https://user-images.githubusercontent.com/18744493/165509616-dfc7199e-8aa6-4648-afb6-3a4e2bbf17fd.png)

## Install


    docker image build -t tonies_web .

Bind the container /upload dir to a local one and put all playlists / audiobooks in different directories
    
    docker run -p 5000:5000 -e MYTONIES_USER=youremail -e MYONIES_PASS=yourpass --mount type=bind,source=/yourhostdir,target=/app/upload tonie_web:latest

## Features


- View all chapters=songs on your creative Tonie
- Delete all or single chapters
- Upload entire directory containing your playlist / audiobook

## ToDo
- Limited to 1 creative Tonie, currently only owning one but will try to add
- Uploading single songs instead of entire directory
