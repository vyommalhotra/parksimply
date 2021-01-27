# parksimply
Machine vision assisted parking system

## Dependencies
- Git LFS
- python (3 < ver. < 3.9)
    - tensorflow
    - cv2
    - numpy
    - flask
- node.js
    - npm
    - npx
- yarn

## Run Locally


### Run Web App
<ins>Rest server </ins> <br>
cd `/parksimply/extractor/src/api` <br> 
run `flask run` <br>
keep this terminal/cmd open and open a new one for react app <br> <br>
<ins>React App <br></ins>
cd `/parksimply/webapp/react-flask-app` <br>
run `yarn start`

### Run Extractor
cd `parksimply/extractor/src` <br>
run `python main.py`



