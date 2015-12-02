((*- extends 'article.tplx' -*))

((* block docclass *))
\documentclass[reprint, floatfix, groupaddress, prb]{revtex4-1}

\usepackage{placeins}

\AtBeginDocument{
\heavyrulewidth=.08em
\lightrulewidth=.05em
\cmidrulewidth=.03em
\belowrulesep=.65ex
\belowbottomsep=0pt
\aboverulesep=.4ex
\abovetopsep=0pt
\cmidrulesep=\doublerulesep
\cmidrulekern=.5em
\defaultaddspace=.5em
}

((* endblock docclass *))

% Author and Title from metadata
((* block maketitle *))

((*- if nb.metadata["latex_metadata"]: -*))
((*- if nb.metadata["latex_metadata"]["author"]: -*))
    \author{((( nb.metadata["latex_metadata"]["author"] )))}
((*- endif *))
((*- else -*))
    \author{Julius C. F. Schulz}
((*- endif *))

((*- if nb.metadata["latex_metadata"]: -*))
((*- if nb.metadata["latex_metadata"]["affiliation"]: -*))
    \affiliation{((( nb.metadata["latex_metadata"]["affiliation"] )))}
((*- endif *))
((*- endif *))

((*- if nb.metadata["latex_metadata"]: -*))
((*- if nb.metadata["latex_metadata"]["title"]: -*))
    \title{((( nb.metadata["latex_metadata"]["title"] )))}
((*- endif *))
((*- else -*))
    \title{((( resources.metadata.name )))}
((*- endif *))

\date{\today}
\maketitle
((* endblock maketitle *))

% New mechanism for rendering figures with captions
((*- block data_png -*))
((*- if cell.metadata.widefigure: -*))
    ((( draw_widefigure_with_caption(output.metadata.filenames['image/png'], cell.metadata.caption, cell.metadata.label) )))
((*- else -*))
    ((*- if cell.metadata.caption: -*))
        ((*- if cell.metadata.label: -*))
            ((( draw_figure_with_caption(output.metadata.filenames['image/png'], cell.metadata.caption, cell.metadata.label) )))
        ((*- else -*))
            ((( draw_figure_with_caption(output.metadata.filenames['image/png'], cell.metadata.caption, "") )))
        ((*- endif *))
    ((*- else -*))
        ((( draw_figure_with_caption(output.metadata.filenames['image/png'], "") )))
    ((*- endif *))
((*- endif *))
((*- endblock -*))
((*- block data_jpg -*))
((*- if cell.metadata.caption: -*))
    ((*- if cell.metadata.label: -*))
        ((( draw_figure_with_caption(output.metadata.filenames['image/jpeg'], cell.metadata.caption, cell.metadata.label) )))
    ((*- else -*))
        ((( draw_figure_with_caption(output.metadata.filenames['image/jpeg'], cell.metadata.caption, "") )))
    ((*- endif *))
((*- else -*))
    ((( draw_figure_with_caption(output.metadata.filenames['image/jpeg'], "") )))
((*- endif *))
((*- endblock -*))
((*- block data_svg -*))
((*- if cell.metadata.caption: -*))
    ((*- if cell.metadata.label: -*))
        ((( draw_figure_with_caption(output.metadata.filenames['image/svg+xml'], cell.metadata.caption, cell.metadata.label) )))
    ((*- else -*))
        ((( draw_figure_with_caption(output.metadata.filenames['image/svg+xml'], cell.metadata.caption, "") )))
    ((*- endif *))
((*- else -*))
    ((( draw_figure_with_caption(output.metadata.filenames['image/svg+xml'], "") )))
((*- endif *))
((*- endblock -*))
((*- block data_pdf -*))
((*- if cell.metadata.widefigure: -*))
    ((( draw_widefigure_with_caption(output.metadata.filenames['application/pdf'], cell.metadata.caption, cell.metadata.label) )))
((*- else -*))
    ((*- if cell.metadata.caption: -*))
        ((*- if cell.metadata.label: -*))
            ((( draw_figure_with_caption(output.metadata.filenames['application/pdf'], cell.metadata.caption, cell.metadata.label) )))
        ((*- else -*))
            ((( draw_figure_with_caption(output.metadata.filenames['application/pdf'], cell.metadata.caption, "") )))
        ((*- endif *))
    ((*- else -*))
        ((( draw_figure_with_caption(output.metadata.filenames['application/pdf'], "") )))
    ((*- endif *))
((*- endif *))
((*- endblock -*))

% Draw a figure using the graphicx package.
((* macro draw_figure_with_caption(filename, caption, label) -*))
((* set filename = filename | posix_path *))
((*- block figure scoped -*))
    \begin{figure}
        \begin{center}\adjustimage{max size={0.9\linewidth}{0.4\paperheight}}{((( filename )))}\end{center}
        \caption{((( caption )))}
        \label{((( label )))}
    \end{figure}
((*- endblock figure -*))
((*- endmacro *))

% Draw a figure using the graphicx package.
((* macro draw_widefigure_with_caption(filename, caption, label) -*))
((* set filename = filename | posix_path *))
((*- block figure_wide scoped -*))
    \begin{figure*}
        \begin{center}\adjustimage{max size={0.9\linewidth}{0.4\paperheight}}{((( filename )))}\end{center}
        \caption{((( caption )))}
        \label{((( label )))}
    \end{figure*}
((*- endblock figure_wide -*))
((*- endmacro *))



% Disable input cells
((* block input_group *))
((* endblock input_group *))
