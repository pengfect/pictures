from pictures.models import User,Image,Comment

def show_pic(page=1,per_page=5):
    images = Image.query.paginate(page, per_page).items
    return images