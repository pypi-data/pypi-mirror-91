__all__ = [
    "image_processing",
    "image_processing_1",
    "make_tex_document",
    "make_tex_document_1",
    "build_bbox",
]
'''
Function used for Batch processing of the confocal images

Inputs 
Confocal images as .plu files (binary standard of Sensofar company)

Input files organization 
For several images 'wafer #-&' per wafer 'wafer #' per cut 'cut ###'

the files organization is as follows:

root / cut ### / wafer # / save_plu / wafer #-&.plu
where:

    - & stands for a, b, c, d, e 
    - \# stands for a digit
    - total number of files is open for each 'wafer #'
    - total number of cuts ### defined by length of list cuts

Outputs
5 files per image 'wafer #-&' 
    - EXCEL file 'wafer#-&.xlsx' containing the morphological information of the features
    - JPEG file of the corrected raw image with indication of the corrected pixels
    - JPEG file 'wafer#-&-im-rebuild.jpg' of the features represented in colored circular dots of equivalent area as the real features
with color scale relative to the features depth
    - JPEG file 'wafer#-&-im-bbox.jpg' of the features size histogram
    - JPEG file 'wafer#-&-im-hist.jpg' of box plot of the features size

A $\LaTeX$ file 'cut_report ###.tex' as a report gathering the 4 JPEG files and a graph per cut integrating all the corresponding box plots 

output files location 
'root / cut ### / wafer # / results /' for 'wafer#-&.xlsx' and the JPEG files 
'root / cut ### /' for cut_report ###.tex

where:
    - & stands for a, b, c, d, e 
    - \# stands for a digit, 

'''


def image_processing_1(param, analyse_morpho=True):
    '''
    Process an image by:
        - reading a .plu image
        - substituing non measured values by interpolated ones
        - levelling the image using a morphological filter (top hat)
        - binarizing the image using a threshold
        - doing an image morphological analysis
    Arguments:
        param (dict) : param["repertoire"] name of the directory
                       param["file"] name of the file to process
                       param["dir_results"] name of the directory where the morphological resuts are stored
                       param['Top_hat_length'] top hat legth should be larger than the largest feature to extract
                       param['threshold'] should be larger than the residual image background
        analyse_morpho (bool): if True do the morphological analysis 
    Returns:
        if analyse_morpho == True
            df (dataframe): index|'x'|'long_x'| 'y'|'long_y'| 'size'|'depth' with :
                - index: feature index
                - x: gravity center x position of the feature
                - long_x: maximum feature width
                - y: gravity center y position of the feature
                - long_y: maximum feature height
                - size: pixels number of the feature 
                - depth : feature depth 
        if analyse_morpho == False  returns None
    '''

    # 3rd party import
    from pathlib import Path
    import pandas as pd
    import numpy as np
    
    # Internal import
    from .image_features_extract import fill_gap, analyse_morphologique
    from .image_features_extract import read_plu_topography, top_hat_flattening

    # .plu image reading and correction
    N, M, confocal_img, rgb = read_plu_topography(param["repertoire"] / param["file"]) # fle .plu reading
    confocal_img1 = fill_gap(confocal_img) # substitute non measured values by interpolated ones

    
    # top hat processing
    im_corr = top_hat_flattening(confocal_img1,param['Top_hat_length'],top_hat_sens=-1)
    
    # binarization
    im_bin = np.where(im_corr < param['threshold'], 1, 0)

    # morphological analysis
    df = None
    if analyse_morpho:
        file_save_excel = Path(param["file"]).stem + ".xlsx"
        df = analyse_morphologique(im_bin, img=im_corr)
        df.to_excel(param["dir_results"] / file_save_excel)
    return confocal_img1, im_corr, im_bin, df

def image_processing(param, analyse_morpho=True):
    '''
    depreciated use image_processing_1
    '''

    # 3rd party import
    from pathlib import Path
    import pandas as pd
    
    # Internal import
    from .image_features_extract import read_image,gaussian_flattening, analyse_morphologique
    from .image_features_extract import xRemoveSpriesHorizontal, Otsu_tresholding

    # lecture de l'image
    im_brute, n_row, n_col = read_image(param["repertoire"] / param["file"])

    # mise à plat de l'image
    im_flat = gaussian_flattening(im_brute, param["sigma"])
    # im_flat = poly_flattening(im_brute)

    # supression des traces verticales
    im_corr_strie = xRemoveSpriesHorizontal(
        im_flat, param["decNum_h"], param["wname"], param["sigma_wl_h"]
    )

    # binarisation de l'image
    im_bin = Otsu_tresholding(im_corr_strie, Ostu_corr=param["Ostu_corr"])

    # analyse morphologique
    df = None
    if analyse_morpho:
        file_save_excel = Path(param["file"]).stem + ".xlsx"
        df = analyse_morphologique(im_bin)
        df.to_excel(param["dir_results"] / file_save_excel)
    return im_brute, im_corr_strie, im_flat, im_bin, df


def make_tex_document(
    param,
    im_brute,
    im_corr_strie,
    im_flat,
    im_bin,
    df,
    mode="w",
    flag=False,
    new_section=False,
):
    '''
    make_tex_document_1
    '''
    # 3rd party import
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib
    from pathlib import Path
    import os
    
    from .image_features_extract import convert
    size_min = 50
    alpha1 = 0.35
    alpha2 = 0.8

    print(param["file"])
    n_row, n_col = np.shape(im_brute)

    fig = plt.figure(figsize=(8, 8))
    ax1 = fig.add_subplot(111)
    im_flat = im_flat - im_flat.min()
    ax1.imshow(im_flat, interpolation="nearest", cmap=plt.cm.gray)

    df1 = df.query("size >= @size_min")
    patchesb = []
    for x1, y1, r in zip(df1["y"], df1["x"], df1["size"]):
        circle = plt.Circle((x1, y1), np.sqrt(r / np.pi))
        patchesb.append(circle)

    df1 = df.query("size < @size_min")
    patchesc = []
    for x1, y1, r in zip(df1["y"], df1["x"], df1["size"]):
        circle = plt.Circle((x1, y1), np.sqrt(r / np.pi))
        patchesc.append(circle)

    p = matplotlib.collections.PatchCollection(
        patchesb, cmap=matplotlib.cm.jet, alpha=alpha1, facecolor="blue"
    )
    pc = matplotlib.collections.PatchCollection(
        patchesc, cmap=matplotlib.cm.jet, alpha=alpha2, facecolor="green"
    )
    ax1.add_collection(p)
    ax1.add_collection(pc)
    file_save_im_brute = Path(param["file"]).stem + "-im-brute.jpg"
    plt.savefig(param["dir_results"] / file_save_im_brute, bbox_inches="tight")
    plt.close(fig)

    fig = plt.figure(figsize=(8, 8))
    ax1 = fig.add_subplot(111)
    ax1.imshow(convert(im_bin), interpolation="nearest", cmap=plt.cm.gray)
    file_save_im_bin = Path(param["file"]).stem + "-im-bin.jpg"
    plt.savefig(param["dir_results"] / file_save_im_bin, bbox_inches="tight")
    plt.close(fig)

    fig = plt.figure(figsize=(8, 8))
    ax1 = fig.add_subplot(111)
    ax1.hist(df["size"], bins=40)
    ax1.set_title("histogramme des tailles")
    file_save_im_hist = Path(param["file"]).stem + "-im-hist.jpg"
    plt.savefig(param["dir_results"] / file_save_im_hist, bbox_inches="tight")
    plt.close(fig)

    fig = plt.figure(figsize=(8, 8))
    ax1 = fig.add_subplot(111)
    ax1.boxplot(df["size"])
    file_save_im_erea = Path(param["file"]).stem + "-im-bbox.jpg"
    plt.savefig(param["dir_results"] / file_save_im_erea, bbox_inches="tight")
    plt.close(fig)

    file_save_doc_tex = Path(param["file"]).stem + "_doc_tex.tex"
    with open(param["dir_tex"] / Path("rapport.tex"), mode) as doc:
        if mode == "w":
            doc.write(
                r"""\documentclass[a4paper, 10pt]{article}
        \usepackage[american]{babel}
        \usepackage{amsmath}
        \usepackage{amsthm}
        \numberwithin{equation}{section}
        \usepackage[left=2cm,right=2cm,top=2cm,bottom=2cm]{geometry}
        \usepackage{graphicx}
        \usepackage{hyperref}
        \usepackage{empheq}
        \usepackage{pythonhighlight}"""
            )
            doc.write(
                r"\graphicspath{"
                + ",".join(
                    ["{./" + "wafer " + str(i) + "/" + "results}" for i in range(1, 6)]
                )
                + "}"
            )
            doc.write(
                r"""\begin{document}
        \tableofcontents
        \newpage"""
                + "\n"
            )
            # doc.write(r'\section{' + str(param['repertoire']).split('\\')[-2]+'}'+'\n')

            doc.write(r"\section{Parameters}")
            doc.write(
                r"\begin{center} \begin{tabular}{|" + " | ".join(["l"] * 2) + "|}\n"
            )
            doc.write("\\hline\n")
            doc.write(" & ".join([str(x) for x in ["parameter", "Value"]]) + " \\\\\n")
            doc.write("\\hline\n")
            doc.write("\\hline\n")
            for key, value in param.items():
                if key in ["wname", "sigma_wl_h", "decNum_h", "sigma", "Ostu_corr"]:

                    doc.write(key.replace("_", "\_") + " & " + str(value) + " \\\\\n")
                    doc.write("\\hline\n")
            doc.write(r"\end{tabular} \end{center} ")

            doc.write(r"\section{" + param["cut"] + "}" + "\n")
        if new_section:
            doc.write(r"\subsection{" + param["wafer"] + "}" + "\n")
        doc.write(r"\subsubsection{" + param["file"] + "}" + "\n")
        doc.write(
            r"""\begin{figure}[h]
        \begin{center}
        \begin{tabular}{cc}
        (a) & (b)\\"""
            + "\n"
        )
        doc.write(
            r"\includegraphics[width=0.5\textwidth]{"
            + file_save_im_brute
            + r"} & \includegraphics[width=0.5\textwidth]{"
            + file_save_im_bin
            + r"}\\"
            + "\n"
        )
        doc.write(r"(c) & (d)\\" + "\n")
        doc.write(
            r"\includegraphics[width=0.5\textwidth]{"
            + file_save_im_hist
            + r"} & \includegraphics[width=0.5\textwidth]{"
            + file_save_im_erea
            + r"}\\"
            + "\n"
        )
        doc.write(
            r"""\end{tabular}
        \end{center}
        \caption{Image processing: (a) Superposition of the flattened image with the detected defaults, the erea of the circles
        are equal to the erea of the defaults, the green circle have an area less than 50 px, the blue one have area greater or
        equal than 50 px
        ; (b) Binarized image; (c) Area histogram; (d) Box plot of the area.}
        \end{figure}"""
            + "\n"
        )
        if flag:
            build_bbox(param, size_min=0)
            doc.write(r"\section {Synthese}")
            doc.write(
                r"\includegraphics[width=0.9\textwidth]{synthesege0.png} \newpage "
            )
            build_bbox(param, size_min=size_min, method="lt")
            doc.write(
                r"\includegraphics[width=0.9\textwidth]{syntheselt"
                + str(size_min)
                + r".png} \newpage "
            )
            build_bbox(param, size_min=size_min, method="ge")
            doc.write(
                r"\includegraphics[width=0.9\textwidth]{synthesege"
                + str(size_min)
                + ".png}"
            )
            doc.write(r"\end {document}")
        else:
            doc.write(r"\newpage")

    return


def build_bbox(param, size_min=50, method="ge"):
    '''
    aggregation of several box plot in a unique one.
    
    Arguments:
        param (dict) : param["root"] root (Path)
                       param["cut"] name of the cut directory
        size_min (int) : threshold used to slect the features according to their size
        method (string): if method = "ge" we build a bbox with features with size >= size_min
                         if method = "lt" we build a bbox with features with size < size_min
    Returns:
        a PNG image stored in param["root"] / Path(param["cut"]) / Path("synthese" + method + str(size_min) + ".png"
    '''

    import os
    
    # 3rd party import
    import pandas as pd
    from pathlib import Path
    import matplotlib.pyplot as plt

    import os
    rep_wafers = [
                  param["root"] / Path(param["cut"]) / Path(x) / Path("results") 
                  for x in os.listdir(param["root"] / Path(param["cut"])) if  'wafer' in x
                 ]
    s = {}
    len_max = 0
    for rep_wafer in rep_wafers:
        for x in [y for y in os.listdir(rep_wafer) if y.split(".")[-1] == "xlsx"]:
            df = pd.read_excel(rep_wafer / x)
            key = x.split(".")[0]
            if method == "ge":
                s[key] = df.query("size >= @size_min")["size"]
            else:
                s[key] = df.query("size < @size_min")["size"]

            len_max = max(len(s[key]), len_max)
    for key, value in s.items():
        dif = len_max - len(value)
        if dif > 0:
            a = list(value)
            a.extend([None] * (dif))
            s[key] = a
    df = pd.DataFrame.from_dict(s)

    ax = df.plot.box(rot=0, figsize=(8, 15), grid=True, vert=False)
    ax.set_title(param['cut'])
    plt.savefig(
        param["root"]
        / Path(param["cut"])
        / Path("synthese" + method + str(size_min) + ".png"),
        bbox_inches="tight",
    )
    return
    
def make_tex_document_1(
    param,
    df,
    mode
):
    '''
    Build a tech report containig a: 
        - header with the experimental condition
        - section per image processing, 
        - tailer with the aggregated box plot
    
    Arguments:
        param (dict):
        df (data frame) : 
        mode (str) : "header" open a new file and add a header
                     "corpus" append section
                     "tailer" add a tailer
    '''
    
    # 3rd party import
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib
    import matplotlib.cm as cmx
    from pathlib import Path
    import os
    
    # internal import
    from .image_features_extract import read_plu_topography, fill_gap

    size_min = 50


    fig = plt.figure(figsize=(8, 8))
    N, M, confocal_img, rgb = read_plu_topography(param['repertoire']/param['file'])
    
    # raw image save
    confocal_img1 = fill_gap(confocal_img)
    plt.imshow(confocal_img1, cmap='gray')
    plt.colorbar()
    mask = np.where(confocal_img == 1000001) # find non measured pixels
    plt.scatter(mask[1],mask[0],c='r',s =1,alpha=0.1 )

    file_save_im_raw = Path(param["file"]).stem + "-im-raw.jpg"
    plt.savefig(param["dir_results"] / file_save_im_raw, bbox_inches="tight")
    plt.close(fig)
    
    # reconstructed image save
    fig = plt.figure(figsize=(8, 8))
    colorsMap = plt.get_cmap("plasma") #("RdYlGn")
    g = list(zip(np.array(df['x']),
                 np.array(df['y']),
                 np.array(df['height']),
                 np.array(df['size'])))
    x,y,c,s = zip(*sorted(g, key=lambda tup: tup[2],reverse=False))

    cm = plt.get_cmap(colorsMap)
    cNorm = matplotlib.colors.Normalize(vmin=min(c), vmax=max(c))
    scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=cm)

    plt.scatter(np.array(x) ,N-np.array(y) ,s=np.array(s)/5, c=scalarMap.to_rgba(c))
    plt.xlim(0,M)
    plt.ylim(0,N)
    scalarMap.set_array(c)

    trash = plt.yticks(ticks=[N,N-100, N-200, N-300, N-400, N-500],labels=[0,100,200,300,400,500],
                                   rotation=0)
    plt.colorbar(scalarMap)

    file_save_im_rebuild = Path(param["file"]).stem + "-im-rebuild.jpg"
    plt.savefig(param["dir_results"] / file_save_im_rebuild, bbox_inches="tight")
    plt.close(fig)

    # features size histogram plot
    fig = plt.figure(figsize=(8, 8))
    ax1 = fig.add_subplot(111)
    ax1.hist(df["size"], bins=40)
    file_save_im_hist = Path(param["file"]).stem + "-im-hist.jpg"
    plt.savefig(param["dir_results"] / file_save_im_hist, bbox_inches="tight")
    plt.close(fig)

    # features size box plot
    fig = plt.figure(figsize=(8, 8))
    ax1 = fig.add_subplot(111)
    ax1.boxplot(df["size"])
    file_save_im_erea = Path(param["file"]).stem + "-im-bbox.jpg"
    plt.savefig(param["dir_results"] / file_save_im_erea, bbox_inches="tight")
    plt.close(fig)

    # tex report generation
    file_save_doc_tex = Path(param["file"]).stem + "_doc_tex.tex"
    
    w_a = "a"
    if mode == 'header': w_a = 'w'
        
    with open(param["dir_tex"] / Path('rapport_'+param['cut']+'.tex'), w_a) as doc:
    
        if mode == "header":
            doc.write(
                r"""\documentclass[a4paper, 10pt]{article}
                    \usepackage[american]{babel}
                    \usepackage{amsmath}
                    \usepackage{amsthm}
                    \numberwithin{equation}{section}
                    \usepackage[left=2cm,right=2cm,top=2cm,bottom=2cm]{geometry}
                    \usepackage{graphicx}
                    \usepackage{hyperref}
                    \usepackage{empheq}
                    \usepackage{pythonhighlight}"""
            )
            doc.write(
                r"\graphicspath{"
                + ",".join(
                    ["{./" + "wafer " + str(i) + "/" + "results}" for i in range(1, 6)]
                )
                + "}"
            )
            doc.write(
                r"""\begin{document}
                    \tableofcontents
                    \newpage"""
                + "\n"
            )
            # doc.write(r'\section{' + str(param['repertoire']).split('\\')[-2]+'}'+'\n')

            doc.write(r"\section{Parameters}")
            doc.write(
                r"\begin{center} \begin{tabular}{|" + " | ".join(["l"] * 2) + "|}\n"
            )
            doc.write("\\hline\n")
            doc.write(" & ".join([str(x) for x in ["parameter", "Value"]]) + " \\\\\n")
            doc.write("\\hline\n")
            doc.write("\\hline\n")
            for key, value in param.items():
                if key in ['threshold', 'Top_hat_length']:

                    doc.write(key.replace("_", "\_") + " & " + str(value) + " \\\\\n")
                    doc.write("\\hline\n")
            doc.write(r"\end{tabular} \end{center} ")
            doc.write(r"\section{" + param["cut"] + "}" + "\n")
            doc.write(r"\subsection{" + param["wafer"] + "}" + "\n")
            
        doc.write(r"\subsubsection{" + param["file"] + "}" + "\n")
        doc.write(
            r"""\begin{figure}[h]
                \begin{center}
                \begin{tabular}{cc}
                (a) & (b)\\"""
            + "\n"
        )
        doc.write(
            r"\includegraphics[width=0.5\textwidth]{"
            + file_save_im_raw
            + r"} & \includegraphics[width=0.5\textwidth]{"
            + file_save_im_rebuild
            + r"}\\"
            + "\n"
        )
        doc.write(r"(c) & (d)\\" + "\n")
        doc.write(
            r"\includegraphics[width=0.5\textwidth]{"
            + file_save_im_hist
            + r"} & \includegraphics[width=0.5\textwidth]{"
            + file_save_im_erea
            + r"}\\"
            + "\n"
        )
        doc.write(
            r"""\end{tabular}
        \end{center}
        \caption{Image processing: (a) Superposition of the confocal topographic image with non measured pixels (in red)
        ; (b) Image of the extracted features where the sizes of the cicles are proportional to the features area 
        and where the color of the circles are related to the features depth; (c) Area histogram; (d) Box plot of the area.}
        \end{figure}"""
            + "\n"
        )
        
        
        if mode == 'tailer':  # add a tailer with the agregated b box
            build_bbox(param, size_min=0)
            doc.write(r"\section {Synthese}")
            doc.write(
                r"\includegraphics[width=0.9\textwidth]{synthesege0.png} \newpage "
            )
            build_bbox(param, size_min=size_min, method="lt")
            doc.write(
                r"\includegraphics[width=0.9\textwidth]{syntheselt"
                + str(size_min)
                + r".png} \newpage "
            )
            build_bbox(param, size_min=size_min, method="ge")
            doc.write(
                r"\includegraphics[width=0.9\textwidth]{synthesege"
                + str(size_min)
                + ".png}"
            )
            doc.write(r"\end {document}")
        else:
            doc.write(r"\newpage")

    return