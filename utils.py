import os
import torch
from transformers import BertModel, BertTokenizer
import onnxruntime as ort

# 模型名称
model_name = 'bert-base-chinese'
onnx_model_path = 'bert-base-chinese.onnx'

# 检查是否存在 ONNX 模型文件
if not os.path.exists(onnx_model_path):
    print(f"{onnx_model_path} 不存在，正在下载并转换为 ONNX 格式...")

    # 加载预训练的 BERT 模型和分词器
    tokenizer = BertTokenizer.from_pretrained(model_name)
    model = BertModel.from_pretrained(model_name)

    # 创建示例输入，供模型导出时使用
    inputs = tokenizer("这是一个示例句子。", return_tensors="pt")

    # 将 PyTorch 模型转换为 ONNX
    torch.onnx.export(
        model,
        (inputs['input_ids']),
        onnx_model_path,
        input_names=['input_ids'],
        output_names=['output'],
        dynamic_axes={'input_ids': {0: 'batch_size', 1: 'sequence_length'}, 
                      'output': {0: 'batch_size', 1: 'sequence_length'}}
    )

    print(f"{model_name} 模型已转换为 ONNX 格式并保存到 {onnx_model_path}")

else:
    print(f"{onnx_model_path} 已存在，跳过下载和转换.")

# 加载 ONNX 模型
print("BERT模型加载中...")
session = ort.InferenceSession(onnx_model_path)
print("BERT模型加载完毕.")

def load_vocab(vocab_file):
    vocab = {}
    with open(vocab_file, 'r', encoding='utf-8') as infile:
        for index, line in enumerate(infile):
            token = line.strip()
            vocab[token] = index
    return vocab

def tokenize(text, vocab):
    input_ids = []
    for char in text:
        token = char
        if token in vocab:
            input_ids.append(vocab[token])
        else:
            # 使用 "[UNK]" 替代未知字符
            if "[UNK]" in vocab:
                input_ids.append(vocab["[UNK]"])
            else:
                # 如果没有UNK替代，返回空列表
                return []
    return input_ids

def get_bert_embedding(text, session, vocab):
    # 将字符串分割为单个汉字
    input_ids = tokenize(text, vocab)
    input_ids = [input_ids]  # 将其包装为二维列表

    ort_inputs = {session.get_inputs()[0].name: input_ids}
    ort_outs = session.run(None, ort_inputs)

    return ort_outs[0]

def syn_judge(s1, s2, session, vocab, threshold=0.707, debug=False):
    vec1 = get_bert_embedding(s1, session, vocab).flatten()
    vec2 = get_bert_embedding(s2, session, vocab).flatten()
    cos_similarity = cosine_similarity(vec1, vec2)
    if debug:
        print(f"Consine Similarity: {cos_similarity}")
    return cos_similarity >= threshold

def cosine_similarity(vec1, vec2):
    # 计算余弦相似度
    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    norm_a = sum(a ** 2 for a in vec1) ** 0.5
    norm_b = sum(b ** 2 for b in vec2) ** 0.5
    return dot_product / (norm_a * norm_b)

vocab = load_vocab("./vocab.txt")

if __name__ == "__main__":
    sentence1 = "你好"
    sentence2 = "您好"
    while 1:
        sentence1 = input("词语/句子1: ")
        if sentence1 == "exit":
            break
        sentence2 = input("词语/句子2: ")
        
        print(f"Sentence 1: {sentence1}")
        print(f"Sentence 2: {sentence2}")
        
        # 判断相似度是否超过阈值
        if syn_judge(sentence1, sentence2, session, vocab, debug=True):
            print("The sentences are similar.")
        else:
            print("The sentences are not similar.")
