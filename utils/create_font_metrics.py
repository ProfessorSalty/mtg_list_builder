from fontTools.pens.t2CharStringPen import T2CharStringPen
from fontTools.ttLib import TTFont
from fontTools.ttLib.tables._n_a_m_e import NameRecord


def create_font_metrics(font_path: str):
    font = TTFont(font_path)
    tfm_data = font.makeTeXMetrics(T2CharStringPen(), NameRecord())
