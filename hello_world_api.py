from fastapi import FastAPI

app=FastAPI() #object of class

@app.get("/") #decorater- listens to get method and the end point name is '/'
def hello():
    return {'message': 'hello world'}

#another endpoint- if someone hits this url, it will land on the about page?
@app.get("/about")
def about():
    return {'message':'Campusx is an educational platform for data science.'}

"""
fastapi generates automatic documentation. go to /docs endpoint for details of all the endpoints and interact with them
"""

# uvicorn hello_world_api:app --reload --port 8000
""" this command to run in terminal. this will start uvicorn server 
--reload automatically updates the changes made in the code to the live server
"""