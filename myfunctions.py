import requests

def get_real_aqi(city_name):
    token = "a38fc3b0502f61b13040af3ba6e8b80a00233362"
    url = f"https://api.waqi.info/feed/{city_name}/?token={token}"

    response = requests.get(url)
    json_data = response.json()
    real_aqi = int(json_data['data']['aqi'])
    return real_aqi

def aqi_category(aqi):
    if aqi <= 50:
        return 'Bon','like.png','green'
    elif aqi <= 100:
        return 'Modere','mark.png', '#ffc300'
    elif aqi <= 150:
        return 'malsain','sick.png', 'orange'
    elif aqi <= 200:
        return 'Mauvais','bad.png', 'red'
    elif aqi <= 300:
        return 'Tres mauvais','alarm.png', 'purple'
    else:
        return 'Dangereux','sign.png', 'maroon'

def get_polluant_description(polluant):
    description = {
        'co' : "Monoxyde de carbone. Un gaz toxique émis par les combustions incomplètes de carburants fossiles. Il interfère avec la capacité du sang à transporter l'oxygène.",
        'pm10' : "Particules en suspension d'un diamètre de 10 micromètres ou moins. Elles peuvent pénétrer les voies respiratoires supérieures et provoquer des problèmes respiratoires.",
        'o3' : "Ozone troposphérique. Un polluant secondaire formé par des réactions chimiques entre les oxydes d'azote (NOx) et les composés organiques volatils (COV) sous l'effet de la lumière solaire. Peut causer des problèmes respiratoires.",
        'so2' : "Dioxyde de soufre. Émis principalement par les processus de combustion de combustibles fossiles et les activités industrielles. Peut causer des irritations des voies respiratoires et aggraver les maladies pulmonaires.",
        'no2' : "Dioxyde d'azote. Produit par les émissions des véhicules et les processus industriels. Peut causer des irritations des voies respiratoires et affecter la santé pulmonaire.",
        'pm25' : "Particules en suspension d'un diamètre de 2.5 micromètres ou moins. Elles peuvent pénétrer profondément dans les poumons et provoquer des problèmes cardiovasculaires et respiratoires."
    }
    
    return description.get(polluant)

def get_city_description(city):
    description = {
        "Beijing": "**Chine** : Niveau élevé de pollution atmosphérique, surtout en hiver.",
        "Delhi": "**Inde** : Connu pour ses niveaux de pollution alarmants.",
        "Tokyo": "**Japon** : Grandes variations de pollution et politiques environnementales strictes.",
        "São Paulo" : "**Brésil** : Pollution due au trafic et à l'industrie.",
        "Santiago" : "**Chili** : Pollution atmosphérique surtout en hiver.",
        "Abidjan" : "**Côte d'Ivoire** : Ville en pleine expansion avec des niveaux de pollution croissants.",
        "Accra" : "**Ghana** : Ville en pleine expansion avec des niveaux de pollution croissants.",
        "Johannesburg" : "**Afrique du Sud** : Niveaux de pollution dus à l'industrie et au trafic.",
        "Londres" : "**Royaume-Uni** : Historique de pollution importante et mesures de réduction en cours.",
        "Paris" : "**France** : Pollution due au trafic et politiques environnementales en place.",
        "Milan" : "**Italie** : Élevé niveaux de pollution atmosphérique, notamment en hiver.",
        "Los Angeles" : "**États-Unis** : Connu pour ses problèmes de smog et de pollution atmosphérique."
    }
    return description.get(city)

country_iso_alpha_3 = {
    'Brazil': 'BRA',
    'Chile': 'CHL',
    'China': 'CHN',
    'France': 'FRA',
    'United Kingdom': 'GBR',
    'India': 'IND',
    'Italy': 'ITA',
    'Japan': 'JPN',
    'United States': 'USA',
    'South Africa': 'ZAF',
    "Côte d'Ivoire": 'CIV',
    'Ghana': 'GHA'
    }
meteo_dict = {
    'temperature': 'temperature',
    'humidité': 'humidity',
    'présion atmospherique': 'pressure'
}
    
