from flask import Flask, request
import requests
import json


app = Flask(__name__)


@app.route("/saludar", methods=["GET"])
def saludar():
    return "hola Mundo"


@app.route("/whatsapp", methods=["GET"])
def VerifyToken():
    try:

        access_token = "myaccesstokensecret"
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")

        if token == access_token:
            return challenge
        else:
            return "error", 400
    except:
        return "error", 400


@app.route("/whatsapp", methods=["POST"])
def ReceivedMessage():

    try:

        body = request.get_json()
        entry = body["entry"][0]
        changes = entry["changes"][0]
        value = changes['value']
        messages = value["messages"][0]
        text = messages['text']
        question_user = text["body"]
        number = messages["from"]

        print(
            f"este es el mensaje recivido {question_user} del numero {number}")

        body_answer = sendMessages(question_user, number)
        send_message = whatsappService(body_answer)

        if send_message:
            print("Mensaje enviado Correctamente")

        else:
            print("error al envio del mensaje")
        return "EVENT_RECEIVED"
    except Exception as e:
        print(e)
        return "EVENT_RECEIVED"


def whatsappService(body):
    try:
        token = "EAAtb0ayuxWgBO6u9FHbZAUE6rNrfRKHUHXrqpYJp8YuSYgXtQrCT1ueqZBZBFhkZCvZC0o7nTmOfutFZB04fw7FeeMDFgbTctCvKGPikhOe20OOwQuNGPPRiju0hZBdjoi19ZAf5kT3CsgDAO6ZA6hZC10c5OsWo3QF4jQOIO7b0tMXIhhZCccIjHpcPC7GacZC0ZCwQszmdD4ByNjrIwMTgZD"
        api_url = "https://graph.facebook.com/v18.0/137846966084180/messages"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }

        response = requests.post(api_url,
                                 data=json.dumps(body),
                                 headers=headers)

        if response.status_code == 200:

            return True
        else:

            return False

    except Exception as e:
        print(e)
        return False


def sendMessages(text, number):

    body = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": number,
        "type": "text",
        "text": {

            "body": "Este es la Respuesta a la pregunta: " + text
        }
    }

    return body


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8501, debug=True)
