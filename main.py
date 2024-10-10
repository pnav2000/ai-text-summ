from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
import os
import base64
from flask_cors import CORS
import uuid
from vectorai import chatbot
from vectorai import filehandling

# PRE FIX [CREATING UPLOAD FOLDER]
if not os.path.exists("uploads"):
        os.makedirs("uploads")

# Initialize chatbot and file handling
file_handling = filehandling.FileHandling()
chatbot = chatbot.chatbot()

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

# global
AI_NAME = "Parkar Tools Team AI"

# Dictionary to store session-specific data
user_data = {}

# Function to get summary for a specific session
def get_summary(session_id):
    return user_data[session_id].get('summary', '')

# Check if a value is a digit or string
def check_string_type(value):
    return "integer" if value.isdigit() else "string"

# Send Message To User
def send_to_user(text):
    emit('response', text)

def send_when_psg_uploaded(text):
    emit('response', f"Thank you for providing the paragraph. It consists of <b>{len(text)}</b> characters in the <b>{chatbot.detect_language(text)[1]}</b>.")
    emit('response', "Could you kindly let me know the <b>maximum Words</b> limit for the summary (e.g., 80, 120)?")


def send_summerized_text_to_user(psg_txt, max_length):
    def related_articles(text_summary):
        try:
            ra = chatbot.get_related_articles(text_summary)
            related_articles_string = "<b> Related Articles: </b>"
            if ra:
                for article in ra:
                    related_articles_string += (f"<li> {article['title']}: {article['url']} </li>")
                
                return related_articles_string
            else:
                pass # Insted of giving no related article recived we are skipping the responce entirely..
        except Exception:
            pass # If any thing wrong happen while finding related articles skip the response instead of breaking code..

    # STEP 1 DETECT LANGUAGE
    DETECTED_LANGUAGE = chatbot.detect_language(psg_txt)

    # STEP 2 TRANSLATE TEXT TO ENGLISH
    if DETECTED_LANGUAGE[0] != "en":
        psg_txt = chatbot.translat_msg(psg_txt, src=DETECTED_LANGUAGE[0], dest="en")

    # STEP 3 SUMMERIZE TEXT
    text_summary = chatbot.summarize_text(psg_txt, max_words=max_length)

    # STEP 4 FINDING CATEGORY
    text_category = chatbot.categorize_text(text_summary)[0]

    # STEP 5 GET RELATED ARTICALS
    text_related_articals = related_articles(text_summary)

    # STEP 6 GET SENTIMANT
    text_sentiment = chatbot.analyze_sentiment(text_summary)

    # STEP 6 TRANSLATE TO ORIGNAL LANGUAGE
    if DETECTED_LANGUAGE[0] != "en":
        text_summary = chatbot.translat_msg(text_summary, src="en", dest=DETECTED_LANGUAGE[0])

    # STEP 7 FINAL TEXT
    FINAL_TEXT = f"<b> Summary: </b><br>{text_summary} <br><br>"
    FINAL_TEXT += f"<b>Category: </b> {text_category} <br><br>"
    FINAL_TEXT += f"<b>Sentiment: </b> {text_sentiment} <br><br>"
    FINAL_TEXT += f"{text_related_articals} <br>"

    # RETURNING TO USER
    send_to_user(FINAL_TEXT)

    # RETURING SUMMERY TEXT
    return text_summary

def send_re_summerized_text_to_user(psg_txt, max_length):
    # STEP 1 DETECT LANGUAGE
    DETECTED_LANGUAGE = chatbot.detect_language(psg_txt)

    # STEP 2 TRANSLATE TEXT TO ENGLISH
    if DETECTED_LANGUAGE[0] != "en":
        psg_txt = chatbot.translat_msg(psg_txt, src=DETECTED_LANGUAGE[0], dest="en")

    # STEP 3 SUMMERIZE TEXT
    text_summary = chatbot.summarize_text(psg_txt, max_words=max_length)

    # STEP 4 TRANSLATE TO ORIGNAL LANGUAGE
    if DETECTED_LANGUAGE[0] != "en":
        text_summary = chatbot.translat_msg(text_summary, src="en", dest=DETECTED_LANGUAGE[0])

    # STEP 5 FINAL TEXT
    FINAL_TEXT = f"<b> Re-summarized text: </b> <br><br>{text_summary}"

    # RETURNING TO USER
    send_to_user(FINAL_TEXT)

# ---------- FLASK METHODS -------------- #

# Handle file uploads (HTTP POST fallback)
@app.route('/uploads', methods=['POST'])
def upload_file():
    print("Upload initiated")
    if 'fileUpload' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['fileUpload']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Save the file
    file_path = os.path.join('uploads', file.filename)
    file.save(file_path)

    return jsonify({'message': 'File uploaded successfully!'}), 200

# WebSocket event for handling new connections
@socketio.on('connect')
def handle_connect(): # User Has been Connected to server
    emit('response', "Hello! I’m **Parkar Tools Team AI** 🤖, your intelligent assistant.")
    emit('response', "I can summarize any text you provide 📄, as well as files in **TXT** 📜, **PDF** 📚, and **DOCX** 📝 formats. <br> Just share the content you’d like summarized, and I’ll take care of the rest! ✨")

# WebSocket for handling text messages
@socketio.on('message')
def handle_websocket_message(message):
    session_id = request.sid  # Unique session ID for each user

    # Initialize session data if it doesn't exist
    if session_id not in user_data:
        user_data[session_id] = {'text': '', 'last_length': 80}

    # Update the text for the current session
    if check_string_type(message) == "integer":
        # Prec checks 
        if int(message) < 50:
            emit('response', f"<b>Error: </b>The input is too short. It needs to be longer for the system to work properly.<br><br> I’m considering using a length of <b>50</b> to provide you with a better summary.")
            message = 50
        
        # Main logic
        if len(user_data[session_id]['text']) > 4:
            user_data[session_id]['last_length'] = int(message)  # Update length
            try:
                user_data[session_id]['text'] = send_summerized_text_to_user(user_data[session_id]['text'], user_data[session_id]['last_length'])
                emit('response', "<b>Would you like to re-summarize this text?</b> [Yes, No]")
            except Exception as e:
                emit('response', f"<b> AI Resived some issue to summerize text. </b><br><br> Error: {e}")
        else:
            emit('response', "No Previous Paragraph Found!! Please Provide Paragraph First!")

    elif message.strip().lower() == 'test':
        emit('response', "<b> Hello </b> <br> <li> This is another line </li> <li> this is line 2 </li>")

    elif message.strip().lower() == 'yes':
        if len(user_data[session_id]['text']) > 4:
            try:
                send_re_summerized_text_to_user(user_data[session_id]['text'], user_data[session_id]['last_length'])
                user_data[session_id]['text'] = ""  # Clearing Older Message
            except Exception as e:
                emit('response', f"<b>AI Resived some issue to Re-summerize your text. </b><br><br> Error: {e}")
        else:
            emit('response', "Please Provide Paragraph First!")

    elif message.strip().lower() == 'no':
        user_data[session_id]['text'] = ""  # Clearing Older Message
        emit('response', "Thank You! Give me another paragraph for summarization!")

    else:
        user_data[session_id]['text'] = message
        send_when_psg_uploaded(user_data[session_id]['text'])

# WebSocket event for handling file uploads
@socketio.on('file_upload')
def handle_file_upload(file_data):
    session_id = request.sid  # Unique session ID for each user

    # Ensure user-specific storage exists
    if session_id not in user_data:
        user_data[session_id] = {'text': '', 'file_name': ''}

    file_name = file_data['name']
    file_path = f"uploads/{session_id}_{uuid.uuid4()}_{file_name}"  # Unique file path with session ID
    file_content = file_data['content']  # Base64 encoded content

    # Decode the base64 content and save the file
    with open(file_path, 'wb') as f:
        f.write(base64.b64decode(file_content))

    user_data[session_id]['file_name'] = file_name  # Store file name for the session
    emit('file_upload_response', f"File <code> {file_name}  </code> uploaded successfully!")

    # Read the content of the uploaded file and store it in the session-specific variable
    user_data[session_id]['text'] = file_handling.read_file(file_path)
    send_when_psg_uploaded(user_data[session_id]['text'])

    # Removing uploaded file after reading
    if os.path.exists(file_path):
        os.remove(file_path)

# Clean up session data when user disconnects
@socketio.on('disconnect')
def handle_disconnect():
    session_id = request.sid
    if session_id in user_data:
        user_data.pop(session_id)  # Remove data when user disconnects

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=80, debug=False)
