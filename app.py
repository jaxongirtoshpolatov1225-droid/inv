from flask import Flask, render_template, request, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import qrcode
import io
import base64
from datetime import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key-here'

db = SQLAlchemy(app)
CORS(app)

# Ma'lumotlar bazasi modellari
class Organization(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    has_floors = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    floors = db.relationship('Floor', backref='organization', lazy=True, cascade='all, delete-orphan')
    rooms = db.relationship('Room', backref='organization', lazy=True, cascade='all, delete-orphan')

class Floor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    organization_id = db.Column(db.Integer, db.ForeignKey('organization.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    rooms = db.relationship('Room', backref='floor', lazy=True, cascade='all, delete-orphan')

class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    organization_id = db.Column(db.Integer, db.ForeignKey('organization.id'), nullable=False)
    floor_id = db.Column(db.Integer, db.ForeignKey('floor.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    equipment = db.relationship('Equipment', backref='room', lazy=True, cascade='all, delete-orphan')

class Equipment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    inv_code = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    brand = db.Column(db.String(100))
    model = db.Column(db.String(100))
    serial_number = db.Column(db.String(100))
    purchase_date = db.Column(db.Date)
    price = db.Column(db.Float)
    status = db.Column(db.String(50), default='Active')
    description = db.Column(db.Text)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Asosiy sahifa
@app.route('/')
def index():
    organizations = Organization.query.all()
    return render_template('index.html', organizations=organizations)

# Tashkilot qo'shish
@app.route('/add_organization', methods=['POST'])
def add_organization():
    data = request.get_json()
    name = data.get('name')
    has_floors = data.get('has_floors', False)
    
    if not name:
        return jsonify({'error': 'Tashkilot nomi kiritilishi shart'}), 400
    
    organization = Organization(name=name, has_floors=has_floors)
    db.session.add(organization)
    db.session.commit()
    
    return jsonify({'success': True, 'organization_id': organization.id})

# Tashkilot sahifasi
@app.route('/organization/<int:org_id>')
def organization_page(org_id):
    organization = Organization.query.get_or_404(org_id)
    if organization.has_floors:
        floors = Floor.query.filter_by(organization_id=org_id).all()
        return render_template('organization_with_floors.html', organization=organization, floors=floors)
    else:
        rooms = Room.query.filter_by(organization_id=org_id, floor_id=None).all()
        return render_template('organization_direct_rooms.html', organization=organization, rooms=rooms)

# Qavat qo'shish
@app.route('/add_floor', methods=['POST'])
def add_floor():
    data = request.get_json()
    name = data.get('name')
    organization_id = data.get('organization_id')
    
    if not name or not organization_id:
        return jsonify({'error': 'Qavat nomi va tashkilot ID kiritilishi shart'}), 400
    
    floor = Floor(name=name, organization_id=organization_id)
    db.session.add(floor)
    db.session.commit()
    
    return jsonify({'success': True, 'floor_id': floor.id})

# Qavat sahifasi
@app.route('/floor/<int:floor_id>')
def floor_page(floor_id):
    floor = Floor.query.get_or_404(floor_id)
    rooms = Room.query.filter_by(floor_id=floor_id).all()
    return render_template('floor.html', floor=floor, rooms=rooms)

# Xona qo'shish
@app.route('/add_room', methods=['POST'])
def add_room():
    data = request.get_json()
    name = data.get('name')
    organization_id = data.get('organization_id')
    floor_id = data.get('floor_id')
    
    if not name or not organization_id:
        return jsonify({'error': 'Xona nomi va tashkilot ID kiritilishi shart'}), 400
    
    room = Room(name=name, organization_id=organization_id, floor_id=floor_id)
    db.session.add(room)
    db.session.commit()
    
    return jsonify({'success': True, 'room_id': room.id})

# Xona sahifasi
@app.route('/room/<int:room_id>')
def room_page(room_id):
    room = Room.query.get_or_404(room_id)
    equipment = Equipment.query.filter_by(room_id=room_id).all()
    return render_template('room.html', room=room, equipment=equipment)

# Jihoz qo'shish
@app.route('/add_equipment', methods=['POST'])
def add_equipment():
    data = request.get_json()
    
    # Inventarizatsiya kodi yaratish
    org = Organization.query.get(data['organization_id'])
    room = Room.query.get(data['room_id'])
    equipment_count = Equipment.query.filter_by(room_id=data['room_id']).count() + 1
    
    inv_code = f"{org.name[:3].upper()}-{room.name[:3].upper()}-{equipment_count:04d}"
    
    equipment = Equipment(
        inv_code=inv_code,
        name=data['name'],
        category=data['category'],
        brand=data.get('brand'),
        model=data.get('model'),
        serial_number=data.get('serial_number'),
        purchase_date=datetime.strptime(data['purchase_date'], '%Y-%m-%d').date() if data.get('purchase_date') else None,
        price=float(data['price']) if data.get('price') else None,
        status=data.get('status', 'Active'),
        description=data.get('description'),
        room_id=data['room_id']
    )
    
    db.session.add(equipment)
    db.session.commit()
    
    return jsonify({'success': True, 'equipment_id': equipment.id, 'inv_code': inv_code})

# QR kod yaratish
@app.route('/generate_qr/<int:equipment_id>')
def generate_qr(equipment_id):
    equipment = Equipment.query.get_or_404(equipment_id)
    
    # QR kod matni
    qr_text = f"Tashkilot: {equipment.room.organization.name}\nInv kode: {equipment.inv_code}"
    
    # QR kod yaratish
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(qr_text)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Rasmni base64 formatiga o'tkazish
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    
    img_base64 = base64.b64encode(buffer.getvalue()).decode()
    
    return jsonify({'qr_code': img_base64, 'inv_code': equipment.inv_code})

# Jihoz ma'lumotlarini olish
@app.route('/equipment/<int:equipment_id>')
def get_equipment(equipment_id):
    equipment = Equipment.query.get_or_404(equipment_id)
    return jsonify({
        'id': equipment.id,
        'inv_code': equipment.inv_code,
        'name': equipment.name,
        'category': equipment.category,
        'brand': equipment.brand,
        'model': equipment.model,
        'serial_number': equipment.serial_number,
        'purchase_date': equipment.purchase_date.isoformat() if equipment.purchase_date else None,
        'price': equipment.price,
        'status': equipment.status,
        'description': equipment.description,
        'room_name': equipment.room.name,
        'organization_name': equipment.room.organization.name
    })

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
