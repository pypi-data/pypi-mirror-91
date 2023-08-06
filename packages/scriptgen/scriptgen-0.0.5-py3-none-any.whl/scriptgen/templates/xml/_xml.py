#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations
from typing import Dict, List, Union

from scriptgen import BlockBuilder, IndentType, StringBuilder, timestamp


class XmlElementBuilder(StringBuilder):

    def __init__(
            self,
            name: str,
            attributes: Dict[str, str] = None,
            content: Union[str, List[XmlElementBuilder]] = None,
            indent_len: int = None,
            indent_space_len: int = None,
            indent_type: IndentType = None,
            rstrip: bool = None
    ) -> None:
        attributes = attributes if attributes is not None else {}
        StringBuilder.__init__(
            self,
            indent_len=indent_len,
            indent_space_len=indent_space_len,
            indent_type=indent_type,
            rstrip=rstrip
        )
        self.name = name
        self.attributes = attributes
        self.content = content

    def add_content_element(self, content: XmlElementBuilder) -> None:
        if self.content is None or isinstance(self.content, str):
            self.content = []
        self.content.append(content)

    def set_content_list(self, content: List[XmlElementBuilder]) -> None:
        self.content = content

    def set_content_str(self, content: str) -> None:
        self.content = content

    def build(
            self,
            rstrip: bool = None
    ) -> str:
        rstrip = self.rstrip if rstrip is None else rstrip
        attributes = [f'{k}="{v}"' for k, v in self.attributes.items()]
        attributes_len = len(attributes)
        sb = StringBuilder()
        sb.wt(f"<{self.name}")
        if attributes:
            sb.wt("" if attributes_len > 1 else " ")
            sb.wb(xml_attributes(attributes), rstrip=True)
        if self.content is None:
            sb.wl(" />")
        else:
            sb.wt(">")
            if isinstance(self.content, str):
                if attributes_len > 1:
                    sb.nl()
                sb.wt(f"{self.content}", addtl_indent_len=1 if attributes_len > 1 else 0)
                if attributes_len > 1:
                    sb.nl()
            elif isinstance(self.content, List) and \
                    all(isinstance(c, XmlElementBuilder) for c in self.content):
                sb.nl()
                bb = BlockBuilder()
                for c in self.content:
                    bb.wb(c, rstrip)
                sb.wb(bb)
            sb.wl(f"</{self.name}>")
        return sb.build(rstrip)


def xml_attributes(attributes: List[str]) -> StringBuilder:
    attributes = attributes if attributes else []
    attributes_len = len(attributes)
    sb = StringBuilder()
    if attributes_len > 1:
        sb.nl()
        for i, a in enumerate(attributes):
            sb.wl(a, addtl_indent_len=1)
    elif attributes_len == 1:
        a = attributes[0]
        sb.wt(a)
    return sb


def xml_autogen() -> StringBuilder:
    return xml_comment(f"Auto-generated: {timestamp()}")


def xml_comment(
        *args: str) -> StringBuilder:
    sb = StringBuilder()
    if args:
        for arg in args:
            sb.wl(f"<!-- {arg} -->")
    return sb


def xml_declaration(
        version: str = "1.0",
        encoding: str = "UTF-8"
) -> StringBuilder:
    sb = StringBuilder()
    sb.wl(f'<?xml version="{version}" encoding="{encoding}" ?>')
    return sb
