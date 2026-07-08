import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import *

from asgiref.sync import sync_to_async
from django.conf import settings
from google import genai
#from google.genai.errors import ClientError


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data["message"]
        name = data.get("name", "Anonymous")

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "name": name,
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "name": event["name"],
            "message": event["message"],
        }))


class GeminiConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

        #testing
        self.gemini_client = genai.Client(
            #api_key="AIzaSyAfmAj6DwmZsg00p9nH3Jozh2Kat11OxEI"
            api_key="AIzaSyC50EQPTY7QYDOlXwehm3Ss_jlJzQLY46A"
        )

        await self.send(json.dumps({
            "status": "connected",
            "message": "Hello"
        }))

    async def receive(self, text_data):
        data = json.loads(text_data)
        chat_mode = data.get("chat_mode")

        #Compare
        if chat_mode == "Compare":
            doc_a_id = data.get("doc_a_id")
            doc_b_id = data.get("doc_b_id")

            #if not doc_a_id or not doc_b_id:
            #    await self.send(json.dumps({
            #        "error": "doc_a_id and doc_b_id are required for Compare mode"
            #    }))
            #    return

            text_a, text_b = await self.get_documents(doc_a_id, doc_b_id)
            subject_a = await self.get_subject(doc_a_id)
            subject_b = await self.get_subject(doc_b_id)
            response = await sync_to_async(self.compare_documents)(text_a, text_b, subject_a, subject_b)

            await self.send(json.dumps({
                "name": "QCRBAI",
                "mode": "Compare",
                "message": response
            }))
            return

        #Summarize
        if chat_mode == "Summarize":
            doc_a_id = data.get("doc_a_id")
            #doc_b_id = data.get("doc_b_id")

            #if not doc_a_id or not doc_b_id:
            #    await self.send(json.dumps({
            #        "error": "doc_a_id and doc_b_id are required for Compare mode"
            #    }))
            #    return

            text_a = await self.get_single_documents(doc_a_id)
            subject_a = await self.get_subject(doc_a_id)
            response = await sync_to_async(self.summarize_documents)(text_a, subject_a)

            await self.send(json.dumps({
                "name": "QCRBAI",
                "mode": "Summarize",
                "message": response
            }))
            return

        #Interact
        if chat_mode == "Interact":
            message = data.get("message")

            if not message:
                await self.send(json.dumps({
                    "error": "message is required for Interact mode"
                }))
                return

            response = await sync_to_async(self.ask_gemini)(message)

            await self.send(json.dumps({
                "name": "QCRBAI",
                "mode": "Interact",
                "message": response
            }))
            return

        #UNKNOWN
        await self.send(json.dumps({
            "error": "Invalid chat_mode. Use Compare or Interact."
        }))

    # ---------- Helpers ----------

    @sync_to_async
    def get_documents(self, doc_a_id, doc_b_id):
        doc_a = DocumentFile.objects.get(id=doc_a_id)
        doc_b = DocumentFile.objects.get(id=doc_b_id)
        return doc_a.content_text, doc_b.content_text
    
    @sync_to_async
    def get_single_documents(self, doc_a_id):
        doc_a = DocumentFile.objects.get(id=doc_a_id)
        return doc_a.content_text

    @sync_to_async
    def get_subject(self, selected_id):
        subject = DocumentFile.objects.get(id=selected_id)
        return subject.subject + '(' + subject.board_resolution_number + ')'

    def compare_documents(self, text_a, text_b, subject_a, subject_b):
        prompt = f"""
        You are a document comparison assistant.

        Compare Document {subject_a} and Document {subject_b}.

        Return:
        1. Summary of differences
        2. Added content
        3. Removed content
        4. Modified content

        Document: {text_a}
        

        Document B: {text_b}
        """

        response = self.gemini_client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=prompt
        )
        return response.text

    def summarize_documents(self, text_a, subject_a):
        prompt = f"""
        You are a document summarize assistant.

        Summarize Document {subject_a}.

        Return:
        1. Summary
        2. Important content

        Document: {text_a}

        """

        response = self.gemini_client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=prompt
        )
        return response.text

    def ask_gemini(self, message):
        response = self.gemini_client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=message
        )
        return response.text
        











"""
class GeminiConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        await self.accept()

        # Initialize Gemini client ONCE per connection
        self.gemini_client = genai.Client(
            api_key='AIzaSyAfmAj6DwmZsg00p9nH3Jozh2Kat11OxEI'
        )
        #client = genai.Client(api_key='AIzaSyAfmAj6DwmZsg00p9nH3Jozh2Kat11OxEI')

        await self.send(json.dumps({
            "status": "connected",
            "message": "AI initialized. Ready to assist."
        }))

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get("message")

        if not message:
            await self.send(json.dumps({
                "error": "message is required"
            }))
            return

        response = await sync_to_async(self.ask_gemini)(message)

        await self.send(json.dumps({
            "message": response,
            "name": "QCRBAI"
        }))

    def ask_gemini(self, message: str) -> str:
        response = self.gemini_client.models.generate_content(
            #model="gemini-2.5-flash",
            model="gemini-2.5-flash-lite",
            contents=message,
        )
        return response.text

    async def disconnect(self, close_code):
        pass
"""