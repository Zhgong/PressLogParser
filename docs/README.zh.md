# PressLogParser

一个用于解析 Festo 压力机日志文件的简单工具，提供可交互的曲线图形界面。

## 安装

项目使用 [Poetry](https://python-poetry.org/) 管理依赖：

```bash
pip install poetry
poetry install
```

## 运行

使用 Streamlit 启动应用：

```bash
poetry run streamlit run app.py
```

运行后，应用会以列表形式显示文件头部的元数据，而非表格。

## 测试

执行单元测试：

```bash
poetry run pytest
```

## 项目结构

```
app.py             # Streamlit 应用入口
src/               # 日志解析与可视化代码
tests/             # 单元测试
pyproject.toml     # Poetry 配置
```

## 功能简介

- 解析日志中 `[Recorded curves]` 部分的记录
- 仅从前四行头部提取元数据，字段包括 Part no.、Program name、Part ID、Timestamp、
  Result、Max. position、Max. force、NOK source、MAC Address、Serial number
- 计算并展示采样间隔及速度曲线
- 通过 Plotly 在 Streamlit 中交互式显示数据
