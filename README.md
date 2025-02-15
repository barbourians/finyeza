# finyeza
Finyeza ~ To shorten

## Deployment to Google Cloud

### Step 1: Enable App Engine in Your Project

- Run this command to create an App Engine application in your project
- It will ask you to select a region (choose the one closest to you).

`gcloud app create --project=wfence-finyeza`

### Step 2: Create an app.yaml File
This file tells App Engine how to run your app.

### Step 3: Install Dependencies & Create requirements.txt
Install Gunicorn (a production-ready server for Flask):

`pip install gunicorn`

Generate requirements.txt:

`pip freeze > requirements.txt`

### Step 4: Deploy to App Engine
Now, deploy your app with:

`gcloud app deploy`

- It will ask for confirmation. Type Y and press Enter.
- The deployment will take a few minutes.

### Step 5: Check Your App
Once deployment is complete, open your app in a browser:

`gcloud app browse`

This will launch your live Hello World Flask app! 🎉

---

## gcloud commands used

- `gcloud auth login`
- `gcloud projects list`
- `gcloud config set project <PROJECT_ID>`
- `gcloud config get-value project`
- `gcloud app create`
- `gcloud app deploy`

### testing
- `gcloud app browse`
- `curl https://<PROJECT_ID>.appspot.com/`
- `gcloud app logs tail -s default`

### trying to fix permissions
- `gcloud storage buckets list --filter="name:staging.<PROJECT_ID>.appspot.com"`
- `gcloud auth configure-docker gcr.io`

### authentication with firebase
- `gcloud auth application-default login`

