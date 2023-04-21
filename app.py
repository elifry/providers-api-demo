from flask import Flask, request
from flask_restful import Resource, Api
from flask_swagger_ui import get_swaggerui_blueprint
from swagger_ui import api_doc
from provider_collection import ProviderCollection

app = Flask(__name__)
api = Api(app)

# Global instance of ProviderCollection with data from providers.json
provider_collection = ProviderCollection("providers.json")

# Providers resource class for GET /providers endpoint
class Providers(Resource):
    def get(self):
        # Get the query parameters from the request and lowercase them
        active = request.args.get("active")
        if active is not None:
            active = active.lower()
        traits = request.args.get("traits")
        if traits is not None:
            traits = traits.lower()

        # Filter the providers by active if param given
        if active is not None:
            active = active == "true"
            providers = provider_collection.filter_by_active(active)
        
        else:
            providers = provider_collection.providers
        
        # Filter the providers by traits if given - example: trait1:value1|value2,trait2:value1|value2
        if traits is not None:
            # Convert the traits param to a dictionary of lists and lowercase them
            traits_dict = {}
            for trait_list in traits.split(","):
                key, value_list = trait_list.split(":")
                traits_dict[key.lower()] = [value.lower() for value in value_list.split("|")]
            
            providers = provider_collection.filter_by_traits(traits_dict, providers)
        
        # Sort the providers by rating and frequency
        providers = provider_collection.sort_by_rating_and_popularity(providers)

        # Return the providers as a json response with their original values
        return {"providers": list(providers)}

# Add the Providers resource to the api with the /providers endpoint
api.add_resource(Providers, "/providers")

# Add the Swagger UI interface with the /docs endpoint and the swagger.yaml file as config_path 
api_doc(app, config_path="./swagger.yaml", url_prefix="/docs", title="API doc")

SWAGGER_URL = '/docs'
API_URL = './swagger.yaml'

# Call factory function to create our blueprint
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL, # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    API_URL,
)

# Register blueprint at URL
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

if __name__ == "__main__":
    app.run(debug=True)