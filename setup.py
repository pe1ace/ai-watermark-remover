from setuptools import setup, find_packages

setup(
    name="ai-watermark-remover",
    version="1.0.0",
    author="你的名字",
    author_email="你的邮箱",
    description="基于LaMa深度学习模型的AI图片去水印工具",
    # 这里加上 encoding="utf-8"
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/pe1ace/ai-watermark-remover",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    # 这里也加上 encoding="utf-8"
    install_requires=open("requirements.txt", encoding="utf-8").read().splitlines(),
    entry_points={
        "console_scripts": [
            "watermark-remover=watermark_remover.cli:cli",
        ],
    },
)