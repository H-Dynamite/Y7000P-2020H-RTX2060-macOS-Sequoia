# 联想拯救者 Y7000P 2020H · RTX 2060 内屏直连 · macOS Sequoia

Lenovo Legion Y7000P 2020H / i7-10875H / RTX 2060 Mobile / macOS 15.8 / NullMoth 2.8。

记录一台实机从核显方案切到 **RTX 2060 驱动笔记本内屏** 的过程，并提供脱敏 EFI。2026-11-08 已确认四个 NVIDIA 驱动加载、6GB 显存、Metal 3、1920×1080 / 144Hz 内屏输出。尚未完成长期稳定性、睡眠唤醒、游戏和视频编码测试。

**这份 EFI 不包含 NVIDIA 系统驱动。首次安装请使用下面的 bootstrap 流程；已经装好系统驱动后，才使用最终 NVIDIA 配置。** 下载仓库后还需要生成自己的三码。公开脱敏副本本身没有再次实机启动，不能把这份配置视为所有同型号机器通用。

## 硬件与验证范围

| 项目 | 本机情况 |
| --- | --- |
| 机型 | Lenovo Legion Y7000P 2020H |
| CPU / 内存 | Intel Core i7-10875H / 32GB |
| 独显 | NVIDIA RTX 2060 Mobile，PCI ID `10DE:1F15`，6GB |
| 内屏 | 1920×1080，144Hz；最终由 NVIDIA 直接输出 |
| 核显 | Intel UHD；原核显配置仿冒 `3EA5`，保留核显恢复配置 |
| 声卡 | Realtek ALC257，保留原 `alcid=18`；本轮未完整测试音频 |
| 系统盘 | Netac NVMe SSD 512GB |
| Windows 盘 | Samsung MZVLB512HBJQ-000L2，固件 3L1QEXF7；在 macOS 中隔离 |
| 网络 | RealtekRTL8111；Intel Wi-Fi 使用 itlwm + HeliPort |
| macOS | Sequoia 15.8，Build 24H23，Darwin 24.6.0 |
| SMBIOS | MacBookPro16,4，公开版已移除真实三码及 ROM |
| 引导 | 使用原有已启动成功的 OpenCore 二进制，未单独核实其版本号 |
| 独显驱动 | [NullMoth 2.8](https://github.com/nullmoth/nvidia-macos-driver/releases/tag/v2.8) |

## 这次成功的关键

1. **先确认显示路径。** 核显混合模式下，删除独显屏蔽后曾发生启动异常，没有足够日志证明唯一根因。切到 BIOS `Discrete Graphics` 后，不改原 EFI 就成功进入 NVIDIA 8MB 基础显示桌面，并能看到 `10DE:1F15`。这一步才确认了内屏可以由独显直接输出。
2. 在上述状态安装 NullMoth 2.8。安装器实际试构建内核集合通过，再写入系统驱动和所需引导设置。
3. 保留 Turing 初始化等待参数 `nvrmsettle=10000` 和 WhateverGreen 的 `gfxrst=4`；不照搬其他主板的 BAR 设置。
4. 继续隔离已有读写超时 panic 证据的 Samsung Windows NVMe。

驱动作者说明：PCI ID 在支持表中不代表每一台笔记本已验证，驱动也不会凭空实现 Optimus 显示切换。本机的结果不能外推到无直连选项的笔记本。[支持范围](https://github.com/nullmoth/nvidia-macos-driver/blob/main/docs/CARD-SUPPORT.md)

## 仓库内容

- `EFI/`：基于本机安装后的配置，含 OpenCore、ACPI、原有 kext、AMFIPass 和恢复菜单工具；不含 `/Library/Extensions` 中的 NVIDIA 驱动。
- `configs/config-nvidia-bootstrap.plist`：装 NVIDIA 驱动前的基础引导配置，不排除 IONDRVSupport；用于独显直连下先进入基础显示桌面。
- `configs/config-intel-recovery.plist`：原核显方案，使用时 BIOS 要恢复混合模式。
- `tools/build_efi.py`：在仓库外生成带个人三码的 EFI，默认选择 bootstrap 模式，不修改本仓库。
- `tools/validate_public.py`：检查公开配置脱敏状态、Wi-Fi 凭据和引导引用。
- `docs/validation.json`：验证事实和未测试范围。
- `THIRD_PARTY.md`、`licenses/`：组件来源与许可证。

## 安装步骤

### 1. 保留能启动的恢复 U 盘

先确认现有 EFI 能进入桌面，再备份整个 EFI。测试使用另一份可恢复的引导；不要覆盖唯一可用的恢复盘。

这不是 macOS 安装镜像。新装系统仍需要自己的 macOS 安装介质。本流程针对已经可以启动 macOS 的机器。

### 2. 生成自己的 EFI

用 [GenSMBIOS](https://github.com/corpnewt/GenSMBIOS) 为 `MacBookPro16,4` 生成自己的序列号与 MLB，然后运行：

```bash
python3 tools/build_efi.py --output /path/outside-this-repo/EFI-bootstrap --mode bootstrap
```

Windows 使用 `python` 或 `py` 代替 `python3`，输出路径同样放在仓库外。工具会交互读取三码，不将它们打印出来；UUID 和本地管理的 ROM 可留空自动生成。它只生成文件夹，不挂载、不格式化、不写入硬盘或 U 盘。

把生成目录内的 `EFI` 文件夹放到测试引导分区根目录；应存在 `EFI/BOOT/BOOTx64.efi`。用 ProperTree 手动填写三码也可以，但不要把个人配置提交回 GitHub。

### 3. BIOS 切为独显直连，先确认基础显示

本机：重启按 `F2` / `Fn+F2`，在 `Configuration → Graphic Device` 选择 `Discrete Graphics`，`F10` 保存。菜单名称可能随 BIOS 版本变化。

使用 bootstrap 配置启动 macOS。安装驱动前应先看到 NVIDIA `10DE:1F15`，内屏有画面，系统可能显示只有 8MB 显存、没有 Metal。这是安装前的基础显示状态。

如果这一步进不了桌面，先回 BIOS 改回原来的混合模式，使用原恢复 EFI。不要继续叠加 NVIDIA 参数，也不要直接使用最终 NVIDIA 配置。

### 4. 安装官方发布包

从 [NullMoth 2.8 Release](https://github.com/nullmoth/nvidia-macos-driver/releases/tag/v2.8) 下载 1401 Mac 应用与驱动，按项目说明安装，并确认它修改的是本次实际启动的测试 EFI。

本机实际使用同一发布版本附带的原版配置脚本与安装器；安装前完成以下检查：

- 驱动压缩包 SHA256：`79251e8b685d98c39d7db7858ba161bba406a90847bccd46057aced4bb59b3dc`。
- 包内 SHA256SUMS 的82个条目全部通过；用户态最低系统版本检查通过。
- 实际试构建 Auxiliary Kernel Collection，确认包含四个驱动。
- 下载 AMFIPass 失败时，改用与安装器固定 SHA256 相同的离线 1.4.1 包，未跳过文件校验。

1401 会处理所需 SIP 配置；若提示先重启应用配置，再次进入系统后继续安装。系统若要求允许扩展，在“系统设置 → 隐私与安全性”允许后按要求重启。

**驱动安装在 `/Library/Extensions`、`/Library/GPUBundles` 和 `/Library/NullMoth`，不在 EFI 中；不要再把四个 NVIDIA kext 重复注入 EFI。** 不要从本仓库下载目录猜测其他版本驱动的校验值。

### 5. 启动并验证

保持 BIOS `Discrete Graphics`，在 OpenCore 选择 **Macintosh HD**。首次显卡初始化先等约两分钟，正常启动不要选择恢复工具。

```bash
kmutil showloaded | grep com.nullmoth
system_profiler SPDisplaysDataType
ioreg -r -c NVRM -l -w0
```

本机结果：`NVRM`、`NVAccel`、`NVRMFB`、`NVRMAGDC` 均为2.8；RTX 2060 显存6GB、Metal 3、内屏1080p/144Hz；`nvrm-autogo=up`、`nvrm-boot-hold=display armed`。

## 最终配置的含义

| 设置 | 本机值与原因 |
| --- | --- |
| NVIDIA 参数 | `nvfb=1 nvaccel=1 nvfbheads=4 -nvkmsnosmooth` |
| Turing 等待 | `nvrmsettle=10000`，按项目 Turing 处理逻辑设置 |
| WhateverGreen | `gfxrst=4`，避免旧启动画面复制路径；保留原 WhateverGreen |
| 背光修补 | `-igfxblt`；原 `-igfxblr` 和对应旧属性已移除 |
| 驱动加载条件 | AMFIPass 1.4.1、`csr-active-config=430A0000`、SecureBootModel Disabled；保留项目要求的 AMFI 参数 |
| BAR | `ResizeGpuBars=-1`、`ResizeAppleGpuBars=-1`，沿用本机原值；实际 BAR1 为256MB，驱动使用 copy path |
| IONDRVSupport | 最终配置按原版安装器加入 Exclude；实际这次运行的已加载列表仍能看到它，未为此继续试改 |
| 核显屏蔽属性 | 原 IGPU 的 `disable-external-gpu` 保留；本机 BIOS 直连后核显不再作为显示设备枚举。不要把这一属性照搬为其他机器的直连方案 |

144Hz 是内屏显示时序，不能等同于游戏能跑144fps。没有做独立渲染基准或游戏性能承诺。

## Windows NVMe 卡死与恢复

Samsung `MZVLB512HBJQ-000L2` 在本机曾有明确读/写命令超时 panic。保留以下设备属性，使 macOS 不为该控制器加载 NVMe 驱动：

```text
PciRoot(0x0)/Pci(0x1D,0x0)/Pci(0x0,0x0)
class-code = Data FFFFFFFF
```

**这条路径是本机 Samsung 盘，另一块 Netac 是系统盘；不能按硬盘编号或盘品牌盲套。** 其他机器必须重新核对设备路径。EFI 未修改 Windows 分区中的文件。本机原有的 NTFS `noauto` 设置位于系统 `/etc/fstab`，未把个人分区 UUID 放进公开仓库。

启动失败时：

1. OpenCore 选 `1401: Start once without NVIDIA driver`，按提示后再选 macOS，只停用本次启动的驱动。
2. 需要撤销驱动时选 `1401: Remove NVIDIA driver`，按项目恢复流程操作；只换 EFI 不等于完整卸载系统驱动。
3. 回到原核显恢复方案时，将 BIOS 改回原来的混合模式，再从已验证的恢复 U 盘启动。

[上游故障排查与恢复说明](https://github.com/nullmoth/nvidia-macos-driver/blob/main/docs/TROUBLESHOOTING.md)

## 已知边界

- 此次启动观察约7分钟，WindowServer 未重启，未出现新 panic 文件；不等于长期稳定。
- 日志有 `RM Access Sys Cap creation failed: 0x56`，随后初始化完成；没有把日志表述为完全无错误。
- 睡眠唤醒、合盖、外接显示、游戏和视频编码未验证。原插电“不自动睡眠/熄屏”是本机系统设置，不在 EFI 里。
- USB 映射、ACPI、CPUFriend 数据及声卡参数来自本机原 EFI，未为其他机器重新生成；原有无线 kext 的版本范围也未重构。
- 旧日志还曾有 AppleHDA 调用栈中的内存异常，不能仅凭调用栈认定 AppleALC 是根因。
- 不包含个人 SSH 密钥、原始诊断日志、三码、Wi-Fi 密码、分区 UUID 或系统镜像。

## 来源与致谢

- [NullMoth NVIDIA driver / 1401](https://github.com/nullmoth/nvidia-macos-driver)：此次独显驱动、安装与恢复流程。
- [OpenCorePkg](https://github.com/acidanthera/OpenCorePkg)、[WhateverGreen](https://github.com/acidanthera/WhateverGreen)、[Dortania](https://dortania.github.io/) 与各 kext 作者，详见 [第三方组件说明](THIRD_PARTY.md)。
- [1orz 同型号 EFI](https://github.com/1orz/y7000p-2020H-macOS-EFI)、[xiaoMGitHub 拯救者系列 EFI](https://github.com/xiaoMGitHub/LEGION_Y7000Series_Hackintosh)：用于对照旧版核显方案，没有将其描述为本次独显成功的验证来源。
- [WhateverGreen 背光文档](https://github.com/acidanthera/WhateverGreen/blob/master/Manual/FAQ.IntelHD.en.md#fix-the-3-minute-black-screen-issue-on-kblcfl-platforms-running-macos-134-or-later)：macOS13.4以后的替代背光修补依据。

提交问题时请先移除三码、SSID、密码、用户名和原始内存内容，再附机型、CPU/GPU PCI ID、macOS Build、BIOS 显示模式、驱动版本及故障阶段。
