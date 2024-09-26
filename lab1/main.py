from lexer import Lexer
from parser import Parser  

if __name__ == "__main__":
    expressions = [
        "cosx*sin(y)+-5+c*d-f3/avc_1",
        "(a+b)+func((a*b+1*(j-c)))",
        "-a+b*(-sin(x+19,5)",
        "g+(a+2.3.3)/()+",
        "/5+(12*(x+y)))",
    ]
    
    for expr in expressions:
        print(f"Expression: {expr}")
        lexer = Lexer(expr)

        while not lexer.is_end:
            lexer.lexical_analysis()
       
        # print(lexer.tokens)
        parser = Parser(lexer.tokens)
        parser.parse()
        print('-' * 20)
