# Geolocation API

This repository contains a Geolocation API built with Flask. It allows users to input an IP address and retrieve geolocation information including country, city, coordinates, and more.

## Technologies Used

- Framework: [Flask](https://flask.palletsprojects.com/)
- Database: [MaxMind GeoLite2](https://dev.maxmind.com/geoip/geoip2/geolite2/) (Free IP geolocation database)

## Features

### IP Geolocation
- Users can input an IP address to retrieve detailed geolocation information.
- Provides country, city, latitude, longitude, timezone, and more.

### Automatic Database Updates
- Automatically downloads and updates the GeoLite2 database at startup.

### UN Geoscheme Integration
- Includes subregion information based on the UN geoscheme. (Source: https://unstats.un.org/unsd/methodology/m49/overview/)

## Requirements

To run and use the Geolocation API, you need the following:

- Python 3.7+
- Flask
- geoip2
- requests
- beautifulsoup4

## Usage

1. Clone this repository.
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Sign up on MaxMind for your GeoLite2 access/account. (https://www.maxmind.com/en/geolite2/signup)
4. Create your MaxMind license key and download the config. (Get it from here: https://www.maxmind.com/en/accounts/XXXXXXX/license-key)
5. Ensure you have the valid MaxMind config at `config/GeoIP.conf`.
6. Run the application:
```bash
   python app.py
```
5. Make a GET request to `http://127.0.0.1:5000/geolocate?ip=<IP_ADDRESS>` to retrieve geolocation data.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. [Maciej Kula](https://github.com/mcjkula).
