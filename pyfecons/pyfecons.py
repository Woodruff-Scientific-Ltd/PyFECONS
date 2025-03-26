import os
import shutil
import subprocess
import tempfile
from typing import Optional
from pyfecons.helpers import base_name_without_extension
from pyfecons.inputs.all_inputs import AllInputs
from pyfecons.enums import *
from pyfecons.costing.mfe.mfe import GenerateCostingData as GenerateMfeCostingData
from pyfecons.costing.mfe.mfe import CreateReportContent as CreateMfeReport
from pyfecons.costing.ife.ife import GenerateCostingData as GenerateIfeCostingData
from pyfecons.costing.ife.ife import CreateReportContent as CreateIfeReport
from pyfecons.report import ReportContent, FinalReport, ReportOverrides
from pyfecons.data import Data


def RunCosting(inputs: AllInputs) -> Data:
    if inputs.basic.reactor_type == ReactorType.MFE:
        return GenerateMfeCostingData(inputs)
    elif inputs.basic.reactor_type == ReactorType.IFE:
        return GenerateIfeCostingData(inputs)
    elif inputs.basic.reactor_type == ReactorType.MIF:
        raise NotImplementedError()
    raise ValueError("Invalid basic reactor type")


def CreateReportContent(
    inputs: AllInputs,
    data: Data,
    overrides: Optional[ReportOverrides] = None,
) -> ReportContent:
    """
    Create report content with given cost calculation inputs and output data.
    :param inputs: The inputs used for cost calculations.
    :param data: The output data and templates providers for cost calculations.
    :param overrides: Overriding substitutions for latex template hydration.
    :return: Report contents including files, hydrated templates, and latex packages.
    """
    if inputs.basic.reactor_type == ReactorType.MFE:
        return CreateMfeReport(data, overrides)
    elif inputs.basic.reactor_type == ReactorType.IFE:
        return CreateIfeReport(data, overrides)
    elif inputs.basic.reactor_type == ReactorType.MIF:
        raise NotImplementedError()
    raise ValueError("Invalid basic reactor type")


def RenderFinalReport(
    report_content: ReportContent, hide_output: bool = False
) -> FinalReport:
    """
    Compiles report contents into a final Tex and Pdf report
    :param report_content: from cost calculations
    :param hide_output: if true, hide console output
    :return: final report
    """
    # Use a temporary directory for tex compilation
    with tempfile.TemporaryDirectory(prefix="pyfecons-") as temp_dir:
        # Write top level document file
        document_tex = report_content.document_template.template_provider.template_file
        document_output_path = os.path.join(temp_dir, document_tex)
        with open(document_output_path, "w", encoding="utf-8") as template_file:
            template_file.write(report_content.document_template.contents)

        # Write hydrated templates to tex compile directory
        for hydrated_template in report_content.hydrated_templates:
            output_path = os.path.join(
                temp_dir, hydrated_template.template_provider.tex_path
            )
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, "w", encoding="utf-8") as template_file:
                template_file.write(hydrated_template.contents)

        # Write figures to tex compile directory
        for tex_path, figure_bytes in report_content.figures.items():
            output_path = os.path.join(temp_dir, tex_path)
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, "wb") as template_file:
                template_file.write(figure_bytes)

        # Copy included files to tex compile directory
        for tex_path, local_path in report_content.included_files.items():
            full_dest_path = os.path.join(temp_dir, tex_path)
            os.makedirs(os.path.dirname(full_dest_path), exist_ok=True)
            shutil.copy(local_path, full_dest_path)

        original_dir = os.getcwd()
        os.chdir(temp_dir)

        document_base_name = base_name_without_extension(document_tex)
        args = (
            {"stdout": subprocess.DEVNULL, "stderr": subprocess.DEVNULL}
            if hide_output
            else {}
        )
        subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", document_tex], check=True, **args
        )
        subprocess.run(["bibtex", document_base_name], check=True, **args)
        subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", document_tex], check=True, **args
        )
        subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", document_tex], check=True, **args
        )

        with open(document_tex, "r", encoding="utf-8") as latex_file:
            tex_content = latex_file.read()
        with open(document_base_name + ".pdf", "rb") as pdf_file:
            pdf_content = pdf_file.read()

        os.chdir(original_dir)

        return FinalReport(report_tex=tex_content, report_pdf=pdf_content)
