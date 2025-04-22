from twilio.rest import Client

class SMSService:
    def send(self, user_id, message):
        user_phone = self._get_user_phone(user_id)
        client = Client()
        message = client.messages.create(body=message, from_="+1234567890", to=user_phone)
        return message.sid

    def _get_user_phone(self, user_id):
        return "+19876543210"
