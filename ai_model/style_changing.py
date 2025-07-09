import os
import torch
from PIL import Image
from torchvision import transforms as T
from model import Generator

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

class StyleTransfer:
    def __init__(self, model_path, c_dim=11):
        self.c_dim = c_dim
        self.transform = T.Compose([
            T.Resize(128),
            T.ToTensor(),
            T.Normalize(mean=(0.5, 0.5, 0.5), std=(0.5, 0.5, 0.5))
        ])

        self.G = Generator(conv_dim=64, c_dim=c_dim, repeat_num=6).to(device)
        self.G.load_state_dict(torch.load(model_path, map_location=device))
        self.G.eval()

    def transfer(self, image_path, selected_attrs):
        attr_list = ['Black_Hair', 'Blond_Hair', 'Brown_Hair', 'Male', 'Young',
                     'Heavy_Makeup', 'Eyeglasses', 'Attractive', 'Bald',
                     'Wearing_Lipstick', 'Goatee']

        c = torch.zeros(1, self.c_dim)
        for attr in selected_attrs:
            if attr in attr_list:
                idx = attr_list.index(attr)
                c[0, idx] = 1

        image = Image.open(image_path).convert('RGB')
        image = self.transform(image).unsqueeze(0).to(device)
        c = c.to(device)

        with torch.no_grad():
            output = self.G(image, c)
            output = (output + 1) / 2

        return T.ToPILImage()(output.squeeze().cpu())


def transfer_style(content_path, selected_attrs, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    model_path = os.path.join(
        os.path.dirname(__file__),
        'stargan_celeba_128/models/200000-G.ckpt'
    )

    st = StyleTransfer(model_path)
    result = st.transfer(content_path, selected_attrs)

    result_path = os.path.join(output_dir, f'result_{os.path.basename(content_path)}')
    result.save(result_path)

    return result_path