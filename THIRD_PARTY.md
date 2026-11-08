# 第三方组件与来源

本仓库的 MIT 许可仅适用于新增文档和辅助脚本。EFI 二进制、kext、ACPI 和图像资源保留各自上游的版权及许可，不能将整包重新声明为 MIT。

公开 EFI 来自实机现有引导，并增加本次安装的 AMFIPass 与 NullMothSafe。文档中的组件版本取自实际 Info.plist；没有把未逐一核对提交号的二进制宣称为可逐字节复现的官方构建。

| 上游 | 许可证／来源 |
| --- | --- |
| [acidanthera/OpenCorePkg](https://github.com/acidanthera/OpenCorePkg) | [BSD-3-Clause](licenses/acidanthera--OpenCorePkg.txt) |
| [acidanthera/OcBinaryData](https://github.com/acidanthera/OcBinaryData) | [请核对上游许可](https://github.com/acidanthera/OcBinaryData) |
| [acidanthera/Lilu](https://github.com/acidanthera/Lilu) | [BSD-3-Clause](licenses/acidanthera--Lilu.txt) |
| [acidanthera/VirtualSMC](https://github.com/acidanthera/VirtualSMC) | [BSD-3-Clause](licenses/acidanthera--VirtualSMC.txt) |
| [acidanthera/WhateverGreen](https://github.com/acidanthera/WhateverGreen) | [BSD-3-Clause](licenses/acidanthera--WhateverGreen.txt) |
| [acidanthera/AppleALC](https://github.com/acidanthera/AppleALC) | [BSD-3-Clause](licenses/acidanthera--AppleALC.txt) |
| [Mieze/RTL8111_driver_for_OS_X](https://github.com/Mieze/RTL8111_driver_for_OS_X) | [请核对上游许可](https://github.com/Mieze/RTL8111_driver_for_OS_X) |
| [OpenIntelWireless/itlwm](https://github.com/OpenIntelWireless/itlwm) | [上游许可文本](licenses/OpenIntelWireless--itlwm.txt) |
| [OpenIntelWireless/IntelBluetoothFirmware](https://github.com/OpenIntelWireless/IntelBluetoothFirmware) | [GPL-3.0](licenses/OpenIntelWireless--IntelBluetoothFirmware.txt) |
| [acidanthera/BrcmPatchRAM](https://github.com/acidanthera/BrcmPatchRAM) | [GPL-2.0](licenses/acidanthera--BrcmPatchRAM.txt) |
| [USBToolBox/kext](https://github.com/USBToolBox/kext) | [请核对上游许可](https://github.com/USBToolBox/kext) |
| [acidanthera/CPUFriend](https://github.com/acidanthera/CPUFriend) | [BSD-3-Clause](licenses/acidanthera--CPUFriend.txt) |
| [acidanthera/CpuTscSync](https://github.com/acidanthera/CpuTscSync) | [BSD-3-Clause](licenses/acidanthera--CpuTscSync.txt) |
| [acidanthera/RestrictEvents](https://github.com/acidanthera/RestrictEvents) | [BSD-3-Clause](licenses/acidanthera--RestrictEvents.txt) |
| [1Revenger1/ECEnabler](https://github.com/1Revenger1/ECEnabler) | [请核对上游许可](https://github.com/1Revenger1/ECEnabler) |
| [acidanthera/NVMeFix](https://github.com/acidanthera/NVMeFix) | [NOASSERTION](licenses/acidanthera--NVMeFix.txt) |
| [acidanthera/HibernationFixup](https://github.com/acidanthera/HibernationFixup) | [BSD-3-Clause](licenses/acidanthera--HibernationFixup.txt) |
| [RehabMan/OS-X-USB-Inject-All](https://github.com/RehabMan/OS-X-USB-Inject-All) | [NOASSERTION](licenses/RehabMan--OS-X-USB-Inject-All.txt) |
| [acidanthera/VoodooPS2](https://github.com/acidanthera/VoodooPS2) | [NOASSERTION](licenses/acidanthera--VoodooPS2.txt) |
| [VoodooI2C/VoodooI2C](https://github.com/VoodooI2C/VoodooI2C) | [GPL-3.0](licenses/VoodooI2C--VoodooI2C.txt) |
| [acidanthera/BrightnessKeys](https://github.com/acidanthera/BrightnessKeys) | [BSD-3-Clause](licenses/acidanthera--BrightnessKeys.txt) |
| [dortania/OpenCore-Legacy-Patcher](https://github.com/dortania/OpenCore-Legacy-Patcher) | [NOASSERTION](licenses/dortania--OpenCore-Legacy-Patcher.txt) |
| [nullmoth/nvidia-macos-driver](https://github.com/nullmoth/nvidia-macos-driver) | [NOASSERTION](licenses/nullmoth--nvidia-macos-driver.txt) |

- `NullMothSafe.efi` 来自 1401 Mac 2.8 原发布包，与 NVIDIA 系统驱动分开；原包 SHA256 信息见安装文档。保留 NullMoth 的 Required Notice：Copyright (c) 2026 NullMoth Systems (https://nullmothsystems.com)。
- `AMFIPass.kext` 来自 OpenCore-Legacy-Patcher 发布的 AMFIPass 1.4.1 压缩包，SHA256 为 `07b266145906db41f4b13a7938fbb173ea28888cc1fa65f84417f8820adc961e`；未将其声明为本仓库原创。
- `XHCI-unsupported.kext`、USB 映射、CPUFriend 数据及 ACPI 来自实机原引导配置。相关上游链接供追溯；不把同型号参考仓库错误署名为这些本机文件的确定来源。
- 不随仓库重新打包 NVIDIA 固件、用户态 GPU 插件或 macOS 系统组件。请从驱动项目的版本发布页获取完整系统驱动及其许可、源码。
- 如需重分发或修改各组件，请按其自身许可处理；本仓库文档不改变上游授权条件。
