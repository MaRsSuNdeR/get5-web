import unittest
import logging
import datetime
import get5
from get5 import db
from models import User, Team, GameServer, Match, Season, Veto


# All tests will use this base test framework, including the test date defined
# in create_test_data. This data will already be in the database on test start.
#
# TODO: make ALL tests not rely on this state. Helper functions are fine -
# but this global state makes tests hard to understand.
class Get5Test(unittest.TestCase):

    def setUp(self):
        get5.app.config.from_pyfile('test_config.py')
        get5.app.logger.setLevel(logging.ERROR)
        self.app = get5.app.test_client()
        get5.register_blueprints()
        db.create_all()
        self.create_test_data()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def create_test_data(self):
        user = User.get_or_create(123)
        user.admin = True
        User.get_or_create(12345)
        db.session.commit()

        team1 = Team.create(user, 'EnvyUs', 'EnvyUs', 'fr',
                            'nv', ['76561198053858673'])
        team2 = Team.create(user, 'Fnatic', 'Fnatic', 'se', 'fntc',
                            ['76561198053858673'])
        server = GameServer.create(
            user, 'myserver1', '127.0.0.1', '27015', 'password', False)
        server.in_use = True

        GameServer.create(
            user, 'myserver2', '127.0.0.1', '27016', 'password', True)
        db.session.commit()
        season = Season.create(user, 'Season One Test', datetime.datetime.utcnow(),
                               datetime.datetime.utcnow() + datetime.timedelta(days=1))
        db.session.commit()

        Match.create(user, team1.id, team2.id, '', '', 1, False,
                     'Map {MAPNUMBER}', ['de_dust2', 'de_cache', 'de_mirage'], season.id, 'always_knife', 'CT', server.id, 0, 0, None, False, False, 5)
        db.session.commit()

        vetoBan = Veto.create(1, 'EnvyUs', 'de_dust2', 'ban')
        vetoPick = Veto.create(1, 'EnvyUs', 'de_overpass', 'pick')
        db.session.commit()
