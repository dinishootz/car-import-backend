def extract_mobile_de_data(url):
    """Extrai dados do Mobile.de de forma mais segura"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept-Language': 'de-DE,de;q=0.9,en;q=0.8',
        'Referer': 'https://www.google.com/',
        'DNT': '1',
        'Connection': 'keep-alive'
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        return {'error': 'Falha ao carregar a página'}
    
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extrair título
    title = soup.find('h1')
    title_text = title.text.strip() if title else 'Título não encontrado'

    # Extrair preço (ajustado para formatos diferentes)
    price_match = soup.find(string=re.compile(r'€'))
    price = price_match.strip() if price_match else 'Preço não encontrado'

    # Extrair ano de fabrico
    year_match = re.search(r'\\b(19|20)\\d{2}\\b', response.text)
    year = year_match.group(0) if year_match else 'Ano não encontrado'

    # Extrair emissões de CO2
    co2_match = re.search(r'(\\d{2,3})\\s*g/km', response.text)
    co2 = co2_match.group(0) if co2_match else 'CO₂ não encontrado'

    return {
        'title': title_text,
        'price': price,
        'year': year,
        'co2': co2
    }
