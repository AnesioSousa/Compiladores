from .parser import GoatParser

class ControllerParser:    
    def make_parser(self, input_tokens, raw_input=None):
        if raw_input:
            self._input_tokens = raw_input.split(' ')
        else:
            self._input_tokens = input_tokens

        self.my_parser = GoatParser(input_tokens)  
        
        return self.my_parser  

    def parse_from_string(self, parser):
        pass
        
    def parse_from_txt(self):
        pass
    
    