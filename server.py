def extract_olx_data(url):
    """Extrai dados de um anúncio no OLX.pt"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept-Language': 'pt-PT,pt;q=0.9,en;q=0.8',
        'Referer': 'https://www.google.com/',
        'DNT': '1',
        'Connection': 'keep-alive'
    }

    try:
        session = requests.Session()
        session.headers.update(headers)
        
        response = session.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Gera erro se o status não for 200

    except requests.exceptions.RequestException as e:
        return {'error': f'Erro ao carregar a página: {str(e)}'}

    soup = BeautifulSoup(response.text, 'html.parser')

    try:
        # Título do anúncio
        title = soup.find("h1")
        title_text = title.text.strip() if title else 'Título não encontrado'

        # Preço do carro
        price_tag = soup.find("h3", class_=re.compile("css-.*"))  # Adaptar para a classe correta
        price = price_tag.text.strip() if price_tag else 'Preço não encontrado'

        # Ano do carro
        year_tag = soup.find("p", string=re.compile(r"(\b19|\b20)\d{2}"))
        year = year_tag.text.strip() if year_tag else 'Ano não encontrado'

        # Quilometragem
        km_tag = soup.find("p", string=re.compile(r"\d{1,3}(?:\.\d{3})* km"))
        km = km_tag.text.strip() if km_tag else 'Quilometragem não encontrada'

    except Exception as e:
        return {'error': f'Erro ao processar os dados: {str(e)}'}

    return {
        'title': title_text,
        'price': price,
        'year': year,
        'kilometers': km
    }

@app.get("/analyze")
def analyze_car(url: str):
    """Extrai dados de um carro a partir do OLX.pt"""
    try:
        car_data = extract_olx_data(url)
        return car_data
    except Exception as e:
        return {"error": f"Erro interno: {str(e)}"}
