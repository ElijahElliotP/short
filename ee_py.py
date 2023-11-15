def requestRectangle(image, point, x_dim, y_dim, crsCode, prefix='p_', scale=10, file_format="GEO_TIFF"):
    """
    Wrapper for ee.data.computePixels(); requires module 'math'
    See: https://developers.google.com/earth-engine/apidocs/ee-data-computepixels
    image = target image
    point = point to get ['coordinates'] from
    type = one of 'coords' ([]) or 'feat'
    (x/y)_dim = width and height of image, in metres
    crsCode = text string EPSG code
    prefix = all images file names will begin with this string. default is 'point_
    scale = resolution, default is '10'
    file_format = default is 'GEO_TIFF'
    example: requestRectangle(clear_montreal_imgs.median(),Map.draw_features[3], 1200, 1200, 'EPSG:32618')
    """
    project = ee.Projection(crsCode)
    point = point.geometry(1, project).getInfo()['coordinates']
    filename = f"{prefix}{point[0]}_{point[1]}.tif"

    request = {
        'expression': image,
        'fileFormat': file_format,
        'grid': {
            'dimensions': {
                'width': math.ceil(x_dim / scale),
                'height': math.ceil(y_dim / scale)
            },
            'affineTransform': {
                'scaleX': scale,
                'shearX': 0,
                'translateX': point[0] - x_dim / 2,
                'shearY': 0,
                'scaleY': -scale,
                'translateY': point[1] + y_dim / 2
            },
            'crsCode': crsCode,
        }
    }
    
    image_returned = ee.data.computePixels(request)

    with open(file=filename, mode='wb') as f:
        f.write(image_returned)
    print(point)
