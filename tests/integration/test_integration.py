"""
test.integration.test_integration
~~~~~~~~~~~~~~~~
"""

from pylox.lox import Lox


class TestConditions:
    def test_if(self, capsys):
        line = "var num = 9; \
               if(num >= 0 and num <= 10) \
               print(true);"
        lox = Lox()
        lox.run(line)
        out, err = capsys.readouterr()
        assert err == ''
        assert out == "True\n"

    def test_of(self, capsys):
        line = 'var s = "hi"; \
               if(s == "hi" or s == "hello") \
               print("Greetings");'
        lox = Lox()
        lox.run(line)
        out, err = capsys.readouterr()
        assert err == ''
        assert out == "Greetings\n"


class TestFunction:
    def test_string_parameters(self, capsys):
        line = 'fun strAppend(str1, str2) { \
        var str = str1 + str2; \
        return str;} \
        print(strAppend("foo", "bar"));'
        lox = Lox()
        lox.run(line)
        out, err = capsys.readouterr()
        assert err == ''
        assert out == "foobar\n"

    def test_num_parameters(self, capsys):
        line = 'fun add(a, b){ \
        return(a + b); \
        } \
        print(add(10, 5));'
        lox = Lox()
        lox.run(line)
        out, err = capsys.readouterr()
        assert err == ''
        assert out == "15.0\n"

    def test_fun_with_conditional(self, capsys):
        line = 'fun checkNegative(num){ \
        if(num <= 0) \
        return(true); \
        else \
        return(false); \
        } \
        print(checkNegative(-1));'
        lox = Lox()
        lox.run(line)
        out, err = capsys.readouterr()
        assert err == ''
        assert out == "True\n"

    def test_recursion(self, capsys):
        line='fun isOdd(n) { \
        if (n == 0) return false; \
        return isEven(n - 1); \
        } \
        fun isEven(n){ \
        if (n == 0) return true; \
        return isOdd(n - 1); \
        } \
        print(isEven(3));'
        lox = Lox()
        lox.run(line)
        out, err = capsys.readouterr()
        assert err == ''
        assert out == "False\n"


class TestLoops:
    def test_while_loop(self, capsys):
        line = 'var i = 0; \
        while(i < 10) { \
        print(i); \
        i = i + 1; \
        }'
        lox = Lox()
        lox.run(line)
        out, err = capsys.readouterr()
        assert err == ''
        assert out == "0.0\n1.0\n2.0\n3.0\n4.0\n5.0\n6.0\n7.0\n8.0\n9.0\n"

    def test_for_loop(self, capsys):
        line = 'for (var i = 0; i < 10; i = i + 1) print i;'
        lox = Lox()
        lox.run(line)
        out, err = capsys.readouterr()
        assert err == ''
        assert out == "0.0\n1.0\n2.0\n3.0\n4.0\n5.0\n6.0\n7.0\n8.0\n9.0\n"
