def extract_mobile_de_data(url):
    """Extrai dados do Mobile.de de forma segura"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept-Language': 'de-DE,de;q=0.9,en;q=0.8',
        'Referer': 'https://www.google.com/',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
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
