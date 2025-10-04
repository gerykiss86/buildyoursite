#!/usr/bin/env python3
"""
Claude Execution Server
A Flask server that executes Claude commands as clauderunner user
"""

import os
import subprocess
import json
import logging
import time
from flask import Flask, request, jsonify, Response, stream_with_context
from flask_cors import CORS
from threading import Thread
from queue import Queue
import uuid
import tempfile

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Store running jobs
jobs = {}

class ClaudeExecutor:
    def __init__(self):
        self.jobs = {}

    def execute_command_stream(self, prompt, job_id=None):
        """Execute claude command with streaming output"""
        if not job_id:
            job_id = str(uuid.uuid4())

        # Build the command
        command = [
            'su', '-', 'clauderunner', '-c',
            f'claude --dangerously-skip-permissions --print "{prompt}"'
        ]

        logger.info(f"Executing streaming command for job {job_id}: {prompt[:100]}...")

        try:
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.DEVNULL,
                text=True,
                bufsize=1,
                universal_newlines=True
            )

            # Stream output line by line
            for line in iter(process.stdout.readline, ''):
                if line:
                    yield json.dumps({
                        'job_id': job_id,
                        'status': 'running',
                        'output': line.rstrip(),
                        'type': 'stdout'
                    }) + '\n'

            process.wait()

            # Get any error output
            stderr = process.stderr.read()

            if process.returncode != 0:
                yield json.dumps({
                    'job_id': job_id,
                    'status': 'error',
                    'error': stderr,
                    'return_code': process.returncode
                }) + '\n'
            else:
                yield json.dumps({
                    'job_id': job_id,
                    'status': 'completed',
                    'return_code': 0
                }) + '\n'

        except subprocess.TimeoutExpired:
            logger.error(f"Command timed out for job {job_id}")
            yield json.dumps({
                'job_id': job_id,
                'status': 'error',
                'error': 'Command execution timed out'
            }) + '\n'
        except Exception as e:
            logger.error(f"Error executing command for job {job_id}: {str(e)}")
            yield json.dumps({
                'job_id': job_id,
                'status': 'error',
                'error': str(e)
            }) + '\n'

    def execute_command(self, prompt, job_id=None):
        """Execute claude command and return complete result"""
        if not job_id:
            job_id = str(uuid.uuid4())

        # Build the command
        command = [
            'su', '-', 'clauderunner', '-c',
            f'claude --dangerously-skip-permissions --print "{prompt}"'
        ]

        logger.info(f"Executing command for job {job_id}: {prompt[:100]}...")

        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                stdin=subprocess.DEVNULL,
                timeout=300  # 5 minute timeout
            )

            return {
                'job_id': job_id,
                'status': 'completed',
                'output': result.stdout,
                'error': result.stderr if result.stderr else None,
                'return_code': result.returncode
            }

        except subprocess.TimeoutExpired:
            logger.error(f"Command timed out for job {job_id}")
            return {
                'job_id': job_id,
                'status': 'error',
                'error': 'Command execution timed out after 5 minutes'
            }
        except Exception as e:
            logger.error(f"Error executing command for job {job_id}: {str(e)}")
            return {
                'job_id': job_id,
                'status': 'error',
                'error': str(e)
            }

executor = ClaudeExecutor()

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'claude-execution-server'})

@app.route('/execute', methods=['POST'])
def execute():
    """Execute a Claude command with the given prompt"""
    try:
        data = request.get_json()
        if not data or 'prompt' not in data:
            return jsonify({'error': 'Missing prompt in request body'}), 400

        prompt = data['prompt']
        stream = data.get('stream', False)

        # Generate job ID
        job_id = str(uuid.uuid4())

        if stream:
            # Return streaming response
            return Response(
                stream_with_context(executor.execute_command_stream(prompt, job_id)),
                mimetype='application/x-ndjson',
                headers={
                    'X-Job-ID': job_id,
                    'Cache-Control': 'no-cache'
                }
            )
        else:
            # Return complete response
            result = executor.execute_command(prompt, job_id)
            return jsonify(result)

    except Exception as e:
        logger.error(f"Error handling request: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/execute-async', methods=['POST'])
def execute_async():
    """Execute a Claude command asynchronously"""
    try:
        data = request.get_json()
        if not data or 'prompt' not in data:
            return jsonify({'error': 'Missing prompt in request body'}), 400

        prompt = data['prompt']
        job_id = str(uuid.uuid4())

        # Store job status
        jobs[job_id] = {
            'status': 'queued',
            'prompt': prompt[:100],  # Store truncated prompt for reference
            'created': time.time()
        }

        # Execute in background
        def run_job():
            jobs[job_id]['status'] = 'running'
            result = executor.execute_command(prompt, job_id)
            jobs[job_id].update(result)

        thread = Thread(target=run_job)
        thread.daemon = True
        thread.start()

        return jsonify({
            'job_id': job_id,
            'status': 'queued',
            'message': 'Job queued for execution'
        })

    except Exception as e:
        logger.error(f"Error handling async request: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/job/<job_id>', methods=['GET'])
def get_job_status(job_id):
    """Get the status of an async job"""
    if job_id not in jobs:
        return jsonify({'error': 'Job not found'}), 404

    return jsonify(jobs[job_id])

@app.route('/jobs', methods=['GET'])
def list_jobs():
    """List all jobs"""
    return jsonify({
        'jobs': [
            {
                'job_id': job_id,
                'status': job_info.get('status'),
                'created': job_info.get('created'),
                'prompt': job_info.get('prompt')
            }
            for job_id, job_info in jobs.items()
        ]
    })

@app.route('/test', methods=['GET'])
def test_endpoint():
    """Test endpoint with a simple prompt"""
    test_prompt = "Print only: Hello from Claude Execution Server"
    result = executor.execute_command(test_prompt)
    return jsonify({
        'test': True,
        'prompt': test_prompt,
        'result': result
    })

if __name__ == '__main__':
    # Configuration
    port = int(os.environ.get('CLAUDE_SERVER_PORT', 5555))
    host = os.environ.get('CLAUDE_SERVER_HOST', '0.0.0.0')

    logger.info(f"Starting Claude Execution Server on {host}:{port}")

    # Clean up old jobs periodically (older than 1 hour)
    def cleanup_jobs():
        while True:
            time.sleep(3600)  # Check every hour
            current_time = time.time()
            expired = [
                job_id for job_id, job_info in jobs.items()
                if current_time - job_info.get('created', current_time) > 3600
            ]
            for job_id in expired:
                del jobs[job_id]
            if expired:
                logger.info(f"Cleaned up {len(expired)} expired jobs")

    cleanup_thread = Thread(target=cleanup_jobs)
    cleanup_thread.daemon = True
    cleanup_thread.start()

    # Run the server
    app.run(host=host, port=port, debug=False)