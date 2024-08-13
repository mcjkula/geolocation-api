from flask import Flask, request, jsonify
import geoip2.database
from utils.geoip import update_geoip_database_if_needed, start_periodic_update, get_geoip_db_path
from utils.un_geoscheme import get_un_geoscheme, get_subregion

app = Flask(__name__)

update_geoip_database_if_needed()

start_periodic_update()

@app.route('/geolocate', methods=['GET'])
def geolocate():
    ip_address = request.args.get('ip')
    if not ip_address:
        return jsonify({'error': 'No IP address provided'}), 400

    geoip_db_path = get_geoip_db_path()

    try:
        with geoip2.database.Reader(geoip_db_path) as reader:
            response = reader.city(ip_address)
            un_geoscheme = get_un_geoscheme()
            subregion = get_subregion(response.country.iso_code, un_geoscheme)
            
            return jsonify({
                'ip': ip_address,
                'country': response.country.name,
                'country_code': response.country.iso_code,
                'subregion': subregion,
                'city': response.city.name,
                'postal_code': response.postal.code,
                'latitude': response.location.latitude,
                'longitude': response.location.longitude,
                'timezone': response.location.time_zone
            })
    except geoip2.errors.AddressNotFoundError:
        return jsonify({'error': 'IP address not found in the database'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
