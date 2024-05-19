import base64
import logging
import uuid
import sqlite3  # Assuming you are using sqlite
from ai.receipt_ocr import invoke_ocr_chain
from inits.s3 import s3_upload
from inits.sql import conn, c
from io import BytesIO

from flask import Flask, Blueprint, jsonify, request
from werkzeug.exceptions import BadRequest

controller = Blueprint('controller', __name__)
logger = logging.getLogger(__name__)


@controller.route('/api/v1/hello', methods=['GET'])
def hello():
    logger.debug('Hello world!')
    return jsonify({'message': 'Hello world!'})


@controller.route('/api/v1/upload', methods=['POST'])
def upload():
    try:
        data = request.json.get('image')
        if not data:
            raise BadRequest('No image provided')

        # Decode the image
        image_data = base64.b64decode(data)
        session_id = str(uuid.uuid4())
        file_name = f'{session_id}.jpeg'
        s3_path = f'receipts/{file_name}'

        # Convert image data to a file-like object
        image_file = BytesIO(image_data)

        # Save to S3
        s3_upload(session_id, s3_path, image_file)
        # Store session details in SQLite
        c.execute(
            'INSERT INTO sessions (session_id, s3_url, processed, result) VALUES (?, ?, 0, NULL)',
            (session_id, s3_path),
        )
        conn.commit()

        # Simulate or trigger image processing
        # Assuming `image_processing` is a function you have defined elsewhere
        res, cb = invoke_ocr_chain(
            "https://divup-images.s3.amazonaws.com/" + s3_path)
        c.execute(
            'UPDATE sessions SET processed = 1, result = ? WHERE session_id = ?',
            (str(res), session_id),
        )
        conn.commit()

        return (
            jsonify(
                {'session_id': session_id, 'status': 'uploaded and processing started',
                 'result': res}
            ),
            200,
        )
    except Exception as e:
        logger.error(f'Error uploading or processing image: {str(e)}')
        return (
            jsonify(
                {'error': 'Failed to upload or process image', 'details': str(e)}),
            500,
        )


@controller.route('/api/v1/result', methods=['GET'])
def result():
    session_id = request.args.get('session_id')
    if not session_id:
        return jsonify({'error': 'No session_id provided'}), 400

    # Retrieve the processing status
    c.execute(
        'SELECT processed, result FROM sessions WHERE session_id = ?', (session_id,))
    row = c.fetchone()

    if row and row[0] == 1:  # Processing complete
        return jsonify({'result': eval(row[1])}), 200
    elif row and row[0] == 0:  # Processing not complete
        return jsonify({'error': 'Image processing not finished yet'}), 202
    else:
        return jsonify({'error': 'Invalid session_id'}), 404
