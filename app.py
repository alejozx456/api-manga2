from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup

# # URL de la página que vamos a scrapear
# url = 'https://visortmo.com/library/manga/55644/tsuetotsuruginowistoria';
# headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}# Reemplaza con la URL real

# session=requests.Session();

# # Hacer la solicitud HTTP
# response = session.get(url,headers=headers)

# # Verificamos que la solicitud fue exitosa
# if response.status_code == 200:
#     # Parsear el contenido HTML
#     soup = BeautifulSoup(response.content, 'html.parser')
    
#     # Seleccionar todos los elementos con la clase 'upload-link'
#     nodos = soup.select('.upload-link')
    
#     # Extraer el texto de los enlaces dentro de esos nodos
#     capitulos = [nodo.select_one('a').get_text() for nodo in nodos if nodo.select_one('a')]
    
#     # Imprimir los capítulos
#     print(capitulos)
#     print(len(capitulos))
# else:
#     print(f'Error al acceder a la página: {response.status_code}')

app = Flask(__name__)
CORS(app)

@app.route('/scrape', methods=['POST'])  # Cambiado a POST
def scrape():
    data = request.json  # Obtener el cuerpo de la solicitud como JSON
    url = data.get('url')  # Obtener la URL del JSON
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, como Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    session = requests.Session()

    try:
        response = session.get(url, headers=headers)
        response.raise_for_status()  # Lanza un error si la respuesta no es 200

        soup = BeautifulSoup(response.content, 'html.parser')
        nodos = soup.select('.upload-link')
        capitulos = [nodo.select_one('a').get_text() for nodo in nodos if nodo.select_one('a')]
        
        return jsonify({'capitulos': capitulos, 'total': len(capitulos)})

    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Error al acceder a la página: {str(e)}'}), 500

    except Exception as e:
        return jsonify({'error': f'Ocurrió un error inesperado: {str(e)}'}), 500

if __name__ == '__main__':
    #app.run(debug=True)
    app.run(host='0.0.0.0', port=5000, debug=True)