document.addEventListener('DOMContentLoaded', () => {
    const token = localStorage.getItem('token');
    if (!token && window.location.pathname !== '/login.html') {
        window.location.href = 'login.html';
    }

    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            // ... (código de inicio de sesión)
        });
    }

    const logoutBtn = document.getElementById('logout-btn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', () => {
            localStorage.removeItem('token');
            window.location.href = 'login.html';
        });
    }

    const navProducts = document.getElementById('nav-products');
    if (navProducts) {
        navProducts.addEventListener('click', loadProductsSection);
    }
});

async function loadProductsSection() {
    const app = document.getElementById('app');
    const token = localStorage.getItem('token');

    try {
        const response = await fetch('http://127.0.0.1:5000/products', {
            headers: { 'Authorization': `Bearer ${token}` }
        });

        if (response.ok) {
            const products = await response.json();
            let html = '<h2>Productos</h2>';
            html += `
                <table>
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Nombre</th>
                            <th>Descripción</th>
                            <th>Precio</th>
                            <th>Categoría</th>
                            <th>Stock</th>
                            <th>Acciones</th>
                        </tr>
                    </thead>
                    <tbody>
            `;
            products.forEach(p => {
                html += `
                    <tr>
                        <td>${p.id}</td>
                        <td>${p.name}</td>
                        <td>${p.description}</td>
                        <td>${p.price}</td>
                        <td>${p.category}</td>
                        <td>${p.stock}</td>
                        <td>
                            <button onclick="editProduct(${p.id})">Editar</button>
                            <button onclick="deleteProduct(${p.id})">Eliminar</button>
                        </td>
                    </tr>
                `;
            });
            html += '</tbody></table>';

            html += `
                <h3>Agregar Producto</h3>
                <form id="add-product-form">
                    <input type="text" name="name" placeholder="Nombre" required>
                    <input type="text" name="description" placeholder="Descripción">
                    <input type="number" name="price" placeholder="Precio" required>
                    <input type="text" name="category" placeholder="Categoría" required>
                    <input type="number" name="stock" placeholder="Stock" required>
                    <button type="submit">Agregar</button>
                </form>
            `;

            app.innerHTML = html;

            const addProductForm = document.getElementById('add-product-form');
            addProductForm.addEventListener('submit', async (e) => {
                e.preventDefault();
                const formData = new FormData(e.target);
                const productData = Object.fromEntries(formData.entries());

                try {
                    const response = await fetch('http://127.0.0.1:5000/products', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'Authorization': `Bearer ${token}`
                        },
                        body: JSON.stringify(productData)
                    });
                    if (response.ok) {
                        loadProductsSection(); // Recargar la sección de productos
                    } else {
                        alert('Error al agregar el producto.');
                    }
                } catch (error) {
                    console.error('Error:', error);
                }
            });
        } else {
            app.innerHTML = '<p>Error al cargar los productos.</p>';
        }
    } catch (error) {
        console.error('Error:', error);
        app.innerHTML = '<p>Error de conexión.</p>';
    }
}

async function deleteProduct(id) {
    const token = localStorage.getItem('token');
    if (confirm('¿Estás seguro de que quieres eliminar este producto?')) {
        try {
            const response = await fetch(`http://127.0.0.1:5000/products/${id}`, {
                method: 'DELETE',
                headers: { 'Authorization': `Bearer ${token}` }
            });
            if (response.ok) {
                loadProductsSection();
            } else {
                alert('Error al eliminar el producto.');
            }
        } catch (error) {
            console.error('Error:', error);
        }
    }
}

// La función editProduct se implementará en un próximo paso
function editProduct(id) {
    alert(`Editar producto con ID: ${id}`);
}

    const navOrders = document.getElementById('nav-orders');
    if (navOrders) {
        navOrders.addEventListener('click', loadOrdersSection);
    }
});

async function loadOrdersSection() {
    const app = document.getElementById('app');
    const token = localStorage.getItem('token');

    try {
        const response = await fetch('http://127.0.0.1:5000/orders', {
            headers: { 'Authorization': `Bearer ${token}` }
        });

        if (response.ok) {
            const orders = await response.json();
            let html = '<h2>Pedidos</h2>';
            html += '<button onclick="showCreateOrderForm()">Crear Pedido</button>';
            html += `
                <table>
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Cliente ID</th>
                            <th>Fecha</th>
                            <th>Total</th>
                            <th>Estado</th>
                            <th>Acciones</th>
                        </tr>
                    </thead>
                    <tbody>
            `;
            orders.forEach(o => {
                html += `
                    <tr>
                        <td>${o.id}</td>
                        <td>${o.customer_id}</td>
                        <td>${o.order_date}</td>
                        <td>${o.total_amount}</td>
                        <td>${o.status}</td>
                        <td>
                            <button onclick="viewOrder(${o.id})">Ver</button>
                        </td>
                    </tr>
                `;
            });
            html += '</tbody></table>';
            app.innerHTML = html;
        } else {
            app.innerHTML = '<p>Error al cargar los pedidos.</p>';
        }
    } catch (error) {
        console.error('Error:', error);
        app.innerHTML = '<p>Error de conexión.</p>';
    }
}

async function viewOrder(id) {
    // Implementación en un próximo paso
    alert(`Ver pedido con ID: ${id}`);
}

async function showCreateOrderForm() {
    // Implementación en un próximo paso
    alert('Mostrar formulario para crear pedido');
}

    const navReports = document.getElementById('nav-reports');
    if (navReports) {
        navReports.addEventListener('click', loadReportsSection);
    }
});

function loadReportsSection() {
    const app = document.getElementById('app');
    let html = `
        <h2>Informes</h2>
        <button onclick="loadDailySalesReport()">Ventas Diarias</button>
        <button onclick="loadProfitLossReport()">Pérdidas y Ganancias</button>
        <button onclick="loadSalesProjectionReport()">Proyección de Ventas</button>
        <div id="report-content"></div>
    `;
    app.innerHTML = html;
}

async function loadDailySalesReport() {
    const reportContent = document.getElementById('report-content');
    const token = localStorage.getItem('token');
    try {
        const response = await fetch('http://127.0.0.1:5000/reports/daily_sales', {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (response.ok) {
            const report = await response.json();
            reportContent.innerHTML = `
                <h3>Ventas del ${report.date}</h3>
                <p>Total de Pedidos: ${report.total_orders}</p>
                <p>Total de Ventas: $${report.total_sales}</p>
            `;
        } else {
            reportContent.innerHTML = '<p>Error al cargar el informe.</p>';
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

async function loadProfitLossReport() {
    const reportContent = document.getElementById('report-content');
    const token = localStorage.getItem('token');
    try {
        const response = await fetch('http://127.0.0.1:5000/reports/profit_loss', {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (response.ok) {
            const report = await response.json();
            reportContent.innerHTML = `
                <h3>Informe de Pérdidas y Ganancias</h3>
                <p>Total de Ventas: $${report.total_sales}</p>
                <p>Total de Compras: $${report.total_purchases}</p>
                <p>Ganancia: $${report.profit}</p>
            `;
        } else {
            reportContent.innerHTML = '<p>Error al cargar el informe.</p>';
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

async function loadSalesProjectionReport() {
    const reportContent = document.getElementById('report-content');
    const token = localStorage.getItem('token');
    try {
        const response = await fetch('http://127.0.0.1:5000/reports/sales_projection', {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (response.ok) {
            const report = await response.json();
            reportContent.innerHTML = `
                <h3>Proyección de Ventas</h3>
                <p>Período de Proyección: ${report.projection_period_days} días</p>
                <p>Ventas Proyectadas: $${report.projected_sales}</p>
            `;
        } else {
            reportContent.innerHTML = '<p>Error al cargar el informe.</p>';
        }
    } catch (error) {
        console.error('Error:', error);
    }
}
});
