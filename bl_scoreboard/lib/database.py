# -*- coding: utf-8 -*-

__author__ = 'ogaidukov'

from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.sql import compiler
from psycopg2.extensions import adapt as sqlescape

Base = declarative_base()
sqla_session = scoped_session(sessionmaker(autocommit=False, autoflush=False))
Base.query = sqla_session.query_property()


def compile_query(query):
    dialect = query.session.bind.dialect
    statement = query.statement
    comp = compiler.SQLCompiler(dialect, statement)
    comp.compile()
    enc = dialect.encoding
    params = {}
    for k, v in comp.params.iteritems():
        if isinstance(v, unicode):
            v = v.encode(enc)
        params[k] = sqlescape(v)
    return (comp.string.encode(enc) % params).decode(enc)
