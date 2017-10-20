from pictures.models import User,Image,Comment

def show_pic(page=1,per_page=5):
    images = Image.query.paginate(page, per_page).items
    return images


def user_by_id(userId):
    user = User.query.filter_by(id=userId).first()
    return user

def image_by_id(imageId):
    image = Image.query.filter_by(id=imageId).first()
    return image