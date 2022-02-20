import flask
from flask import request, jsonify
from flask import Response

import os
import json
import jsonschema
from jsonschema import validate

from datetime import datetime
from datetime import date

import re


clients = ({'card_number': {
    '4539479713709044': {
        'card_name': 'Jackson Johnson',
        'card_type': 'Visa',
        'card_due_date': '07/2041', 
        'card_cvv': '342',
        'available_limit': 2000,
        'document': '89311417009'},
     '5170904803237193': {
        'card_name': 'Abigail Robinson',
        'card_type': 'MasterCard',
        'card_due_date': '08/2049', 
        'card_cvv': '103',
        'available_limit': 2000,
        'document': '49605107066'},
      '342601535935862': {
        'card_name': 'Dominic Cox',
        'card_type': 'American Express',
        'card_due_date': '08/2049', 
        'card_cvv': '1218',
        'available_limit': 2000,
        'document': '49605107066'}
    }
})


creditCardSchema = {
    "type" : "object",
    "properties" : {
        "integration_key": {"type": "string"},
        "operation": {"type" : "string"},
        "payment": {
            "type": "object",
            "properties" : {
                "name": {"type" : "string"},
                "email": {"type" : "string", "format": "email"},
                "document": {"type" : "string"},
                "address": {"type" : "string"},
                "street_number": {"type" : "string"},
                "city": {"type" : "string"},
                "state": {"type" : "string"},
                "zipcode": {"type" : "string"},
                "country": {"enum": ["br"]},
                "phone_number": {"type" : "string"},
                "payment_type_code": {"type" : "string"},
                "merchant_payment_code": {"type" : "string"},
                "order_number": {"type" : "string"},
                "currency_code": {"enum": ["EUR","BRL","MXN","PEN","USD","CLP","COP","ARS","BOB"]},
                "instalments": {"type" : "integer", "minimum": 0, "maximum" : 12},
                "amount_total": {"type" : "number", "minimum": 0.01},
                "creditcard": {
                    "type" : "object",
                    "properties" : {
                        "card_number": {"type" : "string"},
                        "card_name": {"type" : "string"},
                        "card_due_date": {"type" : "string"},
                        "card_cvv": {"type" : "string"}
                    },
                    "required": ["card_number",
                    "card_name",
                    "card_due_date",
                    "card_cvv"]
                }
            }, "required": ["name", 
             "email", 
             "document",
             "address",
             "street_number",
             "city",
             "state",
             "zipcode",
             "country",
             "payment_type_code",
             "merchant_payment_code",
             "order_number",
             "currency_code",
             "instalments",
             "amount_total",
             "creditcard"
             ]   
        }
    },
    "required": ["integration_key", "operation", "payment"]
}


def validate_credit_card(card_number):
    valid_structure = r"[456]\d{3}(-?\d{4}){3}$"
    no_four_repeats = r"((\d)-?(?!(-?\2){3})){16}"
    filters = valid_structure, no_four_repeats

    if all(re.match(f, card_number) for f in filters):
        print("{card_number} is Valid")
        return True
    else:
        print("{card_number} is Invalid")
        return False


def luhn_checksum(card_number):
    def digits_of(n):
        return [int(d) for d in str(n)]
    digits = digits_of(card_number)
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    checksum = 0
    checksum += sum(odd_digits)
    for d in even_digits:
        checksum += sum(digits_of(d*2))
    check = checksum % 10
    if check == 0:
        return True
    else:
        return False


def validateJson(jsonData):
    try:
        validate(instance=jsonData, schema=creditCardSchema)
    except jsonschema.exceptions.ValidationError as err:
        return False
    return True


def ValidateCreditCardCharge(card_number, card_name, card_due_date, card_cvv, document, amount_total, input_json):
    
    card_number_client = clients['card_number'].get(card_number)

    if card_number_client == None:
        return Response(
        '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">'
        + '<title>400 Bad Request</title><h1>Bad Request</h1>'
        + '<p>Credit Card number informed doesn`t exist</p>',
        status=400)
    else:
        card_name_client = card_number_client['card_name'] 
        card_due_date_client = card_number_client['card_due_date']
        card_cvv_client = card_number_client['card_cvv']
        document_client = card_number_client['document']
        card_name_client = card_number_client['card_name']
        available_limit_client = card_number_client['available_limit']
        card_type_client = card_number_client['available_limit']

        check_name = (card_name_client == card_name)
        check_due_date = (card_due_date_client == card_due_date)
        check_cvv_client = (card_cvv_client == card_cvv)
        check_document_client = (document_client == document)

        if (check_name and check_due_date and check_cvv_client and check_document_client):
            
            # Check if client has enough limit to confirm transaction
            available_limit_client = card_number_client['available_limit']
            print("Available limit: ", available_limit_client)
            print("Value to charge: ", amount_total)

            if (available_limit_client >= amount_total):
                available_limit_client = available_limit_client - amount_total
                
                clients['card_number'][card_number].update({'available_limit':available_limit_client})
                print("Updated limit: ", available_limit_client)

                
                return jsonify({
                            "payment": {
                                "hash": "5ef38bd200a530d9a4c218b054744cb81f9b25c99d4365aa",
                                "pin": "025107300",
                                "country": input_json["payment"]["country"],
                                "merchant_payment_code": input_json["payment"]["merchant_payment_code"],
                                "order_number": input_json["payment"]["order_number"],
                                "status": "CO",
                                "status_date": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                "open_date": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                "confirm_date": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                "transfer_date": datetime.now(),
                                "amount_br": input_json["payment"]["amount_total"],
                                "amount_ext": input_json["payment"]["amount_total"],
                                "amount_iof": 0.38,
                                "amount_ext_requested": input_json["payment"]["amount_total"],
                                "currency_rate": 1.0000,
                                "currency_ext": input_json["payment"]["currency_code"],
                                "due_date": datetime.now().strftime('%Y-%m-%d'),
                                "instalments": input_json["payment"]["instalments"],
                                "payment_type_code": input_json["payment"]["payment_type_code"],
                                "details": {
                                    "billing_descriptor": "DEMONSTRATION"
                                            },
                                "transaction_status": {
                                                        "acquirer": "EBANX",
                                                        "code": "OK",
                                                        "description": "Transaction captured"
                                                        },
                                "pre_approved": True,
                                "capture_available": False,
                            },
                            "status": "SUCCESS"
                        })

            
            else:
                return Response(
                '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">'
                 + '<title>400 Bad Request</title><h1>Bad Request</h1>'
                + '<p>Insufficient credit card limit</p>',
                status=400)


        else:
            print("Validate name: ", check_name)
            print("Validate due date: ", check_due_date)
            print("Validate CVV: ", check_cvv_client)
            print("Validate document: ", check_document_client)

            return Response(
        '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">'
        + '<title>400 Bad Request</title><h1>Bad Request</h1>'
        + '<p>One or more credit card data informed is invalid</p>',
        status=400)


app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def hello_world():
    return 'Hello world'




@app.route('/api/v1/ws/direct', methods=['POST'])
def api_all():
    input_json = request.get_json(force=True)
    

    isValid = validateJson(input_json)
    
    if isValid == False:
        print("Given JSON data is not valid")
        return Response(
        '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">'
        + '<title>400 Bad Request</title><h1>Bad Request</h1>'
        + '<p>Failed to decode JSON object</p>',
        status=400)
    else:
        validate_digits = validate_credit_card(input_json["payment"]["creditcard"]["card_number"])
        validate_luhn = luhn_checksum(input_json["payment"]["creditcard"]["card_number"])

        if(validate_digits == True and validate_luhn == True):
            result = ValidateCreditCardCharge(
                input_json["payment"]["creditcard"]["card_number"], 
                input_json["payment"]["creditcard"]["card_name"], 
                input_json["payment"]["creditcard"]["card_due_date"], 
                input_json["payment"]["creditcard"]["card_cvv"], 
                input_json["payment"]["document"],
                input_json["payment"]["amount_total"],
                input_json)
                            
            return result

        else:
            print("Credit card number is not valid")
            print("Check format: ", validate_digits)
            print("Check Luhn: ", validate_luhn)

            return Response(
            '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">'
            + '<title>400 Bad Request</title><h1>Bad Request</h1>'
            + '<p>Card number is not valid</p>',
        status=400)
    


app.run(host='0.0.0.0')





