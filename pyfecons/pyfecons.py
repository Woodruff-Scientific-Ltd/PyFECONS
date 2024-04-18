import os
import glob
import tempfile
from dataclasses import dataclass
from pyfecons.inputs import Inputs
from pyfecons.data import Data
from pyfecons.enums import *
from pyfecons.costing.mfe.mfe import GenerateData as GenerateMFEData
from pyfecons.costing.mfe.mfe import HydrateTemplates as GenerateMFETemplates
from pylatex import Document, Package
from pylatex.utils import NoEscape


def RunCostingWithInput(inputs: Inputs) -> Data:
    if inputs.basic.reactor_type == ReactorType.MFE:
        return GenerateMFEData(inputs)
    elif inputs.basic.reactor_type == ReactorType.MIF:
        raise NotImplementedError()
    elif inputs.basic.reactor_type == ReactorType.IFE:
        raise NotImplementedError()
    raise ValueError('Invalid basic reactor type')


def HydrateTemplates(inputs: Inputs, data: Data) -> dict[str, str]:
    """
    Hydrates templates with given cost calculation inputs and output data.
    :param inputs: The inputs used for cost calculations.
    :param data: The output data for cost calculations.
    :return: A dictionary mapping template names to their hydrated contents.
    """
    if inputs.basic.reactor_type == ReactorType.MFE:
        return GenerateMFETemplates(inputs, data)
    elif inputs.basic.reactor_type == ReactorType.MIF:
        raise NotImplementedError()
    elif inputs.basic.reactor_type == ReactorType.IFE:
        raise NotImplementedError()
    raise ValueError('Invalid basic reactor type')


@dataclass
class FinalReport:
    report_tex: str
    report_pdf: bytes


LATEX_PACKAGES = ['hyperref', 'graphicx', 'color', 'comment']


def CreateFinalReport(hydrated_templates: dict[str, str]) -> FinalReport:
    """
    Parses hydrated templates into a final report
    :param hydrated_templates: from cost calculations
    :return: final report
    """
    # TODO - need to create ordering for the hydrated templates and support \include substitutions
    template_content = '\n\n'.join([hydrated_templates[key] for key in sorted(hydrated_templates.keys())])
    # Uncomment the following two lines to view the compiled .tex file locally if pdf rendering is failing
    # with open(f"temp/report.tex", "w") as file:
    #     file.write(template_content)

    doc = Document(documentclass='article')
    for package in LATEX_PACKAGES:
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