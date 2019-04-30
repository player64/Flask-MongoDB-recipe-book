import json
import os
from flask import url_for


class WebpackManifest:
    JsonExist = False
    manifest = {}

    def __init__(self, app, params: dict):
        try:
            self.staticFolder = params['static_folder']
            self.manifestPath = params['manifest_path']
            self.app = app
            self.JsonExist = self._file_exists(self.manifestPath)
            self.init_app()
            print(self.JsonExist)
        except IOError:
            raise RuntimeError(
                "Incorrect parameters passed to WebpackManifest"
                "it must point to a valid json file.")

    def init_app(self):
        self._set_asset_paths()
        self.app.add_template_global(self.manifest_javascript)
        # app.add_template_global(self.stylesheet_tag)
        # app.add_template_global(self.asset_url_for)

    def _set_asset_paths(self):
        if self.JsonExist:
            with self.app.open_resource(self.manifestPath, 'r') as stats_json:
                self.manifest = json.load(stats_json)

    def manifest_javascript(self, *args):
        tags = []

        for arg in args:
            if self.JsonExist and arg in self.manifest:
                asset_path = '{}/{}'.format(self.staticFolder, self.manifest[arg])
                tags.append('<script src="{0}"></script>'.format(asset_path))
            """
            else:
                if self._file_exists(self.staticFolder + '/js/' + arg):
                    asset_path = url_for('static', filename='js/' + arg)
                else:
                    asset_path = None
            if asset_path:
                tags.append('<script src="{0}"></script>'.format(asset_path))
            """

        return '\n'.join(tags)

    def _file_exists(self, path):
        return os.path.isfile(path)
