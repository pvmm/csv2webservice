# -*- coding: UTF-8 -*-

import csv, sys, click

from db.mongo import client
from pprint import pformat, pprint


def _open_csv_file(filename, delimiter):
    return csv.DictReader(filename, delimiter=delimiter, dialect='excel')


def dump(filename, delimiter=';', pkindex=0, pkname=None):
    reader = _open_csv_file(filename, delimiter)
    header = reader.fieldnames # reader.__next__()
    click.secho(' * Headers: %s' % pformat(header), err=True, color='grey')
    records = 0

    if pkindex != 0 and pkname != None:
        click.secho(' * pkindex e pkname não podem ser usados ao mesmo tempo.', err=True, color='red')
        sys.exit()

    if pkindex != 0:
        pkname = header.get(pkindex)
        click.secho(' * Chave primária definida como índice %d (%s)' % (pkindex, pkname))

    if pkname != None:
        pkindex = header.index(pkname)
        click.secho(' * Chave primária definida como índice %d (%s)' % (pkindex, pkname))

    # Tenta gravar nome dos campos se necessário
    try:
        click.secho(' * Salvando registro de cabeçalho: %s' % pformat(header))
        client.db['csv'].insert({ '_id': 'header', 'contents': header})
        records += 1
    except:
        click.secho(' * Cabeçalho já gravado')

    for line in reader:
        data = { '_id': line[pkname], 'contents': list(line.values()) }
        click.secho(' * Salvando registro "%s"...' % line[pkname])
        #pprint(data)
        client.db['csv'].insert(data)
        records += 1

    client.close()
    if client.db['csv'].count() == records:
        click.secho(' * %d registros gravados.' % client.db['csv'].count())
    else:
        click.secho(' * %d vs. %d registros gravados.' % (client.db['csv'].count(), records))

    click.secho(' * Coleções encontradas: %s' % client.db.list_collection_names())


def clean():
    client.db.drop_collection('csv')
