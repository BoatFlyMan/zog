"""
python -m cog.command.specification

This prints a JSON object describing the inputs of the model.
"""
import json

from ..errors import ConfigDoesNotExist, PredictorNotSet
from ..suppress_output import suppress_output

from ..predictor import get_predictor_ref, load_config
from ..server.http import create_app

if __name__ == "__main__":
    schema = {}
    try:
        with suppress_output():
            config = load_config()
            predictor_ref = get_predictor_ref(config)
    except (ConfigDoesNotExist, PredictorNotSet):
        # If there is no cog.yaml or 'predict' has not been set, then there is no type signature.
        # Not an error, there just isn't anything.
        pass
    else:
        with suppress_output():
            app = create_app(predictor_ref, shutdown_event=None)
        schema = app.openapi()
    print(json.dumps(schema, indent=2))
