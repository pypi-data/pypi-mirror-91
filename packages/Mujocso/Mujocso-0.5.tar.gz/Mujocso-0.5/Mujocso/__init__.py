import os
import io
from django.http.response import HttpResponse
from django.shortcuts import render as django_render
from bs4 import BeautifulSoup
import Mujocso
import re

javascript_files = html_files = css_files = font_files = []

mujocso_location = Mujocso.__file__
mujocso_location = mujocso_location.replace("\\","/")
mujocso_location = mujocso_location.split("/")
mujocso_location.pop()
mujocso_location = '/'.join(mujocso_location)

allowed_font_formats = ['ttf', 'otf', 'eot', 'woff2', 'woff']

for root, directory, files in os.walk(mujocso_location+'/template_files'):
    for file in files:
        if(file.endswith('.js')):
            javascript_files.append(file)

        elif(file.endswith('.html')):
            html_files.append(file)

        elif(file.endswith('.css')):
            css_files.append(file)

        for font_name in allowed_font_formats:
            if(file.endswith('.'+str(font_name))):
                font_files.append(file)
        
        else:
            continue

class MujocsoException(Exception):
    pass

class Mujocso:
    def render(headers=[], elements=[], page_title='Mujocso Page', style=[], addonscripts=[], script=[], template=None):

        # Local Functions
        def URL_validation():
            regex = re.compile(
                r'^(?:http|ftp)s?://'
                r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
                r'localhost|'
                r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
                r'(?::\d+)?'
                r'(?:/?|[/?]\S+)$', re.IGNORECASE)
            
            return re.match(regex, "http://www.example.com") is not None
        #--------------

        global mujocso_location

        allowed_header_inputs = ['value', 'size']
        alowed_element_inputs = ['type', 'value']
        allowed_element_types = ['p', 'a', 'img']
        avaliable_styles = ['CBRORANGE', 'CENTERTITLEORANGE']
        avaliable_page_styles = []
        avaliable_templates = ['CBRO404']
        page_body = ''
        page_style = ''
        page_addonscripts = ''
        page_scripts = ''


        if(template != None):
            if(type(template) == str):
                if(template.upper() in avaliable_templates):
                    with io.open(file=mujocso_location+'/template_files/'+str(template).upper()+'.css', encoding='UTF-8') as template_css:
                        template_css = template_css.read()
                    page_style = template_css
                else:
                    raise MujocsoException('Template not found')
            else:
                raise MujocsoException('Template type is not valid')

        if(style != [] and template == None and type(style) == list):
            for s in style:
                if(s in avaliable_page_styles):
                    with io.open(file=mujocso_location+'/template_files/'+str(s).upper()+'.css', encoding='UTF-8') as style_css:
                        style_css = style_css.read()
                        style_css = style_css.replace('*{ /* Mujocso Css Format Start */\n', '')
                        style_css = style_css.replace('\n} /* Mujocso Css Format End */', '')
                        page_style += style_css
                else:
                    if(s.endswith(";") == False):
                        page_style += s+';'
                    else:
                        page_style += s

        if(script != [] and type(script) == list):
            for script_ in script:
                page_scripts += script_+'\n'

        # Headers Validation
        if(type(headers) == list):
            for header in headers:
                if(type(header) == dict):
                    for key in allowed_header_inputs:
                        if(key in header and int(header['size']) <= 6):
                            continue
                        else:
                            raise MujocsoException('Header values must be valid')
                else:
                    raise MujocsoException('Header values must be a dictionary')
        else:
            raise MujocsoException('The headers type, must be a list')

        # Elements Validation
        if(type(elements) == list):
            for element in elements:
                if(type(element) == dict):
                    
                    # Fix Img Error Passing Bug
                    if(element['type'] == 'img'):
                        alowed_element_inputs.append('src')
                        alowed_element_inputs.append('alt')

                    for key in alowed_element_inputs:
                        if(key in element):
                            continue
                        else:
                            raise MujocsoException('Element values must be valid')
                else:
                    raise MujocsoException('Element values must be a dictionary')
        else:
            raise MujocsoException('The elements type, must be a list')

        # AddonScripts Add & Validation
        if(type(addonscripts) == list):
            for script in addonscripts:
                if(type(script) == str):
                    validation = URL_validation(script)
                    if(validation):
                        element_tag = 'script'
                        add_to_var = '<'+element_tag+' '+'src="'+script+'"'+' '+'>'
                        page_addonscripts += add_to_var
                        page_addonscripts += '\n'
                    else:
                        raise MujocsoException('Addonscripts URL must be valid')
                else:
                    raise MujocsoException('Addonscripts values must be a string')
        else:
            raise MujocsoException('The addonscripts type, must be a list')

        
        
        with io.open(file=mujocso_location+'/template_files/page.html', encoding='UTF-8') as page:
            o = page.read()

        o = o.replace(
            '{*PAGE_TITLE*}',
            page_title 
            )
        
        # Check And Processing Headers
        if(type(headers) == list):
            for header in headers:
                header_tag = 'h'+str(header['size'])
                styles_temp = ''
                tag_parameters = ''
                if('style' in header):
                    if(type(header['style']) == list):
                        for style in header['style']:
                            if(style.upper() in avaliable_styles):
                                with io.open(file=mujocso_location+'/template_files/'+str(style).upper()+'.css', encoding='UTF-8') as style_css:
                                    style_css = style_css.read()
                                    style_css = style_css.replace('*{ /* Mujocso Css Format Start */\n', '')
                                    style_css = style_css.replace('\n} /* Mujocso Css Format End */', '')
                                    styles_temp += style_css
                            else:
                                if(style.endswith(";") == False):
                                    styles_temp += '\n'+style+';'
                                else:
                                    styles_temp += '\n'+style
                        
                    elif(type(header['style']) == str):
                        if(header['style'].upper() in avaliable_styles):
                            with io.open(file=mujocso_location+'/template_files/'+str(header['style']).upper()+'.css', encoding='UTF-8') as style_css:
                                style_css = style_css.read()
                                style_css = style_css.replace('*{ /* Mujocso Css Format Start */\n', '')
                                style_css = style_css.replace('\n} /* Mujocso Css Format End */', '')
                                styles_temp += style_css
                        else:
                            if(header['style'].endswith(";") == False):
                                styles_temp += header['style']+';'
                            else:
                                styles_temp += header['style']
                    else:
                        raise MujocsoException("The headers style type must be string or list")

                    styles_temp = styles_temp.replace('\n', ' ').replace('  ', ' ')
                    style_param = 'style="'+styles_temp+'"'
                    tag_parameters += ' '+style_param


                if('id' in header):
                    id_param = 'id="'+header['id']+'"'
                    tag_parameters += ' '+id_param

                if('class' in header):
                    class_param = 'class="'+header['class']+'"'
                    tag_parameters += ' '+class_param

                
                add_to_body = '<'+header_tag+tag_parameters+'>'+str(header['value'])+'</'+header_tag+'>'
                ## -- Add To Body -- ##
                page_body += add_to_body
                page_body += '\n' 

        if(type(elements) == list):
            for element in elements:
                element_tag = element_value = ''
                element_addons = ' '
                
                if(element['type'] in allowed_element_types):
                    # allowed_element_types[0] = <p> Tag
                    # if(element['type'] == allowed_element_types[0]):
                    element_tag = element['type']
                    element_value = element['value']
                    

                    if(len(element_tag) != 2):
                        element_data_temp = element
                        del element_data_temp['type']
                        del element_data_temp['value']

                        
                        for param, value in element_data_temp.items():
                            element_addons += param+'="'+str(value)+'" '

                    add_to_body = '<'+element_tag+element_addons+'>'+element_value+'</'+element_tag+'>'
                    page_body += add_to_body
                    page_body += '\n' 
                else:
                    raise MujocsoException('Element type must be valid')
        

        o = o.replace(
            '{*BODY_SPACE*}',
            '<body>\n'+
            page_body+
            '\n</body>'
            )

            

        if(page_style != ''):
            
            o = o.replace(
                '{*STYLE_SPACE*}',
                '<style>\n'+
                page_style+
                '\n</style>'
                )
        else:
            o = o.replace(
                '{*STYLE_SPACE*}',
                ''
                )
        
        if(page_scripts != ''):
            
            o = o.replace(
                '{*SCRIPT_SPACE*}',
                '<script>\n'+
                page_scripts+
                '\n</script>'
                )
        else:
            o = o.replace(
                '{*SCRIPT_SPACE*}',
                ''
                )

        if(page_addonscripts != ''):
            
            o = o.replace(
                '{*ADOONSCRIPT_SPACE*}',
                page_scripts
                )
        else:
            o = o.replace(
                '{*ADOONSCRIPT_SPACE*}',
                ''
                )

                

        soup = BeautifulSoup(o, 'html.parser')
        output = soup.prettify()
        return HttpResponse(output)