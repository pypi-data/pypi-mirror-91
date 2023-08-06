from imutils import face_utils
import imutils
import numpy as np
import collections
import dlib
import cv2
import skimage.draw
import scipy as sp
import scipy.spatial
from PIL import Image
import os
from math import sqrt, ceil, floor

from PIL import Image


class Tile(object):
    """Represents a single tile."""

    def __init__(self, image, number, position, coords, filename=None):
        self.image = image
        self.number = number
        self.position = position
        self.coords = coords
        self.filename = filename

    @property
    def row(self):
        return self.position[0]

    @property
    def column(self):
        return self.position[1]

    def generate_filename(
        self, directory=os.getcwd(), prefix="tile", format="png", path=True
    ):
        """Construct and return a filename for this tile."""
        filename = prefix + "_{col:02d}_{row:02d}.{ext}".format(
            col=self.column, row=self.row, ext=format.lower().replace("jpeg", "jpg")
        )
        if not path:
            return filename
        return os.path.join(directory, filename)

    def save(self, filename=None, format="png"):
        if not filename:
            filename = self.generate_filename(format=format)
        self.image.save(filename, format)
        self.filename = filename

    def __repr__(self):
        """Show tile number, and if saved to disk, filename."""
        if self.filename:
            return "<Tile #{} - {}>".format(
                self.number, os.path.basename(self.filename)
            )
        return "<Tile #{}>".format(self.number)


class Face_cropper:
    def __init__(self, dlib_descriptor_filepath):
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor(dlib_descriptor_filepath)

    def crop_out_lips(self, filename):
        img = cv2.imread(filename)
        try:
            rect = self.detector(img)[0]
            sp = self.predictor(img, rect)
            landmarks = np.array([[p.x, p.y] for p in sp.parts()])
            outline = landmarks[[
                x + 48 for x in range(12)]+[48]+[x + 60 for x in range(8)]]
            Y, X = skimage.draw.polygon(outline[:, 1], outline[:, 0])
            cropped_img = np.zeros(img.shape, dtype=np.uint8)
            cropped_img[Y, X] = img[Y, X]
            result_rgb = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2RGB)
            return Image.fromarray(result_rgb)
        except IndexError:
            return False

    def crop_face_without_lips(self, filename):
        img = cv2.imread(filename)
        try:
            rect = self.detector(img)[0]
            sp = self.predictor(img, rect)
            landmarks = np.array([[p.x, p.y] for p in sp.parts()])
            outline = landmarks[[
                x + 48 for x in range(12)]+[48]+[x + 60 for x in range(8)]]
            Y, X = skimage.draw.polygon(outline[:, 1], outline[:, 0])
            img[Y, X] = 0
            result_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            return Image.fromarray(result_rgb)
        except IndexError:
            return False

    def isolate_mouth(self, filename, mouth_only=True, preImg=None):
        try:
            if preImg is None:
                img = cv2.imread(filename)
                #img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                dets = self.detector(img, 1)
            else:
                pil_image = preImg.convert('RGB')
                open_cv_image = np.array(pil_image)
                img = open_cv_image
                dets = self.detector(open_cv_image, 1)
            #print("Number of faces detected: {}".format(len(dets)))
            #result_rgb = False

            for k, d in enumerate(dets):
                # print("Detection {}: Left: {} Top: {} Right: {} Bottom: {}".format(
                #   k, d.left(), d.top(), d.right(), d.bottom()))
                # Get the landmarks/parts for the face in box d.
                shape = self.predictor(img, d)
                # The next lines of code just get the coordinates for the mouth
                # and crop the mouth from the image.This part can probably be optimised
                # by taking only the outer most points.
                xmouthpoints = [shape.part(x).x for x in range(48, 67)]
                ymouthpoints = [shape.part(x).y for x in range(48, 67)]
                maxx = max(xmouthpoints)
                minx = min(xmouthpoints)
                maxy = max(ymouthpoints)
                miny = min(ymouthpoints)

                pad = 10
                crop_image = img.copy()
                if mouth_only:
                    crop_image = crop_image[miny -
                                            pad:maxy+pad, minx-pad:maxx+pad]
                else:
                    crop_image[0:miny-pad, 0::] = 0  # haut
                    crop_image[maxy+pad::, 0::] = 0  # bas
                    crop_image[0::, 0:minx - pad] = 0  # gauche
                    crop_image[0::, maxx+pad::] = 0  # droite
                result_rgb = cv2.cvtColor(crop_image, cv2.COLOR_BGR2RGB)
            if len(dets) > 0:
                return Image.fromarray(result_rgb)
            return False
        except IndexError:
            return False

    def isolate_eye(self, filename, eye_only=True, preImg=None):
        try:
            if preImg is None:
                img = cv2.imread(filename)
                #img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                dets = self.detector(img, 1)
            else:
                pil_image = preImg.convert('RGB')
                open_cv_image = np.array(pil_image)
                img = open_cv_image
                dets = self.detector(open_cv_image, 1)
            #print("Number of faces detected: {}".format(len(dets)))
            #result_rgb = False

            for k, d in enumerate(dets):
                # print("Detection {}: Left: {} Top: {} Right: {} Bottom: {}".format(
                #   k, d.left(), d.top(), d.right(), d.bottom()))
                # Get the landmarks/parts for the face in box d.
                shape = self.predictor(img, d)
                # The next lines of code just get the coordinates for the mouth
                # and crop the mouth from the image.This part can probably be optimised
                # by taking only the outer most points.
                xmouthpoints = [shape.part(x).x for x in range(18, 27)]
                ymouthpoints = [shape.part(x).y for x in range(37, 48)]
                maxx = max(xmouthpoints)
                minx = min(xmouthpoints)
                maxy = max(ymouthpoints)
                miny = min(ymouthpoints)

                pad = 10
                crop_image = img.copy()
                if eye_only:
                    crop_image = crop_image[miny -
                                            pad:maxy+pad, minx-pad:maxx+pad]
                else:
                    crop_image[0:miny-pad, 0::] = 0  # haut
                    crop_image[maxy+pad::, 0::] = 0  # bas
                    crop_image[0::, 0:minx - pad] = 0  # gauche
                    crop_image[0::, maxx+pad::] = 0  # droite
                result_rgb = cv2.cvtColor(crop_image, cv2.COLOR_BGR2RGB)
            if len(dets) > 0:
                return Image.fromarray(result_rgb)
            return False
        except IndexError:
            return False

    def calc_columns_rows(self, n):
        """
        Calculate the number of columns and rows required to divide an image
        into ``n`` parts.
        Return a tuple of integers in the format (num_columns, num_rows)
        """

        num_columns = int(ceil(sqrt(n)))
        num_rows = int(ceil(n / float(num_columns)))
        return (num_columns, num_rows)

    def get_combined_size(self, tiles):
        """Calculate combined size of tiles."""
        # TODO: Refactor calculating layout to avoid repetition.
        columns, rows = calc_columns_rows(len(tiles))
        tile_size = tiles[0].image.size
        return (tile_size[0] * columns, tile_size[1] * rows)

    def join(self, tiles, width=0, height=0):
        """
        @param ``tiles`` - Tuple of ``Image`` instances.
        @param ``width`` - Optional, width of combined image.
        @param ``height`` - Optional, height of combined image.
        @return ``Image`` instance.
        """
        # Don't calculate size if width and height are provided
        # this allows an application that knows what the
        # combined size should be to construct an image when
        # pieces are missing.

        if width > 0 and height > 0:
            im = Image.new("RGBA", (width, height), None)
        else:
            im = Image.new("RGBA", get_combined_size(tiles), None)
        columns, rows = calc_columns_rows(len(tiles))
        for tile in tiles:
            try:
                im.paste(tile.image, tile.coords)
            except IOError:
                # do nothing, blank out the image
                continue
        return im

    def validate_image(self, image, number_tiles):
        """Basic sanity checks prior to performing a split."""
        TILE_LIMIT = 99 * 99

        try:
            number_tiles = int(number_tiles)
        except BaseException:
            raise ValueError("number_tiles could not be cast to integer.")

        if number_tiles > TILE_LIMIT or number_tiles < 2:
            raise ValueError(
                "Number of tiles must be between 2 and {} (you \
                            asked for {}).".format(
                    TILE_LIMIT, number_tiles
                )
            )

    def validate_image_col_row(self, image, col, row):
        """Basic checks for columns and rows values"""
        SPLIT_LIMIT = 99

        try:
            col = int(col)
            row = int(row)
        except BaseException:
            raise ValueError(
                "columns and rows values could not be cast to integer.")

        if col < 1 or row < 1 or col > SPLIT_LIMIT or row > SPLIT_LIMIT:
            raise ValueError(
                f"Number of columns and rows must be between 1 and"
                f"{SPLIT_LIMIT} (you asked for rows: {row} and col: {col})."
            )
        if col == 1 and row == 1:
            raise ValueError(
                "There is nothing to divide. You asked for the entire image.")

    def slice_img(self,
                  filename=None,
                  pre_img=None,
                  number_tiles=None,
                  col=None,
                  row=None,
                  DecompressionBombWarning=False,
                  ):
        """
        Split an image into a specified number of tiles.
        Args:
        filename (str):  The filename of the image to split.
        number_tiles (int):  The number of tiles required.
        Kwargs:
        save (bool): Whether or not to save tiles to disk.
        DecompressionBombWarning (bool): Whether to suppress
        Pillow DecompressionBombWarning
        Returns:
            Tuple of :class:`Tile` instances.
        """
        if DecompressionBombWarning is False:
            Image.MAX_IMAGE_PIXELS = None

        if pre_img is None:
            im = Image.open(filename)
        else:
            im = pre_img
        im_w, im_h = im.size

        columns = 0
        rows = 0
        if number_tiles:
            validate_image(im, number_tiles)
            columns, rows = calc_columns_rows(number_tiles)
        else:
            validate_image_col_row(im, col, row)
            columns = col
            rows = row

        tile_w, tile_h = int(floor(im_w / columns)), int(floor(im_h / rows))

        tiles = []
        number = 1
        # -rows for rounding error.
        for pos_y in range(0, im_h - rows, tile_h):
            for pos_x in range(0, im_w - columns, tile_w):  # as above.
                area = (pos_x, pos_y, pos_x + tile_w, pos_y + tile_h)
                image = im.crop(area)
                position = (int(floor(pos_x / tile_w)) + 1,
                            int(floor(pos_y / tile_h)) + 1)
                coords = (pos_x, pos_y)
                tile = Tile(image, number, position, coords)
                tiles.append(tile)
                number += 1

        return tuple(tiles)

    def save_tiles(self, tiles, prefix="", directory=os.getcwd(), format="png"):
        """
        Write image files to disk. Create specified folder(s) if they
        don't exist. Return list of :class:`Tile` instance.
        Args:
        tiles (list):  List, tuple or set of :class:`Tile` objects to save.
        prefix (str):  Filename prefix of saved tiles.
        Kwargs:
        directory (str):  Directory to save tiles. Created if non-existant.
        Returns:
            Tuple of :class:`Tile` instances.
        """
        for tile in tiles:
            tile.save(
                filename=tile.generate_filename(
                    prefix=prefix, directory=directory, format=format
                ),
                format=format,
            )
        return tuple(tiles)

    def get_image_column_row(self, filename):
        """Determine column and row position for filename."""
        row, column = os.path.splitext(filename)[0][-5:].split("_")
        return (int(column) - 1, int(row) - 1)

    def open_images_in(self, directory):
        """Open all images in a directory. Return tuple of Tile instances."""

        files = [
            filename
            for filename in os.listdir(directory)
            if "_" in filename and not filename.startswith("joined")
        ]
        tiles = []
        if len(files) > 0:
            i = 0
            for file in files:
                pos = get_image_column_row(file)
                im = Image.open(os.path.join(directory, file))

                position_xy = [0, 0]
                count = 0
                for a, b in zip(pos, im.size):
                    position_xy[count] = a * b
                    count = count + 1
                tiles.append(
                    Tile(
                        image=im,
                        position=pos,
                        number=i + 1,
                        coords=position_xy,
                        filename=file,
                    )
                )
                i = i + 1
        return tiles


# Change version number and run :
# python3 setup.py sdist bdist_wheel (build it all)
# python3 -m twine upload --repository-url https://upload.pypi.org/legacy/  dist/* (launch to web)