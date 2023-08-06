import json
import operator
import zipfile
from collections import MutableSequence

import cv2
import numpy as np
import requests

from rbx.manifest.utils import px_to_int, make_white_image, make_transparent_image
from ..clients.aws import S3Bucket
from ..exceptions import FatalException


class ManifestHandler:

    def __init__(self, bucket=None, region=None):
        self.client = None
        if bucket and region:
            self.client = S3Bucket(name=bucket, region=region)
        self.base_url = None

    def build_image_from_manifest(self, manifest_url):
        """Given the location of a manifest, generate the image creative and return it.

        Parameters:
            manifest_url (str):
                The location of the manifest to download and build image from.

        Returns:
            list:
                An iterable containing the final image, build from the manifest.
        """
        manifest = self.get_manifest(manifest_url)

        final_image = Creative(manifest, self.client).render()

        return [final_image]

    def get_manifest(self, url):
        """Retrieve Manifest from HTTP or S3 (expecting a JSON format) and return the decoded dict.

        Parameters:
            url (str):
                The location of the manifest to retrieve.

        Returns:
            dict:
                The decoded JSON, stored as a dict.
        """
        if self.client is None:
            response = requests.get(url)
            if not response.status_code == 200:
                raise FatalException(
                    "Manifest Not Found At Specified Location: {}".format(url)
                )
            try:
                manifest = response.json()
            except json.decoder.JSONDecodeError:
                raise FatalException("Manifest has an invalid format: {}".format(url))

        else:
            manifest_data = self.client.get_key(url)
            if manifest_data is None:
                raise FatalException(
                    "Manifest Not Found At Specified Location: {}/{}".format(self.client.name, url)
                )
            try:
                file_content = manifest_data.get()['Body'].read()
                manifest = json.loads(file_content)
            except UnicodeDecodeError:
                raise FatalException("Manifest has an invalid format: {}".format(url))

        self.base_url = manifest.get('base_url')
        if self.base_url.startswith('//'):
            self.base_url = 'http:{}'.format(self.base_url)
        return manifest


class ComponentSequence(MutableSequence):
    """A mutable sequence of components."""

    def __init__(self):
        self.components = []

    def __len__(self):
        """The length includes the length of its components."""
        length = len(self.components)
        for component in self.components:
            length += len(component)
        return length

    def __getitem__(self, key):
        return self.components[key]

    def __setitem__(self, key, value):
        self.components[key] = value

    def __delitem__(self, key):
        del self.components[key]

    def append(self, component, base_url, client=None):
        result = make_component(component, base_url, client)
        self.components.append(result)

    def insert(self, value):
        self.components.insert(value)


class Creative:

    def __init__(self, manifest, client=None):
        super(Creative, self).__init__()
        self.manifest = manifest
        self.base_url = manifest.get('base_url')
        self.client = client

        root = manifest.get('root_component')
        self.height = px_to_int(root['css']['height'])
        self.width = px_to_int(root['css']['width'])
        self.left = px_to_int(root['css']['left'])
        self.top = px_to_int(root['css']['top'])

        self.root_component = make_component(root, self.base_url, self.client)

    def render(self):
        """Builds an opencv image representation of the manifest and return.

        We start by making a white canvas, whose size is defined by the root component. We then
        call the render function of the root component, which should call the nested render
        functions of all sub components. This image is then ready to be applied to the final white
        canvas.

        Returns:
            ndarray:
                An opencv representation of the final image.
        """
        root_image = make_white_image(
            height=self.height,
            width=self.width
        )

        built_image = self.root_component.render()

        # merge the final image generated from the root_component with the initial canvas
        final_image = merge_images(
            background_image=root_image,
            overlay_image=built_image,
            left=self.left,
            top=self.top,
        )
        return final_image


class Component(ComponentSequence):

    def __init__(self, component, base_url, client=None):
        super(Component, self).__init__()
        self.base_url = base_url
        self.client = client
        self.top = px_to_int(component['css']['top'])
        self.left = px_to_int(component['css']['left'])
        self.height = px_to_int(component['css']['height'])
        self.width = px_to_int(component['css']['width'])
        self.z_index = component['css']['z-index']


class LayoutComponent(Component):
    """A Component which has child Component."""

    def __init__(self, component, base_url, client=None):
        """Initialises the ImageComponent.

        For a LayoutComponent, we need to add the child components that it has underneath it.

        Args:
            component (dict): The details of the component.
            base_url (str): The http url where the component is hosted.
            client (S3Bucket): The S3 client to use instead of http, if needed.
        """
        super(LayoutComponent, self).__init__(
            component=component,
            base_url=base_url,
            client=client
        )
        children = component.get('component_manifests')

        for child_component in children:
            self.append(child_component, self.base_url, self.client)

    def render(self):
        """Builds an opencv image representation of the manifest and return.

        As a layout contains one or more children that need to be positioned relative to each
        other, a transparent image is generated and each child component is applied in z-index
        order.

        Returns:
            ndarray:
                An opencv representation of the retrieved image,
        """
        # these images won't all necessarily overlap cleanly, so we need a transparent image to
        # stick them to
        composite_image = make_transparent_image(self.height, self.width)
        # now we can apply all the images, starting with the lowest z-index and increasing
        for entry in sorted(self.components, key=operator.attrgetter("z_index")):
            merge_images(
                background_image=composite_image,
                overlay_image=entry.render(),
                left=entry.left,
                top=entry.top,
            )

        return composite_image


class ImageComponent(Component):
    """A component that describes an image."""

    def __init__(self, component, base_url, client=None):
        """Initialises the ImageComponent, storing the location of the Image file.

        Args:
            component (dict): The details of the component.
            base_url (str): The http url where the component is hosted.
            client (S3Bucket): The S3 client to use instead of http, if needed.
        """
        super(ImageComponent, self).__init__(
            component=component,
            base_url=base_url,
            client=client
        )
        self.url = component.get('url')
        self.ext = component.get('ext')

    def render(self):
        """Retrieve Image from http or S3, decode it using opencv and return the decoded image.

        Returns:
            ndarray:
                An opencv representation of the retrieved image,
        """
        if self.client is None:
            response = requests.get(f'{self.base_url}{self.url}{self.ext}')
            if not response.status_code == 200:
                raise FatalException(
                    f"Image Not Found At Specified Location: {self.base_url}{self.url}{self.ext}"
                )
            img_data = response.content
        else:
            image = self.client.get_key(f'{self.url}{self.ext}')
            if image is None:
                raise FatalException(
                    f"Image Not Found At Specified Location: "
                    f"{self.client.name}/{self.url}{self.ext}"
                )
            img_data = image.get()['Body'].read()

        decoded_image = cv2.imdecode(np.asarray(bytearray(img_data)), cv2.IMREAD_UNCHANGED)
        # if the image fails to be read, then it will be None
        if decoded_image is None:
            raise FatalException(
                "Image has an invalid format: {}{}{}".format(
                    self.client.name + '/' if self.client else self.base_url,
                    self.url,
                    self.ext
                ),
            )
        return decoded_image


def make_component(component, base_url, client=None):
    """Takes a component and returns the appropriate sub-component.

    Args:
        component (dict): The details of the component.
        base_url (str): The http url where the component is hosted.
        client (S3Bucket): The S3 client to use instead of http, if needed.

    Returns:
        any:
            A instance of a component sub-type.

    """
    component_type = component.get('component_type')

    if component_type == 'layout':
        return LayoutComponent(component, base_url, client)

    elif component_type == 'image':
        return ImageComponent(component, base_url, client)


def merge_images(background_image, overlay_image, left, top):
    """Puts the overlay image on top of the background image.

    Will use the left and top to calculate the position of the overlay image relative to the
    background image. Any transparency the top image has will be applied, showing the background
    image where applicable.

    This logic was sourced from https://stackoverflow.com/questions/14063070/14102014#14102014 with
    minor modifications to fit our needs.

    Parameters:
        background_image (ndarray):
            The opencv representation of the background image, on which the new image will apply.
        overlay_image (ndarray):
            The opencv representation of the overlay image, which is placed over background image.
        left (int):
            How far, in pixels, from the left the overlay image should be applied.
        top (int):
            How far, in pixels, from the top the overlay image should be applied.

    Returns:
        ndarray:
            An opencv representation of the combined image.
    """
    try:
        # reposition overlay image
        y1, y2 = top, top + overlay_image.shape[0]
        x1, x2 = left, left + overlay_image.shape[1]

        # blend alpha channels
        alpha_s = overlay_image[:, :, 3] / 255.0
        alpha_l = 1.0 - alpha_s

        # apply overlay image to background image
        for c in range(0, 3):
            background_image[y1:y2, x1:x2, c] = (
                alpha_s * overlay_image[:, :, c] + alpha_l * background_image[y1:y2, x1:x2, c]
            )

    except IndexError:
        # if there is no alpha channel, the process of overlapping images is different
        background_image[
            top:top + overlay_image.shape[0], left:left + overlay_image.shape[1]
        ] = overlay_image

    return background_image


def zip_images(images, filename='out'):
    """Combine all images in the iterable to a ZIP format and write to specified filename.

        Parameters:
        images (iterable):
            An iterable, containing ndarray entries representing opencv images.
        filename (str):
            The name of the zip file to output.

    """
    zipf = zipfile.ZipFile('{}.zip'.format(filename), 'w', zipfile.ZIP_DEFLATED)
    for image in images:
        retval, buf = cv2.imencode('.png', image)
        zipf.writestr('final_image.png', buf)
