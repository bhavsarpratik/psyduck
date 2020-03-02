from tensorflow.python.client import device_lib


def set_tensorflow_device(device='cpu'):
    """Forcing device."""

    if device == 'cpu':
        os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
    elif device == 'gpu':
        os.environ['CUDA_VISIBLE_DEVICES'] = '1'

    print('Checking device.')
    print(device_lib.list_local_devices())
