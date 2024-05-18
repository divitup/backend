import base64
import logging
import uuid

from flask import Blueprint, jsonify, request, g

controller = Blueprint('controller', __name__)
logger = logging.getLogger(__name__)

@controller.route('/api/v1/hello', methods=['GET'])
def hello():
    logger.debug('Hello world!')
    return jsonify({'message': 'Hello world!'})


@controller.route('/api/v1/upload', methods=['POST'])
def upload():
    # Get base64 encoded image from request
    data = request.json.get('image')
    if not data:
        return jsonify({'error': 'No image provided'}), 400

    # Decode the image and save to S3
    image_data = base64.b64decode(data)
    session_id = str(uuid.uuid4())
    file_name = f"{session_id}.jpeg"
    s3_path = f"receipts/{file_name}"
    s3.upload_fileobj(image_data, bucket_name, s3_path)

    # Store session details in SQLite
    c.execute('INSERT INTO sessions (session_id, s3_url, processed, result) VALUES (?, ?, 0, NULL)',
              (session_id, s3_path))
    conn.commit()

    # Simulate or trigger image processing
    result = image_processing(s3_path)
    c.execute('UPDATE sessions SET processed = 1, result = ? WHERE session_id = ?', (str(result), session_id))
    conn.commit()

    return jsonify({'session_id': session_id, 'status': 'uploaded and processing started'}), 200


@controller.route('/api/v1/result', methods=['GET'])
def result():
    session_id = request.args.get('session_id')
    if not session_id:
        return jsonify({'error': 'No session_id provided'}), 400

    # Retrieve the processing status
    c.execute('SELECT processed, result FROM sessions WHERE session_id = ?', (session_id,))
    row = c.fetchone()

    if row and row[0] == 1:  # Processing complete
        return jsonify({'result': eval(row[1])}), 200
    elif row and row[0] == 0:  # Processing not complete
        return jsonify({'error': 'Image processing not finished yet'}), 202
    else:
        return jsonify({'error': 'Invalid session_id'}), 404
