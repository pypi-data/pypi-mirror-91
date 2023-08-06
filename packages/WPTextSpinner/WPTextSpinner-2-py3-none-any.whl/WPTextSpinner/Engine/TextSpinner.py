#-*- coding: UTF-8 -*-
import random
import re


class TextSpinner:
    def __init__(self, variables, title):
        self.variables = variables
        self.title = title

    def replace_var(self, variable):
        for key in self.variables.keys():
            if key == variable:
                replacement = random.choice(self.variables[key])
                return self.spin_text(replacement)
        raise NotImplementedError("No replacement found for variable: '"+variable+"' ("+str(self.variables.keys())+")")

    def replace_variable(self, match):
        match = match.group(1)
        return self.replace_var(match)

    def spin_text(self, text):
        text = re.sub(r'%%TITLE%%', self.title, text)
        new_text = re.sub(r'%%(\w+)%%', self.replace_variable, text)
        return new_text

    def spin_text_title(self, text):
        return self.spin_text(text)