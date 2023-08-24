import os
from os.path import join, dirname
from dotenv import load_dotenv

from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME =  os.environ.get("DB_NAME")

client = MongoClient(MONGODB_URI)
db = client[DB_NAME]

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/menu')
def menu():
    return render_template('menu.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/getmenu', methods=['POST'])
def getmenu():
    
    # bottle = [
    #     'https://whynotcoffee.id/wp-content/uploads/2020/10/coklat.jpg',
    #     'https://whynotcoffee.id/wp-content/uploads/2020/12/IMG_1317.png',
    #     'https://whynotcoffee.id/wp-content/uploads/2020/10/blackcoffee.jpg',
    #     'https://whynotcoffee.id/wp-content/uploads/2020/10/matchabottle.png',
    #     'https://whynotcoffee.id/wp-content/uploads/2020/12/mineral.png',
    #     'https://whynotcoffee.id/wp-content/uploads/2020/10/kopsu.jpg'
    # ]
    
    # deskripsi = [
    #     'Pure Dark Chocolate + Milk',
    #     'Apple Juice/Orange Juice',
    #     'Double Espresso + Water',
    #     'Pure Matcha + Milk',
    #     'Special Ingredient Whynot + Water',
    #     'Espresso + Brown Sugar + Milk'
    # ]
    
    # bottle_name = [
    #     'Chocolatte (250ml/ 1000ml)',
    #     'Chilled Juice (250ml)',
    #     'Black Coffee (250ml/ 1000ml)',
    #     'Matcha (250ml/ 1000ml)',
    #     'Mineral Water (250ml)',
    #     'Es Kopi Susu (250ml/ 1000ml)'
    # ]
    
    # count = 0
    # for name in bottle_name:
    #     rand_number = random.randint(1, 500) * random.randint(1000, 2000)
    #     test = f'{name}-{rand_number}-bbbbbbbbbbbbbbb'
    #     doc = {
    #         'id': test,
    #         'file': bottle[count],
    #         'judul': name,
    #         'deskripsi': deskripsi[count],
    #         'harga': rand_number,
    #         'status': 0,
    #         'kategori': 'Bottle'
    #     }
        
    #     db.menu.insert_one(doc)
        
    #     count+=1
    
    type_receive = request.form.get('type_give')
    result = list(db.menu.find({'kategori': type_receive},{'_id':False}))
    return jsonify({'menu': result})


@app.route('/admin-control-room/<id>')
def admin_page(id):
    data = list(db.admins.find({'id': id},{'_id': False, 'password': False}))
    level = data[0]['level']
    if level == 'hyperadmin':
        return render_template('index-admin.html')
    else:
        return render_template('index-admins.html')

@app.route('/admin-control-room/adminb')
def admin_page2():
    return render_template('index-admins.html')

@app.route('/admin-menu-addmenu-dd4c43005bbfb6346300d99999e2bcde')
def form_menu():
    return render_template('addmenu.html')

@app.route('/admin-menu-deletemenu-dd4c43005bbfb6346300d99999e2bcde')
def form_dmenu():
    return render_template('deletemenu.html')

@app.route('/admin-menu-editmenu-dd4c43005bbfb6346300d99999e2bcde')
def form_emenu():
    return render_template('editmenu.html')

@app.route('/admin-menu-addmenu-adminb')
def form_menu2():
    return render_template('addmenuadmins.html')

@app.route('/admin-menu-deletemenu-adminb')
def form_dmenu2():
    return render_template('deletemenuadmins.html')

@app.route('/admin-menu-editmenu-adminb')
def form_emenu2():
    return render_template('editmenuadmins.html')

@app.route('/admin-akun-admins-dd4c43005bbfb6346300d99999e2bcde')
def akun_admins():
    return render_template('akun-admins.html')

@app.route('/◻︎□︎⬧︎⧫︎□︎❒︎♋︎■︎♑︎', methods=['GET','POST'])
def post():
    judulproduk_receive = request.form["judulproduk_give"]
    deskripsiproduk_receive = request.form["deskripsiproduk_give"]
    harga_receive = request.form["harga_give"]
    kategori = request.form["kategori_give"]

    foto_receive = request.files["fotoproduk_give"]
    extension = foto_receive.filename.split(".")[-1]
    filename = f'static/pictures/menu/{judulproduk_receive}-{harga_receive}-{deskripsiproduk_receive}.{extension}'
    fid = f'{judulproduk_receive}-{harga_receive}-{deskripsiproduk_receive}'
    id = fid.replace(' ','')
    foto_receive.save(filename)
    doc = {
        'id':id,
        'file': filename,
        'judul': judulproduk_receive,
        'deskripsi': deskripsiproduk_receive,
        'harga':harga_receive,
        'status': 1,
        'kategori':kategori
    }
    db.menu.insert_one(doc)
    return jsonify({
        'msg': 'menu berhasil di tambah'
    })

@app.route('/❍︎♏︎■︎◆︎⬧︎', methods=['GET','POST'])
def menus():
    menu_list = list(db.menu.find({},{'_id':False}))
    return jsonify({'menu': menu_list})

@app.route('/♎︎♏︎♍︎●︎♓︎■︎♏︎', methods=['POST','GET'])
def decline():
    id = request.form['id_give']
    db.menu.delete_one({'id':id})
    return jsonify({'msg':'menu berhasil di hapus'})

@app.route('/♏︎♎︎♓︎⧫︎❍︎♏︎■︎◆︎',methods=['POST','GET'])
def edit_menu():
    id = request.form["id_give"]
    judulproduk = request.form["judulproduk_give"]
    deskripsiproduk = request.form["deskripsiproduk_give"]
    harga = request.form["harga_give"]
    status = request.form["status_give"]
    kategori = request.form["kategori_give"]
    db.menu.update_one({'id':id},{'$set':{'judul':judulproduk}})
    db.menu.update_one({'id':id},{'$set':{'deskripsi':deskripsiproduk}})
    db.menu.update_one({'id':id},{'$set':{'harga':harga}})
    db.menu.update_one({'id':id},{'$set':{'status':status}})
    db.menu.update_one({'id':id},{'$set':{'kategori':kategori}})
    return jsonify({'msg':'menu berhasil di update'})

@app.route('/admin',methods=['POST','GET'])
def admin_login():
    return render_template('admin-login.html')

@app.route('/●︎□︎♑︎♓︎■︎♋︎♎︎❍︎♓︎■︎',methods=['POST','GET'])
def admin_login_sys():
    username = request.form["username_give"]
    #password encryptor
    password = request.form["password_give"]
    hash_obj = hashlib.md5(password.encode())
    password = hash_obj.hexdigest()
    data = list(db.admins.find({'username': username},{'_id': False, 'password': False}))
    id = data[0]['id']
    url = f'/admin-control-room/{id}'
    table = db.admins
    is_username_real = table.find_one({'username': username}, {'_id': False})
    is_password_right = table.find_one({'username': username,'password':password}, {'_id': False})
    if is_username_real:
        if is_password_right:
            return jsonify({
                'msg':f'selamat datang {username}',
                'url':url,
            })
        else:
            return jsonify({'msg':'maaf password yang anda masukan salah'})
    else:
        return jsonify({'msg':'maaf username tidak ada'})
    
@app.route('/admin-create-dd4c43005bbfb6346300d99999e2bcde',methods=['POST','GET'])
def admin_create():
    return render_template('admin-create.html')
    
@app.route('/♍︎❒︎♏︎♋︎⧫︎♏︎♋︎︎♎︎︎❍︎︎♓︎︎■︎︎',methods=['POST','GET'])
def admin_create_sys():
    nama = request.form["nama_give"]
    hash_nama = hashlib.md5(nama.encode())
    id = hash_nama.hexdigest()

    password = request.form["password_give"]
    hash_pw = hashlib.md5(password.encode())
    password = hash_pw.hexdigest()

    username = request.form["username_give"]
    table = db.admins
    is_admins_real = table.find_one({'id': id}, {'_id': False})
    if is_admins_real is None:
        doc = {
            'id':id,
            'nama':nama,
            'username':username,
            'level':'admin',
            'password':password,
        }
        db.admins.insert_one(doc)
        return jsonify({
            'msg':'akun berhasil di tambahkan',
            'url':'/admin-akun-admins-dd4c43005bbfb6346300d99999e2bcde'
        })
    else:
        return jsonify({
            'msg': f'untuk akun dengan nama = {nama} sudah memiliki akun'
        })
    
@app.route('/♋︎🙵◆︎■︎⬧︎', methods=['GET','POST'])
def admins_list():
    admins_list = list(db.admins.find({'level':'admin'},{'_id':False,'password':False}))
    return jsonify({'admins': admins_list})
    
@app.route('/♋︎♎︎❍︎♓︎■︎♎︎♏︎●︎♏︎⧫︎♏︎', methods=['GET','POST'])
def delete_akun():
    id = request.form['id_give']
    db.admins.delete_one({'id':id})
    return jsonify({'msg':'akun berhasil di hapus'})

@app.route('/admin-akun-hyperadmincog-dd4c43005bbfb6346300d99999e2bcde', methods=['GET','POST'])
def edit_akun_hyper():
    return render_template('akun-hyperadmincog.html')

@app.route('/♒︎⍓︎◻︎♏︎❒︎♋︎♎︎❍︎♓︎■︎♍︎□︎■︎', methods=['GET','POST'])
def edit_akun_hyper_sys():
    passwordlama = request.form['passwordlama_give']
    hash_pw = hashlib.md5(passwordlama.encode())
    passwordlama = hash_pw.hexdigest()

    password = request.form['password_give']
    hash_pwl = hashlib.md5(password.encode())
    password = hash_pwl.hexdigest()

    table = db.admins
    is_password_right = table.find_one({'id': 'dd4c43005bbfb6346300d99999e2bcde','password':passwordlama}, {'_id': False})
    if is_password_right:
        db.admins.update_one({'id':'dd4c43005bbfb6346300d99999e2bcde'},{'$set':{'password':password}})
        return jsonify({
            'msg':'password berhasil diubah',
            'url':'mwehe'
        })
    else:
        return jsonify({
            'msg':'password lama tidak benar coba sekali lagi'
        })

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)