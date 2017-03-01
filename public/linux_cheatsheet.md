# Linux Cheatsheet
## Set up python3 environment
Install `git`, `pip`, and `vim`.
```bash
sudo apt-get install git python3-pip vim
```

### Data analysis and visualization
Install `jsonlines`, `pandas`, `numpy`, and `ggplot`.
```bash
sudo python3 -m pip install jsonlines pandas numpy ggplot
```

### SciKit machine learning tools, iPython, Anaconda envrionments
```bash
sudo python3 -m pip install scikit-learn ipykernel conda
```

### Geospatial packages and Python libraries
```bash
sudo apt-get install binutils libproj-dev gdal-bin libgeos-dev
```
Check the versions of the latest `matplotlib` `basemap` toolkit from their GitHub Releases page: https://github.com/matplotlib/basemap/releases. If it is >=1.1.0, simply install basemap with `pip`:
```shell
sudo python3 -m pip install basemap
```
Otherwise, download the `tar.gz` archive of the latest version, likely 1.0.7. Unzip this, navigate to the directory, and open the `setup.py` file in an editor, because in `basemap-1.0.7`, we need to make a change. The newer GEOS library doesn't have the C++ libraries (`libgeos.so`, `geos.so`, etc.), instead only has the C lirbaries (`libgeos_c.so`, `geos_c.so`), and the basemap-1.0.7 release install file looks for the C++ library. To fix this, modify `setup.py` line 86 to remove this bit of code:
```python
libraries=['geos_c', 'geos']))
```
to
```python
libraries=['geos_c']))
```
This is the last bit of a larger code block that tells Python which GEOS library file to look for:
```python
extensions = [Extension("mpl_toolkits.basemap._proj",deps+['src/_proj.c'],include_dirs = ['src'],)]
# can't install _geoslib in mpl_toolkits.basemap namespace,
# or Basemap objects won't be pickleable.
if sys.platform == 'win32':
# don't use runtime_library_dirs on windows (workaround
# for a distutils bug - http://bugs.python.org/issue2437).
    #extensions.append(Extension("mpl_toolkits.basemap._geoslib",['src/_geoslib.c'],
    extensions.append(Extension("_geoslib",['src/_geoslib.c'],
                                library_dirs=geos_library_dirs,
                                include_dirs=geos_include_dirs,
                                libraries=['geos']))
else:
    #extensions.append(Extension("mpl_toolkits.basemap._geoslib",['src/_geoslib.c'],
    extensions.append(Extension("_geoslib",['src/_geoslib.c'],
                                library_dirs=geos_library_dirs,
                                runtime_library_dirs=geos_library_dirs,
                                include_dirs=geos_include_dirs,
                                libraries=['geos_c']))
```
Finally, install `basemap`
```bash
sudo python3 setup.py install
```
