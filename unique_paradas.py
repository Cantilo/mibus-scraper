import json

if __name__ == '__main__':
    with open('paradas.json', 'r', encoding='utf8') as f:
        paradas: list[dict] = json.load(f)

    seen = set()
    unique_paradas = []
    for p in paradas:
        if not p['id_code'] in seen:
            seen.add(p['id_code'])
            unique_paradas.append(p)

    print('Total de paradas:', len(unique_paradas))
    with open('unique_paradas.json', 'w', encoding='utf8') as f:
        json.dump(unique_paradas, f)
