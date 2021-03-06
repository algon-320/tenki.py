#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import copy
import unicodedata


class Color:

    def __init__(self, col):
        """
        col : 十六進数表記での色 "#RRGGBB" (#は無くてもいい) または [R, G, B]のリスト
        """
        if type(col) == str:
            self.color = Color.convert_from_hex_to_rgb(col)
        else:
            self.color = col


    def convert_to_hex(self):
        return '#%02X%02X%02X' % (self.color[0], self.color[1], self.color[2])


    @staticmethod
    def convert_from_hex_to_rgb(hexcolstr):
        """
        hexcolstr : 十六進数表記での色 "#RRGGBB" (#は無くてもいい)
        """
        if hexcolstr[0] == '#':
            hexcolstr = hexcolstr[1:]
        colint = int(hexcolstr, 16)
        b = colint % 256
        colint //= 256
        g = colint % 256
        colint //= 256
        r = colint
        return [r, g, b]



class Style:

    STYLE = (
        RESET,
        BOLD,
        WEAKEN,
        ITALIC,
        UNDERSCORE,
        SLOW_BLINK,
        FAST_BLINK,
        INVERT,
        INVISIBLE,
        STRIKETHROUGH,
    ) = list(map(lambda x: 1 << x, range(10)))



class String:

    @staticmethod
    def get_string_width(string):
        """
        文字列の表示幅を計算
        例: get_string_width('こんにちは') --> 10
            get_string_width('hello') --> 5
            get_string_width('ほげhoge') --> 8
        """
        width = 0
        for c in string:
            cw = unicodedata.east_asian_width(c)
            if cw in 'AFW':
                width += 2
            else:
                width += 1
        return width


    @staticmethod
    def rjust(string, width):
        """
        width文字分を半角スペースで埋めて右寄せにして返す
        string : 対象の文字列
        width : 半角基準の幅
        """
        return (' ' * (width - String.get_string_width(string)) + string)


    @staticmethod
    def ljust(string, width):
        """
        width文字分を半角スペースで埋めて左寄せにして返す
        string : 対象の文字列
        width : 半角基準の幅
        """
        return (string + ' ' * (width - String.get_string_width(string)))


    @staticmethod
    def center(string, width, ljust=True):
        """
        width文字分を半角スペースで埋めて左寄せにして返す
        string : 対象の文字列
        width : 半角基準の幅
        ljust : 中央に揃えられないとき、半角スペース分左に寄せる
        例: center('ほげ', 7, ljust=True)  --> ' ほげ  '
            center('ほげ', 7, ljust=False) --> '  ほげ '
        """
        tmp = width - String.get_string_width(string)
        if ljust:
            return (' ' * (tmp // 2) + string + ' ' * (tmp - tmp // 2))
        else:
            return (' ' * (tmp - tmp // 2) + string + ' ' * (tmp // 2))



class Print:

    @staticmethod
    def change_style(style_opts, conky=False, out=sys.stdout):
        """
        style_opts : 変更したいスタイルのフラグ (|で複数指定可能) Style.BOLD など
        out : 書き込むファイル (標準エラーならsys.stderr)
        """
        if style_opts & Style.RESET:
            if conky:
                out.write('${color}${font}')
            else:
                out.write('\033[0m')
            return

        if conky:
            cmd = ''
            if style_opts & Style.BOLD:
                # cmd += '${font :bold}'  # バグる
                pass
            if style_opts & Style.ITALIC:
                # cmd += '${font :italic}'  # バグる
                pass
            out.write(cmd)

        else:
            cmd = '\033['
            for (i, v) in enumerate(Style.STYLE):
                if style_opts & v > 0:
                    cmd += "%d;" % (i)
            out.write(cmd[:-1] + 'm')


    @staticmethod
    def change_color(col, weaken=False, conky=False, out=sys.stdout):
        """
        col : Colorオブジェクト
        out : 書き込むファイル (標準エラーならsys.stderr)
        """
        color = copy.deepcopy(col.color)
        if weaken:
            color[0] = int(color[0] * 0.6)
            color[1] = int(color[1] * 0.6)
            color[2] = int(color[2] * 0.6)

        if conky:
            cmd = '${color %s}' % Color(color).convert_to_hex()
        else:
            cmd = '\033[38;2;%d;%d;%dm' % (color[0], color[1], color[2])
        out.write(cmd)
