import os
import json
from flask import request, jsonify, make_response

'''
This purpose of this module is to ease the integration of Dash with dataiku. To create a Dash app, create a standard 
web app. Clear the HTML tab and paste the following boiler plate code in the JS tab,

/*
Plotly Dash integration boiler plate code.
*/
window.onload = function() {
    // setup url for application end point
    const appPrefix = 'dash'
    const appUrl = getWebAppBackendUrl('/' + appPrefix + '/')
    // setup url for app configuration
    const configUrl = getWebAppBackendUrl('/configure')
    const args = '?webAppBackendUrl=' + encodeURIComponent(getWebAppBackendUrl('/')) + '&appPrefix=' + appPrefix;
    // do the magic
    fetch( configUrl + args )
   .then(async r=> {
       const json = await r.json()
       // if there is no error, redirect to Dash app
       if (!json.error) {
           location.replace(appUrl)
       }
       // otherwise, output the error to the page
       else {
           document.write(json.error);
       }
   }).catch(e=>console.error('Boo...' + e));
}

Next, go to the Python tab and create the Dash application,

# Path for storing app configuration (must be writeable).
config_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "config.json")
# Create a small example app.
dash_app = dash.Dash(__name__, **setup_dataiku(app, config_path))
dash_app.layout = html.Div("Hello from Dash!")

'''


def parse_config(args):
    return {'webAppBackendUrl': args.get('webAppBackendUrl'), 'appPrefix': args.get('appPrefix')}


def get_dataiku_kwargs(server, config_path):
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        app_prefix = config['appPrefix']
        web_app_backend_url = config['webAppBackendUrl']
        return {
            'server': server,
            'routes_pathname_prefix': f'/{app_prefix}/',
            'requests_pathname_prefix': f"{web_app_backend_url}{app_prefix}/"
        }
    except FileNotFoundError:
        return {'server': server}


def setup_dataiku(server, config_path):
    # Add config route.
    @server.route("/configure")
    def configure():
        config = parse_config(request.args)
        # Check if the configuration has changed.
        if os.path.isfile(config_path):
            with open(config_path, 'r') as f:
                current_config = json.load(f)
            # Configuration has not changed, redirect to app.
            if config == current_config:
                return jsonify(success=True)
        # Configuration changed. Write new config and ask for restart.
        with open(config_path, 'w') as f:
            json.dump(config, f)
        return make_response(jsonify({'error': 'Configuration changed. Backend restart required.'}), 500)

    # Return keyword arguments.
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        app_prefix = config['appPrefix']
        web_app_backend_url = config['webAppBackendUrl']
        return {
            'server': server,
            'routes_pathname_prefix': f'/{app_prefix}/',
            'requests_pathname_prefix': f"{web_app_backend_url}{app_prefix}/"
        }
    except FileNotFoundError:
        return {'server': server}
