import sync
import shell
import itertools

class LoopParse:
   def execute_loop(execution_block,self,loopTimes):
      execution_block = "".join([item for row in execution_block for item in row])

      if loopTimes == float('inf'):
         for i in itertools.count():
            LoopResult = Compiler.compile(self,execution_block,"loopCondition")
            if LoopResult == "loopEnd":
                break
      else:
        for loop in range(loopTimes):
          loopFeedback = Compiler.compile(self,execution_block,"loopCondition")
          if loopFeedback == "loopEnd":
             break

class Compiler:
    def __init__(self):
        self.code = ""
        self.symbol_table = {}
        self.operations = {
            '=': self.assign,
            '-': self.subtract,
            '*': self.multiply,
            '/': self.divide,
        }
    def retrievehiraganaphrases(self):
       return sync.hiraganaphrases
    
    def find_block_end(self,tokenlist,block_start):
        block_start_index = 0
        bash_end_count = 0
        condition_block = []
        for token in tokenlist[block_start_index + 1:]:
            if token.value == block_start.value or token.value == "(":
                bash_end_count += 1
                if block_start_index == 0:
                   block_start_index = tokenlist.index(block_start)
                elif block_start_index > 0:
                   condition_block.append(str(token.value))
            elif block_start_index > 0 and token.value != "}" and token.value != ")":
                if tokenlist.index(token) > block_start_index:
                   condition_block.append(str(token.value))
            elif token.value == "}" or token.value == ")":
                bash_end_count -= 1
                if bash_end_count > 0:
                   condition_block.append(str(token.value))
                elif bash_end_count == 0:
                 return condition_block,tokenlist.index(token)

    def execute_if_condition(self,parent_condition, operator_token, value_token, value2_token, if_block):
        combined_string = "".join([item for row in if_block for item in row])
        canSearch = False
        def checkblock():
           if "打破" in if_block:
              return 'loopEnd'
        if operator_token.value == ">" and int(self.symbol_table[value_token.value]) > int(value2_token.value):
            Compiler.compile(self,combined_string,parent_condition)
            canSearch = True
        elif operator_token.value == "<" and int(self.symbol_table[value_token.value]) < int(value2_token.value):
            Compiler.compile(self,combined_string,parent_condition)
            canSearch = True
        elif operator_token.value == "<=" and int(self.symbol_table[value_token.value]) <= int(value2_token.value):
            Compiler.compile(self,combined_string,parent_condition)
            canSearch = True
        elif operator_token.value == ">=" and int(self.symbol_table[value_token.value]) <= int(value2_token.value):
            Compiler.compile(self,combined_string,parent_condition)
            canSearch = True
        elif value_token != None:
            Compiler.compile(self,combined_string,parent_condition)

        if canSearch == True:
           return checkblock()

    def compile(self, source_code,ParentCondition):
        tokenizer = sync.Tokenizer(source_code)
        tokens = []
        errors = []
        comments = []
        feedback = []
        while (token := tokenizer.get_next_token()) is not None:
            tokens.append(token)

        i = 0
        while i < len(tokens):
            token = tokens[i]
            if token.type == sync.TOKEN_IDENTIFIER:
                if i + 2 < len(tokens):
                    operator_token = tokens[i + 1]
                    value_token = tokens[i + 2]
                    if operator_token.value in self.operations:
                        self.operations[operator_token.value](token.value, value_token.value)
                    else:
                        errors.append(f"エラー: 非対応 オペレーター '{operator_token.value}'")
                else:
                    errors.append("構文エラー: 不完全文")
            elif token.value == "もし":
                operator_token = tokens[i + 2] 
                value_token = tokens[i + 1]
                value2_token = tokens[i + 3]
                if tokens[i + 4].value == '{' or operator_token.value == '{':
                    if operator_token.value == '{':
                        execution_block,executionblockend = self.find_block_end(tokens, tokens[i + 3])
                    elif tokens[i + 4].value == "{":
                       execution_block,executionblockend = self.find_block_end(tokens, tokens[i + 4])
                    i = executionblockend-2
                    if_feedback = self.execute_if_condition(ParentCondition, operator_token, value_token,value2_token, execution_block)
                    if if_feedback:
                       feedback.append(if_feedback)
            elif token.value == "ループ":
                if tokens[i + 2].value == '{':
                   LoopTimes = tokens[i + 1].value
                   execution_block,executionblockend = self.find_block_end(tokens, tokens[i + 2])
                   i = executionblockend-2
                   LoopParse.execute_loop(execution_block,self,int(LoopTimes))
                elif tokens[i + 1].value == '{':
                   execution_block,executionblockend = self.find_block_end(tokens, tokens[i + 1])
                   i = executionblockend-1
                   LoopParse.execute_loop(execution_block,self,float('inf'))
            elif token.value == "表示":
                execution_block,executionblockend = self.find_block_end(tokens, tokens[i + 1])
                ParsedResult = shell.PrintParse.execute_print_block(execution_block,self.symbol_table)
                if ParsedResult:
                  if ParsedResult == "印刷するものがないよ":
                     errors.append(ParsedResult)
                  else:
                     comments.append(ParsedResult)
                i -= 2
            if token.value in self.operations and token.value != "=":
               previous_token = tokens[i - 1]
               value_token = tokens[i + 1]
               if previous_token.value in self.symbol_table and int(value_token.value):
                self.operations[token.value](previous_token, int(value_token.value))
               elif previous_token in self.symbol_table:
                self.operations[token.value](self.symbol_table[previous_token.value], int(value_token.value))
            i += 3

        return feedback,comments,errors
        
    def assign(self, variable, value):
        if value in [item for row in self.symbol_table for item in row]:
          self.symbol_table[variable] = int(self.symbol_table[value])
        elif str(value).isdigit():
          self.symbol_table[variable] = int(value)
        else:
          self.symbol_table[variable] = str(value)

    def subtract(self, variable, value):
        if variable in self.symbol_table:
            if variable != value:
               self.symbol_table[variable] -= int(value)
        else:
            print(f"Error: Variable '{variable}' not defined")

    def multiply(self, variable, value):
        if variable in self.symbol_table:
            self.symbol_table[variable] *= int(value)
        else:
            print(f"Error: Variable '{variable}' not defined")

    def divide(self, variable, value):
        if variable in self.symbol_table:
            if int(value) != 0:
                self.symbol_table[variable] /= int(value)
            else:
                print("Error: Division by zero")
        else:
            print(f"Error: Variable '{variable}' not defined")