# DormMate Final

这是 DormMate（宿舍环境助手）项目的工作目录。

## 📁 目录结构

```
DormMate Final/
├── nova-dormmate-final-2026/    # 主项目目录（完整的 DormMate 系统）
│   ├── README.md               # 详细的项目文档
│   ├── requirements.txt        # Python 依赖
│   ├── config.py               # 配置文件
│   ├── simulator/              # 数据模拟器
│   ├── web/                    # Web 看板界面
│   ├── dashboard/              # 仪表盘
│   ├── mobile/                 # 移动端界面
│   ├── analysis/               # 数据分析模块
│   ├── shared/                 # 共享的规则和配置
│   ├── tests/                  # 测试文件
│   ├── docs/                   # 文档
│   └── ...
│
└── archive/                     # 归档的临时文件和早期版本
    ├── docs/                   # 文档和笔记
    ├── patches/                # 补丁脚本
    └── early-versions/         # 早期版本文件
```

## 🚀 快速开始

进入主项目目录查看完整文档：

```bash
cd nova-dormmate-final-2026
# 查看详细的 README
cat README.md
```

## 📖 运行项目

详细的运行说明请参考：[nova-dormmate-final-2026/README.md](nova-dormmate-final-2026/README.md)

简要步骤：
1. 安装依赖：`py -3.14 -m pip install -r nova-dormmate-final-2026/requirements.txt`
2. 启动 Mosquitto Broker
3. 启动数据模拟器
4. 启动 Web 服务器
5. 访问 http://localhost:8000/web/

## 🗂️ Archive 目录说明

`archive/` 目录包含：
- **docs/**: 开发过程中的临时文档和提交记录
- **patches/**: Phase 7 的补丁脚本
- **early-versions/**: 项目早期的简单版本文件

这些文件已归档，不影响主项目运行。

---

**主要项目目录**: [nova-dormmate-final-2026/](nova-dormmate-final-2026/)
