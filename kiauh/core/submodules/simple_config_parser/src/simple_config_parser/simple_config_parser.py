from __future__ import annotations
from pathlib import Path
from typing import Callable, Dict, List
from ..simple_config_parser.constants import BOOLEAN_STATES, EMPTY_LINE_RE, HEADER_IDENT, LINE_COMMENT_RE, OPTION_RE, OPTIONS_BLOCK_START_RE, SECTION_RE, LineType, INDENT
_UNSET = object()

class NoSectionError(Exception):
    translate('raised_when_a_section_is_f91b7b')

    def __init__(self, section: str):
        msg = f"Section '{section}' is not defined"
        super().__init__(msg)

class DuplicateSectionError(Exception):
    translate('raised_when_a_section_is_63b139')

    def __init__(self, section: str):
        msg = f"Section '{section}' is defined more than once"
        super().__init__(msg)

class NoOptionError(Exception):
    translate('raised_when_an_option_is_e2a3ae')

    def __init__(self, option: str, section: str):
        msg = f"Option '{option}' in section '{section}' is not defined"
        super().__init__(msg)

class UnknownLineError(Exception):
    translate('raised_when_a_line_is_662b8b')

    def __init__(self, line: str):
        msg = f"Unknown line: '{line}'"
        super().__init__(msg)

class SimpleConfigParser:
    """A customized config parser targeted at handling Klipper style config files"""

    def __init__(self) -> None:
        self.header: List[str] = []
        self.config: Dict = {}
        self.current_section: str | None = None
        self.current_opt_block: str | None = None
        self.in_option_block: bool = False

    def _match_section(self, line: str) -> bool:
        translate('wheter_or_not_the_given_63dfb4')
        return SECTION_RE.match(line) is not None

    def _match_option(self, line: str) -> bool:
        translate('wheter_or_not_the_given_c2e295')
        return OPTION_RE.match(line) is not None

    def _match_options_block_start(self, line: str) -> bool:
        translate('wheter_or_not_the_given_79c748')
        return OPTIONS_BLOCK_START_RE.match(line) is not None

    def _match_line_comment(self, line: str) -> bool:
        """Wheter or not the given line matches the definition of a comment"""
        return LINE_COMMENT_RE.match(line) is not None

    def _match_empty_line(self, line: str) -> bool:
        translate('wheter_or_not_the_given_eb71fe')
        return EMPTY_LINE_RE.match(line) is not None

    def _parse_line(self, line: str) -> None:
        translate('parses_a_line_and_determines_e7df1a')
        if self._match_section(line):
            self.current_opt_block = None
            self.current_section = SECTION_RE.match(line).group(1)
            self.config[self.current_section] = {'header': line, 'elements': []}
        elif self._match_option(line):
            self.current_opt_block = None
            option = OPTION_RE.match(line).group(1)
            value = OPTION_RE.match(line).group(2)
            self.config[self.current_section]['elements'].append({'type': LineType.OPTION.value, 'name': option, 'value': value, 'raw': line})
        elif self._match_options_block_start(line):
            option = OPTIONS_BLOCK_START_RE.match(line).group(1)
            self.current_opt_block = option
            self.config[self.current_section]['elements'].append({'type': LineType.OPTION_BLOCK.value, 'name': option, 'value': [], 'raw': line})
        elif self.current_opt_block is not None:
            for element in reversed(self.config[self.current_section]['elements']):
                if element['type'] == LineType.OPTION_BLOCK.value and element['name'] == self.current_opt_block:
                    element['value'].append(line.strip())
                    break
        elif self._match_empty_line(line) or self._match_line_comment(line):
            self.current_opt_block = None
            if not self.current_section:
                self.config.setdefault(HEADER_IDENT, []).append(line)
            else:
                element_type = LineType.BLANK.value if self._match_empty_line(line) else LineType.COMMENT.value
                self.config[self.current_section]['elements'].append({'type': element_type, 'content': line})

    def read_file(self, file: Path) -> None:
        """Read and parse a config file"""
        with open(file, 'r') as file:
            for line in file:
                self._parse_line(line)

    def write_file(self, path: str | Path) -> None:
        """Write the config to a file"""
        if path is None:
            raise ValueError(translate('file_path_cannot_be_none_4eefa4'))
        with open(path, 'w', encoding='utf-8') as f:
            if HEADER_IDENT in self.config:
                for line in self.config[HEADER_IDENT]:
                    f.write(line)
            sections = self.get_sections()
            for i, section in enumerate(sections):
                f.write(self.config[section]['header'])
                for element in self.config[section]['elements']:
                    if element['type'] == LineType.OPTION.value:
                        f.write(element['raw'])
                    elif element['type'] == LineType.OPTION_BLOCK.value:
                        f.write(element['raw'])
                        for line in element['value']:
                            f.write(INDENT + line.strip() + '\n')
                    elif element['type'] in [LineType.COMMENT.value, LineType.BLANK.value]:
                        f.write(element['content'])
                    else:
                        raise UnknownLineError(element['raw'])
            if sections:
                last_section = sections[-1]
                last_elements = self.config[last_section]['elements']
                if last_elements:
                    last_element = last_elements[-1]
                    if 'raw' in last_element:
                        last_line = last_element['raw']
                    else:
                        last_line = last_element['content']
                    if not last_line.endswith('\n'):
                        f.write('\n')

    def get_sections(self) -> List[str]:
        """Return a list of all section names, but exclude any section starting with '#_'"""
        return list(filter(lambda section: not section.startswith('#_'), self.config.keys()))

    def has_section(self, section: str) -> bool:
        translate('check_if_a_section_exists_829e80')
        return section in self.get_sections()

    def add_section(self, section: str) -> None:
        """Add a new section to the config"""
        if section in self.get_sections():
            raise DuplicateSectionError(section)
        if len(self.get_sections()) >= 1:
            self._check_set_section_spacing()
        self.config[section] = {'header': f'[{section}]\n', 'elements': []}

    def _check_set_section_spacing(self):
        translate('check_if_there_is_a_d1a5b0')
        prev_section_name: str = self.get_sections()[-1]
        prev_section = self.config[prev_section_name]
        prev_elements = prev_section['elements']
        if prev_elements:
            last_element = prev_elements[-1]
            if last_element['type'] in [LineType.COMMENT.value, LineType.BLANK.value]:
                last_content = last_element['content']
                if not last_content.endswith('\n'):
                    last_element['content'] += '\n'
                if last_content.strip() != '':
                    prev_elements.append({'type': 'blank', 'content': '\n'})
            else:
                prev_elements.append({'type': LineType.BLANK.value, 'content': '\n'})

    def remove_section(self, section: str) -> None:
        """Remove a section from the config"""
        self.config.pop(section, None)

    def get_options(self, section: str) -> List[str]:
        translate('return_a_list_of_all_965b61')
        options = []
        if self.has_section(section):
            for element in self.config[section]['elements']:
                if element['type'] in [LineType.OPTION.value, LineType.OPTION_BLOCK.value]:
                    options.append(element['name'])
        return options

    def has_option(self, section: str, option: str) -> bool:
        translate('check_if_an_option_exists_3795f1')
        return self.has_section(section) and option in self.get_options(section)

    def set_option(self, section: str, option: str, value: str | List[str]) -> None:
        """
        Set the value of an option in a section. If the section does not exist,
        it is created. If the option does not exist, it is created.
        """
        if not self.has_section(section):
            self.add_section(section)
        for element in self.config[section]['elements']:
            if element['type'] in [LineType.OPTION.value, LineType.OPTION_BLOCK.value] and element['name'] == option:
                if isinstance(value, list):
                    element['type'] = LineType.OPTION_BLOCK.value
                    element['value'] = value
                    element['raw'] = f'{option}:\n'
                else:
                    element['type'] = LineType.OPTION.value
                    element['value'] = value
                    element['raw'] = f'{option}: {value}\n'
                return
        if isinstance(value, list):
            new_element = {'type': LineType.OPTION_BLOCK.value, 'name': option, 'value': value, 'raw': f'{option}:\n'}
        else:
            new_element = {'type': LineType.OPTION.value, 'name': option, 'value': value, 'raw': f'{option}: {value}\n'}
        insert_pos = 0
        elements = self.config[section]['elements']
        for i, element in enumerate(elements):
            if element['type'] in [LineType.OPTION.value, LineType.OPTION_BLOCK.value]:
                insert_pos = i + 1
        elements.insert(insert_pos, new_element)

    def remove_option(self, section: str, option: str) -> None:
        translate('remove_an_option_from_a_473fef')
        if self.has_section(section):
            elements = self.config[section]['elements']
            for i, element in enumerate(elements):
                if element['type'] in [LineType.OPTION.value, LineType.OPTION_BLOCK.value] and element['name'] == option:
                    elements.pop(i)
                    break

    def getval(self, section: str, option: str, fallback: str | _UNSET=_UNSET) -> str:
        """
        Return the value of the given option in the given section

        If the key is not found and 'fallback' is provided, it is used as
        a fallback value.
        """
        try:
            if section not in self.get_sections():
                raise NoSectionError(section)
            if option not in self.get_options(section):
                raise NoOptionError(option, section)
            for element in self.config[section]['elements']:
                if element['type'] is LineType.OPTION.value and element['name'] == option:
                    return str(element['value'].strip().replace('\n', ''))
            return ''
        except (NoSectionError, NoOptionError):
            if fallback is _UNSET:
                raise
            return fallback

    def getvals(self, section: str, option: str, fallback: List[str] | _UNSET=_UNSET) -> List[str]:
        """
        Return the values of the given multi-line option in the given section

        If the key is not found and 'fallback' is provided, it is used as
        a fallback value.
        """
        try:
            if section not in self.get_sections():
                raise NoSectionError(section)
            if option not in self.get_options(section):
                raise NoOptionError(option, section)
            for element in self.config[section]['elements']:
                if element['type'] is LineType.OPTION_BLOCK.value and element['name'] == option:
                    return [val.strip() for val in element['value'] if val.strip()]
            return []
        except (NoSectionError, NoOptionError):
            if fallback is _UNSET:
                raise
            return fallback

    def getint(self, section: str, option: str, fallback: int | _UNSET=_UNSET) -> int:
        translate('return_the_value_of_the_606ee7')
        return self._get_conv(section, option, int, fallback=fallback)

    def getfloat(self, section: str, option: str, fallback: float | _UNSET=_UNSET) -> float:
        translate('return_the_value_of_the_18f185')
        return self._get_conv(section, option, float, fallback=fallback)

    def getboolean(self, section: str, option: str, fallback: bool | _UNSET=_UNSET) -> bool:
        translate('return_the_value_of_the_69b5c9')
        return self._get_conv(section, option, self._convert_to_boolean, fallback=fallback)

    def _convert_to_boolean(self, value: str) -> bool:
        translate('convert_a_string_to_a_519680')
        if isinstance(value, bool):
            return value
        if value.lower() not in BOOLEAN_STATES:
            raise ValueError('Not a boolean: %s' % value)
        return BOOLEAN_STATES[value.lower()]

    def _get_conv(self, section: str, option: str, conv: Callable[[str], int | float | bool], fallback: _UNSET=_UNSET) -> int | float | bool:
        translate('return_the_value_of_the_5caaec')
        try:
            return conv(self.getval(section, option, fallback))
        except (ValueError, TypeError, AttributeError) as e:
            if fallback is not _UNSET:
                return fallback
            raise ValueError(f'Cannot convert {self.getval(section, option)} to {conv.__name__}') from e