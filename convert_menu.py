import re
from bs4 import BeautifulSoup

def process_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')

    # Find all items-grid
    grids = soup.find_all('div', class_='items-grid')

    for grid in grids:
        section = grid.find_parent('section')
        section_id = section.get('id') if section else ''
        
        is_tira_gosto = section_id == 'tiragosto'
        
        # Create a new drinks-list div
        drinks_list = soup.new_tag('div', attrs={'class': 'drinks-list'})
        
        if is_tira_gosto:
            # Add table header
            header = soup.new_tag('div', attrs={'class': 'drinks-table-header'})
            
            name_header = soup.new_tag('span', attrs={'class': 'drink-name-header'})
            header.append(name_header)
            
            for col in ['P', 'M', 'G']:
                col_header = soup.new_tag('span', attrs={'class': 'drink-col-header'})
                col_header.string = col
                header.append(col_header)
                
            drinks_list.append(header)
            
        items = grid.find_all('div', class_=re.compile(r'\bmenu-item\b'))
        
        for item in items:
            info = item.find('div', class_='item-info')
            name_tag = info.find('h3')
            name = name_tag.get_text(strip=True) if name_tag else ''
            
            desc_tag = info.find('p')
            desc = desc_tag.get_text(strip=True) if desc_tag else ''
            
            price_tag = item.find('div', class_='item-price')
            price_text = price_tag.get_text(strip=True) if price_tag else ''
            
            if is_tira_gosto:
                # Parse multiple prices
                # e.g., "R$ 18 (P) | R$ 22 (M) | R$ 26 (G)"
                # or "R$ 10 (P)"
                prices = {'P': '-', 'M': '-', 'G': '-'}
                
                parts = price_text.split('|')
                for part in parts:
                    part = part.strip()
                    if '(P)' in part:
                        prices['P'] = part.replace('(P)', '').strip()
                    elif '(M)' in part:
                        prices['M'] = part.replace('(M)', '').strip()
                    elif '(G)' in part:
                        prices['G'] = part.replace('(G)', '').strip()
                
                row = soup.new_tag('div', attrs={'class': 'drink-row-multi'})
                
                name_span = soup.new_tag('span', attrs={'class': 'drink-name'})
                name_span.string = name
                row.append(name_span)
                
                dots_span = soup.new_tag('span', attrs={'class': 'drink-dots'})
                row.append(dots_span)
                
                for col in ['P', 'M', 'G']:
                    price_span = soup.new_tag('span', attrs={'class': 'drink-price-col'})
                    price_span.string = prices[col]
                    row.append(price_span)
                    
                drinks_list.append(row)
                
                if desc:
                    desc_div = soup.new_tag('div', attrs={'class': 'drink-desc'})
                    desc_div.string = desc
                    drinks_list.append(desc_div)
            else:
                # Single price
                row = soup.new_tag('div', attrs={'class': 'drink-row'})
                if desc:
                    row['style'] = 'margin-top: 10px;'
                
                name_span = soup.new_tag('span', attrs={'class': 'drink-name'})
                name_span.string = name
                row.append(name_span)
                
                dots_span = soup.new_tag('span', attrs={'class': 'drink-dots'})
                row.append(dots_span)
                
                price_span = soup.new_tag('span', attrs={'class': 'drink-price'})
                price_span.string = price_text
                row.append(price_span)
                
                drinks_list.append(row)
                
                if desc:
                    desc_div = soup.new_tag('div', attrs={'class': 'drink-desc'})
                    desc_div.string = desc
                    drinks_list.append(desc_div)
                    
        grid.replace_with(drinks_list)

    with open(file_path, 'w', encoding='utf-8') as f:
        # Use html.parser but keep formatting somewhat nice
        f.write(str(soup))

if __name__ == "__main__":
    process_html(r'c:\Users\Paybrokers\Documents\PitStop\index.html')
