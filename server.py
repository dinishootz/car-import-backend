import os

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
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept-Language': 'de-DE,de;q=0.9,en;q=0.8',
        'Referer': 'https://www.google.com/',
        'DNT': '1',
        'Connection': 'keep-alive'
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return {'error': f'Erro ao carregar a página: {str(e)}'}

    soup = BeautifulSoup(response.text, 'html.parser')

    try:
        title = soup.find('h1')
        title_text = title.text.strip() if title else 'Título não encontrado'

        price_match = soup.find(string=re.compile(r'€'))
        price = price_match.strip() if price_match else 'Preço não encontrado'

        year_match = re.search(r'\\b(19|20)\\d{2}\\b', response.text)
        year = year_match.group(0) if year_match else 'Ano não encontrado'

        co2_match = re.search(r'(\\d{2,3})\\s*g/km', response.text)
        co2 = co2_match.group(0) if co2_match else 'CO₂ não encontrado'
    
    except Exception as e:
        return {'error': f'Erro ao processar os dados: {str(e)}'}

    return {
        'title': title_text,
        'price': price,
        'year': year,
        'co2': co2
    }

@app.get("/analyze")
def analyze_car(url: str):
    car_data = extract_mobile_de_data(url)
    if 'error' in car_data:
        return car_data

    transport_cost = 1000

    isv = 5000 if int(car_data['co2'].split()[0]) > 120 else 2500

    total_import_cost = transport_cost + isv
    car_data['total_import_cost'] = total_import_cost

    return car_data

# 🔥 Adiciona isto no final do ficheiro 🔥
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
