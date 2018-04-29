import json
import time
from pathlib import Path

from flask import Flask, render_template, request, redirect, flash, url_for
from flask_login import login_required, logout_user, login_user, current_user


from .models import *
from .ext import db, login_manager, sockets


template_folder = str(Path(__file__).parent / 'templates')
static_folder = str(Path(__file__).parent / 'static')
app = Flask(
    'demonhunter',
    template_folder=template_folder,
    static_folder=static_folder
)

app.debug = True


@app.before_first_request
def create_database():
    db.create_all()
    users = User.query.all()
    if not users:
        u = User(username="admin", password='admin')
        db.session.add(u)
        db.session.commit()

#########################################
############### DASHBOARD ###############
#########################################

@app.route('/dashboard/')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/')
@login_required
def index():
    return redirect(url_for('dashboard'))

online_users = set()
@sockets.route('/notifications/')
def notifications(ws):
    online_users.add(ws)
    try:
        while True:
            message = ws.wait()
            if message is None:
                break
    finally:
        online_users.remove(ws)

######################################
################ AUTH ################
######################################

@app.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')

        u = User.query.filter_by(username=username).first()
        if u and u.check_password(password):
            login_user(u)
            return redirect('dashboard')
    return render_template('login.html')

@app.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect('login')

#####################################
############### USERS ###############
#####################################

@app.route('/users/list/')
@login_required
def users_list():
    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/users/create/', methods=["POST", "GET"])
@login_required
def users_create():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            flash("Email and username are required")
            return redirect(url_for('users_create'))

        u = User(username=username, password=password)
        db.session.add(u)
        db.session.commit()
        return redirect(url_for('users_list'))
    return render_template('create_user.html')

@app.route('/users/delete/<int:user_id>/')
@login_required
def users_delete(user_id):
    if current_user.id == user_id:
        flash("You can not delete yourself")
        return redirect(url_for('users_list'))

    deleted = User.query.filter_by(id=user_id).delete()
    db.session.commit()
    if deleted:
        flash('User deleted')
    else:
        flash('No user with this id')
    return redirect(url_for('users_list'))

######################################
############### AGENTS ###############
######################################

@app.route('/agents/list/')
@login_required
def agents_list():
    agents = Agent.query.all()
    return render_template('agents.html', agents=agents)

@app.route('/agents/add/', methods=["POST", "GET"])
@login_required
def agents_add():
    if request.method == "POST":
        address = request.form.get('address')

        a = Agent(address=address)
        a.generate_token()
        db.session.add(a)
        db.session.commit()
        return redirect(url_for('agents_list'))
    return render_template('create_agent.html')

@app.route('/agents/delete/<int:agent_id>/')
@login_required
def agents_delete(agent_id):
    deleted = Agent.query.filter_by(id=agent_id).delete()
    db.session.commit()
    if deleted:
        flash('Agent deleted')
    else:
        flash('No Agent with this id')
    return redirect(url_for('agents_list'))

@app.route('/agents/call/<token>/', methods=['POST'])
def agents_call(token):
    a = Agent.query.filter_by(token=token).first()
    if not a or a.address != request.remote_addr:
        for ws in online_users:
            ws.send(json.dumps(
                    {'type':'alart',
                     'content':'An attack to manager or bad honeypot agent configuration',
                     'title':'Attack to manager ?'}
                )
            )
        return "ok"

    a.last_message = time.time()

    data = request.get_json()
    from_address = data['from']
    attack_time = data['time']
    protocol = data['protocol']
    del data['from']
    del data['time']
    del data['protocol']
    hpd = HoneypotData(
        protocol=protocol, honeypot_address=a.address,
        attack_time=attack_time, from_address=from_address, data=json.dumps(data))
    db.session.add(hpd)
    db.session.commit()

    content = 'An attack from %s to %s at %s' % (from_address, a.address, hpd.utc_time())
    for ws in online_users:
        ws.send(json.dumps({'type':'success',
                            'content':content,
                            'title':'Attack to Honeypot'}))
    return "ok"

#############################################
############### HONEYPOT DATA ###############
#############################################

@app.route('/data/')
@login_required
def honeypot_data():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('page', 32, type=int)
    datas = HoneypotData.query.order_by(HoneypotData.id.desc()).paginate(
        page=page, per_page=per_page, error_out=False).items
    return render_template('data.html', datas=datas, page=page)