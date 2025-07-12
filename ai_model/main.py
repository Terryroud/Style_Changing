import os
from ai_model.solver import Solver
from ai_model.data_loader import get_loader
from torch.backends import cudnn


def str2bool(v):
    return v.lower() in ('true')


def main(config):
    cudnn.benchmark = True

    if not os.path.exists(config.log_dir):
        os.makedirs(config.log_dir)
    if not os.path.exists(config.model_save_dir):
        os.makedirs(config.model_save_dir)
    if not os.path.exists(config.sample_dir):
        os.makedirs(config.sample_dir)
    if not os.path.exists(config.result_dir):
        os.makedirs(config.result_dir)

    # Data loader.
    celeba_loader = None
    rafd_loader = None

    if config.dataset in ['CelebA', 'Both']:
        celeba_loader = get_loader(config.celeba_image_dir, config.attr_path, config.selected_attrs,
                                   config.celeba_crop_size, config.image_size, config.batch_size,
                                   'CelebA', config.mode, config.num_workers)
    if config.dataset in ['RaFD', 'Both']:
        rafd_loader = get_loader(config.rafd_image_dir, None, None,
                                 config.rafd_crop_size, config.image_size, config.batch_size,
                                 'RaFD', config.mode, config.num_workers)

    solver = Solver(celeba_loader, rafd_loader, config)

    if config.mode == 'test':
        if config.input_image:
            temp_attr_path = os.path.join(config.result_dir, 'temp_attr.txt')
            with open(temp_attr_path, 'w') as f:
                f.write("1\n")

            celeba_loader = get_loader(config.input_image, temp_attr_path,
                                       config.selected_attrs,
                                       config.celeba_crop_size, config.image_size,
                                       1, config.dataset, config.mode, config.num_workers)

            solver = Solver(celeba_loader, None, config)
            result_path = solver.test()
            os.remove(temp_attr_path)
            return result_path
        else:
            solver.test()
    return None

def Transfer(target_attr, image_path):
    class Config:
        pass

    # Model configuration
    config = Config()
    config.c_dim = 5
    config.c2_dim = 8
    config.celeba_crop_size = 178
    config.rafd_crop_size = 256
    config.image_size = 128
    config.g_conv_dim = 64
    config.d_conv_dim = 64
    config.g_repeat_num = 6
    config.d_repeat_num = 6
    config.lambda_cls = 1
    config.lambda_rec = 10
    config.lambda_gp = 10

    # Training configuration
    config.dataset = 'CelebA'
    config.batch_size = 1
    config.num_iters = 200000
    config.num_iters_decay = 100000
    config.g_lr = 0.0001
    config.d_lr = 0.0001
    config.n_critic = 5
    config.beta1 = 0.5
    config.beta2 = 0.999
    config.resume_iters = None
    config.selected_attrs = ['Black_Hair', 'Blond_Hair', 'Brown_Hair', 'Male', 'Young']

    # Test configuration
    config.test_iters = 200000
    config.target_attr = target_attr

    # Miscellaneous
    config.num_workers = 1
    config.mode = 'test'
    config.use_tensorboard = True

    # Directories
    config.celeba_image_dir = image_path
    config.input_image = image_path
    config.attr_path = 'ai_model/stargan_celeba_128/list_attr_celeba.txt'
    config.rafd_image_dir = 'data/RaFD/train'
    config.log_dir = 'ai_model/stargan_celeba_128/logs'
    config.model_save_dir = 'ai_model/stargan_celeba_128/models_5'
    config.sample_dir = 'starstargan_celeba_128gan/samples'
    config.result_dir = 'ai_model/stargan_celeba_128/results'


    # Step size
    config.log_step = 10
    config.sample_step = 1000
    config.model_save_step = 10000
    config.lr_update_step = 1000

    main(config)

    result_filename = f'result_{os.path.basename(image_path)}'
    result_path = os.path.join(config.result_dir, result_filename)

    from PIL import Image
    return Image.open(result_path)