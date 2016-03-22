from flask import Flask, request, render_template, redirect, url_for, send_file

import cStringIO, qrcode

application = Flask(__name__)

#from app.models import User

def random_qr(url='www.google.com'):
    qr = qrcode.QRCode(version=1,
                       error_correction=qrcode.constants.ERROR_CORRECT_L,
                       box_size=10,
                       border=4)

    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image()
    return img

@application.route("/", methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@application.route("/challenge", methods=['GET', 'POST'])
def thanks():
    img_buf = cStringIO.StringIO()
    img = random_qr(url='www.python.org')
    img.save(img_buf)
    img_buf.seek(0)
    return send_file(img_buf, mimetype='image/png')
    #return render_template('data.html')

if __name__ == "__main__":
    application.run(host='0.0.0.0', debug=True)