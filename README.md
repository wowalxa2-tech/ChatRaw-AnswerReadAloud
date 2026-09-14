# ChatRaw 回答朗读

为 ChatRaw 的助手回答添加小喇叭，点击后通过**阿里云百炼 Qwen-TTS**朗读正文。

**MIT 开源。源码和安装包均公开，下载无需登录 GitHub。** 使用云端语音需要自行配置百炼 API Key，并按阿里云用量计费。

## 下载

- [插件安装包 v1.0.0](https://github.com/wowalxa2-tech/ChatRaw-AnswerReadAloud/releases/download/v1.0.0/answer-read-aloud-1.0.0.zip)
- [ChatRaw 主程序兼容补丁](https://github.com/wowalxa2-tech/ChatRaw-AnswerReadAloud/releases/download/v1.0.0/chatraw-host-read-aloud.patch)
- [SHA-256 校验文件](https://github.com/wowalxa2-tech/ChatRaw-AnswerReadAloud/releases/download/v1.0.0/SHA256SUMS)
- [全部版本](https://github.com/wowalxa2-tech/ChatRaw-AnswerReadAloud/releases)

## 安装

### 1. 检查主程序兼容性

**安装 ZIP 之前先处理这一步。** 插件依赖主程序提供 `ChatRawPlugin.onCleanup`，用于停用、重载、卸载时停止播放和清理监听器。没有该接口的旧版 ChatRaw 无法运行本插件。

本仓库同时提供主程序补丁，基于 [massif-01/ChatRaw 的 b910c45](https://github.com/massif-01/ChatRaw/commit/b910c45d32c37b2f7cd0e5155163368f25baf6e9)。补丁仅修改三个前端文件：增加清理接口，移除重复的 `init()` 调用，并更新编译后的 JS 和资源版本号。

将补丁下载到 ChatRaw 源码根目录，在该目录运行：

```sh
git apply --check chatraw-host-read-aloud.patch
git apply chatraw-host-read-aloud.patch
```

然后按原有方式重新部署或重启 ChatRaw，并刷新页面。补丁已包含编译后的 JS，无需额外运行前端构建。

若检查失败，先核对主程序版本或本地修改，不要强行覆盖。若主程序已经包含清理接口与初始化修复，无需重复应用。此插件面向本仓库标明的 ChatRaw 前端插件架构，不保证适配其他同名分支或 Module / Companion Plugin 架构。

### 2. 安装插件

打开 ChatRaw → **插件 → 本地安装**，上传下载的 `answer-read-aloud-1.0.0.zip`。

也可使用支持源地址安装的 ChatRaw 版本，从下面的公开目录安装：

```text
https://raw.githubusercontent.com/wowalxa2-tech/ChatRaw-AnswerReadAloud/v1.0.0
```

### 3. 配置并试听

打开 **已安装 → 回答朗读 → 设置**：

1. 选择服务地域：北京或新加坡，须与 API Key 所属地域一致。
2. 填入**阿里云百炼 Model Studio API Key**。
3. 选择音色、语言和播放倍速。
4. 点击 **保存并试听**，确认账号权限与实际声音。

使用的是百炼 Qwen-TTS，不是旧版「智能语音交互」的 AppKey / AccessToken，也不是阿里云账号 AccessKey。原来的聊天模型无需更换。

## 功能

- 回答生成结束后显示朗读按钮；播放中可暂停、继续或停止。
- 合成过程中再次点击按钮可取消等待。
- 长回答按句子优先分段，顺序合成与播放，避免超出单次输入限制。
- 当前页面缓存最多 100 段未过期的音频地址，重复朗读可减少重复合成。
- 同时只播放一条回答；切换对话、修改正在朗读的回答、停用插件时停止。
- 音色：Cherry / Serena / Ethan；语言：自动 / 中文 / 英文；播放倍速：0.75–2 倍。
- 中英文设置界面，支持手机布局。

## 数据与费用

只有点击朗读或试听时才会请求云端。朗读提交所选助手回答正文，不提交整段对话、用户问题或独立的思考与工具事件字段。代码块和 Markdown 标记会被清理，复杂公式和表格的朗读效果有限。

密钥使用 ChatRaw 现有后端存储与代理接口，不写入插件源码或 localStorage。浏览器播放云端返回的临时签名 OSS 音频地址。缓存仅存在当前页面内存，刷新或停用后清空。

停止会取消浏览器等待，并阻止后续片段提交；已到达阿里云的请求仍可能完成并计费。长文片段之间可能有等待。本插件不是实时双向语音对话。

## 验证情况

已完成本地 ZIP 安装、14 项模拟浏览器播放测试、2 项后端代理测试，以及设置保存、倍速、手机布局和新回答朗读流程检查。测试的云端响应和音频为模拟数据，**未用真实百炼密钥验收语音质量、账号权限或云端网络可达性**。安装者请通过「保存并试听」完成实际验证。

[测试说明](docs/testing.md) · [阿里云 Qwen-TTS API](https://help.aliyun.com/zh/model-studio/qwen-tts-api)

## 从源码构建安装包

需要 Python 3，无额外依赖：

```sh
python3 scripts/build_release.py
```

生成的安装包、主程序补丁和校验文件位于 `dist/`。插件本身不需要新增 Python 后端依赖。

## 许可与上游

[MIT License](LICENSE)。主程序兼容补丁来源于 [ChatRaw](https://github.com/massif-01/ChatRaw)，保留其许可证及版权声明。
