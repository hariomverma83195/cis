## Home Page

![Home](https://github.com/hariomverma83195/cis/blob/main/assets/homepage.jpg?raw=true)


## Admin Pane

![Admin Paned](https://github.com/hariomverma83195/cis/blob/main/assets/admin_panel.jpg?raw=true)


## Match

![Match](https://github.com/hariomverma83195/cis/blob/main/assets/output_matchm.jpg?raw=true)


## Clear

![Clear](https://github.com/hariomverma83195/cis/blob/main/assets/output_clear.jpg?raw=true)






Clone this repository and install the requirements using the following command
(Recommended installing requirements in virtual environment)

```console
pip install -r requirements.txt
```


### Requirement List

- [x] flask
- [x] pyyaml
- [x] lpips
- [x] argparse
- [x] deepface
- [x] opencv-python
- [x] asyncio
- [x] mysql-connector-python
- [x] tf-keras

## If pytorch is not automatically installed

Make sure to choose the suitable version from their website and install it yourself


## Setup MySQL

Setup user privilleges and create database named 'c'

Don't forget to modify the app.py file to add your db credentials and ofxourse you can change the database name

```or``` 

Add the credential to a '.env' file.


add the tables to the database 'c' given in the tables.txt file


#### Note:- This project is not meant to be used in production



### Project By Team Astro

## Other requirements

- [x] Create folder "input/whole_imgs" if not exists.
- [x] Also create "results/res" folder if not exists.
