IPython/Jupyter Notebook Reader
===============================

This plugin gives Pelican the ability to build blogs from IPython/Jupyter notebooks.

Just install it, edit some metadata in the notebook and you're good to go.

Installation
------------

As this is currently an alpha release, you'll need to clone down the repo and add the path to the pelican plugins path.

    PLUGIN_PATHS = ['/path/to/dir/']
    PLUGINS = ['ipynb']

Metadata
--------

IPython/Juypter provides a handy toolbar for editting the notebook's metadata.

Just create a substructure called "blogdata" and add the needed fields there.

    //stuff here
    "blogdata", {
        "title" : "My first IPyNB post!",
        "date" : "2015-03-03",
        "tags" : "tag1, tag2",
        //...you get the idea
    },
    //more stuff here


Once that's done, Pelican should be able to build your blog!

Known Issues
------------

Since this uses the built in NBConvert functionality to first build an RST document, embedded HTML doesn't seem to be converted. Whoops...
