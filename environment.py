# -*- coding: utf-8 -*-

import click
import re

from os import environ, sep, path


class UndefinedEnvVarError(Exception):
    '''
    Variável de ambiente necessária para o funcionamento do sistema não definida.
    '''
    def __init__(self, env_var):
        self.message = 'undefined environment variable %s' % env_var


class RelativePathTypeError(Exception):
    '''
    Tipo de caminho precisa ser absoluto.
    '''
    def __init__(self, path):
        self.message = 'absolute path required in "%s"' % path


#
# Verifica variáveis de ambiente obrigatórias.
#

if 'DB_URI' in environ.keys():
    db_uri = environ['DB_URI']
    match = re.search('(\S+)://(\S+)@(\S+)', db_uri)

    if len(match.groups()) == 3:
        click.secho(' * db_uri = "%s://****:****@%s".' % (match.groups()[0], match.groups()[2]))
    else:
        click.secho(' * db_uri = "%s".' % db_uri)
else:
    raise UndefinedEnvVarError('DB_URI')

app_base = path.dirname(path.realpath(__file__))
static_folder = path.join(app_base, environ.get('APP_STATICDIR', 'static'))

