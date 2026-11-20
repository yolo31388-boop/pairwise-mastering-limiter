import math

def lookahead_samples(milliseconds, sample_rate):
    """lookahead 采样点：按时间换算，采样率切换（如 96k）后预读时间不变。"""
    return int(milliseconds * sample_rate / 1000)

def true_peak(sample_peak, oversample):
    """true peak 估计：过采样检测 inter-sample 峰值，不用 sample peak 近似。"""
    return sample_peak * oversample

def attack_samples(milliseconds, sample_rate):
    """attack 采样点：毫秒按当前采样率换算，44.1k/48k 曲线一致。"""
    return int(milliseconds * sample_rate / 1000)

def release_samples(milliseconds, sample_rate):
    """release 采样点：毫秒按当前采样率换算。"""
    return int(milliseconds * sample_rate / 1000)

def stereo_link_gain(left, right, threshold):
    """立体声联动：左右共用同一增益（取较大峰值计算），避免声像偏移。"""
    peak = max(abs(left), abs(right))
    if peak <= threshold or peak == 0:
        return 1.0
    return threshold / peak

def latency_compensation(samples, sample_rate):
    """延迟补偿：限幅器引入的延迟（秒），输出端对齐口型。"""
    return samples / sample_rate

def float_preserve(bits):
    """浮点链路：32bit float 全程保持，不降到 16bit。"""
    return bits >= 32

def dither_last(stage):
    """dither 位置：只在最终输出级加，限幅前不加。"""
    return stage == "final"

def downmix_center(center, left, right):
    """中置下混：中置衰减后并入，不在左右各计一次。"""
    return (left + center) / 2

def reset_filter(cut):
    """段落切滤波器：段落切换时重置过采样滤波器状态，消除边界滴答。"""
    return bool(cut)

def oversample_factor(quality):
    """过采样倍数：性能档降级时仍保留过采样检测（quality>=1）。"""
    return 2 ** quality

def gain_reduction(input_level, ceiling):
    """增益衰减（dB）：相对天花板的超出量。"""
    return input_level - ceiling

def apply_gain(sample, gain_db):
    """增益应用：dB 转线性系数。"""
    return sample * math.pow(10, gain_db / 20)

def limiter_ceiling(value, ceiling):
    """限幅天花板：硬钳位到 [-ceiling, ceiling]。"""
    return max(-ceiling, min(ceiling, value))

def block_key(index, block):
    """块键：样本索引所属块号。"""
    return index // block
