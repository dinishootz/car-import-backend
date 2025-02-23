def extract_auto1_data(url):
    """Extrai dados do Auto1.com"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept-Language': 'de-DE,de;q=0.9,en;q=0.8',
        'Referer': 'https://www.google.com/',
        'DNT': '1',
        'Connection': 'keep-alive'
    }

    try:
        session = requests.Session()
        session.headers.update(headers)
        
        response = session.get(url, headers=headers, timeout=10)
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

        km_match = re.search(r'\\d{1,3}(?:\\.\\d{3})* km', response.text)
        km = km_match.group(0) if km_match else 'Quilometragem não encontrada'

    except Exception as e:
        return {'error': f'Erro ao processar os dados: {str(e)}'}

    return {
        'title': title_text,
        'price': price,
        'year': year,
        'kilometers': km
    }
