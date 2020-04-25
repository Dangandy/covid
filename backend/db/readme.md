# database stuff lives here

## specs:
- less than 1TB of info ( 1 file )
- upserts on current date (and yesterday?)
- pull all data to build model 

## setup:
```bash
pip install -r requirements.txt 
python create.py  			# if you don't have site.db present

# on an hourly basis ( currently using airflow )
python update.py
```
- a sandbox example has been provided in sample

## To Do:
-[X] impletement: sqlite 
-[X] airflow 
-[] test cases
