from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup
import re
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Permitir chamadas do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "API de Importação de Carros - Online"}

def extract_mobile_de_data(url):
    """Extrai dados do Mobile.de"""
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        title = soup.find('h1').text.strip() if soup.find('h1') else 'Sem título'
        price = re.search(r'\\d{1,3}(?:\\.\\d{3})*,\\d{2}', response.text)
        year = re.search(r'\\b(19|20)\\d{2}\\b', response.text)
        co2 = re.search(r'(\\d{2,3})\\s*g/km', response.text)
        
        return {
            'title': title,
            'price': price.group(0) if price else 'Sem preço',
            'year': year.group(0) if year else 'Sem ano',
            'co2': co2.group(0) if co2 else 'Sem dados de CO₂'
        }
    else:
        return {'error': 'Erro ao obter dados'}

@app.get("/analyze")
def analyze_car(url: str):
    car_data = extract_mobile_de_data(url)
    if 'error' in car_data:
        return car_data
    
    # Custo fixo de transporte
    transport_cost = 1000
    
    # Cálculo do ISV (simples, pode ser melhorado)
    isv = 5000 if int(car_data['co2'].split()[0]) > 120 else 2500
    
    total_import_cost = transport_cost + isv
    car_data['total_import_cost'] = total_import_cost
    
    return car_data
