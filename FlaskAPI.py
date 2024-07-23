from flask import Flask, request, jsonify
import os
import re
import errno

app = Flask(__name__)
LOG_DIR = 'logs' #TODO remove hardcode and add it as args

try:
    os.makedirs(LOG_DIR)
except OSError as e:
    if e.errno == errno.EEXIST and os.path.isdir(LOG_DIR):
        pass
    elif e.errno == errno.EACCES:
        print(f"Permission denied: cannot create directory '{LOG_DIR}'")
        raise
    elif e.errno == errno.ENOSPC:
        print(f"No space left on device: cannot create directory '{LOG_DIR}'")
        raise
    else:
        print(f"Unexpected error: {e}")
        raise

def get_next_log_id():
    logs = os.listdir(LOG_DIR)
    log_ids = []
    for log in logs:
        match = re.match(r'^(\d+)\.log$', log)
        if match:
            log_ids.append(int(match.group(1)))
    if not log_ids:
        return 1
    return max(log_ids) + 1

@app.route('/get_log', methods=['GET'])
def get_log():
    log_id = request.args.get('id')
    if not log_id:
        return jsonify({'error': 'ID parameter is required'}), 400

    log_file_path = os.path.join(LOG_DIR, f'{log_id}.log')

    try:
        with open(log_file_path, 'r') as log_file:
            data = log_file.read()
    except FileNotFoundError:
        return jsonify({'error': 'Log file not found'}), 404
    except PermissionError:
        return jsonify({'error': 'Permission denied to read the log file'}), 403
    except Exception as e:
        return jsonify({'error': f'An error occurred while reading the log file: {str(e)}'}), 500

    return jsonify({'id': log_id, 'log': data}), 200

@app.route('/save_log', methods=['POST'])
def save_log():
    log_data = request.data.decode('utf-8')
    if not log_data:
        return jsonify({'error': 'Log data is required'}), 400

    log_id = get_next_log_id()
    log_file_path = os.path.join(LOG_DIR, f'{log_id}.log')

    try:
        with open(log_file_path, 'w') as log_file:
            log_file.write(log_data)
    except FileNotFoundError:
        return jsonify({'error': 'Log file path not found'}), 404
    except PermissionError:
        return jsonify({'error': 'Permission denied to write to the log file'}), 403
    except OSError as e:
        if e.errno == errno.ENOSPC:
            return jsonify({'error': 'No space left on device to write the log file'}), 507
        else:
            return jsonify({'error': f'An OS error occurred while writing to the log file: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'An error occurred while writing to the log file: {str(e)}'}), 500

    return jsonify({'message': 'Log data saved', 'id': log_id}), 201

@app.route('/delete_log', methods=['DELETE'])
def delete_log():
    log_id = request.json.get('id')
    if not log_id:
        return jsonify({'error': 'ID parameter is required'}), 400

    try:
        log_file_path = os.path.join(LOG_DIR, f'{log_id}.log')
        os.remove(log_file_path)
    except FileNotFoundError:
        return jsonify({'error': 'Log file path not found'}), 404
    except PermissionError:
        return jsonify({'error': 'Permission denied to write to the log file'}), 403
    except Exception as e:
        return jsonify({'error': f'An error occurred while writing to the log file: {str(e)}'}), 500

    return jsonify({'message': 'Log deleted', 'id': log_id}), 200

@app.route('/parse_log', methods=['POST'])
def parse_log():
    log_id = request.json.get('id')
    log_data = request.json.get('log_data')
    if not log_id and not log_data:
        return jsonify({'error': 'ID and log data is required'}), 400

    log_file_path = os.path.join(LOG_DIR, f'{log_id}.log')

    try:
        with open(log_file_path, 'r') as log_file:
            log_data = log_file.read()
    except FileNotFoundError:
        return jsonify({'error': 'Log file path not found'}), 404
    except PermissionError:
        return jsonify({'error': 'Permission denied to write to the log file'}), 403
    except Exception as e:
        return jsonify({'error': f'An error occurred while writing to the log file: {str(e)}'}), 500
    
    #if not os.path.exists(log_file_path):
     #   return jsonify({'error': 'Log not found'}), 404

    

    result = parse_log_contents(log_data)
    return jsonify(result), 200

"""
Count of ERROR/INFO/MEASUREMENT - done
Average MEASUREMENT by gas - TODO with classes
Highest / lowest MEASUREMENT values - by gas? or general? just do both?
Count of alarms that happened with their exact timestamps - done
"""
def parse_log_contents(log_data):
    error_count = log_data.count('ERROR')
    info_count = log_data.count('INFO')
    measurement_count = log_data.count('MEASUREMENT')

    alarms = re.findall(r'\[(.*?)\] WARNING: .*alarm', log_data)
    alarm_count = len(alarms)

    return {
        'error_count': error_count,
        'info_count': info_count,
        'measurement_count': measurement_count,
        'alarm_count': alarm_count,
        'alarms': alarms
    }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
