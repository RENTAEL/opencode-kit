# 前端通知集成 / add-frontend-notification

---

## 简介

这个 Skill 用来把轻量级 Butterup Toast 通知接入前端或全栈项目，在前端逻辑需要反馈时生成非阻塞式 Toaster。

**功能介绍**

你可以使用它在保存成功、复制完成、请求失败等需要通知的前端交互中集成 Butterup。场景明确时，Skill 会直接完成接入；场景不明确时，则提供适合当前项目的操作指南和代码片段。

**核心价值**

- 自动识别项目现有的前端结构和样式加载方式，选择合适的接入方法。
- 在行为等价且意图明确时，将简单原生提示或手写通知替换为 Butterup Toast。
- 保留是否修改项目的决定权，不会把确认框、输入框或业务 Modal 主观替换成 Toast。

**适用对象**

- `💻` 前端开发者 — 快速为页面交互补充一致的成功、错误、警告或信息反馈。
- `🧩` 全栈开发者 — 在已有项目中完成通知资产、样式和业务调用的接入。

---

## 功能特性

### 核心功能

- 支持 Vanilla JavaScript、Vite、Webpack、Rollup、React、Vue、Next.js 等浏览器端项目形态。
- 支持基础 Toast、六种显示位置、成功/错误/警告/信息类型、图标、按钮、主题和 Promise 状态通知。
- 在用户给出明确通知场景时直接修改项目并完成集成。
- 在目标场景不明确时先询问；若仍无法确定，则只输出操作指南和可复制代码，不改项目。
- 可识别适合替换的简单 `alert` 或纯通知型手写 Modal，同时保留需要用户决策或输入的交互。

---

## 使用指南

直接描述项目和需要通知的具体交互。信息越明确，Skill 越容易直接完成修改。

### 常用说法速查

| 意图 | 示例话术 | 效果 |
| --- | --- | --- |
| 集成指定通知 | `$add-frontend-notification 在保存设置成功后显示 Toast` | 接入 Butterup，并在明确的保存成功流程中添加通知 |
| 替换简单原生提示 | `$add-frontend-notification 把复制成功后的 alert 替换成 Toast` | 保留原有消息和触发时机，替换等价的非阻塞通知 |
| 扫描可替换提示 | `$add-frontend-notification 检查这个前端项目，把适合的简单通知换成 Butterup` | 扫描现有提示，仅修改可明确判断为通知型的场景 |
| 只要接入指南 | `$add-frontend-notification 告诉我如何在这个 Vue 项目中接入，不要修改文件` | 输出项目适配的步骤和代码片段，不写入项目 |
| 场景尚未确定 | `$add-frontend-notification 我想在这个项目中使用 Butterup` | 先询问通知出现的位置；无法确定时只提供指南与示例 |

### 输出示例

```js
butterup.toast({
  title: '已保存设置',
  location: 'top-right',
  dismissable: false,
  type: 'success',
  duration: 2500,
  icon: true,
})
```

---

## 使用场景

| 场景 | 角色 | 示例问法 | 收益 |
| --- | --- | --- | --- |
| 表单保存反馈 | 前端开发者 | `保存成功或失败时使用 Butterup 提示` | 为异步操作提供清晰、非阻塞的结果反馈 |
| 剪贴板操作反馈 | 浏览器扩展作者 | `复制完成后用 Toast 替换 alert` | 避免原生提示中断用户操作 |
| 现有项目统一通知 | 全栈开发者 | `扫描项目中可替换的简单提示并接入 Butterup` | 在保持业务行为的同时统一通知样式 |
| 框架接入参考 | 项目维护者 | `给我 Next.js 客户端组件里的接入示例` | 获取符合当前项目结构的指南和代码片段 |

---

## 致谢

Butterup 原作者：[dgtlss](https://github.com/dgtlss)，项目来源：[dgtlss/butterup](https://github.com/dgtlss/butterup)。

---
