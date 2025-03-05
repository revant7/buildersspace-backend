class MainRouter:
    """
    A router to control all database operations on models in the
    home application.
    """

    def db_for_read(self, model, **hints):
        """
        Attempts to read models go to main.
        """
        if model._meta.app_label == "home":
            return "main"
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write models go to main.
        """
        if model._meta.app_label == "home":
            return "main"
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the home app is involved.
        """
        if obj1._meta.app_label == "home" or obj2._meta.app_label == "home":
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the home app only appears in the 'main'
        database.
        """
        if app_label == "home":
            return db == "main"
        return None
