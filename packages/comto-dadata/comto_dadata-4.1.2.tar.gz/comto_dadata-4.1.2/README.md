# DaData Commercito
Пакет для работы с сервисом "[dadata.ru](https://dadata.ru/ "Информация о клиентах и контрагентах")".  
Его удобно использовать совместно с пакетом "[comto-core](https://pypi.org/project/comto-core/ "Набор полезных функций для повседневной работы")".

## Использование

### Поиск адресов
```python
from comto_dadata import address

token = 'your-token'
secret = 'your-secret'

print(address.suggest(token, 'москва твер'))
print(address.geocoding(token, secret, "москва сухонская 11"))
print(address.geocoding_reverse(token, '55.878', '37.653'))
print(address.by_ip(token, '46.226.227.20'))
print(address.by_fias(token, '9120b43f-2fae-4838-a144-85e43c2bfb29'))
print(address.postal_unit(token, 'дежнева 2а'))
print(address.delivery_uid(token, '3100400100000'))
print(address.dict_by_fias(token, '9120b43f-2fae-4838-a144-85e43c2bfb29'))
print(address.country(token, 'DE'))
```

### Поиск компаний
```python
from comto_dadata import company

payload = {
    'query': 'Иванов Александр',
    'count': 20,
    'status': ["ACTIVE"],
    'locations': [{"kladr_id": "1300000100000"}],
}

response = company.suggest('your-token', payload)
```

### Справочники

```python
from comto_dadata import handbook

okved = handbook.okved('your-token', '51.22.3')
okpd = handbook.okpd('your-token', '95.23.10.133')
```

### Личный кабинет

```python
from comto_dadata import profile

stat = profile.stat('your-token', 'your-secret')
balance = profile.balance('your-token', 'your-secret')
version = profile.version('your-token')
```

### Парсинг ответа сервиса

#### А. Поиск компании

```python
import json
from comto_dadata import company
from comto_dadata import parse

response = company.by_inn('your-token', '1327048147')
response = json.loads(response)

items = response.get('suggestions')

if len(items):
    for item in items:
        person = parse.company(item)
        print(person)
```

Пример результата парсинга ответа

```json
{
  "inn": "1327048147",
  "fio": "Иванов Иван Иванович",
  "type": "LEGAL",
  "name": "ПУБЛИЧНОЕ АКЦИОНЕРНОЕ ОБЩЕСТВО \"ЗАСТРОЙЩИК \"ДОМОСТРОИТЕЛЬНЫЙ КОМБИНАТ\"",
  "district": "Приволжский",
  "region": "Респ Мордовия",
  "kladr_region": "1300000000000",
  "city": "г Саранск",
  "kladr_city": "1300000100000",
  "employee": 78,
  "okved": "41.20",
  "okveds": "41.20, 01.41, ..., 85.42"
}
```

#### Б. Поиск адреса

```python
import json
from comto_dadata import address
from comto_dadata import parse

# search = 'г Ярославль, ул Гагарина, д 12'
search = 'Ярославская обл, деревня Кузнечиха, ул Центральная, д 37'

response = address.suggest('your-token', search)
response = json.loads(response)

items = response.get('suggestions')

if len(items):
    for item in items:
        place = parse.address(item)
        print(place)
```

Пример результата парсинга ответа

```json
{
  "address_full": "150023, Ярославская обл, г Ярославль, ул Гагарина, д 12",
  "geo_lat": "57.588718",
  "geo_lon": "39.844613",
  "postal_code": "150023",
  "federal_district": "Центральный",
  "region_fias_id": "a84b2ef4-db03-474b-b552-6229e801ae9b",
  "region_kladr_id": "7600000000000",
  "place_fias_id": "6b1bab7d-ee45-4168-a2a6-4ce2880d90d3",
  "place_kladr_id": "7600000100000",
  "street_fias_id": "b53a43d6-5cea-448c-bc2b-e360a8561ae0",
  "street_kladr_id": "76000001000014700",
  "house_fias_id": "f30de2da-9115-4eef-a887-0ea1b6d34ff2",
  "house_kladr_id": "7600000100001470030",
  "fias_id": "f30de2da-9115-4eef-a887-0ea1b6d34ff2",
  "fias_code": "76000001000000001470030",
  "kladr_id": "7600000100001470030"
}
```