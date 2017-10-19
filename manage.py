from flask_script import Manager
from pictures import app,db
from pictures.models import User,Image,Comment

manager = Manager(app)

@manager.command
def init_database():
    db.drop_all()
    db.create_all()
    urls = [
        'https://img.alicdn.com/imgextra/i4/1961895911/TB2ymQXcdRopuFjSZFtXXcanpXa_!!1961895911-2-beehive-scenes.png_400x400q75.jpg',
        'http://gw3.alicdn.com/tfscom/tuitui/TB18dWkOXXXXXbcXXXXXXXXXXXX_400x400q75.jpg',
        'https://gtd.alicdn.com/sns_logo/i1/TB11yxeNVXXXXbwXFXXSutbFXXX.jpg_240x240xz.jpg',
        'https://gtd.alicdn.com/sns_logo/i4/TB1BYGDLpXXXXbuXXXXSutbFXXX.jpg_240x240xz.jpg',
        'https://gtd.alicdn.com/sns_logo/i1/TB11yxeNVXXXXbwXFXXSutbFXXX.jpg_240x240xz.jpg',
        'https://gtd.alicdn.com/sns_logo/i4/TB1MwqbLpXXXXaEXpXXSutbFXXX.jpg_240x240xz.jpg',
        'https://gtd.alicdn.com/sns_logo/i7/TB1TlOfQFXXXXX2XXXXwu0bFXXX.png_240x240xz.jpg',
        'https://gtd.alicdn.com/sns_logo/i1/TB1pxCTQpXXXXa2apXXSutbFXXX.jpg_240x240xz.jpg',
        'https://gtd.alicdn.com/sns_logo/i4/TB1IbTJHVXXXXbRXpXXSutbFXXX.jpg_240x240xz.jpg',
        'https://gtd.alicdn.com/sns_logo/i4/TB1flZjKpXXXXXhXXXXSutbFXXX.jpg_240x240xz.jpg',
        'https://img.alicdn.com/sns_logo/i2/TB1oTrsHpXXXXaLXVXXSutbFXXX.jpg_240x240xz.jpg']

    for i in range(1, 10, 1):
        db.session.add(User('用户-' + str(i), '密码-' + str(i), 'salt'))
        db.session.add(Image(urls[i - 1], i))
        for z in range(2):
            db.session.add(Comment(i, i, 'this is a comment' + str(i) + '-' + str(z)))

    db.session.commit()


if __name__ == '__main__':
    manager.run()