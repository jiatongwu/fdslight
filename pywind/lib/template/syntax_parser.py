#!/usr/bin/env python3
"""核心语法解析器,实现核心语法解析功能
"""

### 表示从何种语法标志获取解析结果的
# 没有任何语法标志
SYNTAX_FLAG_NONE = 0

# 从<%block name=''>解析而来
SYNTAX_FLAG_BLOCK_BEGIN = 1
# 从<%block name=''/>解析而来
SYNTAX_FLAG_BLOCK_BEGIN_AND_END = 2

# 从</%block>解析而来
SYNTAX_FLAG_BLOCK_END = 3

# Pyhton代码开始
SYNTAX_FLAG_PYCODE_BEGIN = 4
# Python代码结束
SYNTAX_FLAG_PYCODE_END = 5

# 从美元符号解析得来的
SYNTAX_FLAG_DOL = 6


class SyntaxErr(Exception): pass


class ParserErr(Exception): pass


class parser(object):
    def __parse_step3(self, s):
        """解析美元符号
        :param sts: 
        :return: 
        """
        results = []

        tmplist = s.split("\n")

        for sts in tmplist:
            while 1:
                pos = sts.find("${")
                if pos < 0:
                    results.append((SYNTAX_FLAG_NONE, sts,))
                    break
                s1 = sts[0:pos]
                if s1: results.append((SYNTAX_FLAG_NONE, s1,))
                pos += 2
                sts = sts[pos:]
                pos = sts.find("}")
                if pos < 1: raise SyntaxErr
                s2 = sts[0:pos]
                results.append((SYNTAX_FLAG_DOL, s2,))
                pos += 1
                sts = sts[pos:]
            ''''''
        return results

    def __parse_block(self, sts, start, end):
        """解析块内容
        :param sts: 
        :param start: 
        :param end: 
        :return: 
        """
        results = []

        size_begin = len(start)
        size_end = len(end)

        while 1:
            pos = sts.find(start)
            if pos < 0:
                results.append((False, sts,))
                break
            s1 = sts[0:pos]
            if s1: results.append((False, s1,))

            pos += size_begin
            sts_bak = sts
            sts = sts[pos:]

            pos = sts.find(end)
            if pos < 0:
                results.append((False, sts_bak,))
                break

            results.append((True, sts[0:pos]))
            pos += size_end
            sts = sts[pos:]

        return results

    def __parse_step1(self, sts):
        tmp_results = self.__parse_block(sts, "<%block", "/>")
        results = []

        for flags, s in tmp_results:
            if flags:
                results.append((flags, s,))
                continue
            t = self.__parse_block(s, "<%block", "</%block>")
            results += t

        return results

    def __parse_step2(self, sts):
        pass

    def parse(self, sts):
        pass
