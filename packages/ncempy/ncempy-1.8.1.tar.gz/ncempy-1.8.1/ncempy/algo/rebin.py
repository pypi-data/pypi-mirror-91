def rebin(im, f, funcType='sum'):
    """ Rebin a 2D array. From stackoverflow:
    https://stackoverflow.com/questions/4624112/grouping-2d-numpy-array-in-average

    This should be used carefully. There is not antialiasing applied which could
    produce odd effects for some data sets (such as high resolution data)

        Parameters
        ----------
            im : ndarray
                2D array to reduce
            f : int
                The factor to rebin by. Must be integer
            funcType : str
                The type of reduction. mean or sum are implemented.

        Returns
        -------
            : ndarray
                The 2D array with the new size.
    """

    nbig = im.shape
    nsmall = [ii // f for ii in im.shape]

    # Reshape the array so that the required neighborhood are in arrays along certain axes
    # Then average or sum those neighborhoods
    im_reshape = im.reshape([nsmall[0], nbig[0] // nsmall[0], nsmall[1], nbig[1] // nsmall[1]])
    # Reduce using different types of functions
    if funcType == 'mean':
        small = im_reshape.mean(3).mean(1)
    elif funcType == 'sum':
        small = im_reshape.sum(3).sum(1)
    # elif funcType == 'median':
    #    small = im_reshape.median(3).median(1)
    else:
        print('defaulting to sum')
        small = im_reshape.sum(3).sum(1)

    return small

if __name__ == '__main__':
    import numpy as np
    aa = np.ones((10, 10))

    bb = rebin(aa, 2, funcType='mean')

    print(bb)