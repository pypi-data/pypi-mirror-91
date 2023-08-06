# Python Standard Library
from urllib.parse import urlencode
from enum import Enum,auto
from pprint import pformat as pf
from pathlib import Path, PosixPath
# External Packages
import requests

# df = pd.DataFrame(requests.post("http://astroarchive.noao.edu/api/adv_search/fasearch/?limit=10",json={"outfields": ["instrument","proc_type"],"search": []}).json()[1:])

# TODO (wrap_api):
#   Single search command for File/Hdu
#   No distinction between core/aux on call; but complain if AUX used without
#     INSTRUMENT,PROCTYPE and give list of pairs that contain AUX field(s).
# 
#   Authentication; download_decam_expnum.get_files()
#   Validate response from requests.  PPrint error if not success.
#   Generalize: error handling
#   Always JSON output (or pandas dataframe? or VOTABLE?)
#     Use Generics? https://docs.python.org/3/library/typing.html
#   ENUM for format
#   Cache categoricals, validate against them, output possibles on error.
#   Use Keyword arguments almost everywhere
#   Implement timeout:
#      https://requests.readthedocs.io/en/master/user/advanced/#timeout
#   Use Session in AdaApi class
#   Cache calls to relatively static content:
#      cat_lists, version, *_*_fields, *adoc,
#

# TODO (marsnat):
#   API should return seperate VERSION for SIA and ADS.
#   ADS search; HEADER in response should give full URL for 'endpoint'

class Rec(Enum):
    File = auto()
    Hdu = auto()

class AdsFormat(Enum):
    Csv = auto()
    Json = auto()
    Xml = auto()

class SiaFormat(Enum):    
    Csv = auto()
    Json = auto()
    Xml = auto()
    Votable = auto() # XML
    

class AdaApi():
    """Astro Data Archive"""
    expected_version = 5.0

    def __init__(self,
                 url='https://astroarchive.noao.edu',
                 verbose=False, limit=10,
                 email=None,  password=None):
        self.rooturl=url.rstrip("/")
        self.apiurl = f'{self.rooturl}/api'
        self.adsurl = f'{self.rooturl}/api/adv_search'
        self.siaurl = f'{self.rooturl}/api/sia'
        self.categoricals = None
        self.token = None
        self.version = None
        self.verbose = verbose
        self.limit = limit
        self.email = email
        if email is not None:
            res = requests.post(f'{self.apiurl}/get_token/',
                                json=dict(email=email, password=password))
            res.raise_for_status()
            if res.status_code == 200:
                self.token = res.json()
            else:
                self.token = None
                msg = (f'Credentials given '
                       f'(email="{email}", password={password}) '
                       f'could not be authenticated. Therefore, you will '
                       f'only be allowed to retrieve PUBLIC files. '
                       f'You can still get any metadata.' )
                raise Exception(msg)
            
    def find(self, jspec, rectype='file', limit=False, format='json'):
        # VALIDATE params @@@
        lim = None if limit is None else (limit or self.limit)
        qstr = urlencode(dict(rectype=rectype,
                              limit=lim,
                              format=format))
        url = f'{self.adsurl}/find/?{qstr}'
        if self.verbose:
            print(f'Search invoking "{url}" with: {jspec}')
        res = requests.post(url, json=jspec)
        res.raise_for_status()
        #! if self.verbose:
        #!     print(f'Find status={res.status_code} res={res.content}')

        if res.status_code != 200:
            raise Exception(res)

        if format == 'csv':
            return(res.content)
        elif format == 'xml':
            return(res.content)
        else: #'json'
            result = res.json()
            info = result.pop(0)
            rows = result
            if self.verbose:
                print(f'info={pf(info)}')
                #print(f'rows={pf(rows)}')
            return(info, rows)

    def search(self, jspec, limit=False, format='json'):
        # VALIDATE params @@@
        qstr = urlencode(dict(limit=None if limit is None else (limit or self.limit),
                              format=format))
        t = 'h' if self.type == Rec.Hdu else 'f'
        url = f'{self.adsurl}/{t}asearch/?{qstr}'
        if self.verbose:
            print(f'Search invoking "{url}" with: {jspec}')
        res = requests.post(url, json=jspec)
        res.raise_for_status()
        if self.verbose:
            print(f'Search status={res.status_code} res={res.content}')

        if res.status_code != 200:
            raise Exception(res)

        if format == 'csv':
            return(res.content)
        elif format == 'xml':
            return(res.content)
        else: #'json'
            result = res.json()
            info = result.pop(0)
            rows = result
            if self.verbose:
                print(f'info={pf(info)} rows={pf(rows)}')
            return(info, rows)

    def vosearch(self, ra, dec, size, limit=100, format='json'):
        t = 'hdu' if self.type == Rec.Hdu else 'img'
        qstr = urlencode(dict(POS=f'{ra},{dec}',
                              SIZE=size,
                              limit=None if limit is None else (limit or self.limit),
                              format=format))
        url = f'{self.siaurl}/vo{t}?{qstr}'
        if self.verbose:
            print(f'Search invoking "{url}" with: ra={ra}, dec={dec}, size={size}')
        res = requests.get(url)
        res.raise_for_status()
        if self.verbose:
            print(f'Search status={res.status_code} res={res.content}')

        if res.status_code != 200:
            raise Exception(f'status={res.status_code} content={res.content}')

        if format == 'json':
            result = res.json()
            info = result.pop(0)
            rows = result
            return(info, rows)
        else:
            return(res.content)


    def check_version(self):
        """Insure this library in consistent with the API version."""
        res = requests.get(f"{self.apiurl}​/version​/")
        res.raise_for_status()
        return(False)

    def get_categoricals(self):
        if self.categoricals is None:
            url = f'{self.adsurl}/cat_lists/'
            res = requests.get(url)
            res.raise_for_status()
            self.categoricals = res.json()  # dict(catname) = [val1, val2, ...]
        return(self.categoricals)

    def get_aux_fields(self, instrument, proctype):
        # @@@ VALIDATE instrument, proctype, type
        t = 'hdu' if self.type == Rec.Hdu else 'file'
        url = f'{self.adsurl}/aux_{t}_fields/{instrument}/{proctype}/'
        res = requests.get(url)
        res.raise_for_status()
        print(f"url={url}; res={res}; content={res.content}")
        return(res.json())

    def get_core_fields(self):
        t = 'hdu' if self.type == Rec.Hdu else 'file'
        # @@@ VALIDATE instrument, proctype, type
        res = requests.get(f'{self.adsurl}/core_{t}_fields/')
        res.raise_for_status()
        return(res.json())

        
class FitsFile(AdaApi):
    def __init__(self, 
                 url='https://astroarchive.noao.edu',
                 verbose=False,
                 limit=10,
                 email=None,  password=None):
        super().__init__(url=url.rstrip("/"), verbose=verbose,
                         email=email, password=password)
        self.type = Rec.File
        self.limit = limit

    def retrieve(self, fileid, local_file_path, hdu=None):
        # VALIDATE params @@@
        
        ## 401 Unauthorized: File is proprietary and logged in user is not authorized.
        ## 403 Forbidden: File is proprietary and user is not logged in.
        ## 404 Not Found: File-ID does not exist in Archive.
        qparams = '' if hdu is None else f'/?hdu={hdu}'
        url = f'{self.apiurl}/retrieve/{fileid}/{qparams}'
        if self.token is None:
            res = requests.get(url)
        else:
            res = requests.get(url, headers=dict(Authorization=self.token))
        try:
            res.raise_for_status()
        except Exception as err:
            print(f"Could not get token: {res}")
            # Get propid so to help figure out why request failed
            info,rows = self.search({"outfields": ["proposal"],
                                     "search":[["md5sum",fileid]]})
            raise Exception(f"{str(err)}"
                            f"; Email={self.email} must be authorized for"
                            f" Proposal={rows[0]['proposal']}")
        
        fullpath = PosixPath(local_file_path).expanduser()
        with open(fullpath,'wb') as fits:
            fits.write(res.content)
        return fullpath

class FitsHdu(AdaApi):
    def __init__(self, 
                 url='https://astroarchive.noao.edu',
                 limit=20,
                 verbose=False,
                 email=None,  password=None):
        super().__init__(url=url.rstrip('/'), verbose=verbose,
                         email=email, password=password)
        self.type = Rec.Hdu
        self.limit = limit

##############################################################################

#@@@ # GET
#@@@ def header​(md5):  # @@@  HTML
#@@@     """Return full FITS headers as HTML."""
#@@@     url="/api​/header​/{md5}​/"
#@@@     pass
#@@@ 
#@@@ # GET
#@@@ def object_lookup​():
#@@@     """Retrieve the RA,DEC coordinates for a given object by name."""
#@@@     url="/api​/object-lookup​/"
#@@@     pass
#@@@ 

#!def version​():
#!    """Get version of this API library."""
#!    url="/api​/version​/"
#!    pass
