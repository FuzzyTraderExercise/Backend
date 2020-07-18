from jsonschema import validate
from jsonschema.exceptions import ValidationError
from jsonschema.exceptions import SchemaError

user_investment_schema = {
    "type": "object",
    "properties": {
        "email": {
            "type": "string",
            "format": "email"
        },
        "stock_name": {
            "type": "string",
        }
    },
    "required": ["email", "stock_name"]
}


def validate_user_investment_json(data):
    try:
        validate(data, user_investment_schema)
    except ValidationError as e:
        return {'valid': False, 'error': e}
    except SchemaError as e:
        return {'valid': False, 'error': e}
    return {'valid': True, 'register': data}
