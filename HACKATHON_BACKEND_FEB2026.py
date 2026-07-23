from flask import Flask, render_template
from flask_cors import CORS
import requests

app=Flask(__name__)
CORS(app)

# boh configurato impianto a caso
MQ_PANNELLI = 15
EFFICIENZA = 0.18

ELETTRODOMESTICI = [
    {"id": 1, "nome": "Lavatrice", "watt": 2000, "durata": 2},
    {"id": 2, "nome": "Asciugatrice", "watt": 2500, "durata": 1.5},
    {"id": 3, "nome": "Lavastoviglie", "watt": 1500, "durata": 2},
    {"id": 4, "nome": "Frigorifero", "watt": 150, "durata": 24},
    {"id": 5, "nome": "Condizionatore", "watt": 1200, "durata": 5},
    {"id": 6, "nome": "Congelatore", "watt": 200, "durata": 24}
]



def aggiungi_dispositivo(nome, watt, durata):

    nuovo = {"id": len(ELETTRODOMESTICI) + 1, "nome": nome, "watt": int(watt), "durata": float(durata)}
    ELETTRODOMESTICI.append(nuovo)

def calcola_storico_30gg():

    url = "https://archive-api.open-meteo.com/v1/archive?latitude=45.46&longitude=9.19&start_date=2026-01-01&end_date=2026-01-30&hourly=shortwave_radiation,weather_code"
    res = requests.get(url).json()
    
    mapping = {0: "Sole", 1: "Poco Nuvoloso", 3: "Nuvoloso", 61: "Pioggia", 71: "Neve"}
    storico_completo = {}

    for h, rad, code in zip(res['hourly']['time'], res['hourly']['shortwave_radiation'], res['hourly']['weather_code']):
        giorno = h.split("T")[0]
        if giorno not in storico_completo:
            storico_completo[giorno] = {"picco": 0, "totale_w": 0, "meteo": mapping.get(code, "Variabile")}
        
        storico_completo[giorno]["picco"] = max(storico_completo[giorno]["picco"], rad)
        storico_completo[giorno]["totale_w"] += round(rad * MQ_PANNELLI * EFFICIENZA)
    
    return [{"giorno": g, **info} for g, info in storico_completo.items()]

def ottimizza_planner():
    """ncrocia previsioni meteo e consumi per il calendario"""
    url = "https://api.open-meteo.com/v1/forecast?latitude=45.46&longitude=9.19&hourly=shortwave_radiation"
    previsioni = requests.get(url).json()
    
    #filtro ore di luce
    ore_luce = []
    for h, rad in zip(previsioni['hourly']['time'], previsioni['hourly']['shortwave_radiation']):
        if rad > 0:
            ore_luce.append({"ora": h, "prod": rad * MQ_PANNELLI * EFFICIENZA})
    
    ore_top = sorted(ore_luce, key=lambda x: x['prod'], reverse=True)
    elettro_top = sorted([e for e in ELETTRODOMESTICI if e['durata'] < 24], key=lambda x: x['watt'], reverse=True)

    # Matching: Elettrodomestico pesante -> Ora più potente
    return [{"dispositivo": e['nome'], "consiglio": o['ora'], "resa": round(o['prod'])} 
            for e, o in zip(elettro_top, ore_top)]

# grafico_per_jasky = calcola_storico_30gg()
# planner_per_jasky = ottimizza_planner()
# elettrodomestici_per_jasky = ELETTRODOMESTICI

@app.route('/planner')
def home():
    # exe reale
    grafico = calcola_storico_30gg()
    planner = ottimizza_planner()
    
    # questo passa le 3 variabili a jasky sito
    return render_template('smart-solar-planner.html', 
                           storico=grafico, 
                           consigli=planner, 
                           dispositivi=ELETTRODOMESTICI)

if __name__ == '__main__':
    app.run(debug=True)
