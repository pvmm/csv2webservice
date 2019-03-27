# -*- coding: utf-8 -*-

import click

from flask import Flask, request, jsonify, current_app, make_response, Response
from flask_restful import reqparse, Resource, fields, abort
from bson import json_util
from environment import db_uri


parser = reqparse.RequestParser()

def add_endpoint(api):
    click.secho(' * Adding default endpoint...')
    api.add_resource(CSV, '/root/<string:id_>', '/root', '/root/')


class CSV(Resource):
    '''
    '''

    def abort(self, status_code, message=None):
        if message:
            response = jsonify({ 'message': message })
            response.status_code = status_code
            return response

        return abort(status_code)


    def get(self, id_=None):
        from pymongo import MongoClient
        client = MongoClient(db_uri)

        if id_:
            id_ = '%s.%s.%s/%s-%s' % (id_[0:2], id_[2:5], id_[5:8], id_[8:12], id_[12:14])
            query = { '_id' : id_ }
        else:
            self.abort(404)

        click.secho(' * received ID: "%s"' % id_, err=True)
        item = client.db['csv'].find_one(query)

        return Response(json_util.dumps(item), mimetype='application/json')

