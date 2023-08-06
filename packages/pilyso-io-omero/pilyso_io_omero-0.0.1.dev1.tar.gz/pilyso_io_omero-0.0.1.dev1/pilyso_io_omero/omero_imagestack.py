import os
from urllib.parse import urlunparse
import getpass

from pilyso_io.imagestack import ImageStack, Dimensions


class OMEROImageStack(ImageStack):
    schemes = ('omero', 'omeros')

    priority = 500

    def open(self, location, **kwargs):

        username = location.username

        if username is None:
            if 'OMERO_USER' in os.environ:
                username = os.environ['OMERO_USER']
            else:
                print("Please enter username to connect to %s:" % urlunparse(location))
                username = input()
                print(repr(username))

        passwd = location.password

        if passwd is None:
            if 'OMERO_PASSWORD' in os.environ:
                passwd = os.environ['OMERO_PASSWORD']
            else:
                print("Please enter password to connect to %s:" % urlunparse(location))
                passwd = getpass.getpass()

        if location.port:
            port = int(location.port)
        else:
            port = 4064

        from omero.gateway import BlitzGateway

        connection_kwargs = dict(username=username, passwd=passwd, host=location.hostname, port=port,
                                 useragent='OMEROImageStack', secure=True)

        #print(connection_kwargs)

        self._conn = BlitzGateway(**connection_kwargs)
        self._conn.connect()

        path_split = location.path.split('/')

        if path_split[1] == 'image':
            image_ids = [int(path_split[2])]
        elif path_split[1] == 'dataset':
            dataset_id = int(path_split[2])
            dataset = self._conn.getObject('Dataset', dataset_id)
            image_ids = [child.child.id for child in dataset.getChildLinks()]
        else:
            raise RuntimeError('Unsupported path fragment passed.')

        self._omero_images = [self._conn.getObject('Image', image_id) for image_id in image_ids]
        self._omero_primary_pixels = [image.getPrimaryPixels() for image in self._omero_images]

        image = self._omero_images[0]

        self.set_dimensions_and_sizes(
            [Dimensions.PositionXY, Dimensions.Time, Dimensions.Channel, Dimensions.PositionZ],
            [len(self._omero_images), image.getSizeT(), image.getSizeC(), image.getSizeZ()]
        )

        _, self._global_metadata, self._series_metadata = image.loadOriginalMetadata()

        self._global_metadata, self._series_metadata = dict(self._global_metadata), dict(self._series_metadata)

        # this likely only works for imported ND2 files

        self._timepoints = {}
        for k, v in self._series_metadata.items():
            if k.startswith('timestamp #'):
                self._timepoints[int(k.split('timestamp #')[1])] = v

        # some files seem to have X/Y coordinates (stage), some not ...

    def __del__(self):
        # self.conn.close()
        pass

    def get_data(self, what):
        return self._omero_primary_pixels[what[Dimensions.PositionXY]].getPlane(
            theZ=what.get(Dimensions.PositionZ, 0),
            theC=what[Dimensions.Channel],
            theT=what[Dimensions.Time]
        )

    def get_meta(self, what):
        image = self._omero_images[what[Dimensions.PositionXY]]
        nan = float('nan')

        position = self.__class__.Position(x=nan, y=nan, z=nan)

        try:
            index = what[Dimensions.PositionXY] + what[Dimensions.Time] * self.size[Dimensions.PositionXY]
            time = self._timepoints[index]
        except KeyError:
            time = nan

        meta = self.__class__.Metadata(
            time=float(time),
            position=position,
            calibration=image.getPixelSizeX(units="MICROMETER")._value)

        return meta
