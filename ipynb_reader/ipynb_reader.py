try:
    from IPython.nbconvert.exporters import RSTExporter
except ImportError:
    RSTExporter = False


import docutils
import docutils.io
import docutils.core
from io import StringIO

from pelican import signals
from pelican.readers import BaseReader, PelicanHTMLTranslator, RstReader


def extract_blogdata(nbc, resc):
    '''Simply moves blog metadata found in the notebook's metadata over
    to the resources dictionary provided by the notebook exporters.
    '''

    resc['blogdata'] = nbc.metadata.pop('blogdata')
    return nbc, resc


def append_new_line_to_cell(nbc, resc):
    """There's an edge case where sometimes blocks aren't new line
    terminated. We'll simply just tack a new line on if that's the case.

    The new line isn't such a big deal for straight up reST documents
    but docutils pitches a fit about it.
    """

    for cell in nbc.cells:
        if not cell.source.endswith('\n'):
            cell.source += '\n'

    return nbc, resc


class IPyNBReader(BaseReader):

    enabled = bool(RSTExporter)
    file_extensions = ['ipynb']

    if RSTExporter:
        exporter = RSTExporter()
        exporter.register_preprocessor(extract_blogdata)
        exporter.register_preprocessor(append_new_line_to_cell)

    def __init__(self, *args, **kwargs):
        super(IPyNBReader, self).__init__(*args, **kwargs)

    def _get_publisher(self, contents):
        """
        Stolen from :class:`~Pelican.readers.RstReader` almost
        verbatim, except for the source which now is a file-like object.
        """
        extra_params = {
            'initial_header_level': '2',
            'syntax_highlight': 'short',
            'input_encoding': 'utf-8',
            'exit_status_level': 2,
            'embed_stylesheet': False
            }

        user_params = self.settings.get('DOCUTILS_SETTINGS', None)

        if user_params:
            extra_params.update(user_params)

        pub = docutils.core.Publisher(
            source_class=RstReader.FileInput,
            destination_class=docutils.io.StringOutput)

        pub.set_components('standalone', 'restructuredtext', 'html')
        pub.writer.translator_class = PelicanHTMLTranslator
        pub.process_programmatic_settings(None, extra_params, None)
        pub.set_source(source=contents)
        pub.publish(enable_exit_status=True)
        return pub

    def read(self, filename):
        contents, metadata = self.exporter.from_filename(filename)
        publisher = self._get_publisher(contents=StringIO(contents))
        parts = publisher.writer.parts

        contents = parts.get('body')

        blogdata = metadata.pop('blogdata')
        parsed = {k: self.process_metadata(k, v) for k, v in blogdata.items()}

        return contents, parsed

    @classmethod
    def register_preprocessor(cls, preprocessor, enabled=True):
        '''Helper method to register extra preprocessors onto the RST exporter.
        '''
        return cls.exporter.register_preprocessor(preprocessor, enabled)


def add_reader(readers):
    readers.reader_classes['ipynb'] = IPyNBReader


def register():
    signals.readers_init.connect(add_reader)
