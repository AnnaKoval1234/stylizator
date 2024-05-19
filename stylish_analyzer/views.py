from django.shortcuts import render
from datetime import datetime
import time
from . import common
from .for_analyzers.constant import STYLE_SET

def index(request):
    if request.method == "POST":
        text = request.POST.get("text")
        if text.isspace() == True or len(text) == 0:
            analyze_style = ""
            result_of_lexic_analyze = ""
            result_of_morph_analyze = ""
            result_of_syntax_analyze = ""
            errors = ""

        else:
            analyzer = common.Analyzer(text)
            analyzer.parse()

            lexic_analyzer = analyzer.lexical
            morph_analyzer = analyzer.morphology
            syntax_analyzer = analyzer.syntax

            analyze_style = '<p>' + str(analyzer.analyze()).replace('\n','<br>') + '</p>'

            result_of_lexic_analyze = '<p>' + str(lexic_analyzer).replace('\n','<br>') + '</p>'
            result_of_morph_analyze = '<p>' + str(morph_analyzer).replace('\n','<br>') + '</p>'
            result_of_syntax_analyze = '<p>' + str(syntax_analyzer).replace('\n','<br>') + '</p>'

            errors = '<p>' + str(analyzer.find_errors()).replace('\n','<br>') + '</p>'

        dt = datetime.now()
        
        return render(request, "index.html", {"textareatext": text,
                                              "analyze_style": analyze_style,
                                              "result_of_lexic_analyze": result_of_lexic_analyze,
                                              "result_of_morph_analyze": result_of_morph_analyze,
                                              "result_of_syntax_analyze": result_of_syntax_analyze,
                                              "errors": errors,
                                              "datetime": dt.strftime("Проверено %d.%m.%Y, %H:%M:%S")})
    else:
        return render(request, "index.html", {"textareatext": "",
                                              "analyze_style": "",
                                              "result_of_lexic_analyze": "",
                                              "result_of_morph_analyze": "",
                                              "result_of_syntax_analyze": "",
                                              "errors": "",
                                              "datetime": "Для начала работы введите любой текст в поле ниже"})