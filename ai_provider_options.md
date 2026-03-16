# OpenClaw AI提供商配置方案

由于DeepSeek token不足，需要配置OpenClaw使用其他AI服务。以下是可选的方案：

## 方案1: 使用与Cursor相同的AI服务

### 步骤：
1. 在Cursor中查看AI设置：
   - 打开Cursor，按 `Ctrl+,`
   - 搜索 "AI" 或 "Model"
   - 查看使用的AI服务（OpenAI、Claude、Cursor Cloud等）

2. 获取API密钥（如果显示）：
   - 如果有API密钥，复制它
   - 如果没有，可能需要自己申请

3. 配置OpenClaw：
```bash
# 如果使用OpenAI
openclaw config set model.provider "openai"
openclaw config set openai.apiKey "YOUR_OPENAI_KEY"

# 如果使用Anthropic (Claude)
openclaw config set model.provider "anthropic"
openclaw config set anthropic.apiKey "YOUR_ANTHROPIC_KEY"
```

## 方案2: 使用OpenRouter（推荐）

OpenRouter聚合了多个AI提供商，可能有免费额度：

### 配置：
```bash
# 使用OpenRouter
openclaw config set model.provider "openai"
openclaw config set openai.baseURL "https://openrouter.ai/api/v1"
openclaw config set openai.apiKey "sk-or-v1-xxxxxxxxxxxxxxxxxxxxxxxx"

# 可选：指定模型
openclaw config set openai.model "openai/gpt-3.5-turbo"
```

### 获取OpenRouter API密钥：
1. 访问 https://openrouter.ai
2. 注册账号
3. 获取API密钥
4. 查看免费额度

## 方案3: 使用Google Gemini免费版

Google Gemini有免费额度：

### 配置：
```bash
# 使用Gemini
openclaw config set model.provider "google"
openclaw config set google.apiKey "YOUR_GEMINI_API_KEY"
openclaw config set google.model "gemini-pro"
```

### 获取Gemini API密钥：
1. 访问 https://makersuite.google.com/app/apikey
2. 创建API密钥
3. 免费额度：60次/分钟

## 方案4: 使用Ollama（本地运行）

在本地运行开源模型：

### 安装Ollama：
```bash
# 下载并安装Ollama
# 访问：https://ollama.ai

# 下载模型
ollama pull llama2
ollama pull mistral
```

### 配置OpenClaw：
```bash
# 使用Ollama
openclaw config set model.provider "ollama"
openclaw config set ollama.baseURL "http://localhost:11434"
openclaw config set ollama.model "llama2"
```

## 方案5: 混合使用多个提供商

创建备用机制，当主提供商失败时使用备用：

### 示例配置：
```yaml
# 在OpenClaw配置中设置多个提供商
ai:
  providers:
    - name: "openai"
      priority: 1
      config:
        apiKey: "sk-..."
        model: "gpt-3.5-turbo"
    - name: "gemini"
      priority: 2
      config:
        apiKey: "gemini-key"
        model: "gemini-pro"
    - name: "ollama"
      priority: 3
      config:
        baseURL: "http://localhost:11434"
        model: "llama2"
```

## 方案6: 使用Cursor的配置信息（如果可用）

如果Cursor的配置文件中包含AI服务信息：

### 检查位置：
1. `C:\Users\YKing\AppData\Roaming\Cursor\Local State`
2. `C:\Users\YKing\.cursor\config.json`
3. Cursor设置中的高级配置

### 可能的配置格式：
```json
{
  "ai": {
    "provider": "openai",
    "apiKey": "sk-...",
    "model": "gpt-4"
  }
}
```

## 成本对比

| 提供商 | 免费额度 | 成本/1M tokens | 适合场景 |
|--------|----------|----------------|----------|
| **OpenRouter** | 有 | $0.5-10 | 多种模型选择 |
| **Google Gemini** | 60次/分钟 | 免费(有限) | 日常使用 |
| **Ollama** | 完全免费 | $0 | 本地运行，隐私好 |
| **OpenAI** | 无 | $0.5-30 | 高质量，成本高 |
| **Anthropic** | 无 | $3-30 | 长上下文，成本高 |

## 配置测试脚本

创建测试脚本来验证配置：

```python
# test_ai_config.py
import os
import requests

def test_openai():
    """测试OpenAI配置"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return False
    
    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={"Authorization": f"Bearer {api_key}"},
        json={
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": "Hello"}]
        }
    )
    return response.status_code == 200

# 类似地测试其他提供商...
```

## 立即行动建议

### 优先级1：检查Cursor设置
1. 打开Cursor
2. 按 `Ctrl+,`
3. 告诉我看到的AI配置

### 优先级2：注册OpenRouter（备用）
1. 访问 https://openrouter.ai
2. 注册账号
3. 获取API密钥

### 优先级3：安装Ollama（长期方案）
1. 下载 Ollama
2. 运行 `ollama pull llama2`
3. 测试本地模型

## 配置OpenClaw的完整命令

```bash
# 重启OpenClaw以应用新配置
openclaw gateway restart

# 检查当前模型配置
openclaw config get model

# 设置新模型提供商
openclaw config set model.provider "openai"
openclaw config set openai.apiKey "your-key-here"

# 验证配置
openclaw status
```

## 故障排除

### 常见问题：
1. **API密钥无效**：检查密钥格式和权限
2. **网络连接问题**：检查代理设置
3. **模型不可用**：确认模型名称正确
4. **额度不足**：查看使用量和购买更多额度

### 调试命令：
```bash
# 查看OpenClaw日志
openclaw logs --tail 50

# 测试API连接
curl -X POST https://api.openai.com/v1/chat/completions \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "gpt-3.5-turbo", "messages": [{"role": "user", "content": "Hello"}]}'
```

## 下一步

根据你的选择，我可以帮你：
1. 配置OpenClaw使用特定的AI提供商
2. 创建测试脚本验证连接
3. 设置多个提供商备用机制
4. 监控token使用情况

请告诉我你选择了哪个方案，或者需要更多信息。