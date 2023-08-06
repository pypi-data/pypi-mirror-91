class CSS():
    """ CSS style class.
        Collection of functions for CSS styling
    """

    def inline_block_css():
        """ CSS code to align HTML elements as a row,
            i.e. align HTML horizontally
            CSS element e.g. for HTML.navbar(...)

            INPUTS:
            ------------
            None

            OUTPUTS:
            ------------
            inline_block_css - a string which contains CSS code to style an inline object (e.g. navbar)
        """

        inline_block_css='''\n<!-- ++++++++++++++++++++ CSS: Inline Block ++++++++++++++++++++ -->\n<style>
        .item_row_ul {
            margin: 0;
            padding: 0;
            list-style-type: none;
        }
        .item_row_li {
            display: inline-block;
            margin-right: 20px;
        }\n</style>\n\n'''

        return inline_block_css

    def accordion_css(background_color):
        """ CSS code for HTML.accordion(...)

            INPUTS:
            ------------
            background_color - string, standard: 'steelblue'

            OUTPUTS:
            ------------
            accordion_css - a string which contains CSS code to style an accordion (detail)
        """

        accordion_css='''\n<!-- ++++++++++++++++++++ CSS: Accordion ++++++++++++++++++++ -->\n<style>
        * {
             box-sizing: border-box;
        }

        img {
            max-width: 100%;
        }

        .details-wrapper {
            width: 75vw;
            margin: 0 auto;
            background-color: #BFBFBF;
            box-shadow:0 -1px 1px 5px #BFBFBF;

        }
        details {
            padding: .5rem;
            font: 1rem/1.2 sans-serif;

        }

        summary {
            padding: .07rem 1rem;''' + '''
            background-color: {0};'''.format(background_color) + '''
            font: bold 1.15rem/2 sans-serif;
            color:floralwhite;
            border: none;
            border-radius: 3px;

            box-shadow: 0 -1px 1px 1px rgba(0,0,0,0.5);
          cursor: pointer;
            /*list-style: none;*/ /* Triangle not shown */
        }
        /* Triangle not shown - Style for Webkit-Browser */
        /*summary::-webkit-details-marker {
            display: none;
        }*/
        summary::before {
            padding-right: .25rem;
            /*content: '+ ';*/  /* Instead of Triangle closed */
        }
        details[open] summary::before {
            padding-right: .25rem;
            font-style: italic;
            /*content: '- ';*/ /* Instead of Triangle open */
        }

        /* Styling the summary in case of open 'details' */
        details[open] summary {
            font-style: italic;
            border-radius: 3px 3px 0 0;
        }

        .details-content {
            margin: 0;
            padding: .25rem 1rem;
            background-color: floralwhite;
            border-radius: 0 0 3px 3px;
            box-shadow: 0 1px 1px 1px rgba(0,0,0,0.5);
          color: steelblue;
        }

        .details-content p {
            font: 1.1rem/1.5 sans-serif;
        }\n</style>\n\n'''

        return accordion_css

    def iframe_css(clss, width, height):
        """ CSS code for iframes. Sets height and width of iframes

            INPUTS:
            ------------
            clss - HTML class name (string)
            width - width of iframe (int)
            height - height of iframe (int)

            OUTPUTS:
            ------------
            iframe_css - a string which contains CSS code to style an iframe
        """

        iframe_css="""<!-- ++++++++++++++++++++ CSS: Iframe Style ++++++++++++++++++++ -->\n<style>""" + """
            .{0}""".format(clss) + """{""" + """
              width: {};""".format(width) +"""
              height: {};""".format(height) + """
            }\n</style>\n\n"""

        return iframe_css

    def thumbnail_image_css(clss):
        """ CSS code to build thumbnail images
            - setting border around images
            - setting box-shadow on image hover

            INPUTS:
            ------------
            clss - HTML class name (string)

            OUTPUTS:
            ------------
            thumbnail_image_css - a string which contains CSS code to style a thumbnail image
        """

        thumbnail_image_css="""<!-- ++++++++++++++++++++ CSS: Thumbnail Image Style ++++++++++++++++++++ -->\n<style>""" + """
            .{0}""".format(clss) + """{""" + """
              border: 1px solid #ddd;
              border-radius: 4px;
              padding: 5px;
              width: 150px;
            }""" + """

            .{0}""".format(clss) + """:hover{""" + """
              box-shadow: 0 0 2px 1px rgba(0, 140, 186, 0.5);
            }\n</style>\n\n"""

        return thumbnail_image_css

    def on_hover_text_css(base_element, hover_text):
        """ CSS code to create hover text on HTML elements

            INPUTS:
            ------------
            base_element - Code for an HTML element as string to connect with a hover text
            hover_text - hover Text

            OUTPUTS:
            ------------
            on_hover_text_css - a string which contains CSS code to style hover text
        """

        on_hover_text_css="""<!-- ++++++++++++++++++++ CSS: On Hover Text Style ++++++++++++++++++++ -->\n<style>""" + """
        <style>
        .tooltip {
          position: relative;
          display: inline-block;
        }

        .tooltip .tooltiptext {
          visibility: hidden;
          width: 80%;
          background-color: grey;
          color: #fff;
          text-align: center;
          border-radius: 6px;
          padding: 5px 0;

          /* Position the tooltip */
          position: absolute;
          z-index: 1;
        }

        .tooltip:hover .tooltiptext {
          visibility: visible;
        }
        </style> \n\n""" + """
        <div class="tooltip">{0}<span class="tooltiptext">{1}</span></div>""".format(base_element, hover_text)

        return on_hover_text_css

    def align_horizontal(div1_content, div2_content):
        """ CSS code to align two HTML elements horizontally with equal width

            INPUTS:
            ------------
            div1_content - Code for HTML div1 as string
            div2_content - Code for HTML div1 as string

            OUTPUTS:
            ------------
            style + html - string (CSS + HTML code) to construct horizontally div elements
        """

        style="""<!-- ++++++++++++++++++++ CSS: align_horizontal ++++++++++++++++++++ -->\n<style>""" + """
            #wrapper-div {
            width:100%;
            margin : 0;
            }

            #first-div {
            width:50%;
            margin : 0;
            float : left ;
            }

            #second-div {
            width:50%;
            margin : 0;
            float : left ;
            }\n</style>\n\n"""

        html="""<!-- ++++++++++++++++++++ HTML: align_horizontal ++++++++++++++++++++ -->\n """ + """
            <div id="wrapper-div">
		          <div id="first-div" >""" + """
			               {}""".format(div1_content) + """
		          </div>
		          <div id="second-div" >""" + """
			               {}""".format(div2_content) + """
		          </div>
	        </div>"""

        return style + html

    def align_horizontal_2(div_content_list, item_width_list, min_width_list, id_start=''):
        """ CSS code to align multiple HTML elements horizontally each with a specific width

            INPUTS:
            ------------
            div_content_list - list of HTML elements to align
            item_width_list - list with integers to specify the width for each element
            min_width_list - list with min width for each element
            id_start - id start to make horizontal block id-unique

            OUTPUTS:
            ------------
            style + html - string (CSS + HTML code) to construct horizontally div elements
        """

        style="""<!-- ++++++++++++++++++++ CSS: align_horizontal_2 ++++++++++++++++++++ -->\n<style>""" + """
            .flex_ab_hor {
              display: flex;
              flex-wrap: wrap;
            }
            .container_ab_hor {
              width: auto;
              height: auto;
              border: 5px solid CadetBlue;
              border-radius: .5em;
              padding: 10px;
              justify-content: space-between;
              align-content: space-between;
            }"""
        for index, (width, min_width) in enumerate(zip(item_width_list, min_width_list)):
            style +="""
            #item_ab_hor{0}_{1}""".format(id_start, index) + """ {
              padding: 10px;
              margin: 3px;
              border: 1px solid lightgrey;
              border-radius: .5em;""" + """
              width: {0};""".format(width) + """
              min-width: {}px;""".format(min_width) + """
            }"""
        style += """\n</style>\n\n"""

        html="""<!-- ++++++++++++++++++++ HTML: align_horizontal_2 ++++++++++++++++++++ -->\n """ + """
            <div class="container_ab_hor flex_ab_hor">\n"""
        for index, element in enumerate(div_content_list):
            html +="""<div id="item_ab_hor{0}_{1}">\n{2}\n</div>\n""".format(id_start, index, element)

        html +="""\n</div>\n\n"""

        return style + html

    def align_horizontal_3(div_content_list, alignment_list, item_width_list, min_width_list, id_start=''):
        """ CSS code to align multiple HTML elements horizontally each with a specific width

            INPUTS:
            ------------
            div_content_list - list of HTML elements to align
            alignment_list - list to align elements in the row, list elements: 'left', 'right', 'none'
            item_width_list - list with integers to specify the width for each element
            min_width_list - list with min width for each element
            id_start - id start to make horizontal block id-unique

            OUTPUTS:
            ------------
            style + html - string (CSS + HTML code) to construct horizontally div elements
        """

        style="""<!-- ++++++++++++++++++++ CSS: align_horizontal_3 ++++++++++++++++++++ -->\n<style>""" + """

            .container_ab_hor3 {
              width:98%;
              height: auto;
              color: grey;
              padding-top:10px;
              padding-left:10px;
              padding-right:10px;

            }"""
        for index, (align, width, min_width) in enumerate(zip(alignment_list, item_width_list, min_width_list)):
            style +="""
            #item_ab_hor3{0}_{1}""".format(id_start, index) + """ {"""+ """
              float:{0};""".format(align) + """
              width: {0};""".format(width) + """
              max-width: 100%;
              height:auto;
              background: white;
              border: 1px solid lightgrey;
              border-radius: .5em;
              padding: 10px;""" +"""
              min-width: {}px;""".format(min_width) + """

            }"""
        style += """\n</style>\n\n"""

        html="""<!-- ++++++++++++++++++++ HTML: align_horizontal_3 ++++++++++++++++++++ -->\n """ + """
            <div class="container_ab_hor3">\n"""
        for index, element in enumerate(div_content_list):
            html +="""<div id="item_ab_hor3{0}_{1}">\n{2}\n</div>\n""".format(id_start, index, element)

        html +="""\n</div>\n\n"""

        return style + html

    def grid_align(div_content_list, id_start=''):
        """ CSS code to align elements horizontally with equal width

            INPUTS:
            ------------
            div_content_list - list of HTML elements to align
            id_start - id start to make horizontal block id-unique

            OUTPUTS:
            ------------
            style + html - string (CSS + HTML code) to construct horizontally div elements
        """

        style="""<!-- ++++++++++++++++++++ CSS: grid_align ++++++++++++++++++++ -->\n<style>""" + """

            .container_grid {
                display: grid;
                grid-gap: 5px;
                grid-template-columns: repeat(auto-fit, minmax(600px, 1fr));
                grid-template-rows: repeat(2,auto);
                padding-bottom: 5px;
            }"""

        for index, _ in enumerate(div_content_list):
            style +="""
            #item_grid_2{0}_{1}""".format(id_start, index) + """
            {
              background: white;
              border: 1px solid lightgrey;
              border-radius: .5em;
              padding: 10px;


            }"""

        style += """\n</style>\n\n"""

        html="""<!-- ++++++++++++++++++++ HTML: grid_align ++++++++++++++++++++ -->\n """ + """
            <div class="container_grid">\n"""
        for index, element in enumerate(div_content_list):
            html +="""<div id="item_grid_2{0}_{1}">\n{2}\n</div>\n""".format(id_start, index, element)

        html +="""\n</div>\n\n"""

        return style + html

    def grid_align_w_border(div_content_list, id_start='', minmax='400px'):
        """ CSS code to align elements horizontally with equal width

            INPUTS:
            ------------
            div_content_list - list of HTML elements to align
            id_start - id start to make horizontal block id-unique
            minmax - min max of whole grid section

            OUTPUTS:
            ------------
            style + html - string (CSS + HTML code) to construct horizontally div elements
        """

        style="""<!-- ++++++++++++++++++++ CSS: grid_align_w_border ++++++++++++++++++++ -->\n<style>""" + """

            .container_grid_w_border {
                display: grid;
                grid-gap: 5px;""" +"""
                grid-template-columns: repeat(auto-fit, minmax({}, 1fr));""".format(minmax) + """
                grid-template-rows: repeat(2,auto);
                border: 5px solid CadetBlue;
                border-radius: .5em;
            }"""

        for index, _ in enumerate(div_content_list):
            style +="""
            #item_grid_2{0}_{1}""".format(id_start, index) + """
            {
              background: white;
              border: 1px solid lightgrey;
              border-radius: .5em;
              padding: 10px;


            }"""

        style += """\n</style>\n\n"""

        html="""<!-- ++++++++++++++++++++ HTML: grid_align_w_border ++++++++++++++++++++ -->\n """ + """
            <div class="container_grid_w_border">\n"""
        for index, element in enumerate(div_content_list):
            html +="""<div id="item_grid_2{0}_{1}">\n{2}\n</div>\n""".format(id_start, index, element)

        html +="""\n</div>\n\n"""

        return style + html

    def select_css(font_family='Arial', label_color='black', label_font_size=14, width='40vh', background_color_box='rgba(59, 153, 252, .7)'):
        """ CSS code to style HTML select tag

            INPUTS:
            ------------
            font_family - font family for select tag
            label_color - font color for select tag
            label_font_size - font size for select tag
            width - width of select tag
            background_color_box - background color of select tag

            OUTPUTS:
            ------------
            select_css - string (CSS code) to style HTML select tag
        """

        select_css ='''\n<!-- ++++++++++++++++++++ Style for Dropdown ++++++++++++++++++++ -->\n<style>/* class applies to select element itself, not a wrapper element */
        /* The container_input_slct */
        .container_input_slct {
          display: block;
          position: relative;
          padding-left: 0px;
          margin-top: 5px;
          margin-bottom: 2px;
          cursor: pointer;''' + '''
          font-family: "{0}";'''.format(font_family) + '''
          font-size: {0}px;'''.format(label_font_size) + '''
          color: "{0}";'''.format(label_color) + '''
          -webkit-user-select: none;
          -moz-user-select: none;
          -ms-user-select: none;
          user-select: none;
        }

        .select-css {
            display: block;
            font-size: 16px;
            font-family: sans-serif;
            font-weight: 700;
            color: #444;
            line-height: 1.3;
            padding: .6em 1.4em .5em .8em;''' + '''
            width: {};'''.format(width) + '''
            max-width: 100%; /* useful when width is set to anything other than 100% */
            box-sizing: border-box;
            margin: 0;
            border: 1px solid #aaa;
            box-shadow: 0 1px 0 1px rgba(0,0,0,.04);
            border-radius: .5em;
            -moz-appearance: none;
            -webkit-appearance: none;
            appearance: none;
            background-color: #fff;
            /* note: bg image below uses 2 urls. The first is an svg data uri for the arrow icon, and the second is the gradient.
                for the icon, if you want to change the color, be sure to use `%23` instead of `#`, since it's a url. You can also swap in a different svg icon or an external image reference

            */
            background-image: url('data:image/svg+xml;charset=US-ASCII,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20width%3D%22292.4%22%20height%3D%22292.4%22%3E%3Cpath%20fill%3D%22%23007CB2%22%20d%3D%22M287%2069.4a17.6%2017.6%200%200%200-13-5.4H18.4c-5%200-9.3%201.8-12.9%205.4A17.6%2017.6%200%200%200%200%2082.2c0%205%201.8%209.3%205.4%2012.9l128%20127.9c3.6%203.6%207.8%205.4%2012.8%205.4s9.2-1.8%2012.8-5.4L287%2095c3.5-3.5%205.4-7.8%205.4-12.8%200-5-1.9-9.2-5.5-12.8z%22%2F%3E%3C%2Fsvg%3E'),
              linear-gradient(to bottom, #ffffff 0%,#e5e5e5 100%);
            background-repeat: no-repeat, repeat;
            /* arrow icon position (1em from the right, 50% vertical) , then gradient position*/
            background-position: right .7em top 50%, 0 0;
            /* icon size, then gradient */
            background-size: .65em auto, 100%;
        }
        /* Hide arrow icon in IE browsers */
        .select-css::-ms-expand {
            display: none;
        }
        /* Hover style */
        .select-css:hover {
            border-color: #888;
        }
        /* Focus style */
        .select-css:focus {
            border-color: #aaa;
            /* It'd be nice to use -webkit-focus-ring-color here but it doesn't work on box-shadow */''' + '''
            box-shadow: 0 0 1px 3px {};'''.format(background_color_box) + '''
            box-shadow: 0 0 0 3px -moz-mac-focusring;
            color: #222;
            outline: none;
        }

        /* Set options to normal weight */
        .select-css option {
            font-weight:normal;
        }

        /* Support for rtl text, explicit support for Arabic and Hebrew */
        *[dir="rtl"] .select-css, :root:lang(ar) .select-css, :root:lang(iw) .select-css {
            background-position: left .7em top 50%, 0 0;
            padding: .6em .8em .5em 1.4em;
        }

        /* Disabled styles */
        .select-css:disabled, .select-css[aria-disabled=true] {
            color: graytext;
            background-image: url('data:image/svg+xml;charset=US-ASCII,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20width%3D%22292.4%22%20height%3D%22292.4%22%3E%3Cpath%20fill%3D%22graytext%22%20d%3D%22M287%2069.4a17.6%2017.6%200%200%200-13-5.4H18.4c-5%200-9.3%201.8-12.9%205.4A17.6%2017.6%200%200%200%200%2082.2c0%205%201.8%209.3%205.4%2012.9l128%20127.9c3.6%203.6%207.8%205.4%2012.8%205.4s9.2-1.8%2012.8-5.4L287%2095c3.5-3.5%205.4-7.8%205.4-12.8%200-5-1.9-9.2-5.5-12.8z%22%2F%3E%3C%2Fsvg%3E'),
              linear-gradient(to bottom, #ffffff 0%,#e5e5e5 100%);
        }\n</style>\n\n'''
        return select_css

    def button_css(clss, background_color='steelblue', background_color_active='DarkCyan', background_color_focus='DarkCyan', background_color_hover='DarkCyan', background_color_visited='DarkCyan', keep_visited=False, border='none', border_radius='8px', color='floralwhite', padding='10px', text_align='center', text_decoration='none', display='inline-block', font_size='16px', margin='1px 1px', cursor='pointer'):
        """ CSS code to style an HTML button

            INPUTS:
            ------------
            clss - HTML class
            background_color - bg for button (default: steelblue)
            background_color_active -  bg active for button (default: DarkCyan)
            background_color_focus -  bg focus for button (default: DarkCyan)
            background_color_hover -  bg on hover for button (default: DarkCyan)
            background_color_visited -  bg visited for button (default: DarkCyan)
            keep_visited - bool (default: False) keep color after visit
            border -  string like '1px' to set border width for button (default: none)
            border_radius - string like '8px' to set border radius (default: '8px')
            color - string to set text color (default: 'floralwhite')
            padding - string to set padding (default: '10px')
            text_align - string to align button description (default: 'center'), further options: 'left', 'right'
            text_decoration - string (default: 'none')
            display - string to set button alignment (default: 'inline-block')
            font_size - string to set button font size (default: '16px')
            margin - string to set margins (default: '1px 1px')
            cursor - string to set type of cursor on hover (default: 'pointer')

            OUTPUTS:
            ------------
            button_css - string (CSS code) to style an HTML button
        """

        button_css="""<!-- ++++++++++++++++++++ CSS: Button Style ++++++++++++++++++++ -->\n<style>""" + """
            .{0}""".format(clss) + """{""" + """
              background-color: {};""".format(background_color) +"""
              border: {};""".format(border) + """
              border-radius: {};""".format(border_radius) + """
              color: {};""".format(color) + """
              padding: {};""".format(padding) + """
              text-align: {};""".format(text_align) + """
              text-decoration: {};""".format(text_decoration) + """
              display: {};""".format(display) + """
              font-size: {};""".format(font_size) + """
              margin: {};""".format(margin) + """
              cursor: {};""".format(cursor) + """}""" + """

             .{0}:active""".format(clss) + """{""" + """
              background-color: {};""".format(background_color_active) + """
              border: {};""".format(border) + """
              border-radius: {};""".format(border_radius) + """}""" + """

             .{0}:focus""".format(clss) + """{""" + """
              background-color: {};""".format(background_color_focus) + """
              border: {};""".format(border) + """
              border-radius: {};""".format(border_radius) + """}""" + """

             .{0}:hover""".format(clss) + """{""" + """
              background-color: {};""".format(background_color_hover) + """
              border: {};""".format(border) + """
              border-radius: {};""".format(border_radius) + """}"""

        if keep_visited==True:
            button_css +=""".{0}:visited""".format(clss) + """{""" + """
                  background-color: {};""".format(background_color_visited) + """}"""

        button_css +="""\n</style>\n\n"""

        return button_css

    def button_css_2(clss='input_button_clss', background_color='steelblue', background_color_active='DarkCyan', background_color_focus='DarkCyan', background_color_hover='DarkCyan', background_color_visited='DarkCyan', keep_visited=False, border='none', border_radius='8px', color='floralwhite', padding='10px', text_align='center', text_decoration='none', display='inline-block', font_size='16px', margin='1px 1px', cursor='pointer'):
        """ CSS code to style an HTML button

            INPUTS:
            ------------
            clss - HTML class
            background_color - bg for button (default: steelblue)
            background_color_active -  bg active for button (default: DarkCyan)
            background_color_focus -  bg focus for button (default: DarkCyan)
            background_color_hover -  bg on hover for button (default: DarkCyan)
            background_color_visited -  bg visited for button (default: DarkCyan)
            keep_visited - bool (default: False) keep color after visit
            border -  string like '1px' to set border width for button (default: none)
            border_radius - string like '8px' to set border radius (default: '8px')
            color - string to set text color (default: 'floralwhite')
            padding - string to set padding (default: '10px')
            text_align - string to align button description (default: 'center'), further options: 'left', 'right'
            text_decoration - string (default: 'none')
            display - string to set button alignment (default: 'inline-block')
            font_size - string to set button font size (default: '16px')
            margin - string to set margins (default: '1px 1px')
            cursor - string to set type of cursor on hover (default: 'pointer')

            OUTPUTS:
            ------------
            button_css - string (CSS code) to style an HTML button
        """

        button_css="""<!-- ++++++++++++++++++++ CSS: Button Style ++++++++++++++++++++ -->\n<style>""" + """
            .{0}""".format(clss) + """{""" + """
              background-color: {};""".format(background_color) +"""
              border: {};""".format(border) + """
              border-radius: {};""".format(border_radius) + """
              color: {};""".format(color) + """
              padding: {};""".format(padding) + """
              text-align: {};""".format(text_align) + """
              text-decoration: {};""".format(text_decoration) + """
              display: {};""".format(display) + """
              font-size: {};""".format(font_size) + """
              margin: {};""".format(margin) + """
              cursor: {};""".format(cursor) + """}""" + """

             .{0}:active""".format(clss) + """{""" + """
              background-color: {};""".format(background_color_active) + """
              border: {};""".format(border) + """
              border-radius: {};""".format(border_radius) + """}""" + """

             .{0}:focus""".format(clss) + """{""" + """
              background-color: {};""".format(background_color_focus) + """
              border: {};""".format(border) + """
              border-radius: {};""".format(border_radius) + """}""" + """

             .{0}:hover""".format(clss) + """{""" + """
              background-color: {};""".format(background_color_hover) + """
              border: {};""".format(border) + """
              border-radius: {};""".format(border_radius) + """}"""

        if keep_visited==True:
            button_css +=""".{0}:visited""".format(clss) + """{""" + """
                  background-color: {};""".format(background_color_visited) + """}"""

        button_css +="""\n</style>\n\n"""

        return button_css

    def checkbox_css(width='25px', height='25px', font_family='Arial', label_color='black', label_font_size=20):
        """ CSS code to style an HTML checkbox

            INPUTS:
            ------------
            width - string to set width of checkbox (default: '25px')
            height - string to set height of checkbox (default: '25px')
            font_family - string to set font type for checkbox description (default: 'Arial')
            label_color - string to set font color for checkbox description (default: 'black')
            label_font_size - int to set font size for checkbox description (default: 20)

            OUTPUTS:
            ------------
            checkbox_css - string (CSS code) to style an HTML checkbox
        """

        checkbox_css ='''<!-- ++++++++++++++++++++ Checkbox Style ++++++++++++++++++++ -->\n<style>
        /* The container */
        .container {
          display: block;
          position: relative;
          padding-left: 35px;
          margin-bottom: 12px;
          cursor: pointer;''' + '''
          font-family: "{0}";'''.format(font_family) + '''
          font-size: {0}px;'''.format(label_font_size) + '''
          color: "{0}";'''.format(label_color) + '''
          -webkit-user-select: none;
          -moz-user-select: none;
          -ms-user-select: none;
          user-select: none;
        }

        /* Hide the browser's default checkbox */
        .container input {
          position: absolute;
          opacity: 0;
          cursor: pointer;
          height: 0;
          width: 0;
        }

        /* Create a custom checkbox */
        .checkmark {
          position: absolute;
          top: 0;
          left: 0;''' + '''
          height: {};'''.format(height) + '''
          width: {};'''.format(width) + '''
          background-color: #eee;
        }

        /* On mouse-over, add a grey background color */
        .container:hover input ~ .checkmark {
          background-color: #ccc;
        }

        /* When the checkbox is checked, add a blue background */
        .container input:checked ~ .checkmark {
          background-color: #2196F3;
        }

        /* Create the checkmark/indicator (hidden when not checked) */
        .checkmark:after {
          content: "";
          position: absolute;
          display: none;
        }

        /* Show the checkmark when checked */
        .container input:checked ~ .checkmark:after {
          display: block;
        }

        /* Style the checkmark/indicator */
        .container .checkmark:after {
          left: 9px;
          top: 5px;
          width: 5px;
          height: 10px;
          border: solid white;
          border-width: 0 3px 3px 0;
          -webkit-transform: rotate(45deg);
          -ms-transform: rotate(45deg);
          transform: rotate(45deg);
        }\n</style>\n\n'''

        return checkbox_css

    def hbox_css(margin_right='20'):
        """ CSS code to style a simple horizontal alignment of HTML elements
            CSS code for HTML.hbox(...)

            INPUTS:
            ------------
            margin_right - string to set space to the right between HTML elements (default: '20')

            OUTPUTS:
            ------------
            hbox_css - string (CSS code) to style an HTML hbox element
        """

        hbox_css= '''\n<!-- ++++++++++++++++++++ HBox ++++++++++++++++++++ -->\n<style>
        .inline_items_ul {
            margin: 0;
            padding: 0;
            list-style-type: none;

        }
        .inline_items_li {
            display: inline-block;''' + '''
            margin-right: {}px;'''.format(margin_right) + '''

        }\n</style>\n\n'''

        return hbox_css

    def blog_box_css():
        """ CSS code to style an HTML.blog_box(...) object

            INPUTS:
            ------------
            None

            OUTPUTS:
            ------------
            blog_box_css - string (CSS code) to style an HTML.blog_box(...) object
        """

        blog_box_css = '''
            <style>
                .panel_header{
                  text-align: center;
                  font-family: 'Baloo Tamma', cursive;
                  font-size: 24;
                }
                .li_panelItem{
                  color: #2c3e50;
                  font-size: 18px;
                  line-height: 25px;
                  text-align: left;

                  font-family: 'Arial Narrow', serif;
                }
                /*SG = style grid*/
                .SG{
                  margin: 0;
                  padding: 0;
                  text-align: center;
                }
                .SG .sgLi{
                  min-width: 80%;
                  margin: 2% .35%;
                  display: inline-flex;
                  box-shadow: 0 2px 4px rgba(0,0,0, .2);
                }
                .SG .sgLi:hover{
                  box-shadow:0 5px 10px rgba(0,0,0,.15);}
                .SG .box{
                  width: 100%;

                  padding-right: 5px;
                  padding-bottom: 5px;
                  background: #fff;
                  min-height: 200px;

                  box-sizing: border-box;
                }
            </style>
        '''
        return blog_box_css
