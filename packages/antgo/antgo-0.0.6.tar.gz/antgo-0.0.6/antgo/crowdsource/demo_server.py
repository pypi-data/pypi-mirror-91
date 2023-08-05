# -*- coding: UTF-8 -*-
# @Time    : 18-4-27
# @File    : demo_server.py
# @Author  : jian<jian@mltalker.com>
from __future__ import division
from __future__ import unicode_literals
from __future__ import print_function

import tornado.httpserver
import tornado.ioloop
import tornado.options
from tornado.options import define, options
from tornado import web, gen
from tornado import httpclient
import tornado.web
from antgo.utils import logger
import os
import shutil
import json
import numpy as np
from antgo.utils.fs import *
from antgo.utils.encode import *
from PIL import Image
import imageio
import uuid
import signal
from ..utils.serialize import loads,dumps
from antgo.crowdsource.utils import *
import functools


class BaseHandler(tornado.web.RequestHandler):
  @property
  def demo_name(self):
    return self.settings.get('demo_name', '-')

  @property
  def demo_type(self):
    return self.settings.get('demo_type', '-')

  @property
  def demo_description(self):
    return self.settings.get('demo_description',{})

  @property
  def demo_dump(self):
    return self.settings.get('demo_dump', '')

  @property
  def demo_support_user_upload(self):
    return self.settings.get('support_user_upload', True)

  @property
  def demo_support_user_input(self):
    return self.settings.get('support_user_input', True)

  @property
  def demo_support_user_interaction(self):
    return self.settings.get('support_user_interaction', False)

  @property
  def demo_support_user_comment(self):
    return self.settings.get('support_user_comment', False)

  @property
  def html_template(self):
    return self.settings['html_template']
  
  @property
  def db(self):
    return self.settings['db']
  
  @property
  def port(self):
    return self.settings['port']

  @property
  def demo_constraint(self):
    constraint = self.settings.get('support_user_constraint', None)
    if constraint is None:
      constraint = {}

    return constraint

  @property
  def dataset_queue(self):
    return self.settings['dataset_queue']

  @property
  def recorder_queue(self):
    return self.settings['recorder_queue']

  def _transfer(self, data_key, data_value, data_type, demo_response):
    if data_type == 'IMAGE':
      if os.path.exists(data_value):
        data = os.path.normpath(data_value)
        shutil.copy(data, os.path.join(self.demo_dump, 'static', 'output'))
        demo_response['DATA'].update({data_key: {'DATA': '/static/output/%s' % data.split('/')[-1], 'TYPE': 'IMAGE'}})
    elif data_type == 'VIDEO':
      if os.path.exists(data_value):
        data = os.path.normpath(data_value)
        shutil.copy(data, os.path.join(self.demo_dump, 'static', 'output'))
        demo_response['DATA'].update({data_key: {'DATA': '/static/output/%s' % data.split('/')[-1], 'TYPE': 'VIDEO'}})
    elif data_type == 'AUDIO':
      if os.path.exists(data_value):
        data = os.path.normpath(data_value)
        shutil.copy(data, os.path.join(self.demo_dump, 'static', 'output'))
        demo_response['DATA'].update({data_key: {'DATA': '/static/output/%s' % data.split('/')[-1], 'TYPE': 'AUDIO'}})
    elif data_type == 'FILE':
      if os.path.exists(data_value):
        data = os.path.normpath(data_value)
        shutil.copy(data, os.path.join(self.demo_dump, 'static', 'output'))
        demo_response['DATA'].update({data_key: {'DATA': '/static/output/%s' % data.split('/')[-1], 'TYPE': 'FILE'}})
    else:
      # string
      demo_response['DATA'].update({data_key: {'DATA': str(data_value), 'TYPE': 'STRING'}})

    return demo_response

  def preprocess_model_server(self, data, data_type):
    if data_type == 'URL' or data_type == 'PATH':
      data_path = os.path.normpath(data)
      data_name = data_path.split('/')[-1]
      ext_name = data_path.split('/')[-1].split('.')[-1].lower()

      if ext_name in ['jpg', 'jpeg', 'png', 'bmp', 'gif']:
        return data_path, data_name, 'IMAGE'
      elif ext_name in ['mp4', 'avi']:
        return data_path, data_name, 'VIDEO'
      elif ext_name in ['txt']:
        return data_path, data_name, 'FILE'
      else:
        # TODO: support video and sound
        logger.warn('dont support file type %s' % ext_name)
        return None, None, None
    else:
      return data, str(uuid.uuid4()), 'STRING'

  def postprocess_model_server(self, uuid_flag, demo_result):
    demo_predict = None
    demo_predict_additional = []
    if type(demo_result) == list or type(demo_result) == tuple:
      demo_predict, demo_predict_additional = demo_result[0:2]
    else:
      demo_predict = demo_result

    # build output folder (static/output)
    if not os.path.exists(os.path.join(self.demo_dump, 'static', 'output')):
      os.makedirs(os.path.join(self.demo_dump, 'static', 'output'))

    demo_response = {'DATA': {}}
    if demo_predict['DATA'] is not None and demo_predict['TYPE'] is not None:
      demo_response = self._transfer('RESULT', demo_predict['DATA'], demo_predict['TYPE'], demo_response)
    else:
      demo_response = {'DATA': {'RESULT': {'DATA':'', 'TYPE': 'STRING'}}}

    for data in demo_predict_additional:
      data_type = data['TYPE']
      data_value = None
      data_key = None
      for k,v in data.items():
        if k != 'TYPE':
          data_key = k
          data_value = v
          break

      if data_key is not None and data_value is not None:
        demo_response = self._transfer(data_key, data_value, data_type, demo_response)

    return demo_response

    
class IndexHandler(BaseHandler):
  def get(self):
    image_history_data = []
    history_folder = os.path.join(self.demo_dump, 'static', 'input')
    if os.path.exists(history_folder):
      for f in os.listdir(history_folder):
        ext_name = f.split('.')[-1]
        if ext_name.lower() in ['jpg', 'jpeg', 'png', 'gif']:
          image_history_data.append('/static/input/%s'%f)
    
    input_filter = ''

    if 'file_type' in self.demo_constraint:
      for support_format in self.demo_constraint['file_type']:
        if support_format.lower() in ['jpg', 'jpeg', 'png', 'gif']:
          input_filter += 'image/%s,'%support_format.lower()
        elif support_format.lower() in ['mp4']:
          input_filter += 'video/%s,'%support_format.lower()
        elif support_format.lower() in ['mp3', 'wav']:
          input_filter += 'audio/%s,'%support_format.lower()
        else:
          input_filter += '%s,'%support_format.lower()

    if len(input_filter) > 0:
      input_filter = input_filter[0:-1]
    else:
      input_filter = '*'

    self.render(self.html_template, demo={'name': self.demo_name,
                                          'type': self.demo_type,
                                          'description': self.demo_description,
                                          'upload': self.demo_support_user_upload,
                                          'upload_accept': input_filter,
                                          'input': self.demo_support_user_input,
                                          'image_history': image_history_data})


class ClientQueryHandler(BaseHandler):
  def _file_download(self,file_name, response):
    download_path = os.path.join(self.demo_dump, 'static', 'input', file_name)
    with open(download_path, "wb") as f:
        f.write(response.body)

  @gen.coroutine
  def post(self):
    # 0.step check support status
    if not self.demo_support_user_upload:
      self.set_status(500)
      self.write(json.dumps({'code': 'InvalidSupport', 'message': 'demo dont support upload'}))
      self.finish()
      return

    upload_path = os.path.join(self.demo_dump, 'static', 'input')
    if not os.path.exists(upload_path):
      os.makedirs(upload_path)

    # 1.step parse query data
    model_datas = []
    model_data_names = []
    model_data_types = []
    request_param = None

    data = self.get_argument('DATA', None)
    data_type = self.get_argument('DATA_TYPE', None)
    if data is not None and data_type is not None:
      if data_type == 'URL':
        # download data from url
        http_client = httpclient.AsyncHTTPClient()
        file_name = os.path.normpath(data).split('/')[-1]
        if file_name == '':
          file_name = '%s'%str(uuid.uuid4())
        file_download_func = functools.partial(self._file_download, file_name)
        yield http_client.fetch(data, callback=file_download_func)

        file_path = os.path.join(self.demo_dump, 'static', 'input', file_name)
        if 'file_size' in self.demo_constraint:
          max_file_size = self.demo_constraint['file_size']
          fsize = os.path.getsize(file_path) / float(1024 * 1024)
          if round(fsize,2) > max_file_size:
            self.set_status(400)
            self.write(json.dumps({'code': 'InvalidImageSize', 'message': 'The input file size is too large (>%f MB)'%float(max_file_size)}))
            self.finish()
            return

        # 2.step check file format
        if 'file_type' in self.demo_constraint:
          is_ok, file_path = check_file_types(file_path, self.demo_constraint['file_type'])
          if not is_ok:
            self.set_status(400)
            self.write(json.dumps({'code': 'InvalidImageFormat', 'message': 'The input file is not in a valid image format that the service can support'}))
            self.finish()
            return

        # DATA_TYPE, DATA, TASK_NAME, TASK_TYPE
        model_data, model_data_name, model_data_type = self.preprocess_model_server(file_path, data_type)
        if model_data is None:
          self.set_status(500)
          self.write(json.dumps({'code': 'InvalidIO', 'message': 'couldnt parse data'}))
          self.finish()
          return

        model_datas.append(model_data)
        model_data_names.append(model_data_name)
        model_data_types.append(model_data_type)
    else:
      if len(self.request.files) == 0:
        self.set_status(400)
        self.write(json.dumps({'code': 'InvalidUploadFile', 'message': 'The input file is not uploaded correctly'}))
        self.finish()
        return

      file_paths = []
      file_names = []
      for _, meta in self.request.files.items():
        _file_name = '%s_%s' % (str(uuid.uuid4()), meta[0]['filename'])
        _file_path = os.path.join(upload_path, _file_name)

        with open(_file_path, 'wb') as fp:
          fp.write(meta[0]['body'])

        file_paths.append(_file_path)
        file_names.append(_file_name)

      if len(file_paths) == 0 or len(file_names) == 0:
        self.set_status(400)
        self.write(json.dumps({'code': 'InvalidUploadFile', 'message': 'The input file is not uploaded correctly'}))
        self.finish()
        return

      # 2.step parse query data
      for file_path in file_paths:
        # check file basic infomation
        # 1.step check file size
        if 'file_size' in self.demo_constraint:
          max_file_size = self.demo_constraint['file_size']
          fsize = os.path.getsize(file_path) / float(1024 * 1024)
          if round(fsize, 2) > max_file_size:
            self.set_status(400)
            self.write(json.dumps({'code': 'InvalidImageSize',
                                   'message': 'The input file size is too large (>%f MB)' % float(max_file_size)}))
            self.finish()
            return

        # 2.step check file format
        if 'file_type' in self.demo_constraint:
          is_ok, file_path = check_file_types(file_path, self.demo_constraint['file_type'])
          if not is_ok:
            self.set_status(400)
            self.write(json.dumps({'code': 'InvalidImageFormat',
                                   'message': 'The input file is not in a valid image format that the service can support'}))
            self.finish()
            return

        try:
          model_data, model_data_name, model_data_type = self.preprocess_model_server(file_path, 'PATH')
        except:
          self.set_status(400)
          self.write(json.dumps({'code': 'InvalidDetails', 'message': 'The input file parse error'}))
          self.finish()
          return

        if model_data is None:
          self.set_status(400)
          self.write(json.dumps({'code': 'InvalidDetails', 'message': 'The input file parse error'}))
          self.finish()
          return

        model_datas.append(model_data)
        model_data_names.append(model_data_name)
        model_data_types.append(model_data_type)

      request_param = self.get_argument('params', None)
      if request_param is not None:
        request_param = json.loads(request_param)

    # push to backend
    model_input = (model_datas, model_data_types, request_param) if len(model_datas) > 1 else (model_datas[0], model_data_types[0], request_param)
    self.dataset_queue.put(model_input)

    # wating to get result from backend
    result = self.recorder_queue.get()
    _, demo_result = result

    # data type: 'FILE', 'STRING', 'IMAGE', 'VIDEO', 'AUDIO'
    # data:       PATH,  '',        PATH,    PATH,    PATH
    # 5.step post process and render
    demo_response = self.postprocess_model_server(model_data_names[0], demo_result)

    if len(model_data_names) == 1:
      demo_response['INPUT_TYPE'] = model_data_types[0]
      if model_data_types[0] in ['FILE', 'IMAGE', 'AUDIO', 'VIDEO']:
        demo_response['INPUT'] = '/static/input/%s' % model_data_names[0]
      else:
        demo_response['INPUT'] = model_datas[0]
    else:
      demo_response['INPUT_TYPE'] = []
      demo_response['INPUT'] = []
      for index in range(len(model_data_names)):
        demo_response['INPUT_TYPE'].append(model_data_types[index])
        if model_data_types[index] in ['FILE', 'IMAGE', 'AUDIO', 'VIDEO']:
          demo_response['INPUT'].append('/static/input/%s' % model_data_names[index])
        else:
          demo_response['INPUT'].append(model_datas[index])

    self.write(json.dumps(demo_response))
    self.finish()


class ClientFileUploadAndProcessHandler(BaseHandler):
  @gen.coroutine
  def post(self):
    # 0.step check support status
    if not self.demo_support_user_upload:
      self.set_status(500)
      self.write(json.dumps({'code': 'InvalidSupport', 'message': 'demo dont support upload'}))
      self.finish()
      return

    # 1.step receive client upload file
    upload_path = os.path.join(self.demo_dump, 'static', 'input')
    if not os.path.exists(upload_path):
      os.makedirs(upload_path)

    file_metas = self.request.files.get('file', None)
    if not file_metas:
      self.set_status(400)
      self.write(json.dumps({'code': 'InvalidUploadFile', 'message': 'The input file is not uploaded correctly'}))
      self.finish()
      return

    file_paths = []
    file_names = []
    for meta in file_metas:
      _file_name = '%s_%s'%(str(uuid.uuid4()), meta['filename'])
      _file_path = os.path.join(upload_path, _file_name)

      with open(_file_path, 'wb') as fp:
        fp.write(meta['body'])

      file_paths.append(_file_path)
      file_names.append(_file_name)

    if len(file_paths) == 0 or len(file_names) == 0:
      self.set_status(400)
      self.write(json.dumps({'code': 'InvalidUploadFile', 'message': 'The input file is not uploaded correctly'}))
      self.finish()
      return

    # 2.step parse query data
    model_datas = []
    model_data_names = []
    model_data_types = []
    request_param = None

    for file_path in file_paths:
      # check file basic infomation
      # 1.step check file size
      if 'file_size' in self.demo_constraint:
        max_file_size = self.demo_constraint['file_size']
        fsize = os.path.getsize(file_path) / float(1024 * 1024)
        if round(fsize,2) > max_file_size:
          self.set_status(400)
          self.write(json.dumps({'code': 'InvalidImageSize', 'message': 'The input file size is too large (>%f MB)'%float(max_file_size)}))
          self.finish()
          return

      # 2.step check file format
      if 'file_type' in self.demo_constraint:
        is_ok, file_path = check_file_types(file_path, self.demo_constraint['file_type'])
        if not is_ok:
          self.set_status(400)
          self.write(json.dumps({'code': 'InvalidImageFormat', 'message': 'The input file is not in a valid image format that the service can support'}))
          self.finish()
          return
      try:
        model_data, model_data_name, model_data_type = self.preprocess_model_server(file_path, 'PATH')
      except:
        self.set_status(400)
        self.write(json.dumps({'code': 'InvalidDetails', 'message': 'The input file parse error'}))
        self.finish()
        return
      if model_data is None:
        self.set_status(400)
        self.write(json.dumps({'code': 'InvalidDetails', 'message': 'The input file parse error'}))
        self.finish()
        return

      model_datas.append(model_data)
      model_data_names.append(model_data_name)
      model_data_types.append(model_data_type)

    # 3.step preprocess data, then submit to model
    model_input = (model_datas,model_data_types,request_param) if len(model_datas) > 1 else (model_datas[0], model_data_types[0], request_param)

    self.dataset_queue.put(model_input)
    result = self.recorder_queue.get()
    _, demo_result = result

    # data type: 'FILE', 'STRING', 'IMAGE', 'VIDEO', 'AUDIO'
    # data:       PATH,  '',        PATH,    PATH,    PATH
    # 5.step post process and render
    demo_response = self.postprocess_model_server(model_data_names[0], demo_result)

    if len(model_data_names) == 1:
      demo_response['INPUT_TYPE'] = model_data_types[0]
      if model_data_types[0] in ['FILE', 'IMAGE', 'AUDIO', 'VIDEO']:
        demo_response['INPUT'] = '/static/input/%s' % model_data_names[0]
      else:
        demo_response['INPUT'] = model_datas[0]
    else:
      demo_response['INPUT_TYPE'] = []
      demo_response['INPUT'] = []
      for index in range(len(model_data_names)):
        demo_response['INPUT_TYPE'].append(model_data_types[index])
        if model_data_types[index] in ['FILE', 'IMAGE', 'AUDIO', 'VIDEO']:
          demo_response['INPUT'].append('/static/input/%s' % model_data_names[index])
        else:
          demo_response['INPUT'].append(model_datas[index])

    self.write(json.dumps(demo_response))
    self.finish()


class ClientCommentHandler(BaseHandler):
  def post(self):
    self.set_status(201)
    self.finish()


class PrefixRedirectHandler(BaseHandler):
  def get(self):
    static_pi = self.request.uri.find('static')
    path = self.request.uri[static_pi:]
    self.redirect('http://127.0.0.1:%d/%s'%(self.port, path), permanent=False)


class GracefulExitException(Exception):
  @staticmethod
  def sigterm_handler(signum, frame):
    raise GracefulExitException()


def demo_server_start(demo_name,
                      demo_type,
                      demo_config,
                      parent_id,
                      dataset_queue,
                      recorder_queue):
  # register sig
  signal.signal(signal.SIGTERM, GracefulExitException.sigterm_handler)
  
  try:
    # 0.step define http server port
    define('port', default=demo_config['port'], help='run on port')

    # 1.step prepare static resource
    static_folder = '/'.join(os.path.dirname(__file__).split('/')[0:-1])
    demo_static_dir = os.path.join(demo_config['dump_dir'], 'static')
    if not os.path.exists(demo_static_dir):
      os.makedirs(demo_static_dir)
  
    for static_file in os.listdir(os.path.join(static_folder, 'resource', 'static')):
      if static_file[0] == '.':
        continue
    
      shutil.copy(os.path.join(static_folder, 'resource', 'static', static_file), demo_static_dir)
  
    # 2.step prepare html template
    demo_tempate_dir = os.path.join(demo_config['dump_dir'], 'templates')
  
    if not os.path.exists(demo_tempate_dir):
      os.makedirs(demo_tempate_dir)

    html_template = demo_config['html_template']
    if html_template is None:
      html_template = 'demo.html'
  
      if not os.path.exists(os.path.join(demo_tempate_dir, html_template)):
        assert(os.path.exists(os.path.join(static_folder, 'resource', 'templates',html_template)))
        shutil.copy(os.path.join(static_folder, 'resource', 'templates',html_template), demo_tempate_dir)
    else:
      shutil.copy(html_template, demo_tempate_dir)

    tornado.options.parse_command_line()
    settings = {
      'template_path': demo_tempate_dir,
      'static_path': demo_static_dir,
      'html_template': html_template,
      'port': demo_config['port'],
      'demo_dump': demo_config['dump_dir'],
      'demo_name': demo_name,
      'demo_type': demo_type,
      'demo_description': demo_config['description_config'],
      'support_user_upload': demo_config['interaction']['support_user_upload'],
      'support_user_input': demo_config['interaction']['support_user_input'],
      'support_user_interaction': demo_config['interaction']['support_user_interaction'],
      'support_user_constraint': demo_config['interaction']['support_user_constraint'],
      'dataset_queue': dataset_queue,
      'recorder_queue': recorder_queue
    }
    app = tornado.web.Application(handlers=[(r"/", IndexHandler),
                                            (r"/demo", IndexHandler),
                                            (r"/api/query/", ClientQueryHandler),
                                            (r"/api/comment/", ClientCommentHandler),
                                            (r"/submit/", ClientFileUploadAndProcessHandler),
                                            (r"/.*/static/.*", PrefixRedirectHandler)],
      **settings)
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
  
    logger.info('demo is providing server on port %d'%demo_config['port'])
    tornado.ioloop.IOLoop.instance().start()
    logger.info('demo stop server')
  except GracefulExitException:
    logger.info('demo server exit')
    sys.exit(0)
  except KeyboardInterrupt:
    os.kill(parent_id, signal.SIGKILL)
    
