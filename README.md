# pairwise-mastering-limiter

母带限幅在鼓点密集段落出现泵动，lookahead 只按采样点数固定，采样率切到 96k 后预读时间缩短一半；true peak 用 sample peak 近似，母带转码后 inter-sample 过载；attack 时间按毫秒硬编码但内部按采样点计数，44.1k 与 48k 释放曲线不同；立体声左右通道独立限幅，中央人声在右声道重击时向左偏移；限幅后没做延迟补偿，视频口型比声音早几毫秒；32bit float 输入被降到 16bit 再限幅，低电平细节先丢；dither 在限幅前加，噪声被压成颗粒；5.1 下混时中置声道被重复计入左右，对白偏响；过采样滤波器在段落切换时没重置，边界出现滴答；性能档把 oversampling 关掉，true peak 表仍显示安全。audio/mastering_limiter.py 是核心，tests/test_mastering_limiter.py 15个红。要修的是：lookahead 按时间换算采样点；true peak 过采样检测；attack/release 按采样率重算；立体声联动增益；限幅后延迟补偿；全链路 float；dither 放最后；下混按声道矩阵；段落切换重置滤波器；降级仍过采样检测。

## 运行

```bash
python -m pytest tests -q
```

初始状态：15 个用例失败。修复实现使全部用例通过，不要修改 `tests/` 下的测试。

子方向：见平台；任务类型：Bugfix；语言/框架：Python 3, pytest；环境可复现等级：无外部依赖。
