from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import create_access_token, jwt_required, JWTManager

app = Flask(__name__)

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/asadero_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'super-secret'  # ¡Cambia esto en producción!

db = SQLAlchemy(app)
jwt = JWTManager(app)

# Modelo de Producto
class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    category = db.Column(db.String(255), nullable=False)
    stock = db.Column(db.Integer, nullable=False)

# Modelo de Cliente
class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255))
    phone = db.Column(db.String(20))
    orders = db.relationship('Order', backref='customer', lazy=True)

# Modelo de Pedido
class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    order_date = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.String(50), nullable=False, default='pending')
    items = db.relationship('OrderItem', backref='order', lazy=True)

# Modelo de Detalle de Pedido
class OrderItem(db.Model):
    __tablename__ = 'order_items'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)

# Modelo de Compra
class Purchase(db.Model):
    __tablename__ = 'purchases'
    id = db.Column(db.Integer, primary_key=True)
    purchase_date = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    supplier = db.Column(db.String(255))
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)
    items = db.relationship('PurchaseItem', backref='purchase', lazy=True)

# Modelo de Usuario
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

# Modelo de Detalle de Compra
class PurchaseItem(db.Model):
    __tablename__ = 'purchase_items'
    id = db.Column(db.Integer, primary_key=True)
    purchase_id = db.Column(db.Integer, db.ForeignKey('purchases.id'), nullable=False)
    item_name = db.Column(db.String(255), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)

from flask import request, jsonify
from datetime import date, datetime, timedelta

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and user.password == data['password']:
        access_token = create_access_token(identity=user.username)
        return jsonify(access_token=access_token)
    return jsonify({'message': 'Credenciales incorrectas'}), 401

@app.route('/')
def index():
    return "¡Bienvenido al sistema del asadero!"

# Rutas para productos (CRUD)
@app.route('/products', methods=['GET'])
@jwt_required()
def get_products():
    products = Product.query.all()
    return jsonify([{'id': p.id, 'name': p.name, 'description': p.description, 'price': str(p.price), 'category': p.category, 'stock': p.stock} for p in products])

@app.route('/products/<int:id>', methods=['GET'])
@jwt_required()
def get_product(id):
    product = Product.query.get_or_404(id)
    return jsonify({'id': product.id, 'name': product.name, 'description': product.description, 'price': str(product.price), 'category': product.category, 'stock': product.stock})

@app.route('/products', methods=['POST'])
@jwt_required()
def create_product():
    data = request.get_json()
    new_product = Product(
        name=data['name'],
        description=data.get('description'),
        price=data['price'],
        category=data['category'],
        stock=data['stock']
    )
    db.session.add(new_product)
    db.session.commit()
    return jsonify({'id': new_product.id}), 201

@app.route('/products/<int:id>', methods=['PUT'])
@jwt_required()
def update_product(id):
    product = Product.query.get_or_404(id)
    data = request.get_json()
    product.name = data['name']
    product.description = data.get('description')
    product.price = data['price']
    product.category = data['category']
    product.stock = data['stock']
    db.session.commit()
    return jsonify({'message': 'Producto actualizado'})

@app.route('/products/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': 'Producto eliminado'})

# Rutas para pedidos
@app.route('/orders', methods=['POST'])
@jwt_required()
def create_order():
    data = request.get_json()

    # Crear o encontrar al cliente
    customer_id = data.get('customer_id')
    if not customer_id:
        new_customer = Customer(name=data['customer_name'], email=data.get('customer_email'), phone=data.get('customer_phone'))
        db.session.add(new_customer)
        db.session.commit()
        customer_id = new_customer.id

    # Crear el pedido
    total_amount = 0
    new_order = Order(customer_id=customer_id, total_amount=total_amount)
    db.session.add(new_order)
    db.session.commit()

    # Agregar productos al pedido
    for item_data in data['items']:
        product = Product.query.get_or_404(item_data['product_id'])
        if product.stock < item_data['quantity']:
            return jsonify({'message': f'No hay suficiente stock para {product.name}'}), 400

        order_item = OrderItem(
            order_id=new_order.id,
            product_id=item_data['product_id'],
            quantity=item_data['quantity'],
            price=product.price
        )
        total_amount += product.price * item_data['quantity']
        product.stock -= item_data['quantity']
        db.session.add(order_item)

    new_order.total_amount = total_amount
    db.session.commit()
    return jsonify({'id': new_order.id}), 201

@app.route('/orders', methods=['GET'])
@jwt_required()
def get_orders():
    orders = Order.query.all()
    return jsonify([{'id': o.id, 'customer_id': o.customer_id, 'order_date': o.order_date, 'total_amount': str(o.total_amount), 'status': o.status} for o in orders])

@app.route('/orders/<int:id>', methods=['GET'])
@jwt_required()
def get_order(id):
    order = Order.query.get_or_404(id)
    items = [{'product_id': i.product_id, 'quantity': i.quantity, 'price': str(i.price)} for i in order.items]
    return jsonify({'id': order.id, 'customer_id': order.customer_id, 'order_date': order.order_date, 'total_amount': str(order.total_amount), 'status': order.status, 'items': items})

@app.route('/orders/<int:id>', methods=['PUT'])
@jwt_required()
def update_order(id):
    order = Order.query.get_or_404(id)
    data = request.get_json()
    order.status = data['status']
    db.session.commit()
    return jsonify({'message': 'Pedido actualizado'})

# Ruta para generar factura
@app.route('/orders/<int:id>/bill', methods=['GET'])
@jwt_required()
def get_order_bill(id):
    order = Order.query.get_or_404(id)

    customer_name = order.customer.name if order.customer else "Cliente no especificado"

    bill = {
        'order_id': order.id,
        'order_date': order.order_date,
        'customer_name': customer_name,
        'items': [{'product_name': item.product.name, 'quantity': item.quantity, 'price': str(item.price), 'subtotal': str(item.quantity * item.price)} for item in order.items],
        'total_amount': str(order.total_amount),
        'status': order.status
    }
    return jsonify(bill)


# Rutas para informes
@app.route('/reports/daily_sales', methods=['GET'])
@jwt_required()
def daily_sales_report():
    today = date.today()
    start_of_day = datetime.combine(today, datetime.min.time())
    end_of_day = datetime.combine(today, datetime.max.time())

    orders = Order.query.filter(Order.order_date.between(start_of_day, end_of_day)).all()

    total_sales = sum(order.total_amount for order in orders)
    total_orders = len(orders)

    report = {
        'date': today.isoformat(),
        'total_orders': total_orders,
        'total_sales': str(total_sales)
    }
    return jsonify(report)

# Rutas para compras
@app.route('/purchases', methods=['POST'])
@jwt_required()
def create_purchase():
    data = request.get_json()
    total_amount = 0
    new_purchase = Purchase(supplier=data.get('supplier'), total_amount=total_amount)
    db.session.add(new_purchase)
    db.session.commit()

    for item_data in data['items']:
        purchase_item = PurchaseItem(
            purchase_id=new_purchase.id,
            item_name=item_data['item_name'],
            quantity=item_data['quantity'],
            price=item_data['price']
        )
        total_amount += item_data['price'] * item_data['quantity']
        db.session.add(purchase_item)

    new_purchase.total_amount = total_amount
    db.session.commit()
    return jsonify({'id': new_purchase.id}), 201

@app.route('/purchases', methods=['GET'])
@jwt_required()
def get_purchases():
    purchases = Purchase.query.all()
    return jsonify([{'id': p.id, 'supplier': p.supplier, 'purchase_date': p.purchase_date, 'total_amount': str(p.total_amount)} for p in purchases])

@app.route('/reports/profit_loss', methods=['GET'])
@jwt_required()
def profit_loss_report():
    total_sales = db.session.query(db.func.sum(Order.total_amount)).scalar() or 0
    total_purchases = db.session.query(db.func.sum(Purchase.total_amount)).scalar() or 0

    profit = total_sales - total_purchases

    report = {
        'total_sales': str(total_sales),
        'total_purchases': str(total_purchases),
        'profit': str(profit)
    }
    return jsonify(report)

@app.route('/reports/sales_projection', methods=['GET'])
@jwt_required()
def sales_projection():
    # Calculate average daily sales over the last 30 days
    last_30_days = datetime.now() - timedelta(days=30)
    orders_last_30_days = Order.query.filter(Order.order_date >= last_30_days).all()

    if not orders_last_30_days:
        return jsonify({'message': 'No hay suficientes datos para una proyección'}), 400

    total_sales_last_30_days = sum(order.total_amount for order in orders_last_30_days)
    average_daily_sales = total_sales_last_30_days / 30

    # Project sales for the next 30 days
    projected_sales = average_daily_sales * 30

    report = {
        'projection_period_days': 30,
        'projected_sales': str(projected_sales)
    }
    return jsonify(report)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
