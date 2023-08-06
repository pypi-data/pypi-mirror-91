#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author: zhangkai
Email: zhangkai@cmcm.com
Last modified: 2018-01-05 14:09:42
'''
import argparse
import json
import logging
import re
from configparser import ConfigParser
from pathlib import Path

import yaml

from .utils import Dict


class Config(Dict):

    def __init__(self, config=None, guess=True, parse=True):
        if config is not None:
            self.update(self._load_cfg(config))

        if parse:
            parser = argparse.ArgumentParser()
            parser.add_argument('--config', type=str, default=None)
            args, _ = parser.parse_known_args()
            if args.config:
                self.update(self._load_cfg(args.config))

            parser = argparse.ArgumentParser()
            for key, value in self.items():
                self._add_args(parser, key, value)
            args, params = parser.parse_known_args()

            if params and guess:
                logger = logging.getLogger()
                parsed_params = self._parse(params)
                logger.info(f'{params} is parsed as {parsed_params}')
                args.__dict__.update(parsed_params)

            for key, value in args.__dict__.items():
                self._update(self, key, value)

    def _load_ini(self, config):
        conf = ConfigParser()
        conf.read(config)
        cfg = Dict()
        for section in conf.sections():
            cfg[section] = Dict()
            for key, value in conf.items(section):
                cfg[section][key] = self._convert(value)
        return cfg

    def _load_cfg(self, config):
        cfg = Dict()
        if isinstance(config, dict):
            cfg.update(Dict(config))
        elif config.endswith('.ini'):
            cfg.update(Dict(self._load_ini(config)))
        elif config.endswith('.json'):
            cfg.update(Dict(json.load(open(config))))
        elif config.endswith('.yaml') or config.endswith('.yml'):
            cfg.update(Dict(yaml.load(open(config))))
        else:
            raise TypeError(f'{config} must be dict, ini, json or yaml')

        if cfg.extends:
            base = Dict()
            root = Path(config).parent
            if isinstance(cfg.extends, list):
                for x in cfg.extends:
                    base.update(self._load_cfg(str(root / x)))
            elif isinstance(cfg.extends, str):
                base.update(self._load_cfg(str(root / cfg.extends)))
            base.update(cfg)
            cfg.update(base)

        return cfg

    def _convert(self, value):
        if re.match(r'^-?[\d]+$', value):
            return int(value)
        elif re.match(r'^-?\d+(\.?\d+)?$', value):
            return float(value)
        elif re.match(r'^true|false$', value, re.I):
            return value.lower() == 'true'
        else:
            return value

    def _update(self, opt, key, value):
        if key.find('.') >= 0:
            arr = key.split('.', 1)
            self._update(opt[arr[0]], arr[1], value)
        else:
            if isinstance(value, list):
                opt[key] = list(filter(lambda x: x != '', value))
            elif value == '':
                opt[key] = None
            else:
                opt[key] = value

    def _parse(self, params):
        args = {}
        for i, param in enumerate(params):
            if param.startswith('--') and param.find('=') >= 0:
                arr = param[2:].split('=')
                args[arr[0]] = self._convert(arr[1])
            elif param.startswith('--no-'):
                args[param[5:]] = False
            elif param.startswith('--'):
                args[param[2:]] = True
            else:
                values = [self._convert(param)]
                for j in range(1, i + 1):
                    key = params[i - j]
                    if not key.startswith('--'):
                        values.insert(0, self._convert(key))
                    else:
                        key = key[2:]
                        args[key] = values[0] if len(values) == 1 else values
                        break
        return args

    def _get_type(self, value):
        if isinstance(value, list):
            if len(value) > 0:
                return self._get_type(value[0])
            else:
                return str
        elif value is None:
            return str
        else:
            return type(value)

    def _add_args(self, parser, key, value):
        if isinstance(key, str):
            if isinstance(value, dict):
                for k, v in value.items():
                    if isinstance(k, str):
                        self._add_args(parser, f'{key}.{k}', v)
            elif isinstance(value, list):
                parser.add_argument(f'--{key}', type=self._get_type(value), nargs='+', default=value)
            elif isinstance(value, bool):
                parser.add_argument(f'--{key}', dest=key, action='store_true', default=value)
                parser.add_argument(f'--no-{key}', dest=key, action='store_false', default=(not value))
            else:
                parser.add_argument(f'--{key}', type=self._get_type(value), default=value)
