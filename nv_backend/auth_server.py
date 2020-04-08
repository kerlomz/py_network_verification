#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author: kerlomz <kerlomz@gmail.com>
import base64
import logging
import optparse
import hashlib
from flask import Flask, Response, jsonify, request

from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler
from core import Core

# The order cannot be changed, it must be before the flask.
_core = Core()

app = Flask(__name__)
_except = Response()


@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.errorhandler(400)
def server_error(error=None):
    message = "Bad Request"
    return jsonify(message=message, code=error.code, success=False)


@app.errorhandler(500)
def server_error(error=None):
    message = 'Internal Server Error'
    return jsonify(message=message, code=500, success=False)


@app.errorhandler(404)
def not_found(error=None):
    message = '404 Not Found'
    return jsonify(message=message, code=error.code, success=False)


@app.errorhandler(403)
def permission_denied(error=None):
    message = 'Forbidden'
    return jsonify(message=message, code=error.code, success=False)


def machine_code_auth(username, c_volume_serial_number, mac, hostname):
    auth_code = base64.b64encode(
        hashlib.md5("\u0000\u9999\0||{}||{}||{}||{}||\n\r\0\u8888".format(
            username, c_volume_serial_number, mac, hostname
        ).encode('utf8')).hexdigest().encode("utf8")
    ).decode()
    return auth_code[:6] + auth_code[-10:]


def decrypt_auth(key):
    board_id, bios_id = _core.extract(key)
    auth_code = _core.auth_code(board_id=board_id, bios_id=bios_id)
    return auth_code


@app.route('/auth', methods=['GET'])
def index():
    """
    This api is used for captcha prediction without authentication
    :return:
    """

    return """
    <!DOCTYPE html>
    <!-- saved from url=(0071)https://demo.demohuo.top/jquery/40/4044/demo/demos/template-review.html -->
    <html lang="en"><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
            <title>Auth Code Generator</title>

            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link rel="stylesheet" href="./static/css/modernforms.css">
            <link rel="stylesheet" href="./static/css/font-awesome.min.css">
        </head>
        <body class="mdn-bg">
            <div class="modern-forms">
                <div class="modern-container mc2">
                    <form>
                        <fieldset>
                            <div class="field-group">
                                <textarea id="content" class="mdn-textarea" placeholder="Machine Code"></textarea>
                                <label class="mdn-label">Machine Code</label>
                                <span class="mdn-bar"></span>
                            </div><!-- end mdn-group -->
                        </fieldset>

                        <div class="mdn-footer">
                            <button id="submit" type="button" class="mdn-button btn-primary" onclick="Submit()">Submit</button>
                            <button type="reset" class="mdn-button btn-flat">Cancel</button>
                        </div>
                    </form>    
                </div><!-- modern-container -->
            </div><!-- modern-forms -->
            <script type="text/javascript" src="./static/js/jquery-3.3.1.min.js"></script>
            <script type="text/javascript">
              function Submit(){
                $.ajax({
                    type: "POST",
                    url: "auth/v1",
                    contentType: "application/json; charset=utf-8",
                    data: JSON.stringify({ 'code': $("#content").val()}),
                    dataType: "json",
                    success: function (message) {           
                        $("#content").val(message.key);
                    },
                    error: function (message) {
                        alert("请求失败");
                    }
                });
              }
            </script>
        </body>
    </html>
    """, 200


@app.route('/auth/v1', methods=['POST'])
def common_request():
    """
    This api is used for captcha prediction without authentication
    :return:
    """
    machine_code = request.json['code']
    if len(machine_code) > 100:
        auth_code = decrypt_auth(machine_code)
        return jsonify({"key": auth_code}), 200
    else:
        return jsonify({"key": machine_code}), 200


if __name__ == "__main__":

    parser = optparse.OptionParser()
    parser.add_option('-p', '--port', type="int", default=19991, dest="port")
    opt, args = parser.parse_args()
    server_port = opt.port

    logger = logging.getLogger(__name__)
    logger.setLevel(level=logging.INFO)
    handler = logging.FileHandler("auth_server.log")
    handler.setLevel(logging.INFO)
    logger.addHandler(handler)

    server_host = "0.0.0.0"

    logger.info('Running on http://{}:{}/ <Press CTRL + C to quit>'.format(server_host, server_port))
    server = WSGIServer((server_host, server_port), app, handler_class=WebSocketHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.stop()
