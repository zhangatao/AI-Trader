# 配置系统快速参考

## 🎯 最常用的命令

### 运行项目
```bash
# 使用默认配置
python main.py

# 使用 JSON 配置
python main.py configs/default_config.json

# 并行运行多个模型
python main_parrallel.py

# 只运行特定模型
python main_parrallel.py --signature gpt-4-turbo
```

### 环境变量快速设置
```bash
# 切换到 DeepSeek
export LLM_PROVIDER=deepseek
export DEEPSEEK_API_KEY=sk-xxxxx

# 切换到 OpenAI
export LLM_PROVIDER=openai
export OPENAI_API_KEY=sk-xxxxx

# 运行示例
python CONFIG_EXAMPLES.py
```

## 💻 代码最常用的 API

```python
# 获取配置
from configs import get_config, get_value, get_enabled_models

config = get_config()                              # 完整配置
llm = get_value("llm_provider")                   # 获取值
max_steps = get_value("agent_config.max_steps")  # 嵌套访问
models = get_enabled_models()                     # 列表模型

# 修改配置
from configs import set_value
set_value("agent_config.max_steps", 50)           # 设置值

# 验证配置
from configs import validate
is_valid, errors = validate()                     # 验证配置
```

## 📝 配置文件优先级

1. **环境变量** - 最高优先级 ⬆️
2. **JSON 配置** - 如果指定
3. **Python 默认** - 最低优先级 ⬇️

## 🔑 常用环境变量

```bash
# LLM
LLM_PROVIDER=deepseek|openai|anthropic|google|qwen|minimax
DEEPSEEK_API_KEY=sk-xxxxx
OPENAI_API_KEY=sk-xxxxx

# 数据源
PRIMARY_DATA_SOURCE=yahoo|alphavantage|akshare
ALPHAVANTAGE_API_KEY=xxxxx

# Agent
INIT_DATE=2025-10-01
END_DATE=2025-10-21
```

## 📂 关键文件

| 文件 | 说明 |
|------|------|
| `configs/default_config.py` | Python 配置 |
| `configs/config_manager.py` | 配置管理器 |
| `CONFIG_EXAMPLES.py` | 使用示例 |
| `CONFIG_MIGRATION_GUIDE.md` | 完整指南 |

## ⚡ 3 分钟快速开始

```bash
# 1. 设置 API 密钥
export DEEPSEEK_API_KEY=sk-xxxxx

# 2. 运行项目
python main.py

# 3. 查看结果
# 输出将显示在 ./data/agent_data 中
```

## 🔗 更多资源

- 详细文档: `CONFIG_MIGRATION_GUIDE.md`
- 代码示例: `CONFIG_EXAMPLES.py`
- 配置总结: `CONFIG_UPGRADE_SUMMARY.md`

---

**提示**: 运行 `python CONFIG_EXAMPLES.py` 查看所有实际示例！
