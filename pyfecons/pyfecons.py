import os
import glob
import tempfile
from pyfecons.inputs import Inputs
from pyfecons.data import Data
from pyfecons.enums import *
from pyfecons.costing.mfe.mfe import GenerateData as GenerateMFEData
from pyfecons.costing.mfe.mfe import HydrateTemplates as GenerateMFETemplates
from pylatex import Document, Package
from pylatex.utils import NoEscape
from pyfecons.report import ReportContent, FinalReport


def RunCosting(inputs: Inputs) -> Data:
    if inputs.basic.reactor_type == ReactorType.MFE:
        return GenerateMFEData(inputs)
    elif inputs.basic.reactor_type == ReactorType.MIF:
        raise NotImplementedError()
    elif inputs.basic.reactor_type == ReactorType.IFE:
        raise NotImplementedError()
    raise ValueError('Invalid basic reactor type')


def CreateReportContent(inputs: Inputs, data: Data) -> ReportContent:
    """
    Create report content with given cost calculation inputs and output data.
    :param inputs: The inputs used for cost calculations.
    :param data: The output data for cost calculations.
    :return: Report contents including files, hydrated templates, and latex packages.
    """
    if inputs.basic.reactor_type == ReactorType.MFE:
        return GenerateMFETemplates(inputs, data)
    elif inputs.basic.reactor_type == ReactorType.MIF:
        raise NotImplementedError()
    elif inputs.basic.reactor_type == ReactorType.IFE:
        raise NotImplementedError()
    raise ValueError('Invalid basic reactor type')


def RenderFinalReport(report_content: ReportContent) -> FinalReport:
    """
    Compiles report contents into a final Tex and Pdf report
    :param report_content: from cost calculations
    :return: final report
    """
    # TODO - need to create ordering for the hydrated templates and support \include substitutions
    template_content = '\n\n'.join([report_content.hydrated_templates[key]
                                    for key in sorted(report_content.hydrated_templates.keys())])
    # Uncomment the following two lines to view the compiled .tex file locally if pdf rendering is failing
    # with open(f"temp/report.tex", "w") as file:
    #     file.write(template_content)

    doc = Document(documentclass='article')
    for package in report_content.latex_packages:
        doc.packages.append(Package(package))
    doc.append(NoEscape(template_content))

    # Use a temporary file to generate the PDF
    with tempfile.NamedTemporaryFile(prefix="pyfecons-", delete=False) as temp_file:
        temp_file_path = temp_file.name
    # Uncomment the following line of code to output the pylatex working directory path for debugging
    # print(f"temp filepath: {temp_file_path}")
    doc.generate_pdf(temp_file_path, clean_tex=False)
    with open(temp_file_path + '.tex', 'r') as latex_file:
        tex_content = latex_file.read()
    with open(temp_file_path + '.pdf', 'rb') as pdf_file:
        pdf_content = pdf_file.read()
    # Remove temporary files - comment out for debugging
    pattern = os.path.join(temp_file_path + "*")
    for filename in glob.glob(pattern):
        os.remove(filename)

    return FinalReport(report_tex=tex_content, report_pdf=pdf_content)