import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta
import numpy as np

# Configurar Faker en español
fake = Faker('es_ES')
random.seed(42)  # Para resultados reproducibles

# Listas de categorías y productos
categorias = ['Smartphones', 'Laptops', 'Tablets', 'Audio', 'Accesorios', 'Gaming']
productos = {
    'Smartphones': ['iPhone 15', 'Samsung S23', 'Xiaomi 13', 'Google Pixel 8'],
    'Laptops': ['MacBook Pro', 'Dell XPS', 'HP Spectre', 'Lenovo ThinkPad'],
    'Tablets': ['iPad Pro', 'Samsung Tab S9', 'Surface Pro'],
    'Audio': ['AirPods Pro', 'Sony WH-1000XM5', 'Bose QuietComfort'],
    'Accesorios': ['Cargador USB-C', 'Funda Protectora', 'Soporte Laptop'],
    'Gaming': ['PlayStation 5', 'Xbox Series X', 'Nintendo Switch']
}

# Diccionario para mantener consistencia en nombres por user_id
nombres_usuarios = {}

def generar_nombre_usuario(user_id):
    """Genera nombre consistente para cada user_id"""
    if user_id not in nombres_usuarios:
        nombres_usuarios[user_id] = fake.name()
    return nombres_usuarios[user_id]

def generar_dataset(filas=50000):
    data = []
    
    # Definir rango de fechas CORREGIDO
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)  # 1 año atrás
    
    for _ in range(filas):
        user_id = fake.uuid4()
        nombre_cliente = generar_nombre_usuario(user_id)
        session_id = fake.uuid4()
        
        # FECHA CORREGIDA - usando datetime objects
        fecha = fake.date_time_between(start_date=start_date, end_date=end_date)
        
        evento = random.choices(
            ['landing_page', 'product_view', 'add_to_cart', 'checkout', 'purchase'],
            weights=[0.35, 0.25, 0.20, 0.15, 0.05]
        )[0]
        
        device = random.choice(['mobile', 'desktop', 'tablet'])
        country = fake.country()
        time_on_site = random.randint(30, 600)
        
        # Solo asignar producto si el evento es relacionado a producto
        product_id = None
        product_category = None
        producto_nombre = None
        
        if evento in ['product_view', 'add_to_cart', 'purchase']:
            categoria = random.choice(categorias)
            product_id = fake.uuid4()
            product_category = categoria
            producto_nombre = random.choice(productos[categoria])
        
        # Solo asignar valor de compra si es evento de purchase
        purchase_value = round(random.uniform(50, 2000), 2) if evento == 'purchase' else None
        
        data.append([
            user_id, nombre_cliente, session_id, fecha, evento, device, country,
            time_on_site, product_id, product_category, producto_nombre, purchase_value
        ])
    
    return pd.DataFrame(data, columns=[
        'user_id', 'nombre_cliente', 'session_id', 'fecha', 'evento', 'device', 'country',
        'time_on_site', 'product_id', 'product_category', 'producto_nombre', 'purchase_value'
    ])

# Generar el dataset
print("Generando dataset con nombres de clientes...")
df = generar_dataset(50000)

# Mostrar información del dataset
print(f"Dataset generado: {df.shape[0]} filas x {df.shape[1]} columnas")
print(f"Rango de fechas: {df['fecha'].min()} to {df['fecha'].max()}")
print(f"Usuarios únicos: {df['user_id'].nunique()}")
print(f" Países: {df['country'].nunique()}")

print("\nDistribución de eventos:")
print(df['evento'].value_counts())

print("\n Distribución de dispositivos:")
print(df['device'].value_counts())

#  GUARDO EN CSV EL DATASET
def guardar_dataset(df, nombre_archivo='ecommerce_techshop_clientes.csv'):
    """
    Guarda el dataset en formato CSV con configuración óptima
    """
    # Configurar formato de fecha para Power BI
    df['fecha'] = pd.to_datetime(df['fecha'])
    
    # Guardar en CSV
    df.to_csv(nombre_archivo, index=False, encoding='utf-8')
    print(f"\n💾 Dataset guardado como: {nombre_archivo}")
    print(f"📈 Tamaño del archivo: {df.shape[0]} filas")
    
    return nombre_archivo

# Guardar el dataset
archivo_csv = guardar_dataset(df)

#  ANÁLISIS RÁPIDO
print("\n" + "="*50)
print(" ANÁLISIS RÁPIDO DEL DATASET")
print("="*50)

# Tasa de conversión
visitas = df[df['evento'] == 'landing_page']['user_id'].nunique()
compras = df[df['evento'] == 'purchase']['user_id'].nunique()
tasa_conversion = (compras / visitas * 100) if visitas > 0 else 0

print(f" Tasa de conversión: {tasa_conversion:.2f}%")
print(f" Total compras: {compras}")
print(f" Total visitas: {visitas}")

# Top 5 países
print(f"\n Top 5 países por tráfico:")
print(df['country'].value_counts().head(5))

#  EJEMPLO DE DATOS
print(f"\n Ejemplo de datos de un cliente:")
cliente_ejemplo = df['user_id'].iloc[0]
datos_cliente = df[df['user_id'] == cliente_ejemplo]
print(datos_cliente[['nombre_cliente', 'evento', 'device', 'country', 'fecha']].head(3))
