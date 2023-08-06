import doxycast.config
import doxycast.builder

import sphinx
import sphinx.application

def setup(app: sphinx.application.Sphinx):
    doxycast.config.setup(app)
    doxycast.builder.setup(app)
