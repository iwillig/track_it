import sqlalchemy
from sqlalchemy.pool import QueuePool
from sqlalchemy import create_engine
from sqlalchemy.sql import select
from pyramid.config import Configurator
from pyramid.view import view_config
#from pyramid.response import Response
from track_it.db import (
    initDB,
    users
)
from pyramid.renderers import JSON

# Create our own copy of the render
json_renderer = JSON()


def row_adapter(obj, request):
    """ Convert the sqlalchemy RowProxy into a list in order to
    correctly serialize objects to JSON
    """
    return list(obj)

# register the new type converter with the pyramid render
json_renderer.add_adapter(sqlalchemy.engine.base.RowProxy, row_adapter)


def sqlalchmey_tween_factory(handler, registry):
    """ In order to give each view handler access to the database, we
    create a single Connection Pool for the entire application. Then,
    before each view function is called, we give that view handler
    access to the connection via the request object
    """
    pool = create_engine(
        registry.settings.get('sqlalchemy'),
        poolclass=QueuePool
    )

    def sqlalchmey_tween(request):
        # get a connection
        conn = pool.connect()
        request.db = conn
        response = handler(request)
        # give the connection back to the pool
        conn.close()
        return response

    return sqlalchmey_tween


@view_config(route_name='index', renderer='json')
def index(request):
    return {
        'version': request.registry.settings.get('api.version')
    }


@view_config(route_name='test', renderer='json')
def test(request):
    # return all of the users objects as a json list
    return request.db.execute(select([users])).fetchall()


def main(global_config, **settings):
    """Main function to produce a wsgi object """
    initDB(settings)  # create the database
    config = Configurator(settings=settings)
    # override the default json renderer
    config.add_renderer('json', json_renderer)

    # add the database tween
    config.add_tween('track_it.sqlalchmey_tween_factory')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('index', '/')
    config.add_route('test', '/test')
    config.scan()

    return config.make_wsgi_app()
