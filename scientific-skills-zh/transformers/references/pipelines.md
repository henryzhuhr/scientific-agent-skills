# Pipeline API 参考

## 概述

Pipelines 提供了使用预训练模型进行推理的最简单方法。它们抽象了标记化、模型加载和后处理，为数十个任务提供统一的接口。

## 基本用法

通过指定任务创建管道：

```python
from transformers import pipeline

# Auto-select default model for task
pipe = pipeline("text-classification")
result = pipe("This is great!")
```

或指定模型：

```python
pipe = pipeline("text-classification", model="distilbert-base-uncased-finetuned-sst-2-english")
```

## 支持任务

### 自然语言处理

* *文本生成**：生成文本延续
```python
generator = pipeline("text-generation", model="gpt2")
output = generator("Once upon a time", max_length=50, num_return_sequences=2)
```

* *文本分类**：将文本分类
```python
classifier = pipeline("text-classification")
result = classifier("I love this product!")  # Returns label and score
```

* *标记分类**：标记单个标记（NER、POS）标记）
```python
ner = pipeline("token-classification", model="dslim/bert-base-NER")
entities = ner("Hugging Face is based in New York City")
```

* *问答**：从上下文中提取答案
```python
qa = pipeline("question-answering")
result = qa(question="What is the capital?", context="Paris is the capital of France.")
```

* *填充掩码**：预测掩码标记
```python
unmasker = pipeline("fill-mask", model="bert-base-uncased")
result = unmasker("Paris is the [MASK] of France")
```

* *总结**：总结长texts
```python
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
summary = summarizer("Long article text...", max_length=130, min_length=30)
```

* *翻译**：在语言之间进行翻译
```python
translator = pipeline("translation_en_to_fr", model="Helsinki-NLP/opus-mt-en-fr")
result = translator("Hello, how are you?")
```

* *零样本分类**：无需训练数据进行分类
```python
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
result = classifier(
    "This is a course about Python programming",
    candidate_labels=["education", "politics", "business"]
)
```

* *情感分析**：别名文本分类专注于情感
```python
sentiment = pipeline("sentiment-analysis")
result = sentiment("This product exceeded my expectations!")
```

### 计算机视觉

* *图像分类**：对图像进行分类
```python
classifier = pipeline("image-classification", model="google/vit-base-patch16-224")
result = classifier("path/to/image.jpg")
# Or use PIL Image or URL
from PIL import Image
result = classifier(Image.open("image.jpg"))
```

* *对象检测**：检测中的对象images
```python
detector = pipeline("object-detection", model="facebook/detr-resnet-50")
results = detector("image.jpg")  # Returns bounding boxes and labels
```

* *图像分割**：分割图像
```python
segmenter = pipeline("image-segmentation", model="facebook/detr-resnet-50-panoptic")
segments = segmenter("image.jpg")
```

* *深度估计**：估计深度images
```python
depth = pipeline("depth-estimation", model="Intel/dpt-large")
result = depth("image.jpg")
```

* *零样本图像分类**：无需训练即可对图像进行分类
```python
classifier = pipeline("zero-shot-image-classification", model="openai/clip-vit-base-patch32")
result = classifier("image.jpg", candidate_labels=["cat", "dog", "bird"])
```

### Audio

* *自动语音识别**：转录peech
```python
asr = pipeline("automatic-speech-recognition", model="openai/whisper-base")
text = asr("audio.mp3")
```

* *audio-classification**：对音频进行分类
```python
classifier = pipeline("audio-classification", model="MIT/ast-finetuned-audioset-10-10-0.4593")
result = classifier("audio.wav")
```

* *text-to-speech**：从文本生成语音（具有特定模型）
```python
tts = pipeline("text-to-speech", model="microsoft/speecht5_tts")
audio = tts("Hello, this is a test")
```

### 多式联运

* *视觉问答**：回答有关图像的问题
```python
vqa = pipeline("visual-question-answering", model="dandelin/vilt-b32-finetuned-vqa")
result = vqa(image="image.jpg", question="What color is the car?")
```

* *文档问答**：回答有关文档的问题
```python
doc_qa = pipeline("document-question-answering", model="impira/layoutlm-document-qa")
result = doc_qa(image="document.png", question="What is the invoice number?")
```

* *图像到文本**：生成标题images
```python
captioner = pipeline("image-to-text", model="Salesforce/blip-image-captioning-base")
caption = captioner("image.jpg")
```

## 管道参数

### 常用参数

* *model**：模型标识符或路径
```python
pipe = pipeline("task", model="model-id")
```

* *device**：GPU 设备索引（-1 表示 CPU，0+ 表示GPU)
```python
pipe = pipeline("task", device=0)  # Use first GPU
```

* *device_map**：大型模型的自动设备分配
```python
pipe = pipeline("task", model="large-model", device_map="auto")
```

* *dtype**：模型精度（减少内存）
```python
import torch
pipe = pipeline("task", torch_dtype=torch.float16)
```

* *batch_size**：一次处理多个输入
```python
pipe = pipeline("task", batch_size=8)
results = pipe(["text1", "text2", "text3"])
```

* *框架**：选择PyTorch或TensorFlow
```python
pipe = pipeline("task", framework="pt")  # or "tf"
```

## 批处理

处理多个输入高效：

```python
classifier = pipeline("text-classification")
texts = ["Great product!", "Terrible experience", "Just okay"]
results = classifier(texts)
```

对于大型数据集，使用生成器或KeyDataset：

```python
from transformers.pipelines.pt_utils import KeyDataset
import datasets

dataset = datasets.load_dataset("dataset-name", split="test")
pipe = pipeline("task", device=0)

for output in pipe(KeyDataset(dataset, "text")):
    print(output)
```

## 性能优化

### GPU加速

始终为GPU指定设备用法：
```python
pipe = pipeline("task", device=0)
```

### 混合精度

在支持的 GPU 上使用 float16 实现 2 倍加速：
```python
import torch
pipe = pipeline("task", torch_dtype=torch.float16, device=0)
```

### 批处理指南

- **CPU**：通常跳过批处理
- **具有可变长度的GPU**：可能会降低效率
- **具有相似长度的GPU**：显着加速
- **实时应用程序**：跳过批处理（增加延迟）

```python
# Good for throughput
pipe = pipeline("task", batch_size=32, device=0)
results = pipe(list_of_texts)
```

### 流输出

对于文本生成，生成时流令牌：

```python
from transformers import TextStreamer

generator = pipeline("text-generation", model="gpt2", streamer=TextStreamer())
generator("The future of AI", max_length=100)
```

## 自定义管道配置

分别指定标记器和模型：

```python
from transformers import AutoTokenizer, AutoModelForSequenceClassification

tokenizer = AutoTokenizer.from_pretrained("model-id")
model = AutoModelForSequenceClassification.from_pretrained("model-id")
pipe = pipeline("text-classification", model=model, tokenizer=tokenizer)
```

使用自定义管道类：

```python
from transformers import TextClassificationPipeline

class CustomPipeline(TextClassificationPipeline):
    def postprocess(self, model_outputs, **kwargs):
        # Custom post-processing
        return super().postprocess(model_outputs, **kwargs)

pipe = pipeline("text-classification", model="model-id", pipeline_class=CustomPipeline)
```

## 输入格式

管道接受各种输入类型：

* *文本任务**：字符串或字符串列表
```python
pipe("single text")
pipe(["text1", "text2"])
```

* *图像任务**：URL、文件路径、PIL 图像或 numpy数组
```python
pipe("https://example.com/image.jpg")
pipe("local/path/image.png")
pipe(PIL.Image.open("image.jpg"))
pipe(numpy_array)
```

* *音频任务**：文件路径、numpy 数组或原始波形
```python
pipe("audio.mp3")
pipe(audio_array)
```

## 错误处理

处理通用问题：

```python
try:
    result = pipe(input_data)
except Exception as e:
    if "CUDA out of memory" in str(e):
        # Reduce batch size or use CPU
        pipe = pipeline("task", device=-1)
    elif "does not appear to have a file named" in str(e):
        # Model not found
        print("Check model identifier")
    else:
        raise
```

## 最佳实践

1. **使用管道进行原型设计**：无需样板即可快速迭代
2. **明确指定型号**：默认型号可能会更改
3. **可用时启用 GPU**：显着加速
4. **使用批处理来提高吞吐量**：处理许多输入时
5. **考虑内存使用**：对于大批量使用 float16 或更小的模型
6. **本地缓存模型**：避免重复下载
