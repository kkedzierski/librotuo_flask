import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from librotuo import mail


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/images',
                                picture_fn)

    output_size = (125, 125)
    resized_image = Image.open(form_picture)
    resized_image.thumbnail(output_size)
    resized_image.save(picture_path)

    return picture_fn


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='librotuo.cso@gmail.com',
                  recipients=[user.email])
    msg.html = '''<h3>Reset password to Librouto website </h3>
    To reset your click this link:
    <a href="{urlfor}" >Reset password</a> <br>
    If you did not make
    this reset, ignore it'''.format(urlfor=url_for('reset_token',
                                                   token=token,
                                                   _external=True))
    mail.send(msg)
