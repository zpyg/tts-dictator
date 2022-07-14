from os import system
from tempfile import NamedTemporaryFile

import numpy as np
import soundfile as sf
import yaml
from paddlespeech.t2s.frontend.zh_frontend import Frontend
from paddlespeech.t2s.models.fastspeech2 import (FastSpeech2,
                                                 FastSpeech2Inference)
from paddlespeech.t2s.models.parallel_wavegan import PWGGenerator, PWGInference
from paddlespeech.t2s.modules.normalizer import ZScore
from playsound import playsound
from yacs.config import CfgNode

import paddle

from .base import Speaker

###### 下载预训练模型
BOOTSTRAPED = 0
if not BOOTSTRAPED:
    system(
        "wget -P download https://paddlespeech.bj.bcebos.com/Parakeet/released_models/pwgan/pwg_baker_ckpt_0.4.zip"
    )
    system("unzip -d download download/pwg_baker_ckpt_0.4.zip")
    system(
        "wget -P download https://paddlespeech.bj.bcebos.com/Parakeet/released_models/fastspeech2/fastspeech2_nosil_baker_ckpt_0.4.zip"
    )
    system("unzip -d download download/fastspeech2_nosil_baker_ckpt_0.4.zip")
##### 初始化模型
fastspeech2_config = "download/fastspeech2_nosil_baker_ckpt_0.4/default.yaml"
fastspeech2_checkpoint = "download/fastspeech2_nosil_baker_ckpt_0.4/snapshot_iter_76000.pdz"
fastspeech2_stat = "download/fastspeech2_nosil_baker_ckpt_0.4/speech_stats.npy"
pwg_config = "download/pwg_baker_ckpt_0.4/pwg_default.yaml"
pwg_checkpoint = "download/pwg_baker_ckpt_0.4/pwg_snapshot_iter_400000.pdz"
pwg_stat = "download/pwg_baker_ckpt_0.4/pwg_stats.npy"
phones_dict = "download/fastspeech2_nosil_baker_ckpt_0.4/phone_id_map.txt"
# 读取 conf 配置文件并结构化
with open(fastspeech2_config) as f:
    fastspeech2_config = CfgNode(yaml.safe_load(f))
with open(pwg_config) as f:
    pwg_config = CfgNode(yaml.safe_load(f))
print("========Config========")
print(fastspeech2_config)
print("---------------------")
print(pwg_config)

frontend = Frontend(phone_vocab_path=phones_dict)

with open(phones_dict, "r") as f:
    phn_id = [line.strip().split() for line in f.readlines()]
vocab_size = len(phn_id)
print("vocab_size:", vocab_size)
odim = fastspeech2_config.n_mels
model = FastSpeech2(idim=vocab_size, odim=odim, **fastspeech2_config["model"])
# 加载预训练模型参数
model.set_state_dict(paddle.load(fastspeech2_checkpoint)["main_params"])
# 推理阶段不启用 batch norm 和 dropout
model.eval()
stat = np.load(fastspeech2_stat)
# 读取数据预处理阶段数据集的均值和标准差
mu, std = stat
mu, std = paddle.to_tensor(mu), paddle.to_tensor(std)
# 构造归一化的新模型
fastspeech2_normalizer = ZScore(mu, std)
fastspeech2_inference = FastSpeech2Inference(fastspeech2_normalizer, model)
fastspeech2_inference.eval()

vocoder = PWGGenerator(**pwg_config["generator_params"])
# 模型加载预训练参数
vocoder.set_state_dict(paddle.load(pwg_checkpoint)["generator_params"])
vocoder.remove_weight_norm()
# 推理阶段不启用 batch norm 和 dropout
vocoder.eval()
# 读取数据预处理阶段数据集的均值和标准差
stat = np.load(pwg_stat)
mu, std = stat
mu, std = paddle.to_tensor(mu), paddle.to_tensor(std)
pwg_normalizer = ZScore(mu, std)
# 构建归一化的模型
pwg_inference = PWGInference(pwg_normalizer, vocoder)
pwg_inference.eval()
print("Parallel WaveGAN done!")


class PaddleSpeech(Speaker):

    def __init__(self, text: str, **tts_args):
        input_ids = frontend.get_input_ids(text,
                                           merge_sentences=True,
                                           print_info=True)
        phone_ids = input_ids["phone_ids"][0]
        with paddle.no_grad():
            mel = fastspeech2_inference(phone_ids)
            wav = pwg_inference(mel)
        self.audio = NamedTemporaryFile(delete=True, suffix='.wav')
        sf.write(self.audio.name,
                 wav.numpy(),
                 samplerate=fastspeech2_config.fs)

    def say(self):
        playsound(self.audio.name)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.audio.close()


with PaddleSpeech("你好，我叫张三") as speaker:
    speaker.say()
