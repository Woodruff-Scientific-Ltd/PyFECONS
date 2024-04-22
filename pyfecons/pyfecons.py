import os
import shutil
import subprocess
import tempfile

from pyfecons.helpers import base_name_without_extension
from pyfecons.inputs import Inputs
from pyfecons.data import Data
from pyfecons.enums import *
from pyfecons.costing.mfe.mfe import GenerateData as GenerateMFEData
from pyfecons.costing.mfe.mfe import CreateReportContent as CreateMfeReport
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
        return CreateMfeReport(inputs, data)
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
    # TODO - write hydrated templates to files and include them in tex compilation
    template_content = '\n\n'.join([report_content.hydrated_templates[key]
                                    for key in sorted(report_content.hydrated_templates.keys())])

    # Use a temporary file to generate the PDF
    with tempfile.TemporaryDirectory(prefix="pyfecons-") as temp_dir:
        # Copy included files to tex compile directory
        for tex_path, local_path in report_content.included_files.items():
            full_dest_path = os.path.join(temp_dir, tex_path)
            os.makedirs(os.path.dirname(full_dest_path), exist_ok=True)
            shutil.copy(local_path, full_dest_path)

        # TODO replace this when we copy all hydrated templates
        document_tex = 'Costing_ARPA-E_MFE_Modified.tex'
        shutil.copy(
            '/Users/craastad/code/nttau/PyFECONS/pyfecons/costing/mfe/templates/' + document_tex,
            os.path.join(temp_dir, document_tex)
        )
        document_base_name = base_name_without_extension(document_tex)

        original_dir = os.getcwd()
        os.chdir(temp_dir)

        subprocess.run(['pdflatex', document_tex], check=True)
        subprocess.run(['bibtex', document_base_name], check=True)
        subprocess.run(['pdflatex', document_tex], check=True)
        subprocess.run(['pdflatex', document_tex], check=True)

        with open(document_tex, 'r') as latex_file:
            tex_content = latex_file.read()
        with open(document_base_name + '.pdf', 'rb') as pdf_file:
            pdf_content = pdf_file.read()

        os.chdir(original_dir)

        return FinalReport(report_tex=tex_content, report_pdf=pdf_content)