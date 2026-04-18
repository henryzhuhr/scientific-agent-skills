# 训练和微调

## 概述

使用 Trainer API 在自定义数据集上微调预训练模型。训练器处理训练循环、梯度累积、混合精度、日志记录和检查点。

## 基本微调工作流程

### 步骤 1：加载和预处理数据

```python
from datasets import load_dataset

# Load dataset
dataset = load_dataset("yelp_review_full")
train_dataset = dataset["train"]
eval_dataset = dataset["test"]

# Tokenize
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

def tokenize_function(examples):
    return tokenizer(
        examples["text"],
        padding="max_length",
        truncation=True,
        max_length=512
    )

train_dataset = train_dataset.map(tokenize_function, batched=True)
eval_dataset = eval_dataset.map(tokenize_function, batched=True)
```

### 步骤 2：加载模型

```python
from transformers import AutoModelForSequenceClassification

model = AutoModelForSequenceClassification.from_pretrained(
    "bert-base-uncased",
    num_labels=5  # Number of classes
)
```

### 步骤 3：定义指标

```python
import evaluate
import numpy as np

metric = evaluate.load("accuracy")

def compute_metrics(eval_pred):
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=-1)
    return metric.compute(predictions=predictions, references=labels)
```

### 步骤 4：配置训练

```python
from transformers import TrainingArguments

training_args = TrainingArguments(
    output_dir="./results",
    eval_strategy="epoch",
    save_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    num_train_epochs=3,
    weight_decay=0.01,
    logging_dir="./logs",
    logging_steps=10,
    load_best_model_at_end=True,
    metric_for_best_model="accuracy",
)
```

### 步骤 5：创建训练器并训练

```python
from transformers import Trainer

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    compute_metrics=compute_metrics,
)

# Start training
trainer.train()

# Evaluate
results = trainer.evaluate()
print(results)
```

### 步骤 6：保存Model

```python
trainer.save_model("./fine_tuned_model")
tokenizer.save_pretrained("./fine_tuned_model")

# Or push to Hub
trainer.push_to_hub("username/my-finetuned-model")
```

## TrainingArguments 参数

### 基本参数

* *output_dir**：检查点和日志的目录
```python
output_dir="./results"
```

* *num_train_epochs**：训练数量epochs
```python
num_train_epochs=3
```

* *per_device_train_batch_size**：每个GPU/CPU的批量大小
```python
per_device_train_batch_size=8
```

* *learning_rate**：优化器学习rate
```python
learning_rate=2e-5  # Common for BERT-style models
learning_rate=5e-5  # Common for smaller models
```

* *weight_decay**：L2正则化
```python
weight_decay=0.01
```

### 评估和保存

* *eval_strategy**：何时评估（“no”，“steps”， "epoch")
```python
eval_strategy="epoch"  # Evaluate after each epoch
eval_strategy="steps"  # Evaluate every eval_steps
```

* *save_strategy**：何时保存检查点
```python
save_strategy="epoch"
save_strategy="steps"
save_steps=500
```

* *load_best_model_at_end**：加载之后的最佳检查点训练
```python
load_best_model_at_end=True
metric_for_best_model="accuracy"  # Metric to compare
```

### 优化

* *gradient_accumulation_steps**：在多个步骤中累积梯度
```python
gradient_accumulation_steps=4  # Effective batch size = batch_size * 4
```

* *fp16**：启用混合精度（NVIDIA GPU)
```python
fp16=True
```

* *bf16**：启用 bfloat16（较新的 GPU）
```python
bf16=True
```

* *gradient_checkpointing**：交易计算内存
```python
gradient_checkpointing=True  # Slower but uses less memory
```

* *optim**：优化器选择
```python
optim="adamw_torch"  # Default
optim="adamw_8bit"    # 8-bit Adam (requires bitsandbytes)
optim="adafactor"     # Memory-efficient alternative
```

### 学习率调度

* *lr_scheduler_type**：学习率Schedule
```python
lr_scheduler_type="linear"       # Linear decay
lr_scheduler_type="cosine"       # Cosine annealing
lr_scheduler_type="constant"     # No decay
lr_scheduler_type="constant_with_warmup"
```

* *warmup_steps** 或 **warmup_ratio**：预热期
```python
warmup_steps=500
# Or
warmup_ratio=0.1  # 10% of total steps
```

### Logging

* *logging_dir**：TensorBoard 日志目录
```python
logging_dir="./logs"
```

* *logging_steps**：每N步记录一次
```python
logging_steps=10
```

* *report_to**：记录集成
```python
report_to=["tensorboard"]
report_to=["wandb"]
report_to=["tensorboard", "wandb"]
```

### 分布式培训

* *ddp_backend**：分布式后端
```python
ddp_backend="nccl"  # For multi-GPU
```

* *deepspeed**：DeepSpeed配置文件
```python
deepspeed="ds_config.json"
```

## 数据整理器

H处理动态填充和特殊预处理：

### DataCollatorWithPadding

将序列填充到批次中最长的序列：
```python
from transformers import DataCollatorWithPadding

data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    data_collator=data_collator,
)
```

### DataCollatorForLanguageModeling

对于掩码语言建模：
```python
from transformers import DataCollatorForLanguageModeling

data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer,
    mlm=True,
    mlm_probability=0.15
)
```

### DataCollatorForSeq2Seq

用于序列到序列任务：
```python
from transformers import DataCollatorForSeq2Seq

data_collator = DataCollatorForSeq2Seq(
    tokenizer=tokenizer,
    model=model,
    padding=True
)
```

## Custom Training

### Custom Trainer

自定义的重写方法行为：

```python
from transformers import Trainer

class CustomTrainer(Trainer):
    def compute_loss(self, model, inputs, return_outputs=False):
        labels = inputs.pop("labels")
        outputs = model(**inputs)
        logits = outputs.logits

        # Custom loss computation
        loss_fct = torch.nn.CrossEntropyLoss(weight=class_weights)
        loss = loss_fct(logits.view(-1, self.model.config.num_labels), labels.view(-1))

        return (loss, outputs) if return_outputs else loss
```

### 自定义回调

监控训练：

```python
from transformers import TrainerCallback

class CustomCallback(TrainerCallback):
    def on_epoch_end(self, args, state, control, **kwargs):
        print(f"Epoch {state.epoch} completed")
        # Custom logic here
        return control

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    callbacks=[CustomCallback],
)
```

## 高级训练技巧

### 参数高效微调(PEFT)

使用LoRA进行高效微调：

```python
from peft import LoraConfig, get_peft_model

lora_config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["query", "value"],
    lora_dropout=0.05,
    bias="none",
    task_type="SEQ_CLS"
)

model = get_peft_model(model, lora_config)
model.print_trainable_parameters()  # Shows reduced parameter count

# Train normally with Trainer
trainer = Trainer(model=model, args=training_args, ...)
trainer.train()
```

### 梯度检查点

以速度为代价减少内存：

```python
model.gradient_checkpointing_enable()

training_args = TrainingArguments(
    gradient_checkpointing=True,
    ...
)
```

### 混合精度训练

```python
training_args = TrainingArguments(
    fp16=True,  # For NVIDIA GPUs with Tensor Cores
    # or
    bf16=True,  # For newer GPUs (A100, H100)
    ...
)
```

### DeepSpeed Integration

对于非常大的模型：

```python
# ds_config.json
{
  "train_batch_size": 16,
  "gradient_accumulation_steps": 1,
  "optimizer": {
    "type": "AdamW",
    "params": {
      "lr": 2e-5
    }
  },
  "fp16": {
    "enabled": true
  },
  "zero_optimization": {
    "stage": 2
  }
}
```

```python
training_args = TrainingArguments(
    deepspeed="ds_config.json",
    ...
)
```

## 训练提示

### 超参数调优

共同起点：
- **学习率**：对于BERT类模型为2e-5到5e-5，对于较小模型为1e-4到1e-3
- **批量大小**：8-32取决于GPU内存
- **Epochs**：2-4用于微调，更多用于域适应
- **预热**：总步数的10%

使用Optuna进行超参数搜索：

```python
def model_init():
    return AutoModelForSequenceClassification.from_pretrained(
        "bert-base-uncased",
        num_labels=5
    )

def optuna_hp_space(trial):
    return {
        "learning_rate": trial.suggest_float("learning_rate", 1e-5, 5e-5, log=True),
        "per_device_train_batch_size": trial.suggest_categorical("per_device_train_batch_size", [8, 16, 32]),
        "num_train_epochs": trial.suggest_int("num_train_epochs", 2, 5),
    }

trainer = Trainer(model_init=model_init, args=training_args, ...)
best_trial = trainer.hyperparameter_search(
    direction="maximize",
    backend="optuna",
    hp_space=optuna_hp_space,
    n_trials=10,
)
```

### 监控训练

使用TensorBoard：
```bash
tensorboard --logdir ./logs
```

或权重和偏差：
```python
import wandb
wandb.init(project="my-project")

training_args = TrainingArguments(
    report_to=["wandb"],
    ...
)
```

### 恢复训练

简历来自检查点：
```python
trainer.train(resume_from_checkpoint="./results/checkpoint-1000")
```

## 常见问题

* *CUDA内存不足：**
- 减少批量大小
- 启用梯度检查点
- 使用梯度累积
- 使用8位优化器

* *过度拟合：**
- 增加权重衰减
- 添加dropout
- 使用早期停止
- 减少模型大小或训练周期

* *慢速训练：**
- 增加批量大小
- 启用混合精度(fp16/bf16)
- 使用多个 GPU
- 优化数据加载

## 最佳实践

1. **从小处开始**：首先在小数据集子集
2上进行测试。 **使用评估**：监控验证指标
3. **保存检查点**：启用 save_strategy
4. **广泛记录**：使用 TensorBoard 或 W&B
5. **尝试不同的学习率**：从 2e-5
6 开始。 **使用热身**：帮助训练稳定性
7. **启用混合精度**：更快的训练
8. **考虑 PEFT**：对于资源有限的大型模型
