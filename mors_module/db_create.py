#!flask/bin/python
from mors_module.migrate.versioning import api
from mors_module.config import SQLALCHEMY_DATABASE_URI
from mors_module.config import SQLALCHEMY_MIGRATE_REPO
from mors_module import db
import os.path
db.create_all()
if not os.path.exists(SQLALCHEMY_MIGRATE_REPO):
    api.create(SQLALCHEMY_MIGRATE_REPO, 'database repository')
    api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
else:
    api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, api.version(SQLALCHEMY_MIGRATE_REPO))