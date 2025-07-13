from ai_model.model import Generator
from torch.autograd import Variable
from torchvision.utils import save_image
import torch
import torch.nn.functional as F
import numpy as np
import os
import time
import datetime


class Solver(object):
    def __init__(self, celeba_loader, rafd_loader, config):
        self.config = config

        # Data loader.
        self.celeba_loader = celeba_loader
        self.rafd_loader = rafd_loader

        # Model configurations.
        self.c_dim = config.c_dim
        self.c2_dim = config.c2_dim
        self.image_size = config.image_size
        self.g_conv_dim = config.g_conv_dim
        self.d_conv_dim = config.d_conv_dim
        self.g_repeat_num = config.g_repeat_num
        self.d_repeat_num = config.d_repeat_num
        self.lambda_cls = config.lambda_cls
        self.lambda_rec = config.lambda_rec
        self.lambda_gp = config.lambda_gp

        # Training configurations.
        self.dataset = config.dataset
        self.batch_size = config.batch_size
        self.num_iters = config.num_iters
        self.num_iters_decay = config.num_iters_decay
        self.g_lr = config.g_lr
        self.d_lr = config.d_lr
        self.n_critic = config.n_critic
        self.beta1 = config.beta1
        self.beta2 = config.beta2
        self.resume_iters = config.resume_iters
        self.selected_attrs = config.selected_attrs

        # Test configurations.
        self.test_iters = config.test_iters

        # Miscellaneous.
        self.use_tensorboard = config.use_tensorboard
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

        # Directories.
        self.log_dir = config.log_dir
        self.sample_dir = config.sample_dir
        self.model_save_dir = config.model_save_dir
        self.result_dir = config.result_dir

        # Step size.
        self.log_step = config.log_step
        self.sample_step = config.sample_step
        self.model_save_step = config.model_save_step
        self.lr_update_step = config.lr_update_step

        # Build the model and tensorboard.
        self.build_model()
        if self.use_tensorboard:
            self.build_tensorboard()

    def build_model(self):
        if self.dataset in ['CelebA', 'RaFD']:
            self.G = Generator(self.g_conv_dim, self.c_dim, self.g_repeat_num)
        elif self.dataset in ['Both']:
            self.G = Generator(self.g_conv_dim, self.c_dim + self.c2_dim + 2, self.g_repeat_num)

        self.g_optimizer = torch.optim.Adam(self.G.parameters(), self.g_lr, [self.beta1, self.beta2])
        self.print_network(self.G, 'G')

        self.G.to(self.device)

    def print_network(self, model, name):
        num_params = 0
        for p in model.parameters():
            num_params += p.numel()
        # print(model)
        # print(name)
        # print("The number of parameters: {}".format(num_params))

    def restore_model(self, resume_iters):
        G_path = os.path.join(self.model_save_dir, '{}-G.ckpt'.format(resume_iters))
        self.G.load_state_dict(torch.load(G_path, map_location=lambda storage, loc: storage))

    def build_tensorboard(self):
        from ai_model.logger import Logger
        self.logger = Logger(self.log_dir)

    def denorm(self, x):
        out = (x + 1) / 2
        return out.clamp_(0, 1)

    def create_labels(self, c_org, c_dim=5, dataset='CelebA', selected_attrs=None):
        if dataset == 'CelebA':
            hair_color_indices = []
            for i, attr_name in enumerate(selected_attrs):
                if attr_name in ['Black_Hair', 'Blond_Hair', 'Brown_Hair', 'Gray_Hair']:
                    hair_color_indices.append(i)

        c_trg_list = []
        for i in range(c_dim):
            if dataset == 'CelebA':
                c_trg = c_org.clone()
                if i in hair_color_indices:
                    c_trg[:, i] = 1
                    for j in hair_color_indices:
                        if j != i:
                            c_trg[:, j] = 0
                else:
                    c_trg[:, i] = (c_trg[:, i] == 0)
            elif dataset == 'RaFD':
                c_trg = self.label2onehot(torch.ones(c_org.size(0)) * i, c_dim)

            c_trg_list.append(c_trg.to(self.device))
        return c_trg_list

    def test(self):
        self.restore_model(self.test_iters)

        result_path = None

        with torch.no_grad():
            for x_real, _ in self.celeba_loader:
                x_real = x_real.to(self.device)

                if hasattr(self, 'config') and hasattr(self.config, 'target_attr') and self.config.target_attr:
                    attr_idx = self.selected_attrs.index(self.config.target_attr)
                    c_trg = torch.zeros(1, len(self.selected_attrs))
                    c_trg[0, attr_idx] = 1
                    c_trg = c_trg.to(self.device)

                    x_fake = self.G(x_real, c_trg)
                    result_filename = f'result_{os.path.basename(self.config.input_image)}'
                    result_path = os.path.join(self.result_dir, result_filename)
                    save_image(self.denorm(x_fake.data.cpu()), result_path, nrow=1, padding=0)
                    break

        return result_path