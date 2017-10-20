from pictures import app,logic
from flask import render_template

@app.route('/')
def index():
    images = logic.show_pic()
    return render_template('index.html',images=images)

@app.route('/profile/<int:userId>/')
def profile(userId):
    user = logic.user_by_id(userId)
    return render_template('profile.html',user=user)

@app.route('/detail/<int:imageId>/')
def detail(imageId):
    image = logic.image_by_id(imageId)
    return render_template('detail.html',image=image)