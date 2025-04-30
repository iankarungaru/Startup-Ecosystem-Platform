class SystemAdminRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'systemAdmin':
            return 'sysadmin'
        return 'default'

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'systemAdmin':
            return 'sysadmin'
        return 'default'

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'systemAdmin':
            return db == 'sysadmin'
        return db == 'default'
