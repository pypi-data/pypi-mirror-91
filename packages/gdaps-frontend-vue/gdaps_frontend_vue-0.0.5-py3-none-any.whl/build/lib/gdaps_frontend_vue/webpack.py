from webpack_loader.loader import WebpackLoader

# thanks to [jillesme](https://github.com/jillesme)
# https://github.com/owais/django-webpack-loader/issues/227#issuecomment-735444947
# use in settings.py
# WEBPACK_LOADER = {
#     'DEFAULT': {
#         'LOADER_CLASS': 'gdaps_frontend_vue.webpack.CompatibilityWebpackLoader',
#     }
# }


class CompatibilityWebpackLoader(WebpackLoader):
    """Fixes a django-webpack-loader bug which prevents using webpack-bundle-tracker < 1.0.0"""

    def filter_chunks(self, chunks):
        chunks = [
            chunk if isinstance(chunk, dict) else {"name": chunk} for chunk in chunks
        ]
        return super().filter_chunks(chunks)
