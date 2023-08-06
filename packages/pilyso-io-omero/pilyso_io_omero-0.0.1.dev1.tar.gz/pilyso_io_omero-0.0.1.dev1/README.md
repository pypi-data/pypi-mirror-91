# pilyso-io-omero

Plugin for [`pilyso-io`](https://github.com/modsim/pilyso-io), allowing for access of image data stored on
[OMERO](https://www.openmicroscopy.org/omero/) image storage servers.

Load the module using the `PILYSO_IO_MODULES` environment variable:

```bash
> PILYSO_IO_MODULES=omero python yourscript.py
```

Adds the `omero://` and `omeros://` schemes:

```python

ims = ImageStack("omero://username:password@server.example.com/image/123")

# or

ims = ImageStack("omero://username:password@server.example.com/dataset/456")
```
 
If you do not want to type in the OMERO username or password into the console, the environment variables `OMERO_USER` or `OMERO_PASSWORD` can be used, respectively.

## License

By importing `omero`, GPL.