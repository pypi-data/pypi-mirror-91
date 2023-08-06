__copyright__ = """

    Copyright 2019 Samapriya Roy

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

"""
__license__ = "Apache 2.0"

#! /usr/bin/env python
import pkg_resources
import requests
import argparse,os,ee,sys,platform,subprocess,time
os.chdir(os.path.dirname(os.path.realpath(__file__)))
from bs4 import BeautifulSoup
from os.path import expanduser
if str(platform.system().lower()) == "windows":
    version =sys.version_info[0]
    try:
        import pipwin
        if pipwin.__version__=='0.5.0':
            pass
        else:
            subprocess.call('python'+str(version)+' -m pip install pipwin==0.5.0', shell=True)
            subprocess.call('pipwin refresh', shell=True)
        '''Check if the pipwin cache is old: useful if you are upgrading porder on windows
        [This section looks if the pipwin cache is older than two weeks]
        '''
        home_dir = expanduser("~")
        fullpath=os.path.join(home_dir, ".pipwin")
        file_mod_time = os.stat(fullpath).st_mtime
        if int((time.time() - file_mod_time) / 60) > 20160:
            print('Refreshing your pipwin cache')
            subprocess.call('pipwin refresh', shell=True)
    except ImportError:
        subprocess.call('python'+str(version)+' -m pip install pipwin==0.5.0', shell=True)
        subprocess.call('pipwin refresh', shell=True)
    except Exception as e:
        print(e)
    try:
        import gdal
    except ImportError:
        subprocess.call('pipwin install gdal', shell=True)
    except Exception as e:
        print(e)
    try:
        import pandas
    except ImportError:
        subprocess.call('pipwin install pandas', shell=True)
    except Exception as e:
        print(e)
    try:
        import pyproj
    except ImportError:
        subprocess.call('pipwin install pyproj', shell=True)
    except Exception as e:
        print(e)
    try:
        import shapely
    except ImportError:
        subprocess.call('pipwin install shapely', shell=True)
    except Exception as e:
        print(e)
    try:
        import fiona
    except ImportError:
        subprocess.call('pipwin install fiona', shell=True)
    except Exception as e:
        print(e)
    try:
        import geopandas
    except ImportError:
        subprocess.call('pipwin install geopandas', shell=True)
    except Exception as e:
        print(e)
from .batch_uploader import upload
from .sel_tuploader import seltabup
from .zipfiles import zipshape
from .getmeta import getmeta
lpath=os.path.dirname(os.path.realpath(__file__))
sys.path.append(lpath)


# Get package version
def geeup_version():
    url = "https://pypi.org/project/geeup/"
    source = requests.get(url)
    html_content = source.text
    soup = BeautifulSoup(html_content, "html.parser")
    company = soup.find("h1")
    if (
        not pkg_resources.get_distribution("geeup").version
        == company.string.strip().split(" ")[-1]
    ):
        print(
            "\n"
            + "========================================================================="
        )
        print(
            "Current version of geeup is {} upgrade to lastest version: {}".format(
                pkg_resources.get_distribution("geeup").version,
                company.string.strip().split(" ")[-1],
            )
        )
        print(
            "========================================================================="
        )

geeup_version()

def update():
    if str(platform.system().lower()) =="windows":
        os.system("python sel-latest-win.py")
    elif str(platform.system().lower()) =="linux":
        os.system("python sel-latest-linux.py")
    elif str(platform.system().lower()) =="darwin":
        os.system("python sel-latest-mac.py")
    else:
        print("Architecture not recognized")
def init_from_parser(args):
    update()

def selsetup():
    os.system("python sel_setup.py")

def selsetup_from_parser(args):
    selsetup()

suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
def humansize(nbytes):
    i = 0
    while nbytes >= 1024 and i < len(suffixes)-1:
        nbytes /= 1024.
        i += 1
    f = ('%.2f' % nbytes).rstrip('0').rstrip('.')
    return '%s %s' % (f, suffixes[i])

def quota(project):
    ee.Initialize()
    if project is not None:
        try:
            if not project.endswith('/'):
                project = project+'/'
            else:
                project = project
            project_detail= ee.data.getAsset(project)
            print("")
            if 'sizeBytes' in project_detail['quota']:
                print('Used {} of {}'.format(humansize(int(project_detail['quota']['sizeBytes'])),(humansize(int(project_detail['quota']['maxSizeBytes'])))))
            else:
                print('Used 0 of {}'.format(humansize(int(project_detail['quota']['maxSizeBytes']))))
            if 'assetCount' in project_detail['quota']:
                print('Used {:,} assets of {:,} total'.format(int(project_detail['quota']['assetCount']),int(project_detail['quota']['maxAssetCount'])))
            else:
                print('Used 0 assets of {:,} total'.format(int(project_detail['quota']['maxAssetCount'])))
        except Exception as e:
            print(e)
    else:
        for roots in ee.data.getAssetRoots():
            quota = ee.data.getAssetRootQuota(roots["id"])
            print("")
            print(
                "Root assets path: {}".format(
                    roots["id"].replace("projects/earthengine-legacy/assets/", "")
                )
            )
            print(
                "Used {} of {}".format(
                    humansize(quota["asset_size"]["usage"]),
                    humansize(quota["asset_size"]["limit"]),
                )
            )
            print(
                "Used {:,} assets of {:,} total".format(
                    quota["asset_count"]["usage"], quota["asset_count"]["limit"]
                )
            )


def quota_from_parser(args):
    quota(project=args.project)

def zipshape_from_parser(args):
    zipshape(directory=args.input,export=args.output)

def getmeta_from_parser(args):
    getmeta(indir=args.input,mfile=args.metadata)

def _comma_separated_strings(string):
  """Parses an input consisting of comma-separated strings.
     Slightly modified version of: https://pypkg.com/pypi/earthengine-api/f/ee/cli/commands.py
  """
  error_msg = 'Argument should be a comma-separated list of alphanumeric strings (no spaces or other' \
              'special characters): {}'
  values = string.split(',')
  for name in values:
      if not name.isalnum():
          raise argparse.ArgumentTypeError(error_msg.format(string))
  return values

def upload_from_parser(args):
    upload(user=args.user,
           source_path=args.source,
           destination_path=args.dest,
           metadata_path=args.metadata,
           nodata_value=args.nodata)

def seltabup_from_parser(args):
    seltabup(uname=args.user,
           dirc=args.source,
           destination=args.dest)
def tasks():
    ee.Initialize()
    statuses = ee.data.listOperations()
    st = []
    for status in statuses:
        st.append(status["metadata"]["state"])
    print("Tasks Running: " + str(st.count("RUNNING")))
    print("Tasks Pending: " + str(st.count("PENDING")))
    print("Tasks Completed: " + str(st.count("SUCCEEDED")))
    print("Tasks Failed: " + str(st.count("FAILED")))
    print("Tasks Cancelled: " + str(st.count("CANCELLED")+st.count("CANCELLING")))

def tasks_from_parser(args):
    tasks()

def delete(ids):
    try:
        print('Recursively deleting path: {}'.format(ids))
        subprocess.call('earthengine --no-use_cloud_api rm -r '+ids)
    except Exception as e:
        print(e)
def delete_collection_from_parser(args):
    delete(args.id)

spacing="                               "
def main(args=None):
    parser = argparse.ArgumentParser(description='Simple Client for Earth Engine Uploads with Selenium Support')

    subparsers = parser.add_subparsers()

    parser_init=subparsers.add_parser('init',help='Initializes the tool by downloading and updating selenium drivers for firefox')
    parser_init.set_defaults(func=init_from_parser)

    parser_selsetup = subparsers.add_parser('selsetup', help='Non headless setup for new google account, use if upload throws errors')
    parser_selsetup.set_defaults(func=selsetup_from_parser)

    parser_quota = subparsers.add_parser(
        "quota", help="Print Earth Engine total quota and used quota"
    )
    optional_named = parser_quota.add_argument_group("Optional named arguments")
    optional_named.add_argument(
        "--project",
        help="Project Name usually in format projects/project-name/assets/",
        default=None,
    )
    parser_quota.set_defaults(func=quota_from_parser)

    parser_zipshape = subparsers.add_parser('zipshape', help='Zips all shapefiles and subsidary files into individual zip files')
    required_named = parser_zipshape.add_argument_group('Required named arguments.')
    required_named.add_argument('--input', help='Path to the input directory with all shape files', required=True)
    required_named.add_argument('--output', help='Destination folder Full path where shp, shx, prj and dbf files if present in input will be zipped and stored', required=True)
    parser_zipshape.set_defaults(func=zipshape_from_parser)

    parser_getmeta = subparsers.add_parser('getmeta', help='Creates a generalized metadata for rasters in folder')
    required_named = parser_getmeta.add_argument_group('Required named arguments.')
    required_named.add_argument('--input', help='Path to the input directory with all raster files', required=True)
    required_named.add_argument('--metadata', help='Full path to export metadata.csv file', required=True)
    parser_getmeta.set_defaults(func=getmeta_from_parser)

    parser_upload = subparsers.add_parser('upload', help='Batch Asset Uploader using Selenium')
    required_named = parser_upload.add_argument_group('Required named arguments.')
    required_named.add_argument('--source', help='Path to the directory with images for upload.', required=True)
    required_named.add_argument('--dest', help='Destination. Full path for upload to Google Earth Engine, e.g. users/pinkiepie/myponycollection', required=True)
    required_named.add_argument('-m', '--metadata', help='Path to CSV with metadata.',required=True)
    optional_named = parser_upload.add_argument_group('Optional named arguments')
    optional_named.add_argument('--nodata', type=int, help='The value to burn into the raster as NoData (missing data)')
    required_named.add_argument('-u', '--user', help='Google account name (gmail address).')

    parser_upload.set_defaults(func=upload_from_parser)

    parser_seltabup = subparsers.add_parser('seltabup', help='Batch Table Uploader using Selenium.')
    required_named = parser_seltabup.add_argument_group('Required named arguments.')
    required_named.add_argument('--source', help='Path to the directory with zipped folder for upload.', required=True)
    required_named.add_argument('--dest', help='Destination. Full path for upload to Google Earth Engine, e.g. users/pinkiepie/myponycollection', required=True)
    required_named.add_argument('-u', '--user', help='Google account name (gmail address).')
    parser_seltabup.set_defaults(func=seltabup_from_parser)

    parser_tasks=subparsers.add_parser('tasks',help='Queries current task status [completed,running,ready,failed,cancelled]')
    parser_tasks.set_defaults(func=tasks_from_parser)

    parser_delete = subparsers.add_parser('delete', help='Deletes collection and all items inside. Supports Unix-like wildcards.')
    parser_delete.add_argument('id', help='Full path to asset for deletion. Recursively removes all folders, collections and images.')
    parser_delete.set_defaults(func=delete_collection_from_parser)

    args = parser.parse_args()

    try:
        func = args.func
    except AttributeError:
        parser.error("too few arguments")
    func(args)

if __name__ == '__main__':
    main()
