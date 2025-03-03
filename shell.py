Blocks = []
class BlockIdentification:
    def __init__(self):
      self.codeString = "",

class FunctionParser:
   def __init__(self):
      self.conditionblock = "",

   def parse_block(self,execution_code):
      execution_code = "".join([item for row in execution_code for item in row])
      print(execution_code)


class PrintParse:
    def execute_print_block(execution_block,symboltable):
       import compiler
       print_parse = compiler.compiler
       combined_string = "".join([item for row in execution_block for item in row])

       if len(execution_block) == 1:
        isolated_variable = execution_block[0]
        if isolated_variable in symboltable:
            return symboltable[isolated_variable]
        elif isolated_variable not in symboltable:
            return isolated_variable
       elif str(execution_block).isalpha():
        return combined_string
       elif len(execution_block) == 0:
        return "印刷するものがないよ"
       else:
         code_error = print_parse.compile(str(combined_string),"表示")
       if code_error and len(code_error) > 0:
        for error in code_error:
            print(error)