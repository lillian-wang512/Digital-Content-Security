from flask import render_template, Flask, flash, redirect, url_for
from forms.login_form import LoginForm
from forms.watermark_form import WatermarkForm
import os

app = Flask('__name__')
app.secret_key = 'LearnFlaskTheHardWay2017'

upload_dir = os.path.join(
    app.instance_path, 'upload' 
)

if not os.path.exists(upload_dir):
    os.makedirs(upload_dir, mode=0o755)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@lfthw.com' and form.password.data == 'adminpwd':
            return redirect(url_for('watermark'))

    return render_template('signin.html', form=form)


@app.route('/watermark', methods=['GET', 'POST'])
def watermark():
    form = WatermarkForm()
    if form.validate_on_submit():
        print(form.watermark.data)
        f = form.image.data
        f.save(os.path.join(upload_dir, f.filename))
        flash('Upload success。')
        return redirect(url_for('watermark'))

    return render_template('watermark.html', form=form)


if __name__ == "__main__":
    app.run(debug=True)
