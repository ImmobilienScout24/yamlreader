__all__ = ["YamlReaderError","yaml_load"]
__version__ = "1"

from yaml import MarkedYAMLError, safe_load, safe_dump
import sys
import glob
import os
import logging

class YamlReaderError(Exception):
    pass

def dict_merge(a, b, path=None):
    """merges b into a
    based on http://stackoverflow.com/questions/7204805/python-dictionaries-of-dictionaries-merge
    and extended to also merge arrays and to replace the content of keys with the same name"""
    if path is None: path = []
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                dict_merge(a[key], b[key], path + [str(key)])
            elif isinstance(a[key], list) and isinstance(b[key], list):
                a[key].extend(b[key])
            else:
                a[key] = b[key]
        else:
            a[key] = b[key]
    return a


def yaml_load(source,defaultdata=None):
    """merge YAML data from files found in source
    
    Always returns a dict. The YAML files are expected to contain some kind of 
    key:value structures, possibly deeply nested. When merging, lists are
    appended and dict keys are replaced. The YAML files are read with the
    yaml.safe_load function.
     
    source can be a file, a dir, a list/tuple of files or a string containing 
    a glob expression (with ?*[]).
    
    For a dir all *.yaml files will be read in alphabetical order.
       
    defaultdata can be used to initialize the data.
    """
    logger = logging.getLogger(__name__)
    logger.debug("initilized with source=%s, defaultdata=%s" %(source,defaultdata))
    if defaultdata:
        data = defaultdata
    else:
        data = {}
    files = []
    if type(source) is not str and len(source) == 1:
        # when called from __main source is always a list, even if it contains only one item.
        # turn into a string if it contains only one item to support our different call modes
        source = source[0]
    if type(source) is list or type(source) is tuple:
        # got a list, assume to be files
        files = source
    elif os.path.isdir(source):
        # got a dir, read all *.yaml files 
        files = sorted(glob.glob(os.path.join(source,"*.yaml")))
    elif os.path.isfile(source):
        # got a single file, turn it into list to use the same code
        files = [source]
    else:
        # try to use the source as a glob
        files = sorted(glob.glob(source))
    if files:
        logger.debug("Reading %s\n" % ", ".join(files))
        for yaml_file in files:
            try:
                with open(yaml_file) as f: 
                    new_data = safe_load(f)
                    logger.debug("YAML LOAD: %s" % new_data)
            except MarkedYAMLError, e:
                logger.error("YAML Error: %s" % str(e))
                raise YamlReaderError("YAML Error: %s" % str(e))
            if new_data is not None:
                dict_merge(data,new_data)
    else:
        if not defaultdata:
            logger.error("No YAML data found in %s and no default data given" % source)
            raise YamlReaderError("No YAML data found in %s" % source)

    return data

def __main():
    import optparse
    parser = optparse.OptionParser(usage="%prog [options] source...",
                                   description="Merge YAML data from given files, dir or file glob", 
                                   version="%"+"prog %s" % __version__, 
                                   prog="yamlreader")
    parser.add_option("--debug", dest="debug", action="store_true", default=False, help="Enable debug logging [%default]")
    options, args = parser.parse_args()
    if options.debug:
        logger = logging.getLogger()
        loghandler = logging.StreamHandler()
        loghandler.setFormatter(logging.Formatter('yamlreader: %(levelname)s: %(message)s'))
        logger.addHandler(loghandler)
        logger.setLevel(logging.DEBUG)
        

    if not args:
        parser.error("Need at least one argument")
    try:
        print safe_dump(yaml_load(args,defaultdata={}), 
                        indent=4, default_flow_style=False, canonical=False)
    except Exception, e:
        parser.error(e)

if __name__ == "__main__":
    __main()