%from json2html import *
%import tomd
<!-- 
From: 
SimpleTemplate Engine https://bottlepy.org/docs/0.11/stpl.html 
-->

<!-- 
The contained python statement is executed at render-time and has
access to all keyword arguments passed to the SimpleTemplate.render()
method. HTML special characters are escaped automatically to prevent
XSS attacks.  You can start the statement with an exclamation mark 
to disable escaping for that statement 
-->

<html>
    <head>
        <title>JSON Tables</title>
        <style>
            table {
                border: none;
                border-collapse: collapse;
            }
        </style>
    </head>
    <body>

    %projs = []
    %for row in rows:
	%projs.append(row['project'])
        %end

    %projs = sorted(set(projs))
    %for proj in projs:
        <h2>{{proj}}</h2>

        %for row in rows:
            %if row['project'] == str(proj):
		<!-- dict1=dict2 just points to same object;
		have to use copy() -->
	        %a = row.copy()
		%del a['project'] 
	        %del a['status']
		%if a['date_due'] == '2000-01-01':
		    %del a['date_due']
		%end
                {{ !json2html.convert(json = a) }}
		<p></p>
            %end
	%end
        </hr>
    %end
    </body>
</html>
